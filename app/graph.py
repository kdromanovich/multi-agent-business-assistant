from __future__ import annotations

from typing import Literal, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from app.config import get_settings
from app.tools import build_action_plan, extract_numbers, search_demo_knowledge

Route = Literal["research", "document", "data", "action"]
settings = get_settings()


class AgentState(TypedDict, total=False):
    query: str
    context: str
    route: Route
    answer: str
    requires_approval: bool


class RouteDecision(BaseModel):
    route: Route


def _heuristic_route(query: str) -> Route:
    q = query.lower()
    action_terms = [
        "send",
        "publish",
        "create task",
        "action",
        "execute",
        "отправ",
        "опубли",
        "создай зада",
    ]
    if any(term in q for term in action_terms):
        return "action"
    if any(term in q for term in ["roi", "margin", "revenue", "cost", "calculate", "посч", "марж", "выруч"]):
        return "data"
    if any(
        term in q
        for term in [
            "document",
            "contract",
            "text",
            "summar",
            "документ",
            "договор",
            "текст",
            "резюм",
        ]
    ):
        return "document"
    return "research"


def _model(temperature: float = 0) -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=temperature,
    )


def supervisor(state: AgentState):
    if settings.demo_mode or not settings.openai_api_key:
        return {"route": _heuristic_route(state["query"])}
    router = _model().with_structured_output(RouteDecision)
    decision = router.invoke(
        "Route this business request to exactly one specialist: research, document, "
        f"data, or action. Request: {state['query']}"
    )
    return {"route": decision.route}


def research_agent(state: AgentState):
    local = search_demo_knowledge(state["query"])
    if settings.demo_mode or not settings.openai_api_key:
        answer = f"Research summary (demo mode):\n{local}"
    else:
        answer = _model(0.2).invoke(
            "You are the research specialist. Answer the request using available local "
            "knowledge and context.\n"
            f"Request: {state['query']}\n"
            f"Context: {state.get('context', '')}\n"
            f"Local knowledge: {local}"
        ).content
    return {"answer": str(answer), "requires_approval": False}


def document_agent(state: AgentState):
    context = state.get("context", "").strip()
    if settings.demo_mode or not settings.openai_api_key:
        preview = context[:1200] if context else "No document context was supplied."
        answer = f"Document analysis (demo mode):\n{preview}"
    else:
        answer = _model().invoke(
            "You are the document specialist. Analyze only the supplied text. If "
            "information is missing, say so.\n"
            f"Request: {state['query']}\nDocument/context:\n{context}"
        ).content
    return {"answer": str(answer), "requires_approval": False}


def data_agent(state: AgentState):
    numbers = extract_numbers(state["query"] + " " + state.get("context", ""))
    if settings.demo_mode or not settings.openai_api_key:
        answer = f"Data specialist (demo mode): extracted numeric values = {numbers}."
    else:
        answer = _model().invoke(
            "You are the data specialist. Explain calculations explicitly and never "
            "invent missing values.\n"
            f"Request: {state['query']}\nContext: {state.get('context', '')}"
        ).content
    return {"answer": str(answer), "requires_approval": False}


def action_agent(state: AgentState):
    plan = build_action_plan(state["query"])
    numbered = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(plan))
    return {
        "answer": "Proposed action plan (not executed):\n" + numbered,
        "requires_approval": True,
    }


def route_after_supervisor(state: AgentState):
    return state["route"]


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor)
    graph.add_node("research", research_agent)
    graph.add_node("document", document_agent)
    graph.add_node("data", data_agent)
    graph.add_node("action", action_agent)
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "research": "research",
            "document": "document",
            "data": "data",
            "action": "action",
        },
    )
    for node in ["research", "document", "data", "action"]:
        graph.add_edge(node, END)
    return graph.compile()


agent_graph = build_graph()
