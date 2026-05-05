#!/bin/bash

# Start Backend
cd /home/kittu/My_assignment/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start Frontend
cd /home/kittu/My_assignment/frontend
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!

echo "Both services started. Backend running on port 8000. Frontend running on port 5173. Press Ctrl+C to stop."
trap "kill $BACKEND_PID $FRONTEND_PID" SIGINT
wait
