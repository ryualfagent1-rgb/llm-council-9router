# LLM Council (9Router Gateway Edition)

A 3-stage LLM deliberation system based on Karpathy's `llm-council`, adapted to run against **9Router** (or any OpenAI-compatible gateway).

## Features
- **Stage 1: First opinions**: Parallel responses from council models.
- **Stage 2: Anonymized Peer Review**: Models critique and rank each other blindly.
- **Stage 3: Chairman Synthesis**: Chairman model compiles final consensus answer.
- **9Router Integration**: Uses a single endpoint (`/v1/chat/completions`) with your 9Router models.

## Setup

### 1. Prerequisites
- [9Router](https://github.com/decolua/9router) running (e.g., `http://localhost:20128`).
- [uv](https://docs.astral.sh/uv/) for Python environment management.
- Node.js for frontend.

### 2. Configure Environment
Create `.env` in project root:
```env
NINEROUTER_URL=http://localhost:20128
NINEROUTER_KEY=sk-your-9router-key-here

# Optional model customization (comma-separated):
COUNCIL_MODELS=ryu.alf.agentic1,kr/claude-haiku-4.5,kr/deepseek-3.2,gemini/gemini-3.7-flash
CHAIRMAN_MODEL=gemini/gemini-3.7-flash
```

### 3. Run Backend & Frontend

Terminal 1 (Backend):
```bash
uv sync
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.