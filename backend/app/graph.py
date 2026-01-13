from typing import TypedDict, Literal, List
from langgraph.graph import StateGraph, END
from .hospital_data import hospital_data, HospitalData

# Define State
class AgentState(TypedDict):
    messages: List[str]
    current_intent: str
    response: str

# --- Nodes ---

def guardian_node(state: AgentState):
    """
    Analyzes the latest message to determine if it's medical or hospital-related.
    """
    last_message = state['messages'][-1].lower()
    
    # RISK: Basic keyword matching. In production, utilize an LLM guardrail here.
    medical_keywords = ["pain", "symptom", "hurt", "dose", "pill", 
                       "headache", "fever", "diagnosis", "bleed", "broken", 
                       "itch", "swelling", "burn", "infection", "virus"]
    
    if any(word in last_message for word in medical_keywords):
        return {"current_intent": "medical"}
    
    return {"current_intent": "hospital_info"}

def medical_refusal_node(state: AgentState):
    """
    Returns a strict refusal for medical queries.
    """
    refusal_msg = ("I am not a doctor and I cannot provide medical advice, diagnosis, or treatment. "
                   "If you are experiencing a medical emergency, please call emergency services immediately "
                   "or visit the nearest Emergency Room. Would you like to speak to a hospital representative?")
    return {"response": refusal_msg}

def hospital_expert_node(state: AgentState):
    """
    Retrieves hospital information based on keywords.
    """
    last_message = state['messages'][-1].lower()
    response = ""
    
    if "hour" in last_message or "time" in last_message or "visit" in last_message:
        response = f"Visiting Hours information:\n{hospital_data.get_general_info()}"
    elif "bill" in last_message or "pay" in last_message or "insurance" in last_message or "cost" in last_message:
        response = f"Billing & Insurance:\n{hospital_data.get_billing_info()}"
    elif "doctor" in last_message or "specialist" in last_message or "schedule" in last_message:
        response = f"Our Medical Specialists:\n{hospital_data.get_doctors()}"
    elif "depart" in last_message or "ward" in last_message:
        response = f"Departments:\n{hospital_data.get_departments()}"
    elif "where" in last_message or "location" in last_message or "address" in last_message:
        response = f"Location:\n{hospital_data.get_general_info()}"
    elif "human" in last_message or "representative" in last_message or "agent" in last_message or "yes" in last_message or "call" in last_message or "speak" in last_message:
        response = ("I have connected you to our Pattern Representative.\n\n"
                    "👤 **Name**: Jane Doe\n"
                    "📞 **Phone**: 555-0123\n\n"
                    "She is available 24/7 to assist you with your query.")
    else:
        response = ("I can help with Visiting Hours, Doctor Schedules, Billing, or Departments. "
                    "How can I assist you with hospital information?")
        
    return {"response": response}

# --- Edges ---

def route_intent(state: AgentState) -> Literal["medical_refusal", "hospital_expert"]:
    if state["current_intent"] == "medical":
        return "medical_refusal"
    return "hospital_expert"

# --- Graph Contruction ---

workflow = StateGraph(AgentState)

workflow.add_node("guardian", guardian_node)
workflow.add_node("medical_refusal", medical_refusal_node)
workflow.add_node("hospital_expert", hospital_expert_node)

workflow.set_entry_point("guardian")

workflow.add_conditional_edges(
    "guardian",
    route_intent
)

workflow.add_edge("medical_refusal", END)
workflow.add_edge("hospital_expert", END)

app = workflow.compile()
