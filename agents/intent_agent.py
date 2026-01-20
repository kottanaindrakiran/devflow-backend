from schemas.request import AgentRequest, TaskType
from utils.logger import logger

class IntentAgent:
    """
    Deterministic agent that routes requests based on the 'task' field.
    No LLM is needed as the frontend provides explicit intents.
    """
    
    async def run(self, request: AgentRequest) -> TaskType:
        logger.info(f"IntentAgent resolving task: {request.task}")
        # In a more complex system, this could involve NLU, but here it's direct mapping
        return request.task
