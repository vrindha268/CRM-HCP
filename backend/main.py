from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import models, schemas, agent
from database import engine, get_db, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/interaction", response_model=schemas.Interaction)
async def create_interaction(interaction: schemas.InteractionCreate, db: AsyncSession = Depends(get_db)):
    db_interaction = models.Interaction(**interaction.model_dump())
    db.add(db_interaction)
    await db.commit()
    await db.refresh(db_interaction)
    return db_interaction

@app.post("/api/chat", response_model=schemas.ChatResponse)
async def chat(request: schemas.ChatRequest):
    response, extracted_data = agent.run_chat_agent(request.message, request.current_state)
    return schemas.ChatResponse(response=response, extracted_data=extracted_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
