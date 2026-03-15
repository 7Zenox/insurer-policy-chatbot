import os
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import HF_MODEL_NAME

# Use /app/.cache in Docker, fall back to ~/.cache locally
_default_cache = os.path.join(os.path.expanduser("~"), ".cache")
os.environ.setdefault("TRANSFORMERS_CACHE", os.path.join(_default_cache, "huggingface"))
os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", os.path.join(_default_cache, "sentence_transformers"))

@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=HF_MODEL_NAME)
