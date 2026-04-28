from fastapi.testclient import TestClient

from app.main import app


def test_session_flow() -> None:
    client = TestClient(app)

    start = client.post("/sessions/start", json={})
    assert start.status_code == 200
    payload = start.json()
    assert payload["session_id"]
    assert payload["status"] == "in_progress"

    session_id = payload["session_id"]

    answers = [
        "Alex Morgan",
        "Jordan Lee",
        "100 Main St, Austin, TX 78701",
        "$500,000",
        "$10,000",
        "2026-06-15",
        "No known defects",
        "8",
        "5",
        "1978",
        "no",
        "no",
        "Casey Rivera",
        "Summit Realty Group",
        "Alex Morgan",
        "Buyer representation",
    ]

    for answer in answers:
        response = client.post(f"/sessions/{session_id}/answer", json={"answer": answer})
        assert response.status_code == 200

    docs = client.get(f"/sessions/{session_id}/documents")
    assert docs.status_code == 200
    body = docs.json()
    assert len(body) == 4
    assert any(doc["doc_type"] == "residential_purchase_agreement" for doc in body)

