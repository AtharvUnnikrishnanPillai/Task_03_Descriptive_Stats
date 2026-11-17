"""Export all shared-column metrics and a human-readable comparison."""
import csv,gzip,json,shutil
from pathlib import Path
from collections import Counter
out=Path('results');out.mkdir(exist_ok=True)
datasets={}
for label,token in [('Facebook ads','fb_ads'),('Facebook posts','fb_posts'),('Twitter/X posts','tw_posts')]:
    root=next(Path('outputs').glob('*'+token+'*'))/'pure_python'
    d=json.loads((root/'overall.json').read_text());datasets[label]=d
    shutil.copy(root/'overall.json',out/(token+'_overall.json'))
    manifest=json.loads((root/'manifest.json').read_text())
    (out/(token+'_groups.json')).write_text(json.dumps(manifest['groups'],indent=2))
    with (out/(token+'_group_sizes.csv')).open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['group_columns','key','records'])
        for fn,meta in manifest['groups'].items():
            if meta['count']>10000:continue # High-cardinality summaries remain reproducible locally
            with gzip.open(root/fn,'rt') as lines:
                for line in lines:
                    r=json.loads(line);w.writerow([','.join(meta['keys']),json.dumps(r['key']),r['rows']])
shared=sorted(set.intersection(*(set(d['types']) for d in datasets.values())))
union=sorted(set.union(*(set(d['types']) for d in datasets.values())))
with (out/'schema_matrix.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['column',*datasets])
    for col in union:w.writerow([col,*[d['types'].get(col,'absent') for d in datasets.values()]])
with (out/'shared_columns.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['column','dataset','type','count','missing','missing_pct','mean','min','max','std','median','unique','mode','mode_frequency'])
    for col in shared:
        for label,d in datasets.items():
            s=d['columns'][col];w.writerow([col,label,d['types'][col],*[s.get(k) for k in ['count','missing','missing_pct','mean','min','max','std','median','unique','mode','mode_frequency']]])
def rate(d,col):return 100*d['columns'][col]['mean']
lines=['# What differs across the three election datasets?','',
       f'The three files share **{len(shared)} exact column names**. The shared fields are content classification flags. Page/account keys, dates, and engagement counters are not common under identical names. The full inventory and all shared-column statistics are in [schema_matrix.csv](results/schema_matrix.csv) and [shared_columns.csv](results/shared_columns.csv).','',
       '| Dataset | Records | Columns |','|---|---:|---:|']
for label,d in datasets.items():lines.append(f"| {label} | {d['rows']:,} | {d['column_count']} |")
lines+=['','## Selected positive-label rates','','Percent of nonmissing records coded 1, using a separate denominator for each field and dataset. Labels may overlap.','',
        '| Label | Ads | Facebook posts | Twitter/X posts |','|---|---:|---:|---:|']
for name,col in [('Call to action','cta_msg_type_illuminating'),('Advocacy','advocacy_msg_type_illuminating'),('Attack','attack_msg_type_illuminating'),('Issue','issue_msg_type_illuminating'),('Fundraising','fundraising_cta_subtype_illuminating')]:
    lines.append('| '+name+' | '+' | '.join(f'{rate(d,col):.2f}%' for d in datasets.values())+' |')
lines+=['','Calls to action separate paid ads from posts more sharply than advocacy does. The gap describes these collected records. It cannot establish that buying an ad causes a change in messaging: the files may contain different accounts, posting periods, and selection rules. The row is an ad purchase or a post, not a voter or a unique audience member.','',
        '## Coverage and comparability','',
        'For the Twitter/X call-to-action rate, 1,270 rows lack a label, leaving 26,034 scored posts. Treating missing scores as zero would change the denominator and depress the rate. In Facebook posts, the header combines the scored-message and election-integrity names into one field. We keep it as delivered and do not reconstruct or compare a missing integrity field.','',
        'Facebook Likes and Twitter/X likeCount are analogous but not identically named. Total Interactions, reposts, views, and ad impressions have different meanings. They are reported below in their native units; they are not added together or interpreted as a platform popularity ranking.','',
        '| Measure | Dataset | Nonmissing | Mean | Median |','|---|---|---:|---:|---:|']
for label,col in [('Facebook ads','estimated_impressions'),('Facebook posts','Likes'),('Facebook posts','Total Interactions'),('Twitter/X posts','likeCount'),('Twitter/X posts','retweetCount')]:
    s=datasets[label]['columns'][col];lines.append(f"| {col} | {label} | {s['count']:,} | {s['mean']:,.2f} | {s['median']:,.1f} |")
lines+=['','Ad impressions describe estimated exposure. In both post datasets, the mean likes exceed the median; higher-engagement records pull the average up. Neither likes nor impressions identify unique viewers, persuasion, or electoral outcomes.','',
        '## What grouping adds','']
for label,token in [('Facebook ads','fb_ads'),('Facebook posts','fb_posts'),('Twitter/X posts','tw_posts')]:
    gs=json.loads((out/(token+'_groups.json')).read_text());lines.append(f"- **{label}:** "+'; '.join(f"{v['count']:,} groups by "+', '.join(v['keys']) for v in gs.values())+'.')
lines+=['','Every page/ad pair is a singleton. For Facebook posts, grouping by Facebook_Id measures activity across pages, while Type separates formats. Twitter/X has no explicit author identifier in this file: month_year tracks collection over time and source describes the posting client, not the author. These grouping keys answer different questions and are not joined across platforms.']
Path('CROSS_DATASET.md').write_text('\n'.join(lines)+'\n')
def top_groups(token,index,metric):
    root=next(Path('outputs').glob('*'+token+'*'))/'pure_python'
    manifest=json.loads((root/'manifest.json').read_text())
    c=manifest['columns'].index(metric);m=manifest['numeric_fields'].index('median')
    with gzip.open(root/f'group_{index}.jsonl.gz','rt') as src:
        rows=[json.loads(line) for line in src]
    return sorted(rows,key=lambda r:-r['rows'])[:3],c,m
extra=['','## Within-platform examples','','These are the three largest groups by record count in each grouping, not the groups with the highest engagement. Medians give a typical record within a group.','','| Group | Value | Records | Measure | Median |','|---|---|---:|---|---:|']
for token,label,metric in [('fb_posts','Facebook post format','Total Interactions'),('tw_posts','Twitter/X posting client','likeCount')]:
    rows,c,m=top_groups(token,2,metric)
    for r in rows:
        extra.append(f"| {label} | {r['key'][0]} | {r['rows']:,} | {metric} | {r['stats'][c][m]:,.1f} |")
with Path('CROSS_DATASET.md').open('a') as f:f.write('\n'.join(extra)+'\n')
