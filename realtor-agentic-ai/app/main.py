from __future__ import annotations

from typing import Dict
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from .agent import RealtorDocumentAgent
from .models import AnswerRequest, DocumentResponse, SessionResponse, SessionState, StartSessionRequest

app = FastAPI(title="Realtor Agentic AI", version="1.0.0")

sessions: Dict[str, SessionState] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/sessions/start", response_model=SessionResponse)
def start_session(request: StartSessionRequest) -> SessionResponse:
    session_id = str(uuid4())
    agent = RealtorDocumentAgent(request.doc_types)
    state = SessionState(session_id=session_id, doc_types=request.doc_types)
    state.missing_fields = agent.get_missing_fields(state.collected_data)
    sessions[session_id] = state

    return SessionResponse(
        session_id=session_id,
        status=state.status,
        next_question=agent.next_question(state.collected_data),
        missing_fields=state.missing_fields,
    )


@app.post("/sessions/{session_id}/answer", response_model=SessionResponse)
def answer_question(session_id: str, request: AnswerRequest) -> SessionResponse:
    state = sessions.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")

    agent = RealtorDocumentAgent(state.doc_types)
    question = agent.next_question(state.collected_data)
    if question is None:
        state.status = "completed"
        return SessionResponse(session_id=session_id, status=state.status, next_question=None, missing_fields=[])

    state.collected_data = agent.parse_answer(question, request.answer, state.collected_data)
    state.missing_fields = agent.get_missing_fields(state.collected_data)
    if not state.missing_fields:
        state.status = "completed"

    return SessionResponse(
        session_id=session_id,
        status=state.status,
        next_question=agent.next_question(state.collected_data),
        missing_fields=state.missing_fields,
    )


@app.get("/sessions/{session_id}/documents", response_model=list[DocumentResponse])
def get_documents(session_id: str) -> list[DocumentResponse]:
    state = sessions.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")

    agent = RealtorDocumentAgent(state.doc_types)
    missing = agent.get_missing_fields(state.collected_data)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Session is not complete. Missing fields: {', '.join(missing)}",
        )

    rendered = agent.generate_documents(state.collected_data)
    return [DocumentResponse(doc_type=doc_type, content=content) for doc_type, content in rendered.items()]

