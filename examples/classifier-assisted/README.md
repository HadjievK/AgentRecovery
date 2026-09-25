# Classifier-assisted recovery — sample artifacts

Inspectable JSON for the boundary in [SPEC.md §11](../../SPEC.md#11-classifier-assisted-decisions):
a fast "System One" classifier decides **when** recovery is needed and how urgent;
the deterministic [procurement-request machine](../procurement-request/RECOVERY.yaml)
decides **what** is safe to do. The narrated version is
[../classifier-assisted-walkthrough.md](../classifier-assisted-walkthrough.md).

These files are **illustrative**, not a live integration — there is no API call and
no code to run. They show the *shape* of the data as it crosses the boundary.

## The three artifacts

| File | Role |
|---|---|
| [`jev-classification.json`](jev-classification.json) | A Jev-style classifier response: choice + score questions with calibrated probabilities. **Untrusted input** to the controller. |
| [`candidate-event.json`](candidate-event.json) | What the harness emits *after applying its own policy* to those probabilities. The classifier proposed; harness policy disposed. |
| [`action-ledger.json`](action-ledger.json) | The durable record of the whole recovery, one entry per event. |

## What to notice

1. **The classifier does not pick the event.** Its top answer is `VERIFICATION_INCONCLUSIVE` at 0.62 — below the harness's `confident_routing_threshold`. So the harness emits the most conservative event the state accepts (`START_VERIFICATION`), not the highest-probability one. Policy lives in the harness's code, not in the model's output.

2. **The controller still validates.** The candidate event is checked against the current state like any other event before it advances the machine.

3. **Probability is evidence, never authority.** In every ledger entry, the classifier output sits in `evidence_reference`; it is *always* separate from `guard_decision`. The transitions that authorize real actions (`escalated -> resume-pending`, `resume-pending -> closed`) are gated by deterministic guards and a named human `approver` — never by a probability.

4. **You can reconstruct the decision.** From `action-ledger.json` an auditor can state: "the model judged `VERIFICATION_INCONCLUSIVE` at 0.62, the operation moved to `unknown`, was contained and escalated, and only resumed after guard `resume.evidence-and-owner-approval-verified` passed and owner `a.novak` approved." The probabilistic signal and the provable authorization never blur.

## Not shown on purpose

- **Real API payloads / keys** — field names follow TypeSafe AI's choice/score/noul model, but nothing here calls a service.
- **Guards driven by probability** — forbidden by §11. A guard is a deterministic, side-effect-free predicate over trusted evidence.
