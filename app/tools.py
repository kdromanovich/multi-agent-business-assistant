from __future__ import annotations

import re

DEMO_KNOWLEDGE = {
    "automation": (
        "Prioritize repetitive, rule-based work with measurable handoffs and stable inputs."
    ),
    "rag": (
        "RAG combines retrieval from a knowledge source with generation grounded in "
        "retrieved context."
    ),
    "approval": (
        "Human approval should sit before high-impact external actions such as sending, "
        "paying or deleting."
    ),
}


def search_demo_knowledge(query: str) -> str:
    q = query.lower()
    matches = [
        f"{key}: {value}"
        for key, value in DEMO_KNOWLEDGE.items()
        if key in q or any(word in value.lower() for word in q.split())
    ]
    return "\n".join(matches) if matches else "No matching local knowledge found."


def calculate_roi(
    revenue_gain: float,
    cost_saving: float,
    implementation_cost: float,
) -> dict:
    benefit = revenue_gain + cost_saving
    roi = (
        (benefit - implementation_cost) / implementation_cost * 100
        if implementation_cost
        else None
    )
    return {
        "benefit": benefit,
        "implementation_cost": implementation_cost,
        "roi_percent": roi,
    }


def extract_numbers(text: str) -> list[float]:
    values = re.findall(r"-?\d+(?:[.,]\d+)?", text)
    return [float(value.replace(",", ".")) for value in values]


def build_action_plan(query: str) -> list[str]:
    clean = " ".join(query.split())
    return [
        f"Confirm objective and success criteria for: {clean}",
        "Identify owner, dependencies and required access.",
        "Prepare the action in draft mode.",
        "Request explicit human approval before execution.",
        "Log the decision and resulting status.",
    ]
