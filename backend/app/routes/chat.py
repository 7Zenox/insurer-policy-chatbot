from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.config import PROVIDER_REGISTRY, DEFAULT_PROVIDER
from app.core.rag_chain import stream_response
import json

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: str
    provider: str = DEFAULT_PROVIDER

@router.post("/chat")
async def chat(request: Request, body: ChatRequest):
    provider_cfg = PROVIDER_REGISTRY.get(body.provider)
    if not provider_cfg:
        return {"error": f"Unknown provider: {body.provider}"}

    collection_name = provider_cfg["collection_name"]

    async def generate():
        try:
            async for event in stream_response(body.query, body.session_id, collection_name):
                yield event
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                error_msg = "Rate limit reached. Please wait a moment and try again."
            yield f'data: {json.dumps({"type": "error", "message": error_msg})}\n\n'

    return StreamingResponse(generate(), media_type="text/event-stream")
