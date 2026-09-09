from mcp.server import MCPServer
from app.tools import build_action_plan, calculate_roi, search_demo_knowledge

mcp = MCPServer(
    "Business Assistant Tools",
    instructions="Read-only and planning tools for business analysis. External actions require separate approval.",
)


@mcp.tool()
def knowledge_lookup(query: str) -> str:
    """Search the demo business knowledge base."""
    return search_demo_knowledge(query)


@mcp.tool()
def roi(revenue_gain: float, cost_saving: float, implementation_cost: float) -> dict:
    """Calculate simple ROI from revenue gain, savings and implementation cost."""
    return calculate_roi(revenue_gain, cost_saving, implementation_cost)


@mcp.tool()
def action_plan(request: str) -> list[str]:
    """Prepare a human-reviewable action plan without executing it."""
    return build_action_plan(request)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", stateless_http=True, json_response=True)
