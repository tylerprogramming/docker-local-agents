from fastapi import APIRouter
from typing import List
from app.services.knowledge import (
    create_collection_service,
    add_vectors_service,
    search_vectors_service,
)

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

@router.post("/create_collection")
def create_collection(collection_name: str):
    return create_collection_service(collection_name)

@router.post("/add_vectors")
def add_vectors(docs: List[str], collection_name: str):
    return add_vectors_service(docs, collection_name)

@router.post("/search_vectors")
def search_vectors(query_text: str, collection_name: str, limit: int = 3):
    return search_vectors_service(query_text, collection_name, limit)
