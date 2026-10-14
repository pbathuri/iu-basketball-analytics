# Dashboard build sheet

Tool: Tableau or Power BI. The source Tableau reference was not included with the request. Add its URL/screenshot at kickoff, record which views to reproduce, and use this specification until then.

## Data model
Export with notebook 04. `team_games.csv` is one row per game. `player_games.csv` is many rows per game. Relate on game_id with one-to-many cardinality; do not physically join then sum duplicated team points. `players_summary.csv` is a separate preaggregated table: use it for an unfiltered season view only. For game/date filtering, calculate player summaries from player_games.

## Three pages
1. **Season overview:** win/loss record from margin, points/game, weighted eFG, net rating and game count; trend by date; venue filter. Include season, source and data-through date.
2. **Players:** minutes, games, PPG, eFG, points per 40; player and minimum-minutes controls; explicitly “IU sample rank.” Pair rate statistics with playing time.
3. **Game explorer:** opponent, venue, margin, offensive/defensive rating and source link; select a game to inspect the raw box score.

Tableau calculated field: `(SUM([fgm])+0.5*SUM([fg3m]))/SUM([fga])`. Guard SUM(fga)=0 with NULL. Power BI DAX: `eFG = DIVIDE(SUM(team_games[fgm]) + 0.5*SUM(team_games[fg3m]), SUM(team_games[fga]))`. Net rating uses `100 * (SUM(pts)-SUM(opp_pts))/SUM(poss_est)`.

Use cream/crimson with a neutral comparison color, readable labels, no red/green-only encoding, and explicit units. Avoid a crowded chart for every metric. Include a short text box that explains one basketball insight and one limitation.

## Acceptance
- Pick three games and reconcile dashboard numbers to the box scores and Python.
- Filter to a venue and verify weighted ratios again.
- Ask a peer to find the highest eligible player rate, an unusually poor game, and a home/away comparison without guidance.
- Submit the workbook or a permitted interactive link, exports, screenshots of key views, notebook outputs, and a source register.
- If publication rights are unclear, demonstrate locally; don't silently upload data to Tableau Public.
