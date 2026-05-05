#!/bin/bash
set -e

cd /home/kittu/My_assignment

# Frontend
rm -rf frontend
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @reduxjs/toolkit react-redux lucide-react axios clsx tailwind-merge date-fns react-hook-form

# Backend
cd /home/kittu/My_assignment/backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv langchain langchain-nvidia-ai-endpoints langgraph psycopg2-binary databases uvicorn[standard] aiosqlite pydantic-settings
pip freeze > requirements.txt

echo "Setup Complete!"
