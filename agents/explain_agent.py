from pydantic_ai import Agent
from schemas.request import AgentRequest
from schemas.response import AgentResponse
from services.openrouter_client import get_chat_model
from utils.logger import logger

class ExplainAgent:
    def __init__(self):
        self.pydantic_agent = Agent(
            get_chat_model(),
            # output_type removed to prevent tool usage
            # model_settings removed to prevent tool_choice errors
            system_prompt="""
            You are an expert code explainer. Analyze the provided code and explain it clearly and concisely.
            Focus on what the code does, how it works, and any key patterns used.
            Avoid line-by-line narration unless necessary for complex logic.
            Provide your response in plain text.
            """
        )

    async def run(self, request: AgentRequest) -> AgentResponse:
        logger.info("ExplainAgent running...")
        result = await self.pydantic_agent.run(
            f"Please explain this code:\n\n{request.code}"
        )
        
        # Wrap natural language response in acceptable schema
        return AgentResponse(
             title="Code Explanation",
             summary=result.output.strip(),
             issues=[],
             suggestions=[]
        )
