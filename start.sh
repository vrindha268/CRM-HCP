#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Start Backend
echo "Starting Backend..."
if [ -d "$SCRIPT_DIR/backend" ]; then
    cd "$SCRIPT_DIR/backend"
    if [ -d "venv" ]; then
        source venv/bin/activate
        uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
        BACKEND_PID=$!
    else
        echo "Error: Backend venv not found. Please run setup.sh first."
        exit 1
    fi
else
    echo "Error: Backend directory not found."
    exit 1
fi

# Start Frontend
echo "Starting Frontend..."
if [ -d "$SCRIPT_DIR/frontend" ]; then
    cd "$SCRIPT_DIR/frontend"
    npm run dev -- --host 0.0.0.0 &
    FRONTEND_PID=$!
else
    echo "Error: Frontend directory not found."
    kill $BACKEND_PID
    exit 1
fi

echo "Both services started."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop both services."

trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT
wait
