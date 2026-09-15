# Production Deployment Recovery

The normative state machine is [RECOVERY.yaml](RECOVERY.yaml).

Determine the deployment controller's authoritative state before issuing another
deployment. If the new version is unhealthy, roll back only to a verified target
and under the existing production approval policy.

Freezing the affected environment prevents competing deployments from obscuring
the state under investigation. A rollback is a compensating operation with its
own failure semantics. Unfreeze the environment and restore deployment authority
only through the resume gate.
