from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class TaskType(str, Enum):
    EXPLAIN = "explain"
    DEBUG = "debug"
    REVIEW = "review"
    SUMMARIZE = "summarize"

class AgentRequest(BaseModel):
    task: TaskType = Field(..., description="The type of task to perform")
    code: str = Field(..., description="The code snippet to process")
    error: Optional[str] = Field(None, description="Optional error message for debugging")
