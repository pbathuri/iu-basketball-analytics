from pathlib import Path
import csv
root=Path(__file__).resolve().parents[1]/'data/raw';root.mkdir(parents=True,exist_ok=True)
base=['pts','fgm','fga','fg3m','fg3a','ftm','fta','orb','tov']
tables={'games.csv':['game_id','date','season','team','opponent','venue','overtime']+base+['opp_'+x for x in base],
'players.csv':['game_id','player_id','player_name','minutes','pts','fgm','fga','fg3m','fg3a','ftm','fta'],
'provenance.csv':['game_id','source_url','accessed_utc','entered_by','checked_by','notes']}
for name,cols in tables.items():
    with (root/name).open('x',newline='') as f:csv.writer(f).writerow(cols)
    print('Created',name)
