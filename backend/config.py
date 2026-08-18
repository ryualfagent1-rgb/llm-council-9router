"""Configuration for the LLM Council (9Router compatible)."""

import os
from dotenv import load_dotenv

load_dotenv()

# 9Router API endpoint (can be overridden via env)
NINEROUTER_URL = os.getenv("NINEROUTER_URL", "http://localhost:20128")
NINEROUTER_KEY = os.getenv("NINEROUTER_KEY", "")

# Council members - list of model IDs available on your 9Router
# Override via COUNCIL_MODELS env var (comma-separated) or edit here
_default_models = [
    "ryu.alf.agentic1",
    "kr/claude-haiku-4.5",
    "kr/deepseek-3.2",
    "gemini/gemini-3.7-flash",
]
COUNCIL_MODELS = [
    m.strip() for m in os.getenv("COUNCIL_MODELS", ",".join(_default_models)).split(",")
    if m.strip()
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL", "gemini/gemini-3.7-flash")

# 9Router chat completions endpoint
NINEROUTER_CHAT_URL = f"{NINEROUTER_URL}/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = os.getenv("DATA_DIR", "data/conversations")