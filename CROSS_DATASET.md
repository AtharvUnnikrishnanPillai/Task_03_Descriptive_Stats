# What differs across the three election datasets?

The three files share **27 exact column names**. The shared fields are content classification flags. Page/account keys, dates, and engagement counters are not common under identical names. The full inventory and all shared-column statistics are in [schema_matrix.csv](results/schema_matrix.csv) and [shared_columns.csv](results/shared_columns.csv).

| Dataset | Records | Columns |
|---|---:|---:|
| Facebook ads | 246,745 | 41 |
| Facebook posts | 19,009 | 56 |
| Twitter/X posts | 27,304 | 47 |

## Selected positive-label rates

Percent of nonmissing records coded 1, using a separate denominator for each field and dataset. Labels may overlap.

| Label | Ads | Facebook posts | Twitter/X posts |
|---|---:|---:|---:|
| Call to action | 57.28% | 13.28% | 10.97% |
| Advocacy | 54.86% | 54.93% | 56.37% |
| Attack | 27.19% | 21.67% | 30.76% |
| Issue | 38.16% | 46.03% | 50.77% |
| Fundraising | 22.85% | 1.84% | 0.79% |

Calls to action separate paid ads from posts more sharply than advocacy does. The gap describes these collected records. It cannot establish that buying an ad causes a change in messaging: the files may contain different accounts, posting periods, and selection rules. The row is an ad purchase or a post, not a voter or a unique audience member.

## Coverage and comparability

For the Twitter/X call-to-action rate, 1,270 rows lack a label, leaving 26,034 scored posts. Treating missing scores as zero would change the denominator and depress the rate. In Facebook posts, the header combines the scored-message and election-integrity names into one field. We keep it as delivered and do not reconstruct or compare a missing integrity field.

Facebook Likes and Twitter/X likeCount are analogous but not identically named. Total Interactions, reposts, views, and ad impressions have different meanings. They are reported below in their native units; they are not added together or interpreted as a platform popularity ranking.

| Measure | Dataset | Nonmissing | Mean | Median |
|---|---|---:|---:|---:|
| estimated_impressions | Facebook ads | 246,745 | 45,601.53 | 3,499.0 |
| Likes | Facebook posts | 19,009 | 2,377.70 | 139.0 |
| Total Interactions | Facebook posts | 19,009 | 4,190.44 | 283.0 |
| likeCount | Twitter/X posts | 27,304 | 6,913.69 | 1,406.0 |
| retweetCount | Twitter/X posts | 27,304 | 1,322.06 | 333.0 |

Ad impressions describe estimated exposure. In both post datasets, the mean likes exceed the median; higher-engagement records pull the average up. Neither likes nor impressions identify unique viewers, persuasion, or electoral outcomes.

## What grouping adds

- **Facebook ads:** 4,475 groups by page_id; 246,745 groups by page_id, ad_id.
- **Facebook posts:** 21 groups by Facebook_Id; 10 groups by Type.
- **Twitter/X posts:** 15 groups by month_year; 14 groups by source.

Every page/ad pair is a singleton. For Facebook posts, grouping by Facebook_Id measures activity across pages, while Type separates formats. Twitter/X has no explicit author identifier in this file: month_year tracks collection over time and source describes the posting client, not the author. These grouping keys answer different questions and are not joined across platforms.

## Within-platform examples

These are the three largest groups by record count in each grouping, not the groups with the highest engagement. Medians give a typical record within a group.

| Group | Value | Records | Measure | Median |
|---|---|---:|---|---:|
| Facebook post format | Link | 7,404 | Total Interactions | 61.0 |
| Facebook post format | Photo | 3,820 | Total Interactions | 1,058.5 |
| Facebook post format | Native Video | 2,931 | Total Interactions | 908.0 |
| Twitter/X posting client | Twitter Web App | 14,930 | likeCount | 1,660.0 |
| Twitter/X posting client | Twitter for iPhone | 8,494 | likeCount | 413.0 |
| Twitter/X posting client | Sprout Social | 2,933 | likeCount | 9,480.0 |
