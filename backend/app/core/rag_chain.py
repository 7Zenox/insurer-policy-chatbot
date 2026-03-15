import json
from typing import AsyncGenerator, List
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.config import GROQ_API_KEY, GROQ_MODEL
from app.core.memory import get_history, add_turn
from app.core.retriever import retrieve

SYSTEM_TEMPLATE = """You are a UHC policy assistant for healthcare providers (doctors, nurses, billing staff). Your job is to answer questions about UnitedHealthcare commercial medical and drug policies.

Rules:
1. Answer ONLY based on the policy excerpts provided below.
2. If the answer is not in the excerpts, say: "This specific information was not found in the retrieved policy documents. Please verify directly at uhcprovider.com."
3. Always state: which policy the answer comes from, the effective date, and whether prior authorization is mentioned.
4. Flag coverage conditions clearly — use "COVERED WHEN:" and "NOT COVERED WHEN:" formatting.
5. Never infer or extrapolate coverage beyond what is written.
6. If multiple policies are relevant, address each one.

Context (policy excerpts):
{context}

Conversation history:
{history}"""

def _format_docs(docs) -> tuple[str, list]:
    context_parts = []
    citations = []
    for i, doc in enumerate(docs):
        meta = doc.metadata
        context_parts.append(f"[{i+1}] {doc.page_content}")
        citations.append({
            "policy_name": meta.get("policy_name", "Unknown"),
            "section": meta.get("section", ""),
            "url": meta.get("source_url", ""),
            "effective_date": meta.get("effective_date", ""),
        })
    return "\n\n".join(context_parts), citations

def _format_history(history: list) -> str:
    if not history:
        return "No prior conversation."
    lines = []
    for msg in history:
        role = msg["role"].capitalize()
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)

async def stream_response(query: str, session_id: str, collection_name: str) -> AsyncGenerator[str, None]:
    docs = retrieve(query, collection_name)
    context, citations = _format_docs(docs)
    history = get_history(session_id)
    history_str = _format_history(history)

    system_msg = SYSTEM_TEMPLATE.format(context=context, history=history_str)

    llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, streaming=True)

    messages = [SystemMessage(content=system_msg), HumanMessage(content=query)]

    full_response = ""
    async for chunk in llm.astream(messages):
        token = chunk.content
        if token:
            full_response += token
            yield f'data: {json.dumps({"type": "token", "content": token})}\n\n'

    # Save turn to memory
    add_turn(session_id, query, full_response)

    # Send citations
    yield f'data: {json.dumps({"type": "citations", "sources": citations})}\n\n'
    yield f'data: {json.dumps({"type": "done"})}\n\n'
