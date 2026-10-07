"""reproduce_per_run.py - per-run dG(IN - OUT) of every WT-MetaD production run in this repository.

Usage (from the repository root or from this folder; needs numpy and pandas):
    python Analysis/tp_reweighting/reproduce_per_run.py            # all runs
    python Analysis/tp_reweighting/reproduce_per_run.py CRY2_apo   # runs whose folder contains this text

For each run folder (any folder holding a SOURCE.json with a 7-column HILLS*.gz) it rebuilds the
bias from HILLS, reweights the raw COLVAR rows and writes one row to
tables/reproduced/per_run_TP_from_repository.csv:
  - dG_chi2_1ps_d100   chi2 = 0 partition, every COLVAR row (1 ps), first 100 ns discarded (Methods)
  - jk50_SE_1ps        50 ns block jackknife SE of that value (blocks over 100 ns - end)
  - dG_rotamer_1ps_d100  canonical rotamer cores instead of the chi2 = 0 partition
  - dG_chi2_10ps_d100  the same as the first column on 10 ps frames only (the spacing of the
                       original-submission analysis files)
  - dG_chi2_1ps_d0 / _d200   0 and 200 ns discards (sensitivity)
Runtime: about 1-2 minutes per run.
"""
import csv
import glob
import gzip
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tp_lib as TP  # noqa: E402

REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, 'tables', 'reproduced')


def run_folders():
    for sj in sorted(glob.glob(os.path.join(REPO, '**', 'SOURCE.json'), recursive=True)):
        d = os.path.dirname(sj)
        info = json.load(open(sj, encoding='utf-8'))
        if 'run' not in info:
            continue                       # seed-chain stages
        hills = [f for f in glob.glob(os.path.join(d, 'HILLS*.gz'))]
        colv = [f for f in glob.glob(os.path.join(d, 'COLVAR*.gz')) if 'REWEIGHT' not in os.path.basename(f)]
        if not colv:
            colv = [f for f in glob.glob(os.path.join(d, 'COLVAR*REWEIGHT*.gz'))]
        if len(hills) != 1 or len(colv) != 1:
            continue
        with gzip.open(hills[0], 'rt') as fh:
            head = fh.readline().strip()
        if head.split()[2:5] != ['time', 'chi1', 'chi2']:
            print(f'skip {os.path.relpath(d, REPO)}: HILLS fields "{head}" (not a chi1/chi2 run)')
            continue
        yield d, info, hills[0], colv[0]


def one(d, info, hp, cp):
    ht, hx, hy, hh, sig, hinfo = TP.read_hills(hp)
    ft, fx, fy, cinfo = TP.read_colvar(cp)
    scale = 1.0
    if ft.max() < 0.5 * ht.max():
        # A PLUMED-driver COLVAR may give the time in frame units (10 ps per frame); rescale only when unambiguous.
        scale = ht.max() / ft.max()
        if abs(scale - 10.0) > 1e-6:
            raise ValueError(f'{cp}: COLVAR ends at {ft.max()} but HILLS at {ht.max()}')
        ft = ft * scale
    V, c, _, _, _ = TP.reconstruct(ht, hx, hy, hh, sig, ft, fx, fy)
    rb = V - c
    res = dict(run_folder=os.path.relpath(d, REPO).replace('\\', '/'), system=info['system'], label=info['label'],
               hills=os.path.basename(hp), colvar=os.path.basename(cp), colvar_rows=cinfo['n_rows'],
               t_last_ps=float(ft.max()), colvar_time_scale=scale)
    sel = ft >= 100000.0

    def est(s):
        return TP.dG_tp(ft[s], fy[s], rb[s]) if s.sum() >= 100 else float('nan')

    res['dG_chi2_1ps_d100'] = TP.dG_tp(ft, fy, rb, lo=100000.0)
    res['jk50_SE_1ps'] = TP.jackknife(ft, sel, est, TP.blocks(100000.0, float(ft.max()), 50000.0))
    mout, minn, _, _ = TP.masks(fx, fy)
    res['dG_rotamer_1ps_d100'] = TP.dG_ratio(rb / TP.KT_KJ, minn, mout, sel)
    k10 = np.isclose(np.mod(ft, 10.0), 0.0)
    res['dG_chi2_10ps_d100'] = TP.dG_tp(ft[k10], fy[k10], rb[k10], lo=100000.0)
    res['dG_chi2_1ps_d0'] = TP.dG_tp(ft, fy, rb, lo=0.0)
    res['dG_chi2_1ps_d200'] = TP.dG_tp(ft, fy, rb, lo=200000.0)
    return res


def main():
    only = sys.argv[1:]
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for d, info, hp, cp in run_folders():
        rel = os.path.relpath(d, REPO)
        if only and not any(o in rel for o in only):
            continue
        t0 = time.time()
        r = one(d, info, hp, cp)
        rows.append(r)
        print(f"{r['run_folder']:70s} dG {r['dG_chi2_1ps_d100']:+.3f} +/- {r['jk50_SE_1ps']:.3f}  "
              f"(10 ps {r['dG_chi2_10ps_d100']:+.3f})  {time.time() - t0:.0f} s", flush=True)
    name = 'per_run_TP_from_repository.csv' if not only else 'per_run_TP_from_repository_%s.csv' % '_'.join(only)
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: ('%.4f' % v if isinstance(v, float) else v) for k, v in r.items()})
    print('wrote', os.path.join(OUT, name))


if __name__ == '__main__':
    main()
