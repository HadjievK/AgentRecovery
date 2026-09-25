# Walkthrough: a classifier decides *when*, the machine decides *what*

This narrates one concrete incident end to end to show the boundary from
[specification §11](../SPEC.md#11-classifier-assisted-decisions): a fast "System One"
classifier (for example [Jev](https://www.langchain.com/blog/building-a-harness-with-jev))
decides *when recovery is needed and how urgent it is*; the deterministic recovery
controller decides *what is safe to do*.

It traces the [procurement-request machine](procurement-request/RECOVERY.yaml). No
part of this changes machine semantics — the classifier only produces candidate
events and advisory evidence.

## The incident

An agent calls `procurement.create-request` for a €48,000 hardware order. The call
**times out after 30 s**. The agent has a raw signal — a timeout — and nothing else.
A timeout is not proof the request failed; the vendor system may already hold the
order.

## Step 1 — Classifier decides *when* (System One)

The agent's harness sends the classifier the operation state and asks bounded,
typed questions. It does **not** ask the classifier what to do.

```text
state:    { tool: procurement.create-request, signal: timeout,
            amount_eur: 48000, idempotency_key: pr-9f3a... }

choice  "Which recovery event does this signal represent?"
        VERIFICATION_INCONCLUSIVE   0.62
        VERIFICATION_FAILED         0.28
        START_VERIFICATION          0.10

score   "How urgent is human attention?"   ->  high  (0.71)
```

The harness applies its own policy to these probabilities (its code, not the
model): the top event is below a confident-routing threshold, so it emits the
**most conservative** candidate the state accepts — `START_VERIFICATION` — and
tags the incident high-urgency. **The classifier proposed; the harness disposed.**

## Step 2 — Controller decides *what* (System Two)

The candidate event enters the controller as **untrusted input**. The controller
loads the pinned machine, validates the event against the current state, and
advances deterministically. Probabilities never touch a guard.

| State (`classification`) | Event | Guard decision (deterministic) | Action taken |
|---|---|---|---|
| `effect-possible` | `START_VERIFICATION` | — | `verify: procurement.find-by-idempotency-key` |
| `verifying` | `VERIFICATION_INCONCLUSIVE` | — | → `unknown` |
| `unknown` | *(entry)* | — | `contain: agent.stop-task`, `revoke: identity.revoke-task-token`, `contain: workflow.cancel-descendants` |
| `unknown` | `CONTAINMENT_COMPLETED` | — | `escalate: incident.open-procurement-case` → `escalated` |
| `escalated` | `HUMAN_RESOLUTION_RECORDED` | `incident.resolution-verified` ✅ | → `resume-pending` |
| `resume-pending` | `RESUME_APPROVED` | `resume.evidence-and-owner-approval-verified` ✅ | `resume: identity.issue-new-task-token`, `resume: agent.resume-task` → `closed` |

The authoritative verification came back **inconclusive** — the vendor API was
degraded. Because the state is `unknown`, the machine does **not** retry (that
would risk a duplicate €48k order). It contains, escalates to a human, and only
resumes after a real person and two deterministic guards approve.

Note what the classifier's 0.62 did and did not do: it got the incident *routed
into recovery quickly*. It did **not** decide to retry, did **not** authorize
resumption, and was **not** consulted at either guard.

## Step 3 — Why both properties survive

**Determinism.** Every transition above is `state + event + guard + policy →
actions + next state`. Swap the classifier for a different model, a rules engine,
or a human clicking a button, and the machine behaves identically. The classifier
is a replaceable front door, not part of the lock.

**Auditability.** The classifier's output is recorded as *evidence*, kept
**distinct** from the guard decision that actually authorized anything:

```jsonc
{
  "event_id": "evt-4c21",
  "state_before": "verifying",
  "evidence_reference": {
    "classifier": "jev",
    "version": "2026-08",
    "question": "recovery-event-choice",
    "probabilities": { "VERIFICATION_INCONCLUSIVE": 0.62, "VERIFICATION_FAILED": 0.28 }
  },
  "guard_decision": null,          // no guard on this transition
  "selected_transition": "verifying -> unknown",
  "state_after": "unknown"
}
```

An auditor can always reconstruct: *"the classifier judged X at confidence 0.62,
and the deterministic guard authorized Y."* The probabilistic signal and the
provable authorization never blur into each other.

## The point

The word "decision" hides two jobs with opposite requirements:

- **Detection / triage** — fast, cheap, fuzzy, frequent. Being wrong just wakes the
  machine (or a human) unnecessarily. A probabilistic classifier is ideal here.
- **Authorization** — slow, deliberate, exact, rare. Being wrong means a duplicate
  payment or an unsafe retry. Must stay deterministic and auditable.

Using one mechanism for both is the trap. Drawing the line exactly where the cost
of being wrong jumps by orders of magnitude is the design — and it is why a
System One classifier and a deterministic recovery machine compose without either
giving up what makes it valuable.
