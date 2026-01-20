from pydantic_ai import Agent
from schemas.request import AgentRequest
from schemas.response import AgentResponse
from services.openrouter_client import get_chat_model
from utils.logger import logger

class ReviewAgent:
    def __init__(self):
        self.pydantic_agent = Agent(
            get_chat_model(),
            # output_type removed to prevent tool usage
            # model_settings removed to prevent tool_choice errors
            system_prompt="""
            You are a senior code reviewer. Review the provided code for quality, best practices, performance, and security.
            Identify any code smells, potential bugs, or improvements.
            Provide a summary of the review and specific actionable suggestions.
            Provide your response in plain text.
            """
        )

    async def run(self, request: AgentRequest) -> AgentResponse:
        logger.info("ReviewAgent running...")
        result = await self.pydantic_agent.run(
            f"Please review this code:\n\n{request.code}"
        )
        
        # Wrap natural language response in acceptable schema
        return AgentResponse(
             title="Code Review",
             summary=result.output.strip(),
             issues=[],
             suggestions=[]
        )
