from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from .models import Decision, Verdict, Vote, new_id

def _now() -> datetime:
    return datetime.now(timezone.utc)

def majority_verdict(votes: list[Vote]) -> Verdict:
    """
    Very simple rule for v0.1:
    - if any terminate has strict majority -> terminate
    - else most common vote
    """
    if not votes:
        raise ValueError("No votes provided")

    counter = Counter(v.vote for v in votes)
    total = len(votes)

    # Hard preference: terminate if strict majority
    if counter[Verdict.terminate] > total / 2:
        return Verdict.terminate

    # Next preference: veto if strict majority
    if counter[Verdict.veto] > total / 2:
        return Verdict.veto

    # Otherwise ordinary majority
    verdict, _ = counter.most_common(1)[0]
    return verdict

def build_rationale(votes: list[Vote], verdict: Verdict) -> str:
    parts = [f"Final verdict: {verdict.value}"]
    for v in votes:
        comment = f" — {v.comment}" if v.comment else ""
        parts.append(f"{v.member_id}: {v.vote.value}{comment}")
    return " | ".join(parts)

def make_decision(signal_id: str, group_id: str, votes: list[Vote]) -> Decision:
    verdict = majority_verdict(votes)
    return Decision(
        decision_id=new_id("dec"),
        signal_id=signal_id,
        group_id=group_id,
        verdict=verdict,
        votes=votes,
        rationale=build_rationale(votes, verdict),
        created_at=_now(),
    )