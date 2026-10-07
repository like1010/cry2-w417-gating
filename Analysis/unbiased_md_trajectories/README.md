# Figure 1A-C -- apo cMD chi2 trajectories

Time series of the W417 chi2 dihedral from unbiased apo conventional MD. chi2 stays in
the negative (OUT) region in almost all trajectories; the 500 ns trajectory
`chi2_mda_apo_chi2_res417_500ns.xvg` has one spontaneous OUT -> IN crossing episode at
about 409-425 ns. These traces show that the flip is rare in unbiased MD; they do not
give equilibrium populations.

```bash
python apo_cmd_chi2_trajectories.py
```

**Inputs** (`data/`, 3.9 MB)

| File | Trajectory |
|---|---|
| `chi2_W417_mda_100ns.xvg` | 100 ns apo cMD |
| `chi2_W417_500ns_mda.xvg` | 500 ns, stays in the out state |
| `chi2_mda_apo_chi2_res417_500ns.xvg` | 500 ns, rare spontaneous out -> in transition |
| `chi2_W417_mda_1us.xvg` | 1 us, no inter-basin crossing |

**Outputs** (`results/`) -- `Fig1a_panel1..5_*.png`. Manuscript Figure 1A-C uses
panels 2-4; panels 1 and 5 appear as Figure S2A-B.
