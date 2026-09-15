# Schemas

- `recovery-machine.schema.json` is the current draft 0.2 schema for normative
  `RECOVERY.yaml` statecharts.
- `recovery-plan.schema.json` is retained for draft 0.1 experiments that stored
  normative YAML frontmatter in `RECOVERY.md`.

Implementations must select a schema using `spec_version`; they must not silently
reinterpret one draft as another.
