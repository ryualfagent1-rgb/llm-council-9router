# LLM Council

## Vibe Code Alert

LLM Council (9Router Gateway Edition) is an agentic multi-model deliberation system that queries a panel of LLMs in parallel, coordinates blind peer review, and synthesizes a consensus answer through a designated Chairman model. Powered by **9Router**, it routes requests to any OpenAI-compatible provider without code changes. This project was built as an experimental hack exploring multi-agent consensus and is provided as-is for inspiration and custom adaptation.

## Setup

### 1. Install Dependencies

Ensure Python 3.10+, [uv](https://docs.astral.sh/uv/), and Node.js 18+ are installed.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure API Key

Create a `.env` file in the project root:

```env
NINEROUTER_URL=http://localhost:20128
NINEROUTER_KEY=sk-your-9router-key-here
```

### 3. Configure Models (Optional)

Customize council models and the chairman in `backend/config.py` or via environment variables (`COUNCIL_MODELS`, `CHAIRMAN_MODEL`).

## Running the Application

Start the backend and frontend in separate terminals:

**Terminal 1 (Backend):**
```bash
uv run python -m backend.main
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser.

## Tech Stack

- **Backend:** FastAPI, Python 3.10+, async httpx, Pydantic
- **Frontend:** React, Vite, ReactMarkdown
- **Gateway:** 9Router (OpenAI-compatible REST)
- **Storage:** Local JSON file storage in `data/conversations/`
- **Package Management:** `uv` (Python) and `npm` (JavaScript)
