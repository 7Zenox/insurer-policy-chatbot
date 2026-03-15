from fastapi import APIRouter
from qdrant_client import QdrantClient
from app.config import QDRANT_URL, QDRANT_API_KEY, PROVIDER_REGISTRY, DEFAULT_PROVIDER

router = APIRouter()

@router.get("/policies")
async def list_policies(provider: str = DEFAULT_PROVIDER):
    cfg = PROVIDER_REGISTRY.get(provider)
    if not cfg:
        return {"error": "Unknown provider"}

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    collection_name = cfg["collection_name"]

    seen = {}
    offset = None
    while True:
        results, next_offset = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for point in results:
            p = (point.payload or {}).get("metadata", point.payload or {})
            name = p.get("policy_name", "")
            if name and name not in seen:
                seen[name] = {
                    "name": name,
                    "policy_number": p.get("policy_number"),
                    "effective_date": p.get("effective_date"),
                    "source_url": p.get("source_url"),
                }
        if next_offset is None:
            break
        offset = next_offset

    return {"policies": list(seen.values())}
