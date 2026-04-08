# 🌱 Plant Watering Tracker

A simple web application to track your plants and their watering schedules. Never forget to water your plants again!

## Demo

🌐 **Live demo:** http://10.93.26.70:8000

![Add Plant Form](static/screenshot_add.png)
![Plants Dashboard](static/screenshot_dashboard.png)

## Product Context

### End Users

Plant owners (beginners and experienced) who want to maintain a consistent watering schedule for their indoor/outdoor plants.

### Problem

Plant owners often forget when they last watered their plants or struggle to maintain consistent watering schedules, leading to under/over-watering and plant health issues.

### Solution

A simple web app where users can add plants, set watering frequencies, and track watering status with visual indicators — all in one click.

## Features

### Implemented (Version 2)

- ✅ Add plants with custom watering frequency (in days)
- ✅ Automatic watering schedule calculation
- ✅ Visual status indicators (🔴 overdue / 🟡 due today / 🟢 good)
- ✅ One-click "Water" button to mark as watered
- ✅ Delete plants
- ✅ SQLite database persistence
- ✅ Dockerized for easy deployment
- ✅ Responsive UI
- ✅ RESTful JSON API

### Not Yet Implemented

- ⬜ Plant categories/tags
- ⬜ Email/push notifications/reminders
- ⬜ Photo uploads for plants
- ⬜ Multi-user accounts
- ⬜ Data export/import (CSV, JSON)

## Usage

### Running Locally (without Docker)

1. Ensure Python 3.11+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open browser and navigate to: `http://localhost:8000`

### Using the Application

1. **Add a Plant**: Fill in the plant name and watering frequency (in days), then click "Add"
2. **View Status**: Each plant card shows a colored border:
   - 🔴 **Red**: Overdue for watering
   - 🟡 **Yellow**: Due today
   - 🟢 **Green**: Good, next watering in X days
3. **Water a Plant**: Click the "Water 💧" button to mark it as watered today
4. **Delete a Plant**: Click the "Delete" button to remove a plant

## Deployment

### Requirements

- **OS**: Ubuntu 24.04 (or any Linux with Docker support)
- **Required Software**:
  - Docker
  - Docker Compose

### Step-by-Step Deployment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Kharlova/se-toolkit-hackathon.git
   cd se-toolkit-hackathon
   ```

2. **Build and start with Docker Compose**:
   ```bash
   docker compose up -d --build
   ```

3. **Access the application**:
   Open browser and navigate to: `http://<your-server-ip>:8000`

### Useful Commands

```bash
# View logs
docker compose logs -f

# Stop the application
docker compose down

# Update and redeploy
git pull
docker compose up -d --build
```

## Project Structure

```
se-toolkit-hackathon/
├── app.py              # Backend server (http.server + SQLite)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker ignore patterns
├── data/               # SQLite database (auto-created)
│   └── plants.db
└── static/             # Frontend files
    ├── index.html
    ├── style.css
    └── app.js
```

## Technology Stack

- **Backend**: Python (stdlib `http.server`)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Docker & Docker Compose

## License

MIT License - see LICENSE file for details.
