# LLM Council

A 3-stage LLM deliberation web app adapted from [karpathy/llm-council](https://github.com/karpathy/llm-council). Query a panel of models in parallel, have them anonymously review and rank each other's outputs, then a Chairman model produces the final consensus answer.

This edition runs against **[9Router](https://github.com/decolua/9router)** — a local OpenAI-compatible gateway that lets you mix models from OpenAI, Anthropic, Google, Groq, and other providers behind a single endpoint and key. Any OpenAI-compatible endpoint works by changing one environment variable.

## Vibe Code Alert

This project was assembled in a single session as a working bridge between the [karpathy/llm-council](https://github.com/karpathy/llm-council) architecture and the [9Router](https://github.com/decolua/9router) gateway. It is functional and verified end-to-end, but it is not a polished product. Treat it as a starting point — read the code, change what you want, delete what you don't. Code is ephemeral now and libraries are over; ask your LLM to modify it however you like.

## Setup

### 1. Install Dependencies

**Backend** (Python 3.10+, managed with [uv](https://docs.astral.sh/uv/)):

```bash
uv sync
```

**Frontend** (Node.js 18+):

```bash
cd frontend
npm install
cd ..
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
NINEROUTER_URL=http://localhost:20128
NINEROUTER_KEY=sk-your-9router-key-here
```

| Variable           | Required | Default                     | Description                                                      |
| ------------------ | -------- | --------------------------- | ---------------------------------------------------------------- |
| `NINEROUTER_URL`   | No       | `http://localhost:20128`    | Base URL of your 9Router (or any OpenAI-compatible) gateway.     |
| `NINEROUTER_KEY`   | No       | _(empty)_                   | Bearer token. Required if your gateway has `REQUIRE_API_KEY=true`. Leave blank for local dev. |
| `COUNCIL_MODELS`   | No       | _(see config.py)_           | Comma-separated list of model IDs to query in parallel.          |
| `CHAIRMAN_MODEL`   | No       | `gemini/gemini-3.7-flash`   | Model used to synthesize the final answer.                       |
| `DATA_DIR`         | No       | `data/conversations`        | Where conversation history JSON files are stored.                |

Get a 9Router key from your local gateway dashboard, or run 9Router in unauthenticated mode (`--requireApiKey=false`).

### 3. Configure Models (Optional)

Edit `backend/config.py` to change the default council composition:

```python
COUNCIL_MODELS = [
    "ryu.alf.agentic1",
    "kr/claude-haiku-4.5",
    "kr/deepseek-3.2",
    "gemini/gemini-3.7-flash",
]

CHAIRMAN_MODEL = "gemini/gemini-3.7-flash"
```

Or override at runtime via environment variables (comma-separated):

```bash
COUNCIL_MODELS="openai/gpt-4o,anthropic/claude-3-5-sonnet,gemini/gemini-1.5-pro" \
CHAIRMAN_MODEL="anthropic/claude-3-5-sonnet" \
uv run python -m backend.main
```

Discover what's available on your gateway:

```bash
curl http://localhost:20128/v1/models | jq '.data[].id'
```

## Running the Application

**Terminal 1 — Backend** (FastAPI on port 8001):

```bash
uv run python -m backend.main
```

**Terminal 2 — Frontend** (Vite dev server on port 5173):

```bash
cd frontend
npm run dev
```

Open <http://localhost:5173> in your browser.

When you submit a query, three stages execute:

1. **Stage 1 — First opinions.** Your query is sent in parallel to every model in `COUNCIL_MODELS`. Responses appear as tabs so you can inspect them individually.
2. **Stage 2 — Review.** Each model receives the other responses under anonymized labels (Response A, B, C…). It evaluates and ranks them. The aggregate ranking across all reviewers is displayed.
3. **Stage 3 — Final response.** The Chairman model sees all stage 1 responses plus all stage 2 rankings and produces a single consensus answer.

## Tech Stack

| Layer       | Technology                                                                    |
| ----------- | ----------------------------------------------------------------------------- |
| Backend     | FastAPI, Uvicorn, httpx (async), python-dotenv, Pydantic                      |
| Frontend    | React 19, Vite, react-markdown                                                |
| LLM Gateway | [9Router](https://github.com/decolua/9router) — OpenAI-compatible REST        |
| Storage     | JSON files in `data/conversations/` (one file per conversation)               |
| Tooling     | [uv](https://docs.astral.sh/uv/) (Python), npm (JS), git                      |
