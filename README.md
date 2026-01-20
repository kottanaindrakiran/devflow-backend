# DevFlow AI Backend

The production-ready backend for the DevFlow AI agent system. Built with FastAPI and Pydantic AI.

## Project Overview

This backend powers the **DevFlow AI** frontend (React + Tailwind). It provides a generic AI agent interface that can Explain, Debug, Review, and Summarize code using the OpenRouter API.

**Note**: The frontend is a separate codebase and is already fully built. This repository contains ONLY the backend logic.

## Architecture

The system uses a **Multi-Agent Architecture** powered by **Pydantic AI**:

1.  **Intent Agent**: Deterministically routes requests to the correct specialist agent based on the `task` field.
2.  **Specialist Agents** (LLM-backed):
    *   `ExplainAgent`: Generates clear explanations of code snippets.
    *   `DebugAgent`: Analyzes code and error messages to find root causes.
    *   `ReviewAgent`: Performs code quality and security reviews.
3.  **Fallback Agent**: Ensures the system always returns a valid, user-friendly response, even if external APIs fail.
4.  **Router**: The central brain that orchestrates the flow. It handles:
    *   **Validation**: Ensures all inputs/outputs match Pydantic schemas.
    *   **Retries**: Automatically retries failed LLM calls (exponential backoff).
    *   **Error Handling**: Catches exceptions and delegates to the Fallback Agent.

## Security & Configuration

*   **API Keys**: OpenRouter API keys are read **only** from environment variables (`OPENROUTER_API_KEY`).
*   **Git**: `.env` files are git-ignored to prevent accidental checks-in.


## Folder Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables example
├── agents/                 # Agent implementations
│   ├── intent_agent.py     # Deterministic intent routing
│   ├── explain_agent.py    # Code explanation agent
│   ├── debug_agent.py      # Debugging agent
│   ├── review_agent.py     # Code review agent
│   ├── fallback_agent.py   # Error handling agent
│   └── router.py           # Central orchestration logic
├── schemas/                # Pydantic models
│   ├── request.py          # API Request models
│   └── response.py         # API Response models
├── services/               # External services
│   └── openrouter_client.py # OpenRouter API client
└── utils/                  # Utilities
    ├── logger.py           # Structured logging
    └── retry.py            # Retry logic decorator
```

## Setup & Installation

### Prerequisites

*   Python 3.11+
*   OpenRouter API Key

### Installation

1.  Navigate to the `backend` directory (if you are in the root):
    ```bash
    cd backend
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment:
    Copy `.env.example` to `.env` and add your OpenRouter API key.
    ```bash
    cp .env.example .env
    ```
    Edit `.env`:
    ```
    OPENROUTER_API_KEY=sk-or-v1-...
    ```

## Running Locally

Start the development server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
*Note: Make sure you run this from the parent directory of `backend` (i.e., `devflow-ai-main`), or adjust the import path accordingly.*
If running from inside `backend/`:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoint

**POST /api/agent/run**

Request:
```json
{
  "task": "explain",
  "code": "print('hello')",
  "error": null
}
```

Response:
```json
{
  "title": "Code Explanation",
  "summary": "This code prints hello to the console.",
  "issues": [],
  "suggestions": []
}
```

## Deployment

The application is designed for cloud deployment (Railway/Render/etc.).

### Health Check

**GET /health**
Returns `{"status": "ok"}`. Use this for load balancer or uptime monitoring.

### Deployment Command

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```
(Ensure `$PORT` is set by the platform, defaulting to 8000 if not)

### Environment Variables

Required in production:
*   `OPENROUTER_API_KEY`: Your OpenRouter API key.
*   `PORT`: (Optional) Port to listen on.
*   `LOG_LEVEL`: (Optional) Logging level (INFO, DEBUG).

