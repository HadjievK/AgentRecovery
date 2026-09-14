# Agent Recovery

**A portable, file-based recovery-plan format for AI agents.**

Agent Recovery proposes `RECOVERY.md`: a human-readable and machine-validated plan that tells a trusted recovery controller how to verify, contain, compensate for, and safely resume agent operations.

The project is inspired by the packaging model of the [Agent Skills open specification](https://github.com/agentskills/agentskills), while remaining focused on recovery as a separate operational concern.

Status: **Draft 0.1 - Request for Comments**

> **The core rule:** if an agent may have changed external state, verify what
> happened before retrying.

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
4. **Recovery starts from observable operation state.** A plan does not require a particular failure taxonomy or agent framework.
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

## Recovery flow

```mermaid
flowchart LR
    A[Operation attempted] --> B{Effect possible?}
    B -- No --> C[Retry under policy]
    B -- Yes --> D[Verify authoritative state]
    D --> E{Applied?}
    E -- No --> F[Retry with same idempotency key]
    E -- Yes --> G[Return result or compensate]
    E -- Unknown --> H[Contain and escalate]
    F --> I[Audit and resume gate]
    G --> I
    H --> I
```

## Try it

Validate every included recovery plan:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

Examples currently cover:

- [procurement request creation](examples/procurement-request/RECOVERY.md);
- [external email delivery](examples/email-delivery/RECOVERY.md); and
- [production deployment](examples/production-deployment/RECOVERY.md).

## Join the RFC

This is an early proposal, not an established standard. We are looking for agent
builders, platform engineers, SREs, security teams, and business-system owners to:

1. test `RECOVERY.md` against a real side-effecting workflow;
2. challenge the schema and recovery states;
3. contribute failure-injection cases or another domain example; and
4. discuss interoperability requirements in [GitHub Discussions](https://github.com/HadjievK/AgentRecovery/discussions).

See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md) to get involved.

## Security boundary

`RECOVERY.md` is input to a trusted controller, not an authorization grant. A conformant controller must validate the plan, resolve capability identifiers through an administrator-controlled registry, enforce normal identity and policy checks, and reject any plan that attempts to broaden its own authority.

## Open questions

- Should the standard be named Agent Recovery Plan or Agent Recovery Protocol?
- Should recovery-event records be standardized in the core or in a separate profile?
- How should plans be signed, distributed, and pinned to tool versions?
- How should recovery lineage cross agent, process, and service boundaries?
- Which organization should steward capability and effect-class registries?

## License

Licensed under the [Apache License 2.0](LICENSE).
