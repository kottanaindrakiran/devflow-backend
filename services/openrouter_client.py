import os
from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    _model_instance = None
    
    @classmethod
    def get_model(cls, model_name: str = "meta-llama/llama-3-8b-instruct"):
        """
        Returns a configured Pydantic AI OpenAIModel instance for OpenRouter.
        """
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
            
        if cls._model_instance is None:
            # Set environment variables for OpenAI client to pick up
            os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
            os.environ["OPENAI_API_KEY"] = api_key
            
            cls._model_instance = OpenAIModel(model_name)
        
        return cls._model_instance

def get_chat_model():
    return OpenRouterClient.get_model()
