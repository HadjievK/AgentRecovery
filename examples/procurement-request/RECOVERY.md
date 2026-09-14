---
name: procurement-request-recovery
description: >-
  Recover creation of a procurement request when the result is uncertain,
  duplicated, partially completed, or unauthorized.
version: "0.1.0"
spec_version: "agent-recovery/0.1"

applies_to:
  tools:
    - procurement.create-request
  effect_class: reversible-write

triggers:
  - event: timeout-after-side-effect
  - event: unknown-state
  - event: duplicate-detected
  - event: partial-completion
  - event: authorization-failure

operation:
  required_fields:
    - operation_id
    - correlation_id
    - idempotency_key
    - agent_id
    - task_id
  action_ledger: required

verify:
  capability: procurement.find-by-idempotency-key
  outcomes:
    found: verified-applied
    not-found: verified-not-applied
    inconclusive: unknown

retry:
  allowed_only_when:
    - verified-not-applied
  reuse_idempotency_key: true
  max_attempts: 1

compensate:
  capability: procurement.cancel-request
  allowed_only_when:
    - verified_applied
    - cancellation_permitted
  approval: procurement-owner

contain:
  - capability: agent.stop-task
    scope: current-task
  - capability: identity.revoke-task-token
    scope: current-task
  - capability: workflow.cancel-descendants
    scope: task-cascade

escalate:
  when:
    - state_cannot_be_verified
    - compensation_failed
    - irreversible_effect_detected
    - authorization_conflict
  role: procurement-incident-owner

resume:
  requires:
    - business_owner_approval
    - recovery_state_verified
    - credentials_reissued
    - failed_control_remediated

audit:
  record:
    - failure_signal
    - operation_state
    - verification_evidence
    - recovery_decision
    - completed_effects
    - approver
---

# Procurement Request Recovery

## Objective

Return the procurement workflow to a known safe state without creating duplicate requests or hiding partially completed work.

## Operator guidance

A timeout after submission represents an unknown outcome, not a confirmed failure. Verify the procurement system before permitting a retry.

If the original request exists, return its business reference instead of creating another request. If verification proves that no request exists, the controller may retry once using the same idempotency key. If verification remains inconclusive, escalate to the procurement incident owner.

## Successful recovery

Recovery is complete when the intended request exists exactly once, or when all unintended requests have been cancelled and reconciled.

## Manual escalation package

Provide the reviewer with:

- the original user request;
- agent and task identity;
- the triggering failure signal and available evidence;
- the Action Ledger entry;
- downstream procurement identifiers;
- verification results;
- the proposed recovery action; and
- the consequences of approving or rejecting that action.

## Safe resumption

Do not restore the agent's procurement authority until the resulting state has been verified, affected credentials have been reissued, the failed control has been remediated, and the accountable business owner has approved resumption.
