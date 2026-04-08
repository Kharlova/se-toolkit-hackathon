#!/bin/bash
# Script to run the Plant Watering Tracker locally

echo "🌱 Starting Plant Watering Tracker..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is required but not found."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install -r requirements.txt

# Start the server
echo "🚀 Starting server on http://localhost:8000"
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
