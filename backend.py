from pydantic import BaseModel
from typing import List 
class RequestState(BaseModel):
    model_name: str
    model_provider:str
    system_prompt: str
    messages: List[str]
    allow_search: bool
    
    
from fastapi import FastAPI 
from python_agent_chatbot import get_response_from_ai_agent
ALLOWED_MODELS_NAMES=["llama3-70b-8192", "llama3-70b-versatile", "gpt-4o-mini","mixtral-8x7b-32768"]

app = FastAPI(title="Chatbot API", description="Chatbot API")    
@app.post("/chat")  
def chat_endpoint(request: RequestState):
    """_summary_

    Args:
        request (RequestState): _description_
    """
    if request.model_name not in ALLOWED_MODELS_NAMES:
        return {"error": "Model not allowed"}
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response
    
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)    