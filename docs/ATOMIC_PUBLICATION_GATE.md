# V0.2 exclusive-reservation publication gate

The optional `publish_solid_plan` wrapper first validates DXF in a
temporary directory. It then exclusively reserves the final directory
using `mkdir`, copies verified artifacts and writes `_OAIS_COMPLETE`
last. Consumers MUST check this marker AND verify the report and DXF
SHA-256 before accepting an output as complete.

- Destination must not exist; an existing release is never overwritten.
- Concurrent attempts cannot both reserve the same destination on a
  filesystem with atomic mkdir semantics.
- A directory may be visible **before** the completion marker exists.
  Therefore this is **not atomic whole-directory visibility**.
- A failure after reservation attempts best-effort cleanup.
- Each file is flushed and fsynced; directory fsync and full crash
  durability are NOT implemented.
- On abrupt process termination an incomplete reserved directory may
  remain and require manual recovery.
- This module is optional and is not wired to the default CLI.
- No engineering design approval is conferred.

Required future checks: concurrent-process tests, simulated write failure,
marker-and-hash verification reader, recovery from stale reservations.
