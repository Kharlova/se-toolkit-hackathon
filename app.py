from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import os
from datetime import datetime, timedelta

# Database setup
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "plants.db")

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            watering_frequency_days INTEGER NOT NULL,
            last_watered TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

class PlantHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def _send_json(self, data, status=200):
        response = json.dumps(data)
        self._set_headers(status)
        self.wfile.write(response.encode())

    def _send_file(self, filepath, content_type):
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self._set_headers(200, content_type)
            self.wfile.write(content)
        except FileNotFoundError:
            self._set_headers(404)
            self.wfile.write(b"Not Found")

    def _read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        return json.loads(body)

    def _get_path(self):
        return self.path.split("?")[0]

    def do_GET(self):
        path = self._get_path()

        if path == "/":
            self._send_file(os.path.join(STATIC_DIR, "index.html"), "text/html")
        elif path.startswith("/static/"):
            filename = path[len("/static/"):]
            filepath = os.path.join(STATIC_DIR, filename)
            if filename.endswith(".css"):
                self._send_file(filepath, "text/css")
            elif filename.endswith(".js"):
                self._send_file(filepath, "application/javascript")
            elif filename.endswith(".png") or filename.endswith(".jpg"):
                self._send_file(filepath, "image/" + filename.split(".")[-1])
            else:
                self._send_file(filepath, "text/plain")
        elif path == "/api/plants":
            self._get_plants()
        else:
            self._set_headers(404)
            self.wfile.write(b"Not Found")

    def do_POST(self):
        path = self._get_path()

        if path == "/api/plants":
            self._create_plant()
        elif path.startswith("/api/plants/") and path.endswith("/water"):
            try:
                plant_id = int(path.split("/")[3])
                self._water_plant(plant_id)
            except (ValueError, IndexError):
                self._set_headers(404)
                self.wfile.write(b"Not Found")
        else:
            self._set_headers(404)
            self.wfile.write(b"Not Found")

    def do_PUT(self):
        path = self._get_path()

        if path.startswith("/api/plants/"):
            try:
                plant_id = int(path.split("/")[3])
                self._update_plant(plant_id)
            except (ValueError, IndexError):
                self._set_headers(404)
                self.wfile.write(b"Not Found")
        else:
            self._set_headers(404)
            self.wfile.write(b"Not Found")

    def do_DELETE(self):
        path = self._get_path()

        if path.startswith("/api/plants/"):
            try:
                plant_id = int(path.split("/")[3])
                self._delete_plant(plant_id)
            except (ValueError, IndexError):
                self._set_headers(404)
                self.wfile.write(b"Not Found")
        else:
            self._set_headers(404)
            self.wfile.write(b"Not Found")

    def _get_plants(self):
        conn = get_db()
        plants = conn.execute("SELECT * FROM plants ORDER BY created_at DESC").fetchall()
        conn.close()

        result = []
        today = datetime.now().date()
        for plant in plants:
            last_watered = datetime.fromisoformat(plant["last_watered"]).date() if plant["last_watered"] else None
            next_watering = last_watered + timedelta(days=plant["watering_frequency_days"]) if last_watered else today
            days_until = (next_watering - today).days
            is_overdue = days_until < 0

            result.append({
                "id": plant["id"],
                "name": plant["name"],
                "watering_frequency_days": plant["watering_frequency_days"],
                "last_watered": plant["last_watered"],
                "next_watering": next_watering.isoformat(),
                "days_until_watering": days_until,
                "is_overdue": is_overdue
            })
        self._send_json(result)

    def _create_plant(self):
        data = self._read_body()
        name = data.get("name", "").strip()
        frequency = data.get("watering_frequency_days", 7)

        if not name:
            self._send_json({"error": "Plant name is required"}, 400)
            return

        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO plants (name, watering_frequency_days) VALUES (?, ?)",
            (name, frequency)
        )
        conn.commit()
        plant_id = cursor.lastrowid
        conn.close()
        self._send_json({"id": plant_id, "message": "Plant added successfully"})

    def _water_plant(self, plant_id):
        conn = get_db()
        plant = conn.execute("SELECT * FROM plants WHERE id = ?", (plant_id,)).fetchone()
        if not plant:
            conn.close()
            self._send_json({"error": "Plant not found"}, 404)
            return

        now = datetime.now().isoformat()
        conn.execute("UPDATE plants SET last_watered = ? WHERE id = ?", (now, plant_id))
        conn.commit()
        conn.close()
        self._send_json({"message": f"{plant['name']} watered successfully!"})

    def _update_plant(self, plant_id):
        data = self._read_body()
        conn = get_db()
        existing = conn.execute("SELECT * FROM plants WHERE id = ?", (plant_id,)).fetchone()
        if not existing:
            conn.close()
            self._send_json({"error": "Plant not found"}, 404)
            return

        name = data.get("name", existing["name"])
        frequency = data.get("watering_frequency_days", existing["watering_frequency_days"])

        conn.execute("UPDATE plants SET name = ?, watering_frequency_days = ? WHERE id = ?",
                     (name, frequency, plant_id))
        conn.commit()
        conn.close()
        self._send_json({"message": "Plant updated successfully"})

    def _delete_plant(self, plant_id):
        conn = get_db()
        plant = conn.execute("SELECT * FROM plants WHERE id = ?", (plant_id,)).fetchone()
        if not plant:
            conn.close()
            self._send_json({"error": "Plant not found"}, 404)
            return

        conn.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
        conn.commit()
        conn.close()
        self._send_json({"message": "Plant deleted successfully"})

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

if __name__ == "__main__":
    PORT = 8000
    server = HTTPServer(("0.0.0.0", PORT), PlantHandler)
    print("🌱 Plant Watering Tracker")
    print(f"🌐 Server running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        server.shutdown()
