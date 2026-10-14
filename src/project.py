"""Basketball baseline. Team games are one IU row per game; opponents share that row."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]

def demo_data():
    rng=np.random.default_rng(41); rows=[]; players=[]
    for i in range(24):
        d={'game_id':f'DEMO{i:03}', 'date':str(pd.Timestamp('2025-11-01')+pd.Timedelta(days=4*i))[:10],
           'season':'SYNTHETIC', 'team':'DEMO_IU', 'opponent':f'DEMO_OPP{i%8}',
           'venue':['home','away','neutral'][i%3], 'overtime':0}
        for prefix in ('','opp_'):
            fga=int(rng.integers(50,75)); fg3a=int(rng.integers(15,30)); fg3m=int(rng.integers(4,12))
            fgm=int(rng.integers(15,min(32,fga-fg3a+fg3m+1))); fta=int(rng.integers(10,25)); ftm=int(rng.integers(5,fta+1))
            d.update({prefix+k:v for k,v in dict(fga=fga,fgm=fgm,fg3a=fg3a,fg3m=fg3m,fta=fta,ftm=ftm,orb=int(rng.integers(4,14)),tov=int(rng.integers(7,18)),pts=2*fgm+fg3m+ftm).items()})
        rows.append(d)
        shares=rng.dirichlet(np.ones(8)*3)
        threes=rng.multinomial(d['fg3m'],shares);twos=rng.multinomial(d['fgm']-d['fg3m'],shares)
        missed3=rng.multinomial(d['fg3a']-d['fg3m'],shares)
        missed2=rng.multinomial(d['fga']-d['fg3a']-(d['fgm']-d['fg3m']),shares)
        free=rng.multinomial(d['ftm'],shares);missedft=rng.multinomial(d['fta']-d['ftm'],shares)
        for j in range(8):
            players.append(dict(game_id=d['game_id'],player_id=f'DEMO_P{j}',player_name=f'Demo player {j}',minutes=25,
                pts=int(3*threes[j]+2*twos[j]+free[j]),fgm=int(threes[j]+twos[j]),fga=int(threes[j]+twos[j]+missed2[j]+missed3[j]),
                fg3m=int(threes[j]),fg3a=int(threes[j]+missed3[j]),ftm=int(free[j]),fta=int(free[j]+missedft[j])))
    return pd.DataFrame(rows),pd.DataFrame(players)

def load_data(mode='demo'):
    if mode=='demo':return demo_data()
    if mode!='real':raise ValueError('mode must be demo or real')
    g=pd.read_csv(ROOT/'data/raw/games.csv')
    provenance=ROOT/'data/raw/provenance.csv'
    if provenance.exists():
        links=pd.read_csv(provenance)[['game_id','source_url']]
        g=g.merge(links,on='game_id',how='left',validate='one_to_one')
    return g,pd.read_csv(ROOT/'data/raw/players.csv')

def preview(data):
    print('Team games\n',data[0].head().to_string(index=False));print('Player games\n',data[1].head().to_string(index=False))

def validate(data):
    g,p=data
    assert len(g)>0 and len(p)>0
    assert not g.game_id.duplicated().any(), 'Duplicate game IDs'
    assert not p.duplicated(['game_id','player_id']).any(), 'Duplicate player-game IDs'
    assert set(p.game_id)<=set(g.game_id), 'Orphan player game'
    assert g.venue.isin(['home','away','neutral']).all()
    assert pd.to_datetime(g.date,errors='coerce').notna().all()
    assert (g.overtime>=0).all()
    for frame, prefixes in [(g,('','opp_')),(p,('',))]:
        for pre in prefixes:
            cols=[pre+x for x in ['pts','fgm','fga','fg3m','fg3a','ftm','fta']]
            assert np.isfinite(frame[cols]).all().all() and (frame[cols]>=0).all().all()
            assert (frame[pre+'fgm']<=frame[pre+'fga']).all()
            assert (frame[pre+'fg3m']<=frame[pre+'fg3a']).all()
            assert (frame[pre+'fg3m']<=frame[pre+'fgm']).all()
            assert (frame[pre+'fg3a']<=frame[pre+'fga']).all()
            assert ((frame[pre+'fgm']-frame[pre+'fg3m']) <= (frame[pre+'fga']-frame[pre+'fg3a'])).all()
            assert (frame[cols]==np.floor(frame[cols])).all().all(), 'Integer box-score fields required'
            assert (frame[pre+'ftm']<=frame[pre+'fta']).all()
            assert np.allclose(frame[pre+'pts'],2*frame[pre+'fgm']+frame[pre+'fg3m']+frame[pre+'ftm'])
    assert (g[['orb','tov','opp_orb','opp_tov']]>=0).all().all()
    assert np.isfinite(p.minutes).all() and (p.minutes>=0).all()
    sums=p.groupby('game_id').pts.sum().reindex(g.game_id)
    assert np.allclose(sums,g.pts), 'Player points must reconcile to team points'
    return pd.DataFrame({'check':['unique keys','valid shots','points reconcile'],'status':['PASS']*3})

def metrics(data):
    validate(data);g,p=data;g=g.copy()
    poss=g.fga-g.orb+g.tov+0.475*g.fta
    opp=g.opp_fga-g.opp_orb+g.opp_tov+0.475*g.opp_fta
    g['poss_est']=(poss+opp)/2
    if (g.poss_est<=0).any():raise ValueError('Nonpositive estimated possessions')
    g['efg']=(g.fgm+0.5*g.fg3m)/g.fga.replace(0,np.nan)
    g['off_rating']=100*g.pts/g.poss_est
    g['def_rating']=100*g.opp_pts/g.poss_est
    g['net_rating']=g.off_rating-g.def_rating
    g['margin']=g.pts-g.opp_pts
    g['pace_40']=g.poss_est*40/(40+5*g.overtime)
    return g

def player_summary(data,min_minutes=100):
    p=data[1];cols=['minutes','pts','fgm','fga','fg3m','fg3a','ftm','fta']
    a=p.groupby(['player_id','player_name'])[cols].sum().reset_index()
    a['games']=p.groupby('player_id').game_id.nunique().reindex(a.player_id).to_numpy()
    a['ppg']=a.pts/a.games
    a['efg']=(a.fgm+0.5*a.fg3m)/a.fga.replace(0,np.nan)
    a['pts_per40']=40*a.pts/a.minutes.replace(0,np.nan)
    a['eligible']=a.minutes>=min_minutes
    a['rank_pts_per40']=a.pts_per40.where(a.eligible).rank(ascending=False,method='min')
    return a

def bootstrap(data,seed=41,n=2000):
    g=metrics(data);rng=np.random.default_rng(seed)
    idx=rng.integers(0,len(g),size=(n,len(g)))
    # Ratio of sums: season efficiency, not average game efficiency.
    rates=100*g.margin.to_numpy()[idx].sum(1)/g.poss_est.to_numpy()[idx].sum(1)
    return pd.DataFrame({'seed':[seed],'estimate':[100*g.margin.sum()/g.poss_est.sum()],
       'low':[np.quantile(rates,.025)],'high':[np.quantile(rates,.975)],'games':[len(g)]})

def export(data,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    g=metrics(data);a=player_summary(data)
    g.to_csv(out/'team_games.csv',index=False);a.to_csv(out/'players_summary.csv',index=False)
    data[1].to_csv(out/'player_games.csv',index=False)
    bootstrap(data).to_csv(out/'uncertainty.csv',index=False)
    fig,ax=plt.subplots(figsize=(9,4));ax.plot(pd.to_datetime(g.date),g.net_rating,marker='o')
    ax.axhline(0,color='grey');ax.set(ylabel='Net points per 100 estimated possessions',title='Game-level net rating | '+str(g.season.iloc[0]));fig.autofmt_xdate();fig.tight_layout()
    fig.savefig(out/'net_rating.png',dpi=150);plt.close(fig)
    return g,a

def run_demo():
    data=load_data();out=ROOT/'outputs/demo';export(data,out)
    print('SYNTHETIC demo complete:',out)
