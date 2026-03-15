from functools import lru_cache
from langchain_community.embeddings import FastEmbedEmbeddings
from app.config import HF_MODEL_NAME

@lru_cache(maxsize=1)
def get_embeddings() -> FastEmbedEmbeddings:
    return FastEmbedEmbeddings(model_name=HF_MODEL_NAME)
