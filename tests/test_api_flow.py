from fastapi.testclient import TestClient

from app.main import app


def test_agent_api_action_approval_and_persistence():
    headers = {"x-api-key": "test-key"}

    with TestClient(app) as client:
        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"
        assert health.json()["demo_mode"] is True

        unauthorized = client.post(
            "/v1/agent/run",
            json={"query": "send the weekly report", "context": ""},
        )
        assert unauthorized.status_code in {401, 403}

        run = client.post(
            "/v1/agent/run",
            headers=headers,
            json={"query": "send the weekly report", "context": "Revenue is stable."},
        )
        assert run.status_code == 200, run.text
        body = run.json()
        assert body["route"] == "action"
        assert body["requires_approval"] is True
        assert body["status"] == "pending_approval"
        run_id = body["run_id"]

        stored = client.get(f"/v1/agent/runs/{run_id}", headers=headers)
        assert stored.status_code == 200
        assert stored.json()["status"] == "pending_approval"
        assert stored.json()["route"] == "action"

        approved = client.post(
            f"/v1/agent/runs/{run_id}/approve",
            headers=headers,
        )
        assert approved.status_code == 200
        assert approved.json()["status"] == "approved"

        stored_after = client.get(f"/v1/agent/runs/{run_id}", headers=headers)
        assert stored_after.status_code == 200
        assert stored_after.json()["status"] == "approved"
        assert stored_after.json()["approved_at"]


def test_agent_api_routes_read_only_request_without_approval():
    headers = {"x-api-key": "test-key"}

    with TestClient(app) as client:
        run = client.post(
            "/v1/agent/run",
            headers=headers,
            json={"query": "summarize this document", "context": "Contract term is 12 months."},
        )
        assert run.status_code == 200
        body = run.json()
        assert body["route"] == "document"
        assert body["requires_approval"] is False
        assert body["status"] == "completed"
        assert "Contract term is 12 months." in body["answer"]
