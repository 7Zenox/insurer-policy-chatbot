import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
QDRANT_URL: str = os.environ.get("QDRANT_URL", "")
QDRANT_API_KEY: str = os.environ.get("QDRANT_API_KEY", "")
HF_MODEL_NAME: str = os.environ.get("HF_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

PROVIDER_REGISTRY = {
    "uhc": {
        "name": "UnitedHealthcare",
        "policy_index_url": "https://www.uhcprovider.com/en/policies-protocols/commercial-policies/commercial-medical-drug-policies.html",
        "collection_name": "uhc_policies",
        "scraper_class": "UHCScraper",
    }
}

DEFAULT_PROVIDER = "uhc"
GROQ_MODEL = "llama-3.3-70b-versatile"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K_RETRIEVAL = 6
CONVERSATION_WINDOW = 4
RATE_LIMIT = "10/minute"
