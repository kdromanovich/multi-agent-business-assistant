from typing import Literal
from pydantic import BaseModel, Field

Route = Literal["research", "document", "data", "action"]


class AgentRequest(BaseModel):
    query: str = Field(min_length=2, max_length=6000)
    context: str = Field(default="", max_length=20000)


class AgentResponse(BaseModel):
    run_id: str
    route: Route
    answer: str
    requires_approval: bool
    status: str


class ApprovalResponse(BaseModel):
    run_id: str
    status: str
