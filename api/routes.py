from fastapi import APIRouter
from api.schemas import ChatRequest, ChatResponse
from api.dependencies import predictor

router = APIRouter()
@router.post("/chat", response_model=ChatResponse)

def chat(request: ChatRequest):
    response = predictor.predict(request.prompt)
    return ChatResponse(response=response)
