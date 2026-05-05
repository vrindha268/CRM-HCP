from pydantic import BaseModel
from typing import Optional, Dict

class InteractionBase(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    interaction_date: Optional[str] = None
    interaction_time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    current_state: Dict[str, Optional[str]] = {}

class ChatResponse(BaseModel):
    response: str
    extracted_data: dict
