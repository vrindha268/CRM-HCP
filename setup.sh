#!/bin/bash
set -e

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Setting up project in $SCRIPT_DIR..."

# Frontend
if [ -d "frontend" ]; then
    echo "Frontend directory found, updating..."
else
    echo "Creating frontend with Vite..."
    npm create vite@latest frontend -- --template react-ts
fi

cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @reduxjs/toolkit react-redux lucide-react axios clsx tailwind-merge date-fns react-hook-form

# Backend
cd "$SCRIPT_DIR"
if [ ! -d "backend" ]; then
    echo "Creating backend directory..."
    mkdir -p backend
fi

cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv langchain langchain-groq langgraph asyncpg databases uvicorn[standard] aiosqlite pydantic-settings
pip freeze > requirements.txt

echo "Setup Complete!"
