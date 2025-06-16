from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from fastembed import TextEmbedding
import os

# Initialize embedding model and Qdrant client
model = TextEmbedding("BAAI/bge-small-en-v1.5")
client = QdrantClient(url="http://host.docker.internal:6333")

# Get vector dimension from a sample text
sample_text = "This is a sample sentence to get the vector dimension."
query_embedding = list(model.passage_embed(sample_text))[0]
vector_dimension = len(query_embedding)

def create_collection_service(collection_name: str):
    response = client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_dimension, distance=Distance.COSINE)
    )
    return response

def add_vectors_service(docs, collection_name: str):
    points = []
    for i, text in enumerate(docs):
        embeddings = list(model.embed([text]))[0]
        points.append(
            PointStruct(
                id=i + 1,
                vector=embeddings,
                payload={"text": text},
            )
        )
    response = client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points,
    )
    return response

def search_vectors_service(query_text: str, collection_name: str, limit: int = 3):
    query_embedding = list(model.passage_embed(query_text))[0]
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=limit,
    )
    return search_result
