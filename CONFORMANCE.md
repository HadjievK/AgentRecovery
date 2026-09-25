# Agent Recovery Conformance

Conformance is layered so teams can adopt deterministic recovery incrementally.

## Level 1 - Recovery Machine

A conformant machine:

1. Uses a `RECOVERY.yaml` file that validates against the normative schema.
2. Declares an initial state, accepted events, transitions, and a final state.
3. References guards and actions by registered identifier.
4. Contains no scripts, executable expressions, prompts, or credentials.
5. Never permits retry directly from unknown state after a possible side effect.

## Level 2 - Recoverable Tool

A conformant tool integration additionally:

1. accepts or returns operation, correlation, and idempotency identifiers;
2. reports whether a side effect was possible and confirmed;
3. provides an authoritative verification mechanism;
4. emits deduplicated recovery events with evidence references; and
5. declares whether compensation is supported.

A tool MAY use a fast classification model to propose a candidate recovery event
or an advisory urgency signal, provided the classification is recorded as evidence
and the controller still validates the event under Level 3. A classifier is never
a guard or a transition authority (see specification §11).

## Level 3 - Recovery Controller

A conformant controller additionally:

1. validates and pins the machine version and provenance;
2. stores current state and evidence in a durable Action Ledger;
3. resolves guards and actions through administrator-controlled registries;
4. selects transitions deterministically and fails closed;
5. records a transition before invoking its actions;
6. handles action results as new events; and
7. enforces enterprise policy when it is stricter than the machine.

## Level 4 - Enterprise Recovery

An enterprise-conformant deployment additionally:

1. can separately stop execution and revoke authority;
2. can isolate an affected capability, destination, or delegated workflow;
3. supports risk-driven human escalation and authenticated decisions;
4. enforces a resume gate after material incidents;
5. correlates recovery events with security and business telemetry; and
6. exercises recovery through failure injection and response drills.

## Level 5 - Multi-Agent Recovery

A multi-agent-conformant deployment additionally:

1. preserves origin and cascade lineage across agents and protocols;
2. identifies and stops descendant tasks and queued work;
3. revokes delegated credentials throughout the affected chain;
4. reconstructs completed effects for every participating agent; and
5. prevents a child or peer agent from silently resuming a contained incident.

## Required conformance scenarios

- timeout before a side effect;
- timeout after a side effect;
- duplicate event delivery;
- duplicate business operation detection;
- verification unavailable or conflicting;
- partial multi-step completion;
- guard resolution failure;
- rejected invalid transition;
- failed compensation;
- containment action failure;
- authorization conflict;
- descendant-task cancellation; and
- resume-gate rejection.
