from pathlib import Path
import sys,argparse,time,subprocess,json
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'src'))
import project as p
parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=0);parser.add_argument('--mode',choices=['demo','real'],default='demo');a=parser.parse_args()
out=root/'outputs'/a.mode/f'sensitivity_{a.seed}';out.mkdir(parents=True,exist_ok=True)
start=time.perf_counter()
data=p.load_data(a.mode)
result=p.bootstrap(data,seed=a.seed,n=20000)
result.to_csv(out/'bootstrap.csv',index=False)
(out/'run.json').write_text(json.dumps({'seed':a.seed,'mode':a.mode,'wall_seconds':time.perf_counter()-start},indent=2))
print('Wrote',out)
