# Multi-Agent Business Assistant

[![CI](https://github.com/kdromanovich/multi-agent-business-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/kdromanovich/multi-agent-business-assistant/actions/workflows/ci.yml)

[Русская версия](README_RU.md)

A **LangGraph** multi-agent reference backend that routes business requests to specialist agents, persists runs, requires human approval for action-oriented requests, and exposes reusable tools through the **Model Context Protocol (MCP)**.

## Architecture

```mermaid
flowchart TD
    U[Client] --> API[FastAPI]
    API --> S[Supervisor]
    S --> R[Research Agent]
    S --> D[Document Agent]
    S --> A[Data Agent]
    S --> X[Action Agent]
    X --> H{Human approval}
    R --> DB[(Run store)]
    D --> DB
    A --> DB
    X --> DB
    T[MCP clients] --> MCP[MCPServer v2]
    MCP --> K[Knowledge / ROI / planning tools]
```

## What it demonstrates

- LangGraph state graph and conditional routing;
- supervisor + specialist agent pattern;
- OpenAI-backed routing and generation in live mode;
- deterministic `DEMO_MODE=true` so the repository runs without paid APIs;
- human-in-the-loop boundary before high-impact actions;
- persisted run/audit state;
- separate MCP v2 server exposing typed tools;
- FastAPI, Docker, integration tests and CI.

## Agents

| Agent | Purpose |
|---|---|
| Research | Finds relevant local knowledge and synthesizes context |
| Document | Analyzes only supplied document/context text |
| Data | Handles numeric/business-analysis requests |
| Action | Creates an action proposal and forces human approval |

## CI verification

The CI suite exercises the FastAPI surface in deterministic demo mode. It verifies API-key protection, supervisor routing, persisted run state, the `pending_approval` safety boundary and the explicit approval transition. Tool-level and routing unit tests run alongside this API integration flow.

## Run the API

```bash
cp .env.example .env
docker compose up --build
```

The default is demo mode. Set `DEMO_MODE=false` and provide `OPENAI_API_KEY` for live LLM routing and specialist responses.

API: `http://localhost:8001/docs`

## Run the MCP server

```bash
pip install -e .
python -m app.mcp_server
```

The MCP server uses the current SDK v2 style and exposes typed tools for knowledge lookup, ROI calculation and action-plan preparation.

## Safety design

The action agent **never performs an external side effect**. It produces a proposal with `pending_approval`, and `/v1/agent/runs/{run_id}/approve` records explicit approval. A real integration can attach execution only after that state transition.

## Scope

This is a portfolio reference implementation, not a claim of a deployed customer production system. Demo mode is intentionally deterministic so reviewers can inspect the architecture and run the API without paid credentials.

## License

MIT
