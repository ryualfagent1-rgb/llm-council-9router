"""JSON-based conversation storage."""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from .config import DATA_DIR

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def _conversation_path(conversation_id: str) -> str:
    return os.path.join(DATA_DIR, f"{conversation_id}.json")


def list_conversations() -> List[Dict[str, Any]]:
    """List all conversations (metadata only)."""
    conversations = []
    for filename in sorted(os.listdir(DATA_DIR), reverse=True):
        if filename.endswith('.json'):
            path = os.path.join(DATA_DIR, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                conversations.append({
                    "id": data.get("id", filename[:-5]),
                    "created_at": data.get("created_at", ""),
                    "title": data.get("title", "Untitled"),
                    "message_count": len(data.get("messages", []))
                })
            except Exception:
                continue
    return conversations


def create_conversation(conversation_id: str) -> Dict[str, Any]:
    """Create a new conversation."""
    now = datetime.utcnow().isoformat() + "Z"
    conversation = {
        "id": conversation_id,
        "created_at": now,
        "title": "New Conversation",
        "messages": []
    }
    with open(_conversation_path(conversation_id), 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)
    return conversation


def get_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific conversation with all its messages."""
    path = _conversation_path(conversation_id)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_conversation_title(conversation_id: str, title: str) -> bool:
    """Update conversation title."""
    conversation = get_conversation(conversation_id)
    if conversation is None:
        return False
    conversation["title"] = title
    with open(_conversation_path(conversation_id), 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)
    return True


def add_user_message(conversation_id: str, content: str) -> bool:
    """Add a user message to a conversation."""
    conversation = get_conversation(conversation_id)
    if conversation is None:
        return False
    conversation["messages"].append({
        "role": "user",
        "content": content
    })
    with open(_conversation_path(conversation_id), 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)
    return True


def add_assistant_message(
    conversation_id: str,
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]],
    stage3_result: Dict[str, Any]
) -> bool:
    """Add an assistant message with all three stages."""
    conversation = get_conversation(conversation_id)
    if conversation is None:
        return False
    conversation["messages"].append({
        "role": "assistant",
        "stage1": stage1_results,
        "stage2": stage2_results,
        "stage3": stage3_result
    })
    with open(_conversation_path(conversation_id), 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)
    return True