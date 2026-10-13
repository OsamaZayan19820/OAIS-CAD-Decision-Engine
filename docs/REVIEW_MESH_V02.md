# V0.2 review mesh — project-only pilot

Decision: approve next engineering validation stage, **not** production or regulatory approval.
Decision owner: human repository owner. Evidence: source at exact commit and GitHub CI.
Authority roles: owner approves/rejects; CI supplies test result, not approval.

## Selected analytic lenses and minimum review maps

| Lens | Purpose / Question | Required input | Allowed evidence | Forbidden inference | Maps | Quality test | Output | Stop condition |
|---|---|---|---|---|---|---|---|---|
| Geometry | Detect centerline clashes | wall endpoints, opening intervals | source, test results, exported coordinates | centerline pass means structural safety | Architecture, Failure Modes | CROSS/OVERLAP/TOUCH regression | classified findings | unresolved CROSS/OVERLAP |
| Security | Reject unsafe or unsupported inputs | JSON contract, parser | validator behavior, negative tests | CI pass proves safe arbitrary execution | Risk, Controls | unknown fields and nonfinite values rejected | attack surface assessment | unchecked executable input |
| QA | Preserve deterministic behavior | baseline tests and V0.2 tests | CI run tied to commit | old green run proves new code | QA, Regression | full test suite and DXF reparse | pass/fail per commit | failing CI |
| Evidence | Control claims and scope | source versions, report schema | GitHub commit and artifacts | passing tests imply building code approval | Evidence, Decision Authority | no unsupported certification claim | evidence map | material evidence void |

## CROSS-REVIEW / CONFLICT GATE / RED TEAM / SYNTHESIS

Cross-review: compare source behavior against declared supported geometry and test coverage.
Conflict gate: preserve source-vs-report disagreements; never average or vote them away.
Red team: target T-junctions, near-collinearity, endpoint contacts, thickness collisions and DXF manipulation.
Synthesis: only a centerline geometry pilot; thickness and physical clearance remain DATA VOID.

## Measurement spine

Evidence Integrity: commit-linked CI and generated input SHA (partial).
Claim Discipline: explicit centerline-only limitations (implemented).
Context Relevance: CAD V0.2 branch isolated (implemented).
Handoff Completeness: documented CLI, examples and draft PR (partial).
Decision Readiness: HOLD merge pending test run and human review.
Regression: automated test suite exists; results must be tied to latest commit.

## Return to Double Recall

Resolved frictions: basic intersection classification and fail-closed helper.
New frictions: tolerances are absolute and not formally calibrated.
Conflicts: none established; do not infer none exist outside tested cases.
DATA VOID: CAD GUI compatibility, thickness interference, building-code rules, end-user acceptance.
Role coverage: geometry, security, QA, evidence.
Map coverage: Architecture, Failure Modes, Risk, Controls, QA, Regression, Evidence, Decision Authority.
Evidence coverage: unit tests and CI only.
Measurement status: partial; no calibrated score.
Recommended corrections: integrate intersection gate into exporter; property-based and adversarial testing.
Regression risk: false-positive TOUCH/CROSS classification around numerical tolerances.
Reuse scope: this CAD V0.2 pilot only.
Verdict: GO for branch development; HOLD merge and production.
