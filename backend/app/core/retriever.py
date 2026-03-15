import re
from typing import Literal, List
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny
from app.config import QDRANT_URL, QDRANT_API_KEY, TOP_K_RETRIEVAL
from app.core.embeddings import get_embeddings

PRIORITY_SECTIONS = {"coverage_rationale", "exclusions"}

def route_query(query: str) -> Literal["cpt_filter", "semantic"]:
    if re.search(r"\b\d{5}\b|\b[A-Z]\d{4}\b", query):
        return "cpt_filter"
    return "semantic"

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def _rerank(docs: list) -> list:
    """Promote coverage_rationale and exclusions chunks to the top."""
    priority = [d for d in docs if d.metadata.get("section") in PRIORITY_SECTIONS]
    rest = [d for d in docs if d.metadata.get("section") not in PRIORITY_SECTIONS]
    return priority + rest

def retrieve(query: str, collection_name: str, top_k: int = TOP_K_RETRIEVAL) -> list:
    client = get_qdrant_client()
    embeddings = get_embeddings()
    mode = route_query(query)

    store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )

    if mode == "cpt_filter":
        codes = re.findall(r"\b\d{5}\b|\b[A-Z]\d{4}\b", query)
        # CPT codes are stored under metadata.cpt_codes (LangChain nested payload)
        search_filter = Filter(
            must=[FieldCondition(key="metadata.cpt_codes", match=MatchAny(any=codes))]
        )
        docs = store.similarity_search(query, k=top_k, filter=search_filter)
        # Fallback to semantic search if filter returns no results
        if not docs:
            docs = store.similarity_search(query, k=top_k)
    else:
        docs = store.similarity_search(query, k=top_k)

    return _rerank(docs)
