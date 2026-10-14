# Five-week roadmap

Week 1 begins at kickoff; enter actual dates on the issue board. Every gate needs a peer review and mentor sign-off.

## Week 1 — Acquire and audit

**Build:** Collect ten games plus player box scores; agree IDs and scope.

**Learn:** Review the official page and manually reconcile one box score.

**Evidence:** games.csv, players.csv, source register and a clean-clone run.

**Done when:** At least ten games; unique game/team and game/player keys; every record traceable.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 2 — Build metrics and explain variation

**Build:** Finish season coverage; derive rate metrics and weighted season aggregates.

**Learn:** Calculate eFG% and possessions by hand; compare raw points with pace-adjusted efficiency.

**Evidence:** KPI dictionary, missingness report, three annotated figures.

**Done when:** Five spot checks pass; zero-denominator values remain missing; overtime identified.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 3 — Test one basketball claim

**Build:** Bootstrap game-level net rating; compare home/away descriptively; add player rankings.

**Learn:** Explain the unit of resampling and why association is not causation.

**Evidence:** Claim notebook, uncertainty intervals, eligible player ranking.

**Done when:** State sample size and minutes threshold; compare with a simple season-average baseline.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 4 — Build and test the dashboard

**Build:** Import tidy exports into Tableau or Power BI; build overview, players and game explorer.

**Learn:** Practice star-schema relationships, weighted ratios and filter context.

**Evidence:** Working workbook, KPI reconciliation sheet and two peer usability reviews.

**Done when:** Three user tasks completed; filtered KPIs match Python; no unsupported national ranking.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 5 — Freeze and present

**Build:** Finish source audit, accessibility, narrative and clean rerun.

**Learn:** Defend a metric and a limitation without reading code.

**Evidence:** Dashboard, 6-slide story, reproducible release and individual reflections.

**Done when:** Another student rebuilds tables from approved inputs; every chart has a source and denominator.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## If time gets tight

Keep acquisition, one defensible baseline, validation and the final explanation. Defer extra seasons/assets, advanced models and visual polish. Do not replace missing real data with unlabeled demo outputs.
