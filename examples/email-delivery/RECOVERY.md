# Email Delivery Recovery

The normative state machine is [RECOVERY.yaml](RECOVERY.yaml).

A lost provider response is not permission to send the message again. Query the
delivery provider using the original idempotency key. Retry only when the provider
authoritatively proves that it did not accept the message.

Email cannot usually be unsent, so this machine intentionally has no compensation
action. If delivery remains unknown or a duplicate was sent, contain the sender
and escalate for a business decision. Restore sending authority only after the
delivery state and accountable approval are verified.
