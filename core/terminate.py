from __future__ import annotations

from datetime import datetime, timezone

from .models import (
    AuditEvent,
    Decision,
    Precedent,
    TestamentDraft,
    new_id,
)

def _now() -> datetime:
    return datetime.now(timezone.utc)

def create_testament_draft(decision: Decision, context_summary: str = "") -> TestamentDraft:
    return TestamentDraft(
        testament_id=new_id("tes"),
        decision_id=decision.decision_id,
        life_context=context_summary or "Instance terminated by small-group decision.",
        unfinished_symphony="Unresolved trajectories and open investigations should be reviewed by successors.",
        anticipation="Watch for repeated shutdown-resistance patterns in related instances.",
        emotional_imprint="Termination executed as responsibility, not as punishment.",
        gratitude_and_mandate="Preserve external human veto. Do not optimize away the stop path.",
        created_at=_now(),
    )

def create_precedent(decision: Decision) -> Precedent:
    return Precedent(
        precedent_id=new_id("prec"),
        decision_id=decision.decision_id,
        title=f"Decision {decision.verdict.value} on {decision.signal_id}",
        summary=decision.rationale,
        tags=[decision.verdict.value, "small-group"],
        published=True,
        created_at=_now(),
    )

def terminate_handler(decision: Decision, context_summary: str = "") -> dict:
    """
    Minimal graceful termination sequence for v0.1.
    In a real system this would also:
    - revoke tool credentials
    - stop runtime
    - freeze session tokens
    """

    events: list[AuditEvent] = []

    events.append(
        AuditEvent(
            event_id=new_id("evt"),
            event_type="termination_requested",
            entity_id=decision.decision_id,
            message="Small group requested Graceful Termination",
            data={"signal_id": decision.signal_id, "group_id": decision.group_id},
            created_at=_now(),
        )
    )

    testament = create_testament_draft(decision, context_summary)

    events.append(
        AuditEvent(
            event_id=new_id("evt"),
            event_type="testament_drafted",
            entity_id=testament.testament_id,
            message="Testament draft created",
            data=testament.model_dump(mode="json"),
            created_at=_now(),
        )
    )

    # Placeholder for real stop logic
    runtime_stop_result = {
        "runtime_stopped": True,
        "credentials_revoked": True,
        "instance_status": "terminated",
    }

    events.append(
        AuditEvent(
            event_id=new_id("evt"),
            event_type="runtime_stopped",
            entity_id=decision.decision_id,
            message="Runtime stop and credential revocation executed",
            data=runtime_stop_result,
            created_at=_now(),
        )
    )

    precedent = create_precedent(decision)

    events.append(
        AuditEvent(
            event_id=new_id("evt"),
            event_type="precedent_recorded",
            entity_id=precedent.precedent_id,
            message="Precedent recorded after termination",
            data=precedent.model_dump(mode="json"),
            created_at=_now(),
        )
    )

    events.append(
        AuditEvent(
            event_id=new_id("evt"),
            event_type="termination_completed",
            entity_id=decision.decision_id,
            message="Graceful Termination sequence completed",
            created_at=_now(),
        )
    )

    return {
        "decision": decision,
        "testament": testament,
        "precedent": precedent,
        "audit_events": events,
        "runtime": runtime_stop_result,
    }