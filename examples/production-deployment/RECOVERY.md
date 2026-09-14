---
name: production-deployment-recovery
description: >-
  Recover an agent-initiated production deployment that is partial, unhealthy,
  or has an uncertain completion state after the deployment API returns.
version: "0.1.0"
spec_version: "agent-recovery/0.1"

applies_to:
  tools:
    - delivery.deploy-production
  effect_class: multi-step-workflow

triggers:
  - event: timeout-after-side-effect
  - event: unknown-state
  - event: partial-completion
  - event: verification-failure

operation:
  required_fields:
    - operation_id
    - correlation_id
    - idempotency_key
    - agent_id
    - task_id
  action_ledger: required

verify:
  capability: delivery.get-deployment-state
  outcomes:
    healthy: verified-applied
    not-started: verified-not-applied
    unhealthy: verified-applied
    in-progress: unknown

retry:
  allowed_only_when:
    - verified-not-applied
  reuse_idempotency_key: true
  max_attempts: 1

compensate:
  capability: delivery.rollback-to-last-known-good
  allowed_only_when:
    - verified_applied
    - health_checks_failed
    - rollback_target_verified
  approval: production-incident-commander

contain:
  - capability: agent.stop-task
    scope: current-task
  - capability: identity.revoke-task-token
    scope: current-task
  - capability: delivery.freeze-environment
    scope: affected-environment

escalate:
  when:
    - deployment_state_cannot_be_verified
    - rollback_failed
    - data_migration_may_be_irreversible
    - service_health_below_threshold
  role: production-incident-commander

resume:
  requires:
    - environment_state_verified
    - service_health_verified
    - deployment_credentials_reissued
    - incident_commander_approval

audit:
  record:
    - operation_state
    - deployment_id
    - artifact_version
    - environment
    - health_evidence
    - recovery_decision
    - approver
---

# Production Deployment Recovery

Determine the deployment controller's authoritative state before issuing another
deployment. If the new version is unhealthy, roll back only to a verified target
and under the existing production approval policy.

Freezing the affected environment prevents competing deploys from obscuring the
state under investigation. Unfreeze it only through the resume gate.
