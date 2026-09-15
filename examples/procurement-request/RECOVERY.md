# Procurement Request Recovery

The normative state machine is [RECOVERY.yaml](RECOVERY.yaml).

## Objective

Return the procurement workflow to a known safe state without creating duplicate
requests or hiding partially completed work.

## Operator guidance

A timeout after submission represents an unknown outcome, not a confirmed
failure. Verify the procurement system before permitting a retry.

If the request exists, return its business reference instead of creating another
request. If authoritative verification proves that no request exists, the
controller may retry once using the original idempotency key. If verification
remains inconclusive, contain the task and escalate.

Recovery is complete when the intended request exists exactly once, or when all
unintended requests have been cancelled and reconciled. Do not restore authority
until state, credentials, remediation, and owner approval have been verified.
