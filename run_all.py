"""Run the three files in a directory; core engines have no platform-specific branches."""
import argparse,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('data_dir',type=Path);p.add_argument('--only',choices=['ads','facebook','twitter']);a=p.parse_args()
for label,stem,groups in [('ads','fb_ads',['page_id','page_id,ad_id']),('facebook','fb_posts',['Facebook_Id','Type']),('twitter','tw_posts',['month_year','source'])]:
    if a.only and label!=a.only:continue
    file=a.data_dir/f'2024_{stem}_president_scored_anon.csv'
    for engine in ['pure_python','pandas','polars']:
        print(label,engine,flush=True)
        subprocess.run([sys.executable,engine+'_stats.py',str(file)]+[v for g in groups for v in ['--group',g]],check=True)
    subprocess.run([sys.executable,'compare_results.py','--root',str(Path('outputs')/file.stem),'--out',f'results/{label}_validation.json'],check=True)
