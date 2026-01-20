from typing import List, Optional
from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    title: str = Field(..., description="A concise title for the response")
    summary: str = Field(..., description="A summary of the analysis")
    issues: Optional[List[str]] = Field(default_factory=list, description="List of identified issues")
    suggestions: Optional[List[str]] = Field(default_factory=list, description="List of suggestions for improvement")
