# Per-run Tiwary-Parrinello reweighting

```bash
python reproduce_per_run.py            # every run in the repository, about 1-2 min per run
python reproduce_per_run.py CRY2_TH301 # only folders whose path contains CRY2_TH301
python compare_with_reported.py        # needs the full per_run_TP_from_repository.csv
```

Requirements: Python 3, NumPy and pandas.

**What is computed** (`tp_lib.py`). For each run folder with a 7-column chi1/chi2 HILLS:

1. The bias V(chi1, chi2, t) is rebuilt from the run's HILLS on a periodic 360 x 360 grid, with PLUMED's
   stretched-Gaussian kernel and cutoff and bias factor 10. c(t) is computed every 100 ps.
2. Each COLVAR row gets the bias of the hills deposited before it. Its weight is exp[(V - c(t)) / kT], with
   T = 300 K.
3. dG(IN - OUT) = -kT ln(P_IN / P_OUT), in kcal/mol, with IN = chi2 > 0 and OUT = chi2 < 0 over all chi1. The first
   100 ns are discarded. Negative values mean IN is lower.
4. The SE is a leave-one-block-out jackknife over 50 ns blocks of 100-500 ns.
5. Also reported: the canonical rotamer cores (|chi1| > 150 deg; OUT -120 to -55 deg, IN 60 to 120 deg in chi2),
   10 ps frames only, and 0 and 200 ns discards.

The functions are the authors' analysis code with unchanged arithmetic. The only change is that the readers accept
the gzipped files of this repository (see the header of `tp_lib.py`).

**Outputs.**
- `../../tables/reproduced/per_run_TP_from_repository.csv`
- `../../tables/reproduced/comparison_with_reported.csv`, which compares the first file with
  `../../tables/reported/reported_TP_per_run.csv`

Runs reported on 10 ps frames are compared on 10 ps frames. These runs (the CRY1-TH301 primaries and the earlier apo
CRY1 run) were reported from PLUMED-driver reweighting files. For them, differences of a few thousandths of a
kcal/mol are expected, because the bias here is rebuilt from HILLS.
