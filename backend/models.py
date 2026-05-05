from sqlalchemy import Column, Integer, String, DateTime, Text
import datetime
from database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String, index=True, nullable=True)
    interaction_type = Column(String, nullable=True)
    interaction_date = Column(String, nullable=True) 
    interaction_time = Column(String, nullable=True)
    attendees = Column(String, nullable=True)
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(String, nullable=True)
    samples_distributed = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    outcomes = Column(Text, nullable=True)
    follow_up_actions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
