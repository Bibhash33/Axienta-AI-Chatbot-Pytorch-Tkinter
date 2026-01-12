from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Axienta AI chatbot", version="1.0.0")
app.include_router(router)
