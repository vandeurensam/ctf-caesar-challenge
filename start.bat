@echo off
REM Start docker compose with automatic initialization

echo 🚀 Starting CTF environment...
echo.

REM Start all containers
docker compose up --build -d

echo.
echo ⏳ Waiting for CTFd to be ready...
timeout /t 10 /nobreak

echo.
echo 📝 Initializing CTFd with challenges and hints...

REM Copy and run initialization script
docker cp init_ctfd.py ctfd:/tmp/
docker exec ctfd python /tmp/init_ctfd.py

echo.
echo ✅ All services are running!
echo.
echo 📍 Access points:
echo    - CTFd: http://localhost:8000
echo    - HTTP Challenge: http://localhost:5000
echo.
echo 🧹 To stop all services: docker compose down
echo 📋 To view logs: docker compose logs -f
