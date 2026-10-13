# Release Reader Gate V0.2

The independent `verify_release(destination)` reader rejects missing
completion markers, unexpected files, SHA-256 mismatches, false approval
claims, incorrect entity count, wrong layer, and invalid DXF syntax.

It is a verification candidate, not a cryptographic authenticity
signature: a malicious actor able to rewrite all files and checksums can
forge a consistent release. The input SHA-256 is recorded by the writer
but cannot be independently checked without the original input.

TOCTOU warning: files can change after verification; the reader does not
lock or snapshot the directory. Symlink entries are rejected.

Promotion requires CI, fault-injection tests, external signer or immutable
storage for provenance, and explicit human review.
