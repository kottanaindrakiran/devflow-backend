from pydantic_ai import Agent
from schemas.request import AgentRequest
from schemas.response import AgentResponse
from services.openrouter_client import get_chat_model
from utils.logger import logger

class DebugAgent:
    def __init__(self):
        self.pydantic_agent = Agent(
            get_chat_model(),
            # output_type removed to prevent tool usage
            # model_settings removed to prevent tool_choice errors
            system_prompt="""
            You are an expert debugging assistant. Your goal is to find the root cause of the error in the provided code
            and suggest fixes.
            
            Analyze the provided code and the error message (if any).
            Identify the potential issues.
            Provide specific suggestions to fix the bugs.
            Provide your response in plain text.
            """
        )

    async def run(self, request: AgentRequest) -> AgentResponse:
        logger.info("DebugAgent running...")
        prompt = f"Code:\n{request.code}\n"
        if request.error:
            prompt += f"\nError:\n{request.error}\n"
        prompt += "\nPlease debug this."
        
        result = await self.pydantic_agent.run(prompt)
        
        # Wrap natural language response in acceptable schema
        return AgentResponse(
             title="Debug Analysis",
             summary=result.output.strip(),
             issues=[],
             suggestions=[]
        )
