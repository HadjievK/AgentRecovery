# Agent Recovery

**A portable, file-based recovery-plan format for AI agents.**

Agent Recovery proposes `RECOVERY.md`: a human-readable and machine-validated plan that tells a trusted recovery controller how to verify, contain, compensate for, and safely resume agent operations.

The project is inspired by the packaging model of the [Agent Skills open specification](https://github.com/agentskills/agentskills) and is designed to complement the [Agentic Failure Framework (AFF)](https://github.tools.sap/I535106/AI-Ideas):

```text
AFF          = What failed, where it failed, and the suggested disposition
RECOVERY.md  = How to verify the external state, contain effects, recover, and resume
```

Status: **Draft 0.1 - Request for Comments**

## Why this exists

An agent can receive a timeout after an external operation has already succeeded. Blindly retrying can then create duplicate payments, purchase requests, emails, tickets, deployments, or access grants. A kill switch can stop the next action, but it cannot determine what already happened or repair the resulting business state.

Agent Recovery makes that missing operational contract explicit. A recovery plan defines:

- which tools and effects it applies to;
- how downstream state is verified;
- when a retry is safe;
- which compensating action is available;
- how tasks, credentials, and downstream work are contained;
- when a human must intervene; and
- what evidence and approvals are required before resumption.

## Design principles

1. **Declarative, not executable by default.** Plans reference trusted capability identifiers; they do not embed arbitrary shell commands.
2. **Unknown is a real state.** A timeout is not proof that an operation failed.
3. **No blind retries after possible side effects.** Verify external state first.
4. **Failure classification and recovery remain separate.** AFF records can trigger a plan, but do not themselves perform remediation.
5. **Stopping and revoking are separate operations.** A stopped task may leave valid tokens or delegated work behind.
6. **Recovery includes safe resumption.** The agent does not authorize its own return to service after a material incident.
7. **Human authority is risk-driven.** Irreversible, ambiguous, or high-impact recovery decisions require an accountable person.
8. **Every transition is auditable.** Recovery must be reconstructable from durable evidence, not conversational memory.

## Package layout

```text
recovery-plan-name/
├── RECOVERY.md       # Required: YAML frontmatter plus operator guidance
├── tests/            # Optional: failure-injection and conformance cases
├── references/       # Optional: runbooks and system documentation
└── handlers/         # Optional: trusted, separately approved implementations
```

See the [draft specification](SPEC.md), [conformance levels](CONFORMANCE.md), [normative plan schema](schema/recovery-plan.schema.json), and [procurement example](examples/procurement-request/RECOVERY.md).

## Security boundary

`RECOVERY.md` is input to a trusted controller, not an authorization grant. A conformant controller must validate the plan, resolve capability identifiers through an administrator-controlled registry, enforce normal identity and policy checks, and reject any plan that attempts to broaden its own authority.

## Open questions

- Should the standard be named Agent Recovery, AFF Recovery Profile, or remain neutral with an optional AFF binding?
- Should recovery-event records be standardized in the core or in a separate profile?
- How should plans be signed, distributed, and pinned to tool versions?
- How should recovery lineage cross A2A and MCP process boundaries?
- Which organization should steward capability and effect-class registries?

## License

No license has been selected yet. Repository owners should choose an appropriate license before accepting external contributions.
