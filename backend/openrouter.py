"""9Router API client - OpenAI-compatible REST via 9router gateway."""

import httpx
import asyncio
from typing import List, Dict, Any, Optional
from .config import NINEROUTER_KEY, NINEROUTER_CHAT_URL


async def query_model(model: str, messages: List[Dict[str, str]], timeout: float = 120.0) -> Optional[Dict[str, Any]]:
    """Query a single model via 9Router API.
    
    Args:
        model: Model identifier (e.g., "gemini/gemini-3.7-flash", "kr/claude-haiku-4.5")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds
    
    Returns:
        Response dict with 'content' key, or None if failed
    """
    headers = {}
    if NINEROUTER_KEY:
        headers["Authorization"] = f"Bearer {NINEROUTER_KEY}"
    headers["Content-Type"] = "application/json"
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,  # 9router defaults to streaming; we want full JSON
    }
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                NINEROUTER_CHAT_URL,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            # 9Router returns same structure as OpenAI/OpenRouter
            message = data.get('choices', [{}])[0].get('message', {})
            content = message.get('content')
            if content is None:
                return None
            return {
                'content': content,
            }
    except Exception as e:
        print(f"Error querying model {model} via 9Router: {e}")
        return None


async def query_models_parallel(models: List[str], messages: List[Dict[str, str]]) -> Dict[str, Optional[Dict[str, Any]]]:
    """Query multiple models in parallel via 9Router.
    
    Args:
        models: List of model identifiers
        messages: List of message dicts to send to each model
    
    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]
    
    # Wait for all to complete
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Map models to their responses, converting exceptions to None
    result = {}
    for model, response in zip(models, responses):
        if isinstance(response, Exception):
            result[model] = None
        else:
            result[model] = response
    
    return result