# OUT and IN conformations of the CRY2 gatekeeper W417: simulation data

Simulation inputs, raw well-tempered metadynamics (WT-MetaD) outputs, derived tables and analysis code for:

> Li, K.; Ki, M.-R.; Pack, S. P.; Cho, A. E. *Sampling the OUT and IN Conformations of the CRY2 Gatekeeper W417.*

The study samples the side-chain orientation of the gatekeeper W417 at the entrance of the CRY2 FAD pocket. Steered
preparation generates starting structures in different torsional regions. Separate 500 ns WT-MetaD runs with the
chi1 and chi2 torsions as collective variables are then started from those structures. The same protocol is applied to
the homologous W399 in CRY1.

## Layout

| Directory | Contents |
|---|---|
| [`simulations/`](simulations/) | one folder per WT-MetaD production run: inputs, gzipped HILLS and COLVAR, topology, start structure, `SOURCE.json`; plus the steered seeding chains |
| [`topology/`](topology/) | TH301 parameters with their ACPYPE record, KL101 parameters, and the CRY2-TH301 complex topology |
| [`Structures/`](Structures/) | homology models and the six CRY2-TH301 seed structures |
| [`Analysis/`](Analysis/) | per-run reweighting code that reproduces the reported free-energy differences from this repository; apo unbiased MD chi2 traces |
| [`tables/`](tables/) | reported per-run tables, and the values reproduced from this repository |

## Simulations

All production runs are 500 ns of 2D WT-MetaD on the gatekeeper chi1 and chi2. Settings: Gaussian width 0.3 rad on
both CVs, initial height 0.01 kJ/mol, deposition every 1 ps, bias factor 10, 300 K. Every run folder lists its seed
time and region.

| System | Runs | Folder |
|---|---|---|
| CRY2-TH301 | 3 (OUT, near-zero chi2 and IN seeds) | `simulations/CRY2_TH301/` |
| apo CRY2 | 3 staged + 2 started from unbiased-MD frames + 1 earlier single run | `simulations/CRY2_apo/` |
| apo CRY1 | 3 staged + 1 earlier single run | `simulations/CRY1_apo/` |
| CRY1-TH301 | 3 primary + 3 second-seed-set runs | `simulations/CRY1_TH301/` |
| KL101-CRY2 (DiffDock pose) | 3 | `simulations/CRY2_KL101/` |

[`simulations/README.md`](simulations/README.md) has the full run table.

## Reproducing the per-run free-energy differences

```bash
python Analysis/tp_reweighting/reproduce_per_run.py
python Analysis/tp_reweighting/compare_with_reported.py
```

The first script rebuilds each run's bias from its HILLS and reweights its COLVAR (Tiwary-Parrinello). It writes
dG(IN - OUT) and its 50 ns block-jackknife SE to `tables/reproduced/`. The second script compares these values with
the reported ones. Both need only NumPy and pandas, and take about 1-2 minutes per run.

## Using the files with GROMACS and PLUMED

HILLS, COLVAR, topologies and structures are gzipped. Decompress before use, for example `gunzip -k topol.top.gz`.
A run folder then contains what `gmx grompp` and `mdrun -plumed` need. The only exception is the AMBER99SB-ILDN
force-field folder, which comes with GROMACS.

## Software

| Stage | Version |
|---|---|
| MD and enhanced sampling | GROMACS 2024 / 2024.2 patched with PLUMED 2.9.2 |
| Ligand parameters | GAFF2 with AM1-BCC charges via ACPYPE 2022.7.21 (AmberTools antechamber/sqm) |
| Ligand hydrogens of the CRY2-TH301 seed structures | RDKit 2025.09 (Schrödinger Python 3.11) |
| Analysis | Python 3 with NumPy and pandas (`environment.yml`) |
| Homology modelling | SWISS-MODEL |
| Molecular graphics | Maestro 14.8 (Schrödinger, academic edition) |

Force field: AMBER99SB-ILDN with TIP3P water. In the CRY2 complex, TH301 was placed by superposition of the mouse
CRY2-TH301 crystal structure (6KX8) on the homology model. The KL101-CRY2 pose is a DiffDock model.

## Not in this repository

MD trajectories (`.xtc`, several hundred GB) are available from the authors on request.

## Third-party data

Experimental structures come from the PDB and are not redistributed here: 6KX8 (mouse CRY2-TH301), 6KX7 (mouse
CRY1-TH301), 6KX4 (mouse CRY1 apo), 4I6J (homology-model template) and 7D0N (apo CRY2 reference). The human CRY2
sequence is NCBI NP_066940.

## License

Code is released under the MIT License and data files under CC BY 4.0. See [`LICENSE`](LICENSE).
