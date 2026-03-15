import re
from typing import List
import tiktoken
from app.core.provider_base import PolicyChunk
from app.providers.uhc.metadata import extract_cpt_codes

ENCODING = tiktoken.get_encoding("cl100k_base")
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
HIGH_PRIORITY_SECTIONS = {"coverage_rationale", "exclusions"}

def _tokenize(text: str) -> List[int]:
    return ENCODING.encode(text)

def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current_tokens = []
    current_text = []

    for sentence in sentences:
        s_tokens = _tokenize(sentence)
        if len(current_tokens) + len(s_tokens) > chunk_size and current_tokens:
            chunks.append(" ".join(current_text))
            # Keep overlap
            overlap_tokens = 0
            overlap_sents = []
            for s in reversed(current_text):
                t = _tokenize(s)
                if overlap_tokens + len(t) <= overlap:
                    overlap_sents.insert(0, s)
                    overlap_tokens += len(t)
                else:
                    break
            current_text = overlap_sents
            current_tokens = _tokenize(" ".join(current_text))
        current_text.append(sentence)
        current_tokens = _tokenize(" ".join(current_text))

    if current_text:
        chunks.append(" ".join(current_text))

    return chunks

def create_chunks(parsed: dict, source_url: str, provider: str = "uhc") -> List[PolicyChunk]:
    chunks = []
    sections = parsed.get("sections", {})
    policy_name = parsed.get("policy_name", "")
    policy_number = parsed.get("policy_number")
    effective_date = parsed.get("effective_date")

    for section_name, text in sections.items():
        if not text.strip():
            continue
        text_chunks = _chunk_text(text)
        for chunk_text in text_chunks:
            if not chunk_text.strip():
                continue
            cpt_codes = extract_cpt_codes(chunk_text)
            chunks.append(PolicyChunk(
                text=chunk_text,
                policy_name=policy_name,
                policy_number=policy_number,
                section=section_name,
                cpt_codes=cpt_codes,
                effective_date=effective_date,
                source_url=source_url,
                provider=provider,
            ))
    return chunks
