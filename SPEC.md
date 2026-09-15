# Agent Recovery State Machine Specification

## Status

Draft 0.2 - Request for Comments

## 1. Scope

This specification defines a portable, deterministic statechart for recovering
side-effecting AI-agent operations. Its required artifact is `RECOVERY.yaml`.
An optional `RECOVERY.md` provides human guidance but does not change machine
semantics.

The statechart controls verification, safe retry, compensation, containment,
escalation, and resumption. It is interpreted by a trusted recovery controller,
not by the affected agent.

## 2. Non-goals

Agent Recovery does not:

- control normal agent reasoning or planning;
- classify every root cause of failure;
- replace workflow engines or incident-response systems;
- grant credentials or bypass resource authorization;
- execute arbitrary scripts or model-generated conditions;
- guarantee that every external effect is reversible; or
- permit an affected agent to approve its own material resumption.

## 3. Terminology

**Recovery machine**: A versioned statechart describing recovery states, accepted
events, guarded transitions, registered actions, and final states.

**Recovery controller**: A trusted component that validates and pins machines,
loads durable operation state, evaluates registered guards, invokes approved
capabilities, enforces policy, and records transitions.

**Action Ledger**: A durable record of attempted operations, identifiers,
side-effect state, downstream references, attempts, evidence, and recovery
outcomes.

**Event**: An observable fact offered to the machine, such as
`VERIFICATION_FOUND`, `COMPENSATION_FAILED`, or `HUMAN_APPROVED`.

**Guard**: A named, side-effect-free predicate resolved by the controller and
evaluated against trusted ledger evidence and policy.

**Action**: An administrator-approved capability referenced by opaque identifier,
such as `agent.stop-task` or `procurement.cancel-request`.

**Unknown state**: A state in which the controller cannot determine whether an
external side effect occurred.

## 4. Package

```text
<machine-name>/
├── RECOVERY.yaml     # Required: normative statechart
├── RECOVERY.md       # Optional: informative operator guidance
├── tests/            # Optional: conformance and failure-injection cases
├── references/       # Optional: runbooks and evidence-source documentation
└── handlers/         # Optional: separately trusted implementations
```

The directory name should equal the machine `name`. Optional content must not
override or weaken the normative statechart.

## 5. Required fields

`RECOVERY.yaml` must validate against
`schema/recovery-machine.schema.json`. Required top-level fields are:

- `name`
- `description`
- `version`
- `spec_version`
- `applies_to`
- `initial`
- `states`
- `audit`

`spec_version` is `agent-recovery/0.2` for this draft.

## 6. Machine semantics

### 6.1 States

`initial` names the first state. Each state may declare:

- `entry`: actions invoked after the state is durably entered;
- `on`: events accepted in the state and their transitions; and
- `type: final`: a terminal state that accepts no further events.

The initial draft uses atomic states. Parallel and compound states are reserved
for a future compatible profile after execution semantics are tested.

### 6.2 Events

Events are opaque, uppercase identifiers. An event must carry the machine name
and version, operation ID, correlation ID, event ID, event time, evidence
reference, and producer identity in the runtime envelope.

The envelope is stored in the Action Ledger. It is not embedded in the machine.
Duplicate event IDs must be handled idempotently.

### 6.3 Guards

A transition may reference one registered guard. Guards must be deterministic,
side-effect-free predicates over trusted evidence and policy. A machine must not
contain executable expressions such as `outcome == found`.

Unknown, unavailable, or failed guards evaluate to false and generate an auditable
controller error. They must never broaden authority or make a retry safe.

### 6.4 Actions

Actions are opaque capability identifiers with optional static parameters. A
machine must not contain shell commands, scripts, credentials, tokens, prompts,
or untrusted destination values.

Loading a machine does not authorize its actions. Every invocation remains
subject to identity, policy, resource, destination, and approval checks.

Action completion or failure returns as a new event. An action must not silently
advance machine state.

### 6.5 Transition selection

An event may map to one transition or an ordered list of guarded transitions. The
controller selects the first transition whose registered guard evaluates true.
An unguarded transition is the default and must appear last.

If no transition is selected, the state does not change and the rejection is
audited. Controllers may escalate the rejection under stricter enterprise policy.

The controller must durably record the selected transition before invoking its
actions.

## 7. Core safety invariants

Every conformant controller must enforce these invariants independently of the
machine:

1. A possible side effect in unknown state is never retried directly.
2. Retry requires authoritative evidence that the effect was not applied, plus
   idempotency and attempt-limit policy.
3. Stopping execution and revoking authority are separate actions.
4. Compensation is a new business operation with its own failure semantics.
5. Unknown or conflicting evidence fails closed and escalates.
6. Material resumption requires verified state and accountable external approval.
7. An affected agent cannot modify its machine, ledger evidence, policy, or trust
   status during recovery.

## 8. Processing model

A controller performs these steps:

1. Validate and pin the selected machine and trusted provenance.
2. Match the affected operation to `applies_to`.
3. Load the current state and Action Ledger using operation and correlation IDs.
4. Validate and deduplicate the incoming event.
5. Find transitions accepted for the current state.
6. Evaluate registered guards against authoritative evidence and policy.
7. Apply a permitted state transition atomically and record its decision.
8. Invoke registered actions using task-scoped authority.
9. Store action results as new evidence events.
10. Continue until a final, contained, or escalated state is reached.

The model may recommend or explain a transition. It must not be the sole
enforcement point for a consequential recovery action.

## 9. Human intervention and resumption

Human decisions enter the machine as authenticated events. The reviewer should
receive the initiating request, identities, operation and correlation IDs,
triggering event, current state, ledger history, downstream references,
verification evidence, proposed action, and consequences of approval or rejection.

Resumption must be represented explicitly, normally through a `resume-pending`
state followed by an approval-and-evidence guarded transition. Recovery is not
complete merely because execution stopped.

## 10. Audit requirements

A controller must durably record:

- machine name, version, digest, and provenance;
- initiating principal, agent, runtime, and task;
- operation, correlation, and event identifiers;
- states before and after each event;
- evidence references and guard decisions;
- selected or rejected transitions;
- invoked capabilities and their effects;
- human approvals or rejections; and
- final recovery and resumption status.

Sensitive prompt and context content should be referenced or minimized rather than
copied indiscriminately.

## 11. Security considerations

Recovery machines are security-sensitive supply-chain artifacts. Controllers
should verify provenance, pin reviewed versions, enforce schema validation,
restrict guard and action resolution, and prevent machines from changing audit
evidence, policy, or their own trust status.

The format uses a restricted statechart profile inspired by W3C SCXML concepts.
It does not accept SCXML script, expression, or arbitrary executable-content
features.

## 12. Compatibility

Draft 0.1 used YAML frontmatter inside `RECOVERY.md`. Draft 0.2 moves the normative
contract to `RECOVERY.yaml`; the 0.1 schema remains available for experiments but
is not the current format. Controllers must select behavior using `spec_version`
and must not silently reinterpret a 0.1 plan as a 0.2 machine.

## 13. Future profiles

Future drafts may add compound and parallel states, a standardized event envelope,
signed distribution, multi-agent lineage, protocol bindings, and mappings to
existing state-machine or workflow engines.
