# V0.2 release reader resource limits

The independent release verifier rejects files larger than:
- DXF: 32 MiB
- JSON report: 2 MiB
- Completion marker: 4 KiB

These checks occur before file contents are read or passed to the DXF
parser. The budgets protect against straightforward oversized-file
attacks, but do not bound CPU consumption inside a permitted-size DXF,
TOCTOU races, symbolic links in ancestor directories, or hostile
filesystem behavior. A future hardening stage must use descriptor-based
no-follow opening, bounded streaming, resource/time limits for parsing,
and a sandboxed worker for untrusted DXF.

Do not disclose sensitive geometry, paths or credentials in public CI
artifacts. Keep failures visible to authorized reviewers. No deployment
approval is implied.
