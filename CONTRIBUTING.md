# Contributing to Agent Recovery

Agent Recovery is a draft Request for Comments. Contributions should help test
whether `RECOVERY.yaml` can express safe, portable recovery for real agent
operations.

## Useful contributions

- A recovery state machine for a real side-effecting workflow
- A failure case the current model cannot represent
- A schema or specification clarification
- A failure-injection or conformance test
- Feedback from implementing a recovery controller or recoverable tool

Please avoid coupling the core format to one agent framework, model provider,
cloud, or workflow engine.

## Propose a change

1. Open a Discussion or issue describing the operation, possible side effect,
   authoritative verification source, safe retry rule, containment, and resume
   gate.
2. For a new example, copy an existing example into
   `examples/<domain>/RECOVERY.yaml` and replace every domain-specific capability.
   Add `RECOVERY.md` only when operator guidance is useful.
3. Run `python scripts/validate.py`.
4. Submit a focused pull request and explain which uncertainty or recovery path
   it exercises.

Specification changes should include a motivating scenario and note compatibility
impact. Until version 1.0, the draft may change based on implementation feedback.

By contributing, you agree that your contribution is licensed under Apache-2.0.
