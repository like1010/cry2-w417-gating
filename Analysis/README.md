# Analysis

| Folder | What it does |
|---|---|
| [`tp_reweighting/`](tp_reweighting/) | Rebuilds the bias of every WT-MetaD run from its HILLS and reweights the COLVAR (Tiwary-Parrinello). Writes the per-run dG(IN - OUT) and jackknife SE to `../tables/reproduced/`, then compares them with the reported values. |
| [`unbiased_md_trajectories/`](unbiased_md_trajectories/) | W417 chi2 traces of the apo CRY2 unbiased MD (manuscript Figure 1A-C). |
