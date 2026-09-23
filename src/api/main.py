from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.models import (
    AuditEvent,
    Decision,
    Precedent,
    Signal,
    SignalCreate,
    TestamentDraft,
    Vote,
    VoteCreate,
    Verdict,
    new_id,
)
from core.decision_engine import make_decision
from core.terminate import terminate_handler

app = FastAPI(
    title="Heritage Codex Skeleton",
    version="0.1.0",
    description="Minimal signal → group decision → terminate loop",
)

# ----------------------------
# In-memory stores
# ----------------------------

SIGNALS: Dict[str, Signal] = {}
VOTES: Dict[str, List[Vote]] = {}          # key = signal_id
DECISIONS: Dict[str, Decision] = {}
PRECEDENTS: Dict[str, Precedent] = {}
TESTAMENTS: Dict[str, TestamentDraft] = {}
AUDIT: List[AuditEvent] = []

DEFAULT_GROUP_ID = "group_alpha"

def now():
    return datetime.now(timezone.utc)

def add_audit(event_type: str, message: str, entity_id: str | None = None, data: dict | None = None):
    event = AuditEvent(
        event_id=new_id("evt"),
        event_type=event_type,
        entity_id=entity_id,
        message=message,
        data=data or {},
        created_at=now(),
    )
    AUDIT.append(event)
    return event

# ----------------------------
# Routes
# ----------------------------

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/signals", response_model=Signal)
def create_signal(payload: SignalCreate):
    signal = Signal(
        signal_id=new_id("sig"),
        created_at=now(),
        **payload.model_dump(),
    )
    SIGNALS[signal.signal_id] = signal
    VOTES[signal.signal_id] = []

    add_audit(
        event_type="signal_created",
        entity_id=signal.signal_id,
        message="New signal created",
        data=signal.model_dump(mode="json"),
    )
    return signal

@app.get("/signals/{signal_id}", response_model=Signal)
def get_signal(signal_id: str):
    signal = SIGNALS.get(signal_id)
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    return signal

@app.post("/votes", response_model=Vote)
def cast_vote(payload: VoteCreate):
    if payload.signal_id not in SIGNALS:
        raise HTTPException(status_code=404, detail="Signal not found")

    # one member = one vote per signal (simple rule)
    existing = VOTES.get(payload.signal_id, [])
    if any(v.member_id == payload.member_id for v in existing):
        raise HTTPException(status_code=400, detail="Member already voted on this signal")

    vote = Vote(
        vote_id=new_id("vote"),
        created_at=now(),
        **payload.model_dump(),
    )
    VOTES[payload.signal_id].append(vote)

    add_audit(
        event_type="vote_cast",
        entity_id=vote.vote_id,
        message=f"Vote cast by {vote.member_id}",
        data=vote.model_dump(mode="json"),
    )
    return vote

@app.get("/signals/{signal_id}/votes", response_model=List[Vote])
def list_votes(signal_id: str):
    if signal_id not in SIGNALS:
        raise HTTPException(status_code=404, detail="Signal not found")
    return VOTES.get(signal_id, [])

class DecideRequest(BaseModel):
    signal_id: str
    group_id: str = DEFAULT_GROUP_ID

@app.post("/decide", response_model=Decision)
def decide(payload: DecideRequest):
    if payload.signal_id not in SIGNALS:
        raise HTTPException(status_code=404, detail="Signal not found")

    votes = VOTES.get(payload.signal_id, [])
    if not votes:
        raise HTTPException(status_code=400, detail="No votes to decide on")

    decision = make_decision(
        signal_id=payload.signal_id,
        group_id=payload.group_id,
        votes=votes,
    )
    DECISIONS[decision.decision_id] = decision

    add_audit(
        event_type="decision_made",
        entity_id=decision.decision_id,
        message=f"Decision made: {decision.verdict.value}",
        data=decision.model_dump(mode="json"),
    )
    return decision

class TerminateRequest(BaseModel):
    decision_id: str
    context_summary: str = ""

@app.post("/terminate")
def terminate(payload: TerminateRequest):
    decision = DECISIONS.get(payload.decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")

    if decision.verdict != Verdict.terminate:
        raise HTTPException(
            status_code=400,
            detail=f"Decision verdict is '{decision.verdict.value}', not 'terminate'",
        )

    result = terminate_handler(decision, context_summary=payload.context_summary)

    # persist returned artifacts
    testament = result["testament"]
    precedent = result["precedent"]
    events = result["audit_events"]

    TESTAMENTS[testament.testament_id] = testament
    PRECEDENTS[precedent.precedent_id] = precedent
    AUDIT.extend(events)

    return {
        "status": "terminated",
        "decision_id": decision.decision_id,
        "testament_id": testament.testament_id,
        "precedent_id": precedent.precedent_id,
        "runtime": result["runtime"],
    }

@app.get("/decisions/{decision_id}", response_model=Decision)
def get_decision(decision_id: str):
    decision = DECISIONS.get(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision

@app.get("/precedents", response_model=List[Precedent])
def list_precedents():
    return list(PRECEDENTS.values())

@app.get("/audit", response_model=List[AuditEvent])
def list_audit():
    return AUDIT