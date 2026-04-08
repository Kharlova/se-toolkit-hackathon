#!/bin/bash
# Script to deploy with Docker

echo "🌱 Deploying Plant Watering Tracker with Docker..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not found."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is required but not found."
    exit 1
fi

# Build and start
echo "📦 Building and starting containers..."
docker compose up -d --build

echo "✅ Application is running!"
echo "🌐 Access it at: http://localhost:8000"
echo ""
echo "To stop: docker compose down"
echo "To view logs: docker compose logs -f"
