# Simulations

One folder per 500 ns WT-MetaD production run (chi1 and chi2 of the gatekeeper biased; sigma 0.3 / 0.3 rad,
initial height 0.01 kJ/mol, deposition every 1 ps, bias factor 10, 300 K).

## What each run folder contains

| File | Contents |
|---|---|
| `HILLS*.gz` | the run's HILLS (time, chi1, chi2, sigma_chi1, sigma_chi2, height, biasf) |
| `COLVAR*.gz` | chi1, chi2 every 1 ps (500,001 rows over 0-500 ns; a few runs have duplicated restart rows) |
| `*.mdp`, `plumed*.dat` | the run's GROMACS and PLUMED inputs, as in the run folder (restart variants included) |
| `topol.top.gz`, `*.itp` | the topology the run used |
| `start_*.gro.gz` | the production start structure, identified by matching the gatekeeper chi1/chi2 of the file with the first COLVAR row |
| `seed_*.gro.gz` | the seed frame, where it differs from the start structure |
| `SOURCE.json` | for every stored file: source path, md5 and size of the source, md5 of the stored file; HILLS/COLVAR row counts and time range; the start-structure check; notes |

Decompress before use (`gunzip -k`). The force-field folder (amber99sb-ildn.ff) comes with GROMACS.

`seed_chain/` folders hold the steered seeding chains of apo CRY2, apo CRY1, CRY1-TH301 and KL101-CRY2
(COLVAR and inputs of each stage); the seed frames of those production runs were selected from them.

## CRY2-TH301 (`CRY2_TH301/`)

| Run folder | Description | chi1 / chi2 at t = 0 (deg) | Start structure |
|---|---|---|---|
| `run1_OUT_seed_960ps` | Run 1 (OUT seed, 960 ps) | -169.95 / -76.94 | npt.gro (within 0.01 rad) |
| `run2_transition_seed_11550ps` | Run 2 (transition seed, 11550 ps) | -116.83 / +5.86 | em2.gro (within 0.01 rad) |
| `run3_IN_seed_13870ps` | Run 3 (IN seed, 13870 ps) | +175.97 / +107.82 | npt.gro (within 0.01 rad) |

- `run1_OUT_seed_960ps`: em1 (ring carbons free), em2, 100 ps NVT + 100 ps NPT (protein and ligand heavy atoms restrained, new 300 K velocities), then 500 ns WT-MetaD from npt.gro/npt.cpt (md.mdp).
- `run2_transition_seed_11550ps`: em1 and em2 with W417 chi1/chi2 restrained to the seed values (topol.top #ifdef DIHRES_W417, -DDIHRES_W417 in em1.mdp/em2.mdp); no NVT/NPT; 500 ns WT-MetaD started from em2.gro with new 300 K velocities (wtmd_from_em.mdp: continuation = no, gen_vel = yes, gen_seed = -1) and plumed_from_em.dat. nvt.mdp/npt.mdp/md.mdp/plumed.dat in this folder belong to the planned route that was not used.
- `run3_IN_seed_13870ps`: As Run 1.

## apo CRY2 (`CRY2_apo/`)

| Run folder | Description | chi1 / chi2 at t = 0 (deg) | Start structure |
|---|---|---|---|
| `earlier_single_run` | Earlier single run (original submission) | -168.66 / -70.09 | npt.gro (exact) |
| `staged1_OUT_seed_4040ps` | Staged Run 1 (OUT seed, 4040 ps of stage I) | +157.25 / -74.81 | start.gro (within 0.01 rad) |
| `staged2_transition_seed_57640ps` | Staged Run 2 (near-zero chi2 seed, 57640 ps of stage IV) | -106.02 / -0.00 | start.gro (within 0.01 rad) |
| `staged3_IN_seed_80480ps` | Staged Run 3 (IN seed, 80480 ps of stage III) | -37.85 / +94.17 | start.gro (within 0.01 rad) |
| `unstaged_IN_cMD_455760ps` | Unstaged run from an IN frame of unbiased MD (455.76 ns) | -157.90 / +71.31 | seed_apo_unbiased_in_455760ps.gro (within 0.01 rad) |
| `unstaged_OUT_cMD_201820ps` | Unstaged run from an OUT frame of unbiased MD (201.82 ns) | -172.01 / -56.26 | npt.gro (within 0.01 rad) |

## apo CRY1 (`CRY1_apo/`)

| Run folder | Description | chi1 / chi2 at t = 0 (deg) | Start structure |
|---|---|---|---|
| `earlier_single_run` | Earlier single run (original submission) | +179.50 / -74.66 | npt.gro (within 0.01 rad) |
| `staged1_OUT_seed_3980ps` | Staged Run 1 (OUT seed, 3980 ps) | +160.02 / -75.60 | start.gro (within 0.01 rad) |
| `staged2_transition_seed_20060ps` | Staged Run 2 (near-zero chi2 seed, 20060 ps) | +70.71 / +0.47 | start.gro (within 0.01 rad) |
| `staged3_IN_seed_79690ps` | Staged Run 3 (IN seed, 79690 ps) | +54.09 / +94.05 | start.gro (within 0.01 rad) |

## CRY1-TH301 (`CRY1_TH301/`)

| Run folder | Description | chi1 / chi2 at t = 0 (deg) | Start structure |
|---|---|---|---|
| `primary1_IN_seed_2530ps` | Primary Run 1 (IN seed, 2530 ps) | -152.18 / +94.63 | conf.gro (exact) |
| `primary2_transition_seed_24710ps` | Primary Run 2 (near-zero chi2 seed, 24710 ps) | -164.41 / +0.60 | conf.gro (exact) |
| `primary3_OUT_seed_113160ps` | Primary Run 3 (OUT seed, 113160 ps) | +98.41 / -77.17 | conf.gro (exact) |
| `validation1_transition_seed_93110ps` | Second seed set Run 1 (near-zero chi2 seed, 93110 ps) | +128.17 / +0.48 | conf.gro (within 0.01 rad) |
| `validation2_OUT_seed_66070ps` | Second seed set Run 2 (OUT seed, 66070 ps) | +158.00 / -77.90 | conf.gro (within 0.01 rad) |
| `validation3_IN_seed_166600ps` | Second seed set Run 3 (IN seed, 166600 ps) | -145.25 / +94.45 | conf.gro (within 0.01 rad) |

- `primary1_IN_seed_2530ps`: md.mdp is the shared production file of CRY1/CRY1_WTMD (the run folder has none).

## KL101-CRY2 (DiffDock pose; response letter) (`CRY2_KL101/`)

| Run folder | Description | chi1 / chi2 at t = 0 (deg) | Start structure |
|---|---|---|---|
| `run1_OUT_seed_570ps` | Run 1 (OUT seed, 570 ps) | -151.56 / -75.69 | KL_md_01_570ps.gro (within 0.01 rad) |
| `run2r_IN_seed_41060ps` | Run 2r (IN seed, 41060 ps) | -163.35 / +94.58 | KL_md_02r_41060ps.gro (within 0.01 rad) |
| `run3r_transition_seed_93060ps` | Run 3r (near-zero chi2 seed, 93060 ps) | -67.96 / -0.30 | KL_md_03r_93060ps.gro (within 0.01 rad) |
