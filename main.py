from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.request import AgentRequest
from schemas.response import AgentResponse
from agents.router import AgentRouter
from utils.logger import logger

app = FastAPI(title="DevFlow AI Backend", version="1.0.0")

# Configure CORS
# In production, specific origins should be allowed.
# For this project, we allow all to match the frontend development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
agent_router = AgentRouter()

@app.get("/")
async def root():
    return {"message": "DevFlow AI Backend is running"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint for deployment verification.
    """
    return {"status": "ok"}

@app.post("/api/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    Main endpoint for the AI agent system.
    Orchestrates the request to the appropriate agent.
    """
    logger.info(f"Received request: {request.task}")
    try:
        response = await agent_router.route_request(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled error in endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    # When running directly, app is just "main:app" because we are in main.py
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
