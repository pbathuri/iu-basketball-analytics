# Basketball inputs

Use the official IU season statistics and linked box scores in SOURCES.md. Default is the completed 2025–26 men's season. If selecting women's basketball, replace the source URL and scope together. Collect the complete season by Week 2, including postseason, or explicitly document exclusions. Automated scraping is optional; the reliable baseline is a reviewed CSV assembled from official box scores. Respect the site's terms; cache what you are permitted to use.

Run `python scripts/create_input_templates.py` to create empty CSV templates under data/raw (it refuses to replace existing files). Open them in a spreadsheet or notebook and enter source values. Two students independently check the first game. Put the exact box-score URL and date in data/raw/provenance.csv. Run the Week 1 notebook in real mode after ten games and complete player rows are entered.

## games.csv — one row per IU game
| Fields | Meaning / constraint |
|---|---|
| game_id | Stable unique key, e.g. season-date-opponent; not a row number |
| date, season | ISO date; season label such as 2025-26 |
| team, opponent | Canonical names; do not confuse Indiana with Indiana State |
| venue | home / away / neutral, from IU's perspective |
| overtime | Nonnegative integer number of 5-minute overtime periods |
| pts, fgm, fga, fg3m, fg3a, ftm, fta, orb, tov | IU box-score totals; nonnegative numbers |
| opp_pts, opp_fgm, opp_fga, opp_fg3m, opp_fg3a, opp_ftm, opp_fta, opp_orb, opp_tov | Opponent equivalents |

## players.csv — one row per player per game played
`game_id,player_id,player_name,minutes,pts,fgm,fga,fg3m,fg3a,ftm,fta`.
Use a stable player identifier independent of display name. Convert 12:30 to 12.5 minutes. DNP is not a zero-minute appearance: omit it from played-game rows and document that policy. Player points should reconcile to team points. Investigate team-only administrative adjustments rather than inventing a player. Aggregate team rebounds may differ from the sum of credited player rebounds.

## Provenance
`game_id,source_url,accessed_utc,entered_by,checked_by,notes`.
Record raw-file hashes in DATA_REGISTER.csv and save an immutable source snapshot where terms permit. Do not redistribute source pages or images without checking permissions. A public webpage is not necessarily open-licensed data.

The synthetic fixture allocates team totals across fictional players to exercise aggregation. It has no real player meaning and is never an acceptable analysis dataset. Box-score shot and point fields must be integers.

For Big Ten or national rankings, acquire the same metric, season, coverage and eligibility rules for every comparison team. Until then, the dashboard ranks **IU players within the chosen sample only**. Never label that national rank.
