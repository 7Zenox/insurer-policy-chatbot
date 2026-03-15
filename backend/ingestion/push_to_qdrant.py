import uuid
from typing import List
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, PayloadSchemaType
from app.core.provider_base import PolicyChunk
from app.core.embeddings import get_embeddings
from app.config import QDRANT_URL, QDRANT_API_KEY

BATCH_SIZE = 100
VECTOR_SIZE = 384

def push_chunks(chunks: List[PolicyChunk], collection_name: str):
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    embeddings = get_embeddings()

    # Create collection if not exists
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        client.create_payload_index(collection_name, "metadata.cpt_codes", PayloadSchemaType.KEYWORD)
        client.create_payload_index(collection_name, "metadata.section", PayloadSchemaType.KEYWORD)

    # Batch upsert
    for i in tqdm(range(0, len(chunks), BATCH_SIZE), desc="Upserting batches"):
        batch = chunks[i:i + BATCH_SIZE]
        texts = [c.text for c in batch]
        vectors = embeddings.embed_documents(texts)

        points = []
        for chunk, vector in zip(batch, vectors):
            section = chunk.section
            priority = "high" if section in {"coverage_rationale", "exclusions"} else "normal"
            # LangChain QdrantVectorStore expects page_content + metadata keys
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "page_content": chunk.text,
                    "metadata": {
                        "policy_name": chunk.policy_name,
                        "policy_number": chunk.policy_number,
                        "section": section,
                        "cpt_codes": chunk.cpt_codes,
                        "effective_date": chunk.effective_date,
                        "source_url": chunk.source_url,
                        "provider": chunk.provider,
                        "priority": priority,
                    },
                }
            ))
        client.upsert(collection_name=collection_name, points=points)
