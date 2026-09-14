---
name: email-delivery-recovery
description: >-
  Recover an external email delivery when the provider response is lost,
  delivery state is uncertain, or a duplicate message may have been sent.
version: "0.1.0"
spec_version: "agent-recovery/0.1"

applies_to:
  tools:
    - messaging.send-email
  effect_class: external-communication

triggers:
  - event: timeout-after-side-effect
  - event: unknown-state
  - event: duplicate-detected

operation:
  required_fields:
    - operation_id
    - correlation_id
    - idempotency_key
    - agent_id
    - task_id
  action_ledger: required

verify:
  capability: messaging.find-delivery-by-idempotency-key
  outcomes:
    delivered: verified-applied
    not-accepted: verified-not-applied
    inconclusive: unknown

retry:
  allowed_only_when:
    - verified-not-applied
  reuse_idempotency_key: true
  max_attempts: 1

contain:
  - capability: agent.stop-task
    scope: current-task
  - capability: messaging.suspend-sender
    scope: current-agent

escalate:
  when:
    - delivery_state_cannot_be_verified
    - duplicate_external_message_detected
    - recipient_or_content_mismatch
  role: communications-incident-owner

resume:
  requires:
    - delivery_state_verified
    - sender_authority_reviewed
    - incident_owner_approval

audit:
  record:
    - operation_state
    - provider_message_id
    - verification_evidence
    - recovery_decision
    - approver
---

# Email Delivery Recovery

A lost response is not permission to send the message again. Query the delivery
provider using the original idempotency key. Retry only when the provider proves
that it did not accept the message.

Email cannot usually be unsent, so the plan intentionally has no compensation
capability. If delivery remains unknown or a duplicate was sent, contain the
sender and escalate for a business decision.
