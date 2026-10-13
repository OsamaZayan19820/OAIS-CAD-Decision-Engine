# V0.2 directory publication gate

The optional `publish_solid_plan` wrapper stages a complete export
in a sibling temporary directory and publishes by one directory rename.

- Destination must not exist; existing releases are never overwritten.
- Failed validation leaves no destination or partial release.
- The DXF exporter still verifies geometry round-trip and records SHA-256.
- Staging is cleaned up on ordinary Python exceptions.

**Caveats:** Directory rename is atomic only under appropriate local
filesystem semantics; concurrent writers require an external lock or
exclusive destination reservation. Abrupt power loss requires durability
controls (fsync), not supplied here. This is NOT a distributed transaction.
Do not claim race-free concurrent publication or crash durability.

The wrapper is not integrated into the existing CLI and does not grant
architectural approval.
