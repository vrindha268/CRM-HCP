import os
import json
from typing import Annotated, TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv

load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")

# --- TOOLS ---

@tool
def log_interaction(
    hcp_name: str = "", 
    interaction_type: str = "Meeting", 
    interaction_date: str = "", 
    sentiment: str = "Neutral", 
    topics_discussed: str = "", 
    materials_shared: str = "", 
    samples_distributed: str = "",
    attendees: str = ""
) -> str:
    """
    Log a NEW interaction with an HCP. 
    Use this tool when the user first describes meeting an HCP, logging their name, date, sentiment, etc.
    """
    updates = {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type,
        "interaction_date": interaction_date,
        "sentiment": sentiment,
        "topics_discussed": topics_discussed,
        "materials_shared": materials_shared,
        "samples_distributed": samples_distributed,
        "attendees": attendees
    }
    return json.dumps({"action": "update_form", "updates": {k:v for k,v in updates.items() if v}})

@tool
def edit_interaction(field_to_update: str, new_value: str) -> str:
    """
    Edit a specific field in the interaction form.
    Use this when the user corrects a mistake (e.g., "sorry, the name was actually Dr. John").
    Valid fields: hcp_name, interaction_type, interaction_date, interaction_time, attendees, topics_discussed, materials_shared, samples_distributed, sentiment, outcomes, follow_up_actions.
    """
    return json.dumps({"action": "update_form", "updates": {field_to_update: new_value}})

@tool
def add_materials_samples(materials: str = "", samples: str = "") -> str:
    """
    Append materials shared or samples distributed to the existing form.
    Use this when the user says "I also shared the X brochure" or "Gave them 5 samples of Y".
    """
    updates = {}
    if materials: updates["materials_shared"] = materials
    if samples: updates["samples_distributed"] = samples
    return json.dumps({"action": "update_form", "updates": updates})

@tool
def plan_follow_up(action_items: str) -> str:
    """
    Plan a follow up action or task.
    Use this when the user mentions what needs to be done next.
    """
    return json.dumps({"action": "update_form", "updates": {"follow_up_actions": action_items}})

@tool
def analyze_outcomes(outcomes_summary: str) -> str:
    """
    Summarize the key outcomes or agreements from the interaction.
    Use this when the user explicitly mentions the outcome, conclusion, or final agreement of the meeting.
    """
    return json.dumps({"action": "update_form", "updates": {"outcomes": outcomes_summary}})

tools = [log_interaction, edit_interaction, add_materials_samples, plan_follow_up, analyze_outcomes]

# --- LANGGRAPH ---

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    current_state: dict

def call_model(state: AgentState):
    llm = ChatNVIDIA(model="z-ai/glm-5.1", nvidia_api_key=NVIDIA_API_KEY, temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    
    sys_msg = SystemMessage(content=f"""You are an AI assistant for a life science field representative.
    Your job is to control the CRM form on the left panel using your tools based on the user's natural language input.
    You MUST use tools to update the form. Do not just reply with text if a form update is implied.
    Current form state: {json.dumps(state.get('current_state', {}))}
    
    Rules:
    - If it's a new interaction, use 'log_interaction'.
    - If they correct a mistake, use 'edit_interaction'.
    - If they add materials/samples, use 'add_materials_samples'.
    - If they mention next steps, use 'plan_follow_up'.
    - If they mention outcomes, use 'analyze_outcomes'.
    
    After using a tool, you can briefly acknowledge the update to the user. Keep it brief.""")
    
    response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

tool_node = ToolNode(tools)

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app_graph = workflow.compile()

def run_chat_agent(message: str, current_state: dict):
    if not NVIDIA_API_KEY:
        return "Please set NVIDIA_API_KEY in the backend .env file.", {}
        
    state = {
        "messages": [HumanMessage(content=message)],
        "current_state": current_state
    }
    
    result = app_graph.invoke(state)
    
    final_message = result["messages"][-1]
    response_text = final_message.content
    
    form_updates = {}
    for msg in result["messages"]:
        if isinstance(msg, ToolMessage):
            try:
                data = json.loads(msg.content)
                if data.get("action") == "update_form":
                    form_updates.update(data.get("updates", {}))
            except json.JSONDecodeError:
                pass
                
    return response_text, form_updates
