import os
import json
from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

class ExtractionResult(BaseModel):
    hcp_name: str = Field(description="Name of the Healthcare Professional", default="")
    interaction_type: str = Field(description="Type of interaction, e.g., Meeting, Call", default="")
    topics_discussed: str = Field(description="Topics discussed during the interaction", default="")
    sentiment: str = Field(description="Observed/Inferred HCP Sentiment. One of: Positive, Neutral, Negative", default="")
    outcomes: str = Field(description="Key outcomes or agreements", default="")
    follow_up_actions: str = Field(description="Next steps or tasks", default="")
    attendees: str = Field(description="Attendees of the meeting", default="")

class AgentState(TypedDict):
    messages: List[Any]
    current_state: Dict[str, str]
    extracted_data: Dict[str, str]
    response: str

def process_chat(state: AgentState):
    if not GROQ_API_KEY:
        return {"response": "Please set GROQ_API_KEY in the backend .env file to enable AI features.", "extracted_data": {}}
        
    try:
        llm_extract = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY, temperature=0)
        structured_llm = llm_extract.with_structured_output(ExtractionResult)
        
        llm_chat = ChatGroq(model="gemma2-9b-it", groq_api_key=GROQ_API_KEY, temperature=0.7)
        
        sys_msg_chat = SystemMessage(content="You are an AI assistant helping a life science field representative log interactions with Healthcare Professionals (HCPs). Be brief, helpful, and acknowledge the details they provided.")
        
        chat_messages = [sys_msg_chat] + state["messages"]
        ai_response = llm_chat.invoke(chat_messages)
        
        sys_msg_extract = SystemMessage(content="Extract relevant CRM data from the user's latest message. Current form state is: " + json.dumps(state.get("current_state", {})))
        extract_messages = [sys_msg_extract, state["messages"][-1]]
        
        extraction = structured_llm.invoke(extract_messages)
        
        extracted_data = {k: v for k, v in extraction.dict().items() if v}
        
        return {
            "response": ai_response.content,
            "extracted_data": extracted_data
        }
    except Exception as e:
        print(f"Error in agent: {e}")
        return {
            "response": f"I processed your message, but there was an error extracting structured data: {str(e)}",
            "extracted_data": {}
        }

workflow = StateGraph(AgentState)
workflow.add_node("agent", process_chat)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
app_graph = workflow.compile()

def run_chat_agent(message: str, current_state: dict):
    state = {
        "messages": [HumanMessage(content=message)],
        "current_state": current_state,
        "extracted_data": {},
        "response": ""
    }
    result = app_graph.invoke(state)
    return result["response"], result.get("extracted_data", {})
