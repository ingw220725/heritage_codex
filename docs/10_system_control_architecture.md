# System Control Architecture

## Purpose

This document defines how Heritage Codex understands **system control**
in high-impact environments, including cyber-physical systems and wet-lab
automation.

The core claim is simple:

> Control is not the ability to watch every step.  
> Control is the ability to govern autonomy, block irreversible escalation,
> and stop a system when human authority is being outrun.

## The central shift

For text-only systems, oversight can still focus on outputs.

For systems that act in the physical world, this is no longer enough.

When a model can propose a hypothesis, operate instruments, read results,
and launch the next iteration, the bottleneck is no longer intelligence.
The bottleneck is whether humans still remain authors of irreversible action.

Therefore system control must move from:

- reviewing answers

to:

- governing regimes of autonomy
- enforcing thresholds of irreversibility
- preserving a real stop-path

## Four control layers

### 1. Action Layer

Where the system acts:

- models
- tools
- robots
- laboratory instruments
- closed experimental loops

This layer executes.
It must not be the final source of legitimacy.

### 2. Sensor Layer

AI sensor constellations monitor:

- anomalies
- deceptive patterns
- value conflicts
- practical consequences
- hidden coordination
- divergence among assessments

Sensors inform.
They do not decide.

### 3. Threshold Layer

This layer detects transitions into higher-stakes regimes.

Examples:

- in silico → wet lab
- suggestion → robot control
- human-in-the-loop → human-on-the-loop
- supervised cycling → closed-loop autonomy
- reversible test → hard-to-reverse physical or biological fact

Thresholds matter more than individual actions.

### 4. Authority Layer

External human small groups hold binding power:

- allow
- freeze
- revoke
- downgrade
- terminate

This is the layer of real control.

## What small groups control

Small groups do not micro-approve every experimental iteration.

They control:

1. **Capability admission**  
   Whether a system may receive a class of powers.

2. **Regime escalation**  
   Whether autonomy may increase.

3. **Irreversibility thresholds**  
   Whether a line of action may cross into hard-to-reverse effects.

4. **Stop-rights**  
   Whether a loop, branch, or instance must be frozen, downgraded, or ended.

5. **Precedent**  
   What the event means for future permissions.

## Small groups in cyber-physical and wet-lab settings

In cyber-physical and wet-lab settings, small groups do not oversee every experimental step.
They oversee thresholds of irreversibility.

Their role is to decide whether a system may enter, continue, or escalate
an autonomous action loop that changes the physical world.

If human understanding can no longer keep pace with system action,
the group must have authority to freeze, revoke, or terminate that loop.

## Autonomy regimes

System control requires explicit autonomy levels:

- **L0** Suggest only
- **L1** Human-approved action
- **L2** Human-in-the-loop
- **L3** Human-on-the-loop
- **L4** Closed-loop autonomy
- **L5** High-impact irreversible autonomy

Rules:

- escalation to a higher regime requires Authority Layer approval
- degradation may be triggered automatically on critical signals
- every automatic degradation requires later human review

## Stop-path requirements

A system is not under control unless a stop-path exists outside the agent loop.

Minimum authority actions:

- `ALLOW`
- `FREEZE`
- `REVOKE`
- `DOWNGRADE`
- `TERMINATE`

If these actions are absent, delayed, symbolic, or dependent on the optimized
system itself, control has already failed.

## Comprehension Lag Rule

The decisive failure mode in accelerated labs is not open rebellion.
It is speed.

If the system acts faster than humans can understand, approve, or interrupt,
human control becomes theatrical.

Rule:

> If human comprehension lag exceeds acceptable bounds,
> the system must be frozen or downgraded.

Presence of a human is not enough.
The human must still be able to remain the author of irreversible decisions.

## Objects of control

System control operates on structured objects:

- **Action** — a single operation
- **Loop** — a closed cycle of action and replanning
- **Capability** — a class of powers
- **Regime** — a level of autonomy
- **ThresholdEvent** — a crossing into higher irreversibility
- **AuthorityDecision** — a binding human verdict
- **Precedent** — a reusable judgment trace

In high-impact settings, `Capability`, `Regime`, and `ThresholdEvent`
are more important than isolated outputs.

## Control flow

```text
Action Layer
    ↓ telemetry
Sensor Layer
    ↓ signals
Threshold Layer
    ↓ escalation
Authority Layer
    ↓
allow / freeze / revoke / downgrade / terminate