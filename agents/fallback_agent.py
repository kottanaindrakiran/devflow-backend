from schemas.request import AgentRequest
from schemas.response import AgentResponse
from utils.logger import logger

class FallbackAgent:
    """
    Returns a safe, user-friendly response if anything fails.
    """
    
    async def run(self, request: AgentRequest, error_message: str = "Unknown error") -> AgentResponse:
        logger.warning(f"FallbackAgent invoked due to error: {error_message}")
        
        return AgentResponse(
            title="Analysis Unavailable",
            summary=f"We encountered an issue while processing your request. Please try again later.",
            issues=["System could not process the request.", error_message],
            suggestions=["Check your internet connection.", "Try simpler code snippets.", "Contact support if the issue persists."]
        )
