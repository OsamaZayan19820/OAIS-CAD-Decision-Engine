# Cross-process release competition — V0.2

Two independently spawned Python processes synchronize at a start gate
and attempt to publish to the same local directory. Exactly one must
publish, one must reject; the resulting release must pass the independent
reader. The test uses the spawn multiprocessing context to avoid reliance
on inherited fork state.

This is a local-filesystem integration test, not proof of distributed
locking, NFS/cloud filesystem guarantees, crash durability, or stale
reservation recovery. Those remain explicitly out of scope.

Promotion is gated by CI for the exact commit and human approval.
