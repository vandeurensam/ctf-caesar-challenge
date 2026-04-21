#!/bin/bash
# Start docker compose with automatic initialization

echo "🚀 Starting CTF environment..."
echo ""

# Start all containers
docker compose up --build -d

echo ""
echo "⏳ Waiting for CTFd to be ready..."
sleep 10

echo ""
echo "📝 Initializing CTFd with challenges and hints..."

# Copy and run initialization script
docker cp init_ctfd.py ctfd:/tmp/
docker exec ctfd python /tmp/init_ctfd.py

echo ""
echo "✅ All services are running!"
echo ""
echo "📍 Access points:"
echo "   - CTFd: http://localhost:8000"
echo "   - HTTP Challenge: http://localhost:5000"
echo ""
echo "🧹 To stop all services: docker compose down"
echo "📋 To view logs: docker compose logs -f"
