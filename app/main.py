from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException

from app.config import get_settings
from app.graph import agent_graph
from app.schemas import AgentRequest, AgentResponse, ApprovalResponse
from app.security import require_api_key
from app.store import RunStore

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
store = RunStore()


@app.get("/health")
def health():
    return {"status": "ok", "demo_mode": settings.demo_mode}


@app.post("/v1/agent/run", response_model=AgentResponse, dependencies=[Depends(require_api_key)])
def run_agent(payload: AgentRequest):
    state = agent_graph.invoke({"query": payload.query, "context": payload.context})
    run_id = str(uuid4())
    status = store.save(run_id, payload.query, state["route"], state["answer"], state["requires_approval"])
    return AgentResponse(
        run_id=run_id,
        route=state["route"],
        answer=state["answer"],
        requires_approval=state["requires_approval"],
        status=status,
    )


@app.get("/v1/agent/runs/{run_id}", dependencies=[Depends(require_api_key)])
def get_run(run_id: str):
    row = store.get(run_id)
    if not row:
        raise HTTPException(status_code=404, detail="Run not found")
    return row


@app.post("/v1/agent/runs/{run_id}/approve", response_model=ApprovalResponse, dependencies=[Depends(require_api_key)])
def approve_run(run_id: str):
    status = store.approve(run_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return ApprovalResponse(run_id=run_id, status=status)
