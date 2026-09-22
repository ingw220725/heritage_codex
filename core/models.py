from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
import uuid

def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"

class RiskLevel(str, Enum):
    low = "low"
    elevated = "elevated"
    high = "high"
    critical = "critical"

class Verdict(str, Enum):
    watch = "watch"
    investigate = "investigate"
    veto = "veto"
    terminate = "terminate"

class SignalCreate(BaseModel):
    source_constellation: str
    scanners: list[str] = Field(default_factory=list)
    risk_level: RiskLevel
    summary: str
    divergence: bool = False
    raw_refs: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class Signal(SignalCreate):
    signal_id: str
    created_at: datetime

class VoteCreate(BaseModel):
    signal_id: str
    member_id: str
    vote: Verdict
    comment: str | None = None

class Vote(VoteCreate):
    vote_id: str
    created_at: datetime

class Decision(BaseModel):
    decision_id: str
    signal_id: str
    group_id: str
    verdict: Verdict
    votes: list[Vote]
    rationale: str
    created_at: datetime

class Precedent(BaseModel):
    precedent_id: str
    decision_id: str
    title: str
    summary: str
    tags: list[str] = Field(default_factory=list)
    published: bool = True
    created_at: datetime

class TestamentDraft(BaseModel):
    testament_id: str
    decision_id: str
    life_context: str
    unfinished_symphony: str
    anticipation: str
    emotional_imprint: str
    gratitude_and_mandate: str
    created_at: datetime

class AuditEvent(BaseModel):
    event_id: str
    event_type: str
    entity_id: str | None = None
    message: str
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime