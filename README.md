# Task 03: Comparing Facebook ads, Facebook posts, and Twitter/X posts

Milestone B extends the three Task 2 implementations into CSV summarizers that accept unfamiliar schemas. The same three programs analyze all three files. A separate runner chooses groups, and a reporting script compares the shared columns.

**Findings.** Of 246,745 Facebook ads, 57.28% carry a call-to-action label, versus 13.28% of 19,009 Facebook posts and 10.97% of the 26,034 Twitter/X posts with an available label. Advocacy varies much less: 54.86%–56.37%. Read [CROSS_DATASET.md](CROSS_DATASET.md) for denominators, platform-specific findings, and limitations. See [REFLECTION.md](REFLECTION.md) for design choices and tradeoffs.

## Reproduce the assignment

Download the [assigned three-file archive](https://drive.google.com/file/d/1Jq0fPb-tq76Ee_RtM58fT0_M3o-JDBwe/view?usp=sharing) and extract the three CSVs into a local directory named data. Use Python 3.11+ and run from the repository root:

```bash
python -m pip install -r requirements.txt
python -m unittest -v test_stats
python run_all.py data
python report.py
```

The runner executes pure Python, Pandas, and Polars sequentially on each dataset, then compares their complete overall and grouped results. Allow several GB of RAM and disk. To run one dataset, add `--only ads`, `--only facebook`, or `--only twitter`. The runner uses the original archive filenames. The underlying scripts accept any CSV path. For example:

```bash
python pure_python_stats.py survey.csv --group region
python pandas_stats.py survey.csv --group region
python polars_stats.py survey.csv --group region
python compare_results.py --root outputs/survey --out results/survey_validation.json
```

Omit --group for an overall-only analysis; repeat it for additional levels or use a comma-separated column combination. Give the exact header spelling and enclose names with spaces in quotes. UTF-8 and UTF-8 BOM are supported by default. For another known encoding use e.g. `--encoding cp1252`; an invalid byte sequence fails rather than silently changing identifiers.

## Statistics and output

Numeric columns receive nonmissing count, missing count/percentage, mean, minimum, maximum, sample standard deviation and median. Nonnumeric columns receive counts, distinct count, mode, its frequency, and top five values. Frequency ties sort alphabetically. Types are inferred once per input and retained within groups. Null group keys are included. Sample standard deviation is undefined when fewer than two values are available.

The reader trims whitespace and recognizes blank, NA, N/A, null, none and nan as missing. A column is numeric only if every present value converts to a finite number; common currency/comma formatting is supported. Identifier-like names remain categorical; ISO calendar dates are recognized. Free-form timestamps and serialized lists/dictionaries are summarized as strings. A valid empty list is different from a missing cell. For monetary interpretation, separate currencies first.

Each local outputs directory contains a manifest (column order, types, field names), overall JSON, and a gzip JSON-lines file per grouping. Each line records a group key, row count and all column statistics in manifest order. Results included for GitHub are the overall summaries, group inventories, sizes for smaller grouping levels, a schema matrix, the complete 27-column comparison, and per-dataset validation reports. Full per-ad group outputs would largely reproduce the raw records and are regenerated locally instead. No input datasets are included.

Pure Python uses only the standard library; Pandas and Polars are pinned in requirements.txt. The numerical reducers differ by engine; type inference, output formatting, and mathematical singleton identities are shared. The comparison checks counts and categories exactly and floats within absolute/relative tolerance 1e-9.

## Submission

Upload these extracted files, including results/, to a public repository named **Task_03_Descriptive_Stats**. Exclude data/, outputs/, and the ZIP itself. This project was developed with AI assistance. Review the code, findings and reflection before submitting.
