# Tables

## `reported/` - per-run values as reported

| File | Contents |
|---|---|
| `reported_TP_per_run.csv` | One row per reported run: the run folder in this repository, the reported dG(IN - OUT) (chi2 = 0 partition, 100 ns discarded, kcal/mol), its 50 ns jackknife SE, the frame spacing used, and the source table. `Analysis/tp_reweighting/compare_with_reported.py` reads it. |
| `per_run_TP_CRY2_TH301_57atom.csv` | CRY2-TH301 runs. Columns: TP dG on 1 ps rows (`1ps_d0/d100/d200` = 0/100/200 ns discarded), rotamer-window TP (`1ps_rot`), 50 ns jackknife SE (`jk50`), running values at 200-500 ns (`run_*`), the same on 10 ps frames, OUT/IN minima of the final sum_hills surface, `dF_min`, a minimax barrier on that surface, and transition counts. |
| `per_run_TP_apo_CRY1_validation_jackknife.csv` | apo CRY2 (staged, unstaged, earlier single run), apo CRY1 (staged, earlier single run), and CRY1-TH301 (primary and second seed set): TP dG with jackknife SE on the chi2 = 0 partition and on the rotamer windows. The `reweighted file` column refers to the authors' analysis tree. |
| `per_run_KL101_CRY2.csv` | KL101-CRY2: seed provenance, sum_hills and reweighted estimates, and TP dG with jackknife SE (100 ns discarded, and 0 and 200 ns). |

## `reproduced/` - recomputed from this repository

Written by `Analysis/tp_reweighting/`:
- `per_run_TP_from_repository.csv`: every run, recomputed from the gzipped HILLS and COLVAR here;
- `comparison_with_reported.csv`: the reported value, the recomputed value and their difference.
