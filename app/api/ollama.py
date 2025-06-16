from fastapi import APIRouter
from app.services.ollama import download_model_service

router = APIRouter(prefix="/ollama", tags=["ollama"])

@router.post("/download_model")
def download_model(model_name: str):
    return download_model_service(model_name)
