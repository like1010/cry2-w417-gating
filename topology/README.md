# Topologies

Every run folder under `simulations/` carries the exact topology it was run with (`topol.top.gz` plus the `.itp`
files it includes). This folder holds the ligand parameters and the CRY2-TH301 complex topology for new work.

| Folder | Contents |
|---|---|
| `TH301_57atom/` | `DYX_smiles_GMX.itp` (md5 `38fe05ce2536d102feae61234dd1ebd7`): TH301, 57 atoms, C24H24ClN3O4S, GAFF2 + AM1-BCC, net charge 0. `acpype/` holds the ACPYPE 2022.7.21 record: input SMILES and command in `acpype.log`, the AM1-BCC mol2, frcmod, prmtop/inpcrd, sqm input/output, and acpype's own `posre_DYX_smiles.itp`. The CRY1-TH301 and CRY2-TH301 runs use this file. |
| `CRY2_TH301_57atom_complex/` | `topol.top` for the human CRY2 homology model with TH301 (protein 8196 atoms, TH301 57, 46877 TIP3P waters, 9 Cl-; 148,893 atoms), with `posre.itp` (protein), `posre_DYX_smiles.itp` (all 33 TH301 heavy atoms, `-DPOSRES_LIG`) and `posre_DYX_smiles_ringfree.itp` (heavy atoms except the five ring carbons, `-DPOSRES_LIG_RINGFREE`). It matches the six seed structures in `Structures/seed_structures/CRY2_TH301_57atom/`. |
| `KL101/` | `KL101_GAFF2.itp` and `ligand_atomtypes.itp` of the KL101-CRY2 runs. |

TH301 SMILES used by ACPYPE: `COc1ccc(cc1)n1nc2c(c1NC(=O)[C@]1(CCCC1)c1ccc(cc1)Cl)CS(=O)(=O)C2`.
