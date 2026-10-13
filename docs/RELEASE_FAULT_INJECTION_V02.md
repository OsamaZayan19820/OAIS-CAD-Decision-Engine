# V0.2 Release Fault-Injection Gate

Tests cover:
1. Two simultaneous Python threads competing to publish to the same
   destination: exactly one succeeds, the other is rejected.
2. An injected failure while creating the completion marker: best-effort
   rollback leaves no published destination.
3. An abandoned incomplete reservation: independent reader rejects it
   and publisher refuses to overwrite it.

These tests do not prove cross-process or distributed filesystem behavior,
power-loss durability, tamper-proof provenance, or immutable releases.
A follow-up should add process-level concurrency and a recovery protocol.

No automatic merge or engineering approval.
