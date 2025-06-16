from fastapi import FastAPI
from app.api.todos import router as todos_router
from app.api.knowledge import router as knowledge_router
from app.api.ollama import router as ollama_router
from app.models.todo import Base
from app.core.database import engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(todos_router)
app.include_router(knowledge_router)
app.include_router(ollama_router)
