# Agent Recovery Plan Specification

## Status

Draft 0.1 - Request for Comments

## 1. Scope

This specification defines a portable package for describing recovery behavior for side-effecting AI-agent operations. Its required artifact is a `RECOVERY.md` file containing YAML frontmatter followed by Markdown operator guidance.

The YAML frontmatter is normative and must validate against `schema/recovery-plan.schema.json`. The Markdown body is informative unless another specification explicitly promotes a section to normative status.

## 2. Non-goals

Agent Recovery does not:

- classify the root cause of agent failures;
- replace AFF, A2A, MCP, workflow engines, or incident-response systems;
- grant credentials or bypass resource-side authorization;
- make arbitrary scripts trustworthy;
- guarantee that every external effect is reversible; or
- permit an affected agent to approve its own recovery or resumption.

## 3. Terminology

**Recovery plan**: A versioned declaration describing verification, retry, compensation, containment, escalation, audit, and resumption behavior.

**Recovery controller**: A trusted component that validates plans, reads durable operation state, applies policy, invokes approved capabilities, and records transitions.

**Action Ledger**: A durable record of attempted business operations, idempotency keys, side-effect state, downstream references, retry attempts, and recovery outcomes.

**Capability**: An administrator-approved operation that a recovery controller may request, such as `agent.stop-task` or `procurement.cancel-request`.

**Compensation**: A business action that counteracts a completed effect. Compensation is not necessarily a perfect rollback.

**Unknown state**: A state in which the controller cannot determine whether an external side effect occurred.

**Resume gate**: The policy and approval boundary that must be satisfied before affected work can continue.

## 4. Required package

Every package must contain:

```text
<plan-name>/
└── RECOVERY.md
```

The directory name should equal the frontmatter `name`. Optional files must not override or weaken the normative plan.

## 5. `RECOVERY.md` format

The document must begin with YAML frontmatter delimited by `---`. Required top-level fields are:

- `name`
- `description`
- `version`
- `spec_version`
- `applies_to`
- `operation`
- `verify`
- `retry`
- `contain`
- `escalate`
- `resume`
- `audit`

`compensate` and `aff_triggers` are optional.

### 5.1 Capability identifiers

Capability identifiers are opaque names resolved by a trusted registry. A plan must not embed operating-system commands, credentials, access tokens, or executable code in capability fields.

Loading a plan does not authorize its capabilities. Every invocation remains subject to identity, policy, resource, destination, and approval checks outside the plan.

### 5.2 Effect classes

The core effect classes are:

- `read-only`
- `reversible-write`
- `irreversible-write`
- `external-communication`
- `financial-action`
- `authority-change`
- `multi-step-workflow`

Controllers may apply stricter policy than the plan requests. Unknown effect classes must fail closed unless a registered extension defines their semantics.

## 6. Processing model

A conformant recovery controller performs these steps:

1. Validate the plan and establish its trusted provenance and version.
2. Match the failed operation to `applies_to` and any declared failure triggers.
3. Load the Action Ledger using the operation and correlation identifiers.
4. Determine whether an external side effect was impossible, possible, confirmed, or unknown.
5. If a side effect was possible but unconfirmed, verify authoritative downstream state before retrying.
6. Select only a transition permitted by both the plan and current enterprise policy.
7. Invoke capabilities through a trusted registry using task-scoped credentials.
8. Record verification evidence, decisions, approvals, capability results, and material effects.
9. Require the resume gate before restoring affected authority or continuing work.

The model may propose or explain a transition. It must not be the sole enforcement point for a consequential recovery action.

## 7. Recovery states

The core states are:

```text
started
effect-possible
verified-not-applied
verified-applied
unknown
retry-safe
compensating
contained
recovered
escalated
resume-pending
closed
```

A typical uncertain-write flow is:

```text
started
  -> effect-possible
  -> unknown
  -> verified-not-applied -> retry-safe
  -> verified-applied     -> recovered or compensating
  -> unknown              -> escalated
```

Unknown state must never transition directly to a repeated side-effecting operation.

## 8. AFF binding

An AFF record may select or influence a recovery plan through `aff_triggers`. The AFF disposition remains a hint, not a recovery authorization.

Examples:

| AFF signal | Recovery refinement |
| --- | --- |
| `AF-9xx` timeout | Verify downstream state before retry when a side effect was possible. |
| `AF-7xx` tool failure | Consult tool semantics and the Action Ledger. |
| `AF-8xx` safety failure | Stop the branch, contain authority, and inspect completed effects. |
| `AF-6xx` orchestration failure | Stop descendant tasks and cancel queued work. |
| `AF-4xx` context failure | Quarantine affected context or memory before reformulation. |
| Observer-diagnosed wrongness | Identify and recover downstream effects produced before detection. |

AFF cascade references should be preserved in recovery evidence so one origin failure and its downstream effects can be investigated as one incident.

## 9. Containment and revocation

Stopping execution and revoking authority are separate operations. A plan for consequential work should normally include both, plus cancellation or isolation of delegated work where applicable.

Containment should use the narrowest safe scope: one task before one agent, one capability before one connector, and one destination before an organization-wide shutdown, unless evidence indicates broader compromise.

## 10. Human intervention

The controller must escalate when required by enterprise policy or the plan. Typical triggers include:

- external state cannot be verified;
- an irreversible effect may have occurred;
- compensation failed;
- data sources conflict;
- authorization or user intent is ambiguous;
- the recovery capability would increase authority; or
- the business impact exceeds the autonomous-recovery threshold.

The reviewer should receive the initiating request, agent and task identity, AFF record when present, attempted operation, tool result, ledger state, downstream references, verification evidence, recommended action, and consequences of approval or rejection.

## 11. Resumption

Recovery is not complete merely because execution stopped. The resume gate must define the evidence, remediation, credential state, testing, and accountable approval required to continue.

An affected runtime must not approve its own resumption after a material incident.

## 12. Audit requirements

A controller must durably record:

- plan name and version;
- initiating principal, agent, runtime, and task;
- operation and correlation identifiers;
- failure signal and supporting evidence;
- verification attempts and authoritative results;
- recovery transitions and policy decisions;
- capabilities invoked and their effects;
- human approvals or rejections; and
- final recovery and resumption status.

Sensitive prompt and context content should be minimized or referenced rather than copied indiscriminately.

## 13. Security considerations

Recovery plans are security-sensitive supply-chain artifacts. Controllers should pin reviewed versions, verify provenance, enforce schema validation, restrict capability resolution, and prevent plans from modifying audit evidence, policy, or their own trust status.

Recovery capabilities should be idempotent where possible. Compensation must itself have failure semantics because a failed recovery can increase the original impact.

## 14. Protocol bindings

The core format is protocol-neutral. Future bindings may define how plan references, operation identifiers, recovery states, and evidence references are carried through A2A task metadata, MCP structured content, workflow events, and tracing systems.
