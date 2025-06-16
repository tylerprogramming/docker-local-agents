import requests
from app.core.config import settings

def download_model_service(model_name: str):
    url = f"{settings.OLLAMA_URL}/api/pull"
    response = requests.post(url, json={"name": model_name})
    if response.status_code == 200:
        return {"detail": f"Model '{model_name}' download completed."}
    else:
        return {"detail": f"Failed to start download for model '{model_name}'.", "error": response.text}
