# Structures

## `homology_models/`

| File | Contents |
|---|---|
| `CRY2_HM.pdb` | human CRY2 photolyase-homology region (SWISS-MODEL, template: the CRY2 chain of mouse 4I6J), numbered as mouse CRY2: residues 21-527 (human 22-528), W417 = human W418 |
| `CRY2_TH301.pdb` | the same model with TH301 transferred from 6KX8 by superposition. The ligand has all 57 atoms of TH301 (residue DYX) |

## `seed_structures/CRY2_TH301_57atom/`

These are six seed frames of the CRY2-TH301 complex: the three seeds of the production runs in
`simulations/CRY2_TH301/` and three further seeds. Each file has 148,893 atoms with coordinates only, and matches
`topology/CRY2_TH301_57atom_complex/topol.top`.

| File | Seed time | W417 chi1 / chi2 (deg) | Region |
|---|---|---|---|
| `CRY2_TH301_57atom_primary1_960ps.gro` | 960 ps | -161.85 / -75.77 | OUT |
| `CRY2_TH301_57atom_primary2_11550ps.gro` | 11550 ps | -116.35 / +2.17 | near-zero chi2 |
| `CRY2_TH301_57atom_primary3_13870ps.gro` | 13870 ps | +174.54 / +94.77 | IN |
| `CRY2_TH301_57atom_val1_73660ps.gro` | 73660 ps | -73.54 / +0.08 | near-zero chi2 |
| `CRY2_TH301_57atom_val2_97240ps.gro` | 97240 ps | -136.84 / +94.37 | IN |
| `CRY2_TH301_57atom_val3_86660ps.gro` | 86660 ps | +169.89 / -77.02 | OUT |

**How they were made.** The frames were taken from the steered seeding chain of the CRY2 complex. That chain was
run with an earlier ligand model, so the ligand of each frame was rebuilt as TH301 (`topology/TH301_57atom/`):
- the 33 heavy atoms keep their frame coordinates;
- all 24 hydrogens were added with RDKit (C-H 1.09 A, N-H 1.01 A);
- protein, water, ions and box are unchanged.

`independent_check.txt` checks every file against the topology (atom order and count) and against its source frame
(protein, solvent, box and W417 torsions unchanged).

**Before MD.** One ring C-C bond of the rebuilt TH301 (C13-C14) is 1.29-1.36 A in these frames, against 1.548 A in
the topology, so each structure must be minimised first. The production runs used two steps:
- em1 with protein and ligand heavy atoms restrained except the five ring carbons (`-DPOSRES -DPOSRES_LIG_RINGFREE`);
- em2 without position restraints.

For the near-zero-chi2 seed primary2, W417 chi1/chi2 were also restrained to their seed values during both steps.
Without that restraint the side chain slid off the barrier during minimisation; the same is likely needed for val1.
See `simulations/CRY2_TH301/*/SOURCE.json`.
