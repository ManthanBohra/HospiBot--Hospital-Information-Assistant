from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph import app as workflow_app
from typing import List

app = FastAPI(title="HospiBot API", description="Hospital Information Chatbot Backend")

class ChatRequest(BaseModel):
    message: str
    history: List[str] = []

class ChatResponse(BaseModel):
    response: str
    intent: str

@app.get("/")
def read_root():
    return {"status": "HospiBot Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Prepare state
        # In a real app we'd maintain history properly. Here we treat 'message' as the new input
        # and 'history' as context if needed, but the graph mainly looks at the last message.
        input_state = {
            "messages": request.history + [request.message],
            "current_intent": "",
            "response": ""
        }
        
        # Invoke LangGraph
        result = workflow_app.invoke(input_state)
        
        return ChatResponse(
            response=result["response"],
            intent=result["current_intent"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
