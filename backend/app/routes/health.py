from fastapi import APIRouter
from qdrant_client import QdrantClient
from app.config import QDRANT_URL, QDRANT_API_KEY, PROVIDER_REGISTRY, DEFAULT_PROVIDER
from app.core.embeddings import get_embeddings

router = APIRouter()

@router.get("/health")
async def health():
    qdrant_connected = False
    policy_count = 0
    model_loaded = False

    try:
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        cfg = PROVIDER_REGISTRY[DEFAULT_PROVIDER]
        info = client.get_collection(cfg["collection_name"])
        policy_count = info.points_count or 0
        qdrant_connected = True
    except Exception:
        pass

    try:
        get_embeddings()
        model_loaded = True
    except Exception:
        pass

    return {
        "status": "ok" if qdrant_connected and model_loaded else "degraded",
        "qdrant_connected": qdrant_connected,
        "model_loaded": model_loaded,
        "policy_count": policy_count,
    }
