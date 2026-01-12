from pydantic import BaseModel

class ChatResponse(BaseModel):
    prompt: str

class ChatRequest(BaseModel):
    response: str