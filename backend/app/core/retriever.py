import re
from typing import Literal, List
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny
from app.config import QDRANT_URL, QDRANT_API_KEY, TOP_K_RETRIEVAL
from app.core.embeddings import get_embeddings

def route_query(query: str) -> Literal["cpt_filter", "semantic"]:
    if re.search(r"\b\d{5}\b|\b[A-Z]\d{4}\b", query):
        return "cpt_filter"
    return "semantic"

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def retrieve(query: str, collection_name: str, top_k: int = TOP_K_RETRIEVAL) -> List[dict]:
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
        search_filter = Filter(
            must=[FieldCondition(key="cpt_codes", match=MatchAny(any=codes))]
        )
        docs = store.similarity_search(query, k=top_k, filter=search_filter)
    else:
        docs = store.similarity_search(query, k=top_k)

    return docs
