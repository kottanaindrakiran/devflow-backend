from typing import Dict, Any
from schemas.request import AgentRequest, TaskType
from schemas.response import AgentResponse
from .intent_agent import IntentAgent
from .explain_agent import ExplainAgent
from .debug_agent import DebugAgent
from .review_agent import ReviewAgent
from .fallback_agent import FallbackAgent
from utils.logger import logger
from utils.retry import async_retry

class AgentRouter:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.explain_agent = ExplainAgent()
        self.debug_agent = DebugAgent()
        self.review_agent = ReviewAgent()
        self.fallback_agent = FallbackAgent()
        
    @async_retry(max_retries=2, delay=1.0)
    async def _execute_agent(self, agent: Any, request: AgentRequest) -> AgentResponse:
        """
        Executes a specific agent with retry logic.
        """
        return await agent.run(request)

    async def route_request(self, request: AgentRequest) -> AgentResponse:
        """
        Main entry point. Routes the request to the appropriate agent.
        """
        try:
            # 1. Determine Intent
            # Since request.task is already validated by Pydantic, we can trust it.
            # But we still use IntentAgent as per architecture, though it's simple here.
            task_type = await self.intent_agent.run(request)
            
            logger.info(f"Routing request to {task_type}")
            
            # 2. Select Agent
            target_agent = None
            if task_type in [TaskType.EXPLAIN, TaskType.SUMMARIZE]:
                # "Explain Agent ... Also used for 'summarize'"
                target_agent = self.explain_agent
            elif task_type == TaskType.DEBUG:
                target_agent = self.debug_agent
            elif task_type == TaskType.REVIEW:
                target_agent = self.review_agent
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            # 3. Execute with Retry
            response = await self._execute_agent(target_agent, request)
            return response
            
        except Exception as e:
            logger.error(f"Error in routing/execution: {str(e)}")
            # 4. Fallback
            return await self.fallback_agent.run(request, str(e))
