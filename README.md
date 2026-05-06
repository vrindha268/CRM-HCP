# AI-Driven HCP CRM Interaction Module

A professional-grade, AI-first module for Healthcare Professional (HCP) CRM systems. This application allows field representatives to log interactions using natural language, which is then processed by an intelligent agent to automatically populate structured CRM forms.

## 🚀 Key Features

- **AI-Powered Interaction Logging**: Talk or type to an AI assistant that understands healthcare meeting nuances and fills out the CRM form for you.
- **Dynamic Form Synchronization**: The structured form on the left updates in real-time as the AI agent extracts data from your conversation.
- **Agentic Intelligence**: Built with LangGraph and Groq, using the `gemma2-9b-it` model for high-speed, accurate tool calling and data extraction.
- **Premium UI/UX**: Modern, sleek design using Tailwind CSS and Google Inter typography, optimized for field productivity.
- **Multi-Database Support**: Configured for high-performance PostgreSQL in production, with SQLite support for local development.

## 🛠 Tech Stack

- **Frontend**: React 18, TypeScript, Vite, Redux Toolkit, Tailwind CSS, Lucide Icons.
- **Backend**: FastAPI, Python 3.x, SQLAlchemy (Async), Pydantic.
- **AI/LLM**: LangGraph, LangChain, Groq API (`gemma2-9b-it`).
- **Database**: PostgreSQL (Production) / SQLite (Dev).

## 📋 Prerequisites

- **Node.js** (v18+)
- **Python** (v3.9+)
- **Groq API Key**: Obtain one from [Groq Console](https://console.groq.com/).

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CRM-HCP
   ```

2. **Run the setup script**:
   This script will install all frontend and backend dependencies and set up the Python virtual environment.
   ```bash
   ./setup.sh
   ```

3. **Configure Environment Variables**:
   Update the `.env` file in the `backend/` directory:
   ```bash
   # backend/.env
   GROQ_API_KEY=your_groq_api_key_here
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
   ```

## 🏃 Running the Application

To start both the frontend and backend services simultaneously, use the provided start script:

```bash
./start.sh
```

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📂 Project Structure

- `frontend/`: React application and design system.
- `backend/`: FastAPI server and LangGraph agent logic.
- `setup.sh`: Automated environment configuration and installation.
- `start.sh`: Portable service orchestrator.

## 📝 License

Distributed under the MIT License.
