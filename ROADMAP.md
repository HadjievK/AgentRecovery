# Roadmap

Agent Recovery is being developed in public as an implementation-led RFC.

## 0.1 - Validate the recovery contract

- Collect examples from at least three business domains
- Validate plans automatically in continuous integration
- Test unknown-state, duplicate, partial-completion, and failed-compensation paths
- Resolve naming and core-schema feedback

## 0.2 - Prove interoperability

- Build a minimal reference recovery controller
- Define a portable Action Ledger event shape
- Add bindings for common agent tool and workflow protocols
- Demonstrate the same plan across two independent agent runtimes

## 0.3 - Harden the trust model

- Define plan signing, provenance, and version-pinning guidance
- Add capability-registry and policy examples
- Add multi-agent lineage and descendant containment tests
- Publish a security and threat-model review

## 1.0 - Stable recovery-plan specification

- Publish compatibility and extension rules
- Ship a complete conformance suite
- Document governance and registry stewardship
- Graduate after independent production-oriented implementations

The roadmap is directional. Evidence from real recovery scenarios takes priority
over adding fields to the format.
