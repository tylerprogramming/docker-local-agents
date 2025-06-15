import requests
import os

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

from fastembed import TextEmbedding

from .models import Todo, Base
from .database import get_db, engine

from .todos_crew.src.todos_crew.crew import TodosCrew

model = TextEmbedding("BAAI/bge-small-en-v1.5")
sample_text = "This is a sample sentence to get the vector dimension."
query_embedding = list(model.passage_embed(sample_text))[0] 

vector_dimension = len(query_embedding)
print(f"Vector dimension: {vector_dimension}")

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic model for request and response
class TodoCreate(BaseModel):
    title: str
    description: str

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True

# CRUD endpoints
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return todos

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo deleted"} 

@app.get("/ollama")
def check_ollama():
    response = requests.get("http://localhost:11434/api/version")
    print(response.json())
    if response.status_code == 200:
        return {"detail": "Ollama is running"}
    else:
        return {"detail": "Ollama is not running"}
    
@app.post("/ollama/pull-model")
def pull_model(model_name: str):
    print(f"Pulling model {model_name}")
    print(f"Ollama host: {os.getenv('OLLAMA_HOST')}")
    print(f"Ollama port: {os.getenv('OLLAMA_PORT')}")
 
    data = {"name": model_name}
    
    ollama_api_url = "http://host.docker.internal:11434" # Use host.docker.internal
    response = requests.post(f'{ollama_api_url}/api/pull', json=data)
    
    if response.status_code == 200:
        return {"detail": f"Model {model_name} pulled successfully"}
    else:
        return {"detail": f"Failed to pull model {model_name}", "error": response.text}

client = QdrantClient(url="http://host.docker.internal:6333")

@app.post("/create_collection")
async def create_collection(collection_name: str):
    response =client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_dimension, distance=Distance.COSINE)
    )
    
    return response

# Example: Add vectors
@app.post("/add_vectors")
async def add_vectors(docs: List[str], collection_name: str):
    points = []
    for i, text in enumerate(docs):
        # Embed the text
        embeddings = list(model.embed([text]))[0] # Use list() to get embeddings from iterator
        # Create a PointStruct (a point in Qdrant)
        points.append(
            PointStruct(
                id=i + 1, # Unique identifier for each point
                vector=embeddings,
                payload={"text": text}, # Store the original text as payload
            )
        )

    response = client.upsert(
        collection_name=collection_name,
        wait=True, # Wait for the operation to complete
        points=points,
    )

    return response

@app.post("/search_vectors")
async def search_vectors(query_text: str, collection_name: str, limit: int = 3):
    # Convert the query text to a vector
    query_embedding = list(model.passage_embed(query_text))[0] # Embed the query text and get the first embedding

    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=limit,
    )
    
    return search_result
