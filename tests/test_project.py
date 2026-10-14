from pathlib import Path
import sys,unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import project as p

class Tests(unittest.TestCase):
    def test_weighted_efficiency(self):
        g,players=p.demo_data();out=p.metrics((g,players))
        self.assertAlmostEqual(out.efg.iloc[0],(g.fgm.iloc[0]+.5*g.fg3m.iloc[0])/g.fga.iloc[0])
        self.assertTrue(np.allclose(out.net_rating,100*(g.pts-g.opp_pts)/out.poss_est))
    def test_duplicate_rejected(self):
        g,players=p.demo_data();g.loc[1,'game_id']=g.loc[0,'game_id']
        with self.assertRaises(AssertionError):p.validate((g,players))
    def test_points_mismatch_rejected(self):
        g,players=p.demo_data();players.loc[0,'pts']+=1
        with self.assertRaises(AssertionError):p.validate((g,players))
    def test_bootstrap_seed(self):
        a=p.bootstrap(p.demo_data(),seed=7,n=100);b=p.bootstrap(p.demo_data(),seed=7,n=100)
        pd.testing.assert_frame_equal(a,b)
        self.assertLessEqual(a.low.iloc[0],a.high.iloc[0])
    def test_zero_attempt_ratio(self):
        g,players=p.demo_data();players.loc[players.player_id=='DEMO_P0',['fga','fgm','fg3m','fg3a']]=0
        summary=p.player_summary((g,players));self.assertTrue(pd.isna(summary.set_index('player_id').loc['DEMO_P0','efg']))

if __name__=='__main__':unittest.main()
