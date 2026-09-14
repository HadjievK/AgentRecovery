# Agent Recovery Conformance

Conformance is layered so teams can adopt the format incrementally.

## Level 1 - Recovery Plan

A conformant plan:

1. Uses a `RECOVERY.md` file with YAML frontmatter.
2. Validates against `schema/recovery-plan.schema.json`.
3. References capabilities by identifier rather than embedding commands or credentials.
4. Defines verification, retry, containment, escalation, audit, and resumption behavior.
5. Never permits retry directly from unknown state for a side-effecting operation.

## Level 2 - Recoverable Tool

A conformant tool integration additionally:

1. Accepts or returns an operation identifier and correlation identifier.
2. Provides an idempotency strategy for side-effecting operations.
3. Reports whether a side effect was possible and whether it was confirmed.
4. Provides an authoritative verification mechanism.
5. Declares whether compensation is supported.

## Level 3 - Recovery Controller

A conformant controller additionally:

1. Validates and pins the selected plan version.
2. Uses durable Action Ledger state rather than conversational memory.
3. Resolves capabilities through an administrator-controlled registry.
4. Enforces recovery transitions deterministically.
5. Records evidence and outcomes for every transition.
6. Applies enterprise policy even when it is stricter than the plan.

## Level 4 - Enterprise Recovery

An enterprise-conformant deployment additionally:

1. Can separately stop execution and revoke authority.
2. Can disable or isolate an affected capability or destination.
3. Supports risk-driven human escalation and accountable approval.
4. Enforces a resume gate after material incidents.
5. Correlates recovery evidence with existing security and business telemetry.
6. Exercises recovery through failure-injection tests and response drills.

## Level 5 - Multi-Agent Recovery

A multi-agent-conformant deployment additionally:

1. Preserves origin and cascade lineage across agents and protocols.
2. Identifies and stops descendant tasks and queued work.
3. Revokes delegated credentials throughout the affected chain.
4. Reconstructs completed effects for every participating agent.
5. Prevents a child or peer agent from silently resuming a contained incident.

## Conformance testing

A future reference suite should include at least:

- timeout before a side effect;
- timeout after a side effect;
- duplicate-operation detection;
- verification unavailable;
- partial multi-step completion;
- failed compensation;
- authorization conflict;
- safety containment;
- descendant-task cancellation; and
- resume-gate rejection.
