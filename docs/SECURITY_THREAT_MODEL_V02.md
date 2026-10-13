# OAIS CAD V0.2 — Defensive threat map and information minimization

## Scope
Protect CAD intent, release DXF, report, marker and publication path.
Threat model assumes untrusted inputs, accidental corruption, competing
local writers and malicious tampering of artifacts. No internet service
or user authentication is implemented in V0.2.

## Attack likelihood and consequence
These are qualitative hypotheses, NOT measured incident probabilities.

| Threat | Exposure | Impact | Defense | Residual risk |
| --- | --- | --- | --- | --- |
| Modify DXF only | Local release files | High | SHA-256 marker binding | Attacker able to rewrite marker too |
| Modify report only | Local release files | High | SHA-256 marker binding | No authenticated signing key |
| Rewrite DXF, report and marker | Writable release directory | Critical | File permissions, trusted storage and external signed attestations required | NOT MITIGATED by hashes |
| Symlink replacement | Release paths | High | Reader rejects symlink entries and symlink root | Ancestor links and TOCTOU remain |
| Competing publishers | Shared output name | Medium | Exclusive mkdir; marker written last | Crash leftovers and distributed FS |
| Partial write / power loss | Local filesystem | High | fsync files; reader requires complete marker | Directory fsync/crash durability not established |
| Excessive disclosure | Public artifacts and logs | Medium | Keep detailed CAD reports private, publish only vetted summary | Operator-dependent |
| Malicious geometry | Untrusted JSON | High | Strict schema, bounds and fail-closed review | Resource-exhaustion budgets not established |
| Supply chain compromise | CI dependencies/actions | High | Pin reviewed actions by immutable SHA; lock dependencies with hashes | Not yet implemented |

## Defensive concealment policy
- Never embed tokens, access keys, private CAD layouts or customer identities
  in repository, sample inputs, public reports or CI logs.
- Keep the full threat register and operational topology in restricted
  access storage when real deployments are introduced.
- Public-facing diagnostics should use stable codes such as
  INVALID_RELEASE and not echo filesystem paths or sensitive input values.
- Do not use secret paths, code obfuscation or random file names as the
  primary security control.
- Security failures remain observable to authorized reviewers; do not
  suppress evidence or falsify success.

## Security gates
1. Treat untrusted CAD input and third-party DXF as hostile.
2. Reject symlinks and unexpected release entries.
3. Reject any DXF or report mismatch before trusting report claims.
4. Publish to a new directory; never overwrite a prior release.
5. Require independent integrity verification before consumption.
6. Restrict filesystem write permissions and keep backups.
7. Require human review for any geometry conflict.
8. Do not promote to production without external CAD validation,
   resource limits, signed provenance, dependency review and
   adversarial filesystem tests.

## Decision
DEFENSE_IN_DEPTH_CANDIDATE. Integrity checks detect accidental or
unsophisticated modification, but DO NOT provide authenticated
provenance. No claim of resistance to a privileged local adversary.
