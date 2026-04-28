from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class StartSessionRequest(BaseModel):
    doc_types: List[str] = Field(
        default_factory=lambda: [
            "residential_purchase_agreement",
            "seller_disclosure",
            "lead_paint_disclosure",
            "agency_disclosure",
        ]
    )


class SessionResponse(BaseModel):
    session_id: str
    status: str
    next_question: str | None = None
    missing_fields: List[str] = Field(default_factory=list)


class AnswerRequest(BaseModel):
    answer: str


class DocumentResponse(BaseModel):
    doc_type: str
    content: str


class SessionState(BaseModel):
    session_id: str
    doc_types: List[str]
    collected_data: Dict[str, Any] = Field(default_factory=dict)
    missing_fields: List[str] = Field(default_factory=list)
    status: str = "in_progress"

