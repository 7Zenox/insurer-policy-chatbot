from cachetools import TTLCache
from typing import List, Dict
from app.config import CONVERSATION_WINDOW

# TTLCache: max 1000 sessions, 30-minute TTL
_sessions: TTLCache = TTLCache(maxsize=1000, ttl=1800)

def get_history(session_id: str) -> List[Dict[str, str]]:
    return _sessions.get(session_id, [])

def add_turn(session_id: str, user_msg: str, assistant_msg: str) -> None:
    history = list(_sessions.get(session_id, []))
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": assistant_msg})
    # Keep only last CONVERSATION_WINDOW turn pairs
    max_messages = CONVERSATION_WINDOW * 2
    if len(history) > max_messages:
        history = history[-max_messages:]
    _sessions[session_id] = history
