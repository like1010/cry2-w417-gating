"""compare_with_reported.py - compare tables/reproduced/per_run_TP_from_repository.csv with the
values reported in the manuscript, Supporting Information and response letter
(tables/reported/reported_TP_per_run.csv). Writes tables/reproduced/comparison_with_reported.csv.

Runs reported on 10 ps frames are compared with the 10 ps column. Their reported values came from
PLUMED-driver bias files, so small differences (a few thousandths of a kcal/mol) are expected, because
the bias here is rebuilt from HILLS instead.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))


def main():
    rep = {r['run_folder']: r for r in csv.DictReader(open(os.path.join(REPO, 'tables', 'reported',
                                                                         'reported_TP_per_run.csv'), encoding='utf-8'))}
    got = {r['run_folder']: r for r in csv.DictReader(open(os.path.join(REPO, 'tables', 'reproduced',
                                                                         'per_run_TP_from_repository.csv'), encoding='utf-8'))}
    out = []
    for k, r in rep.items():
        g = got.get(k)
        if g is None:
            out.append(dict(run_folder=k, reported_dG=r['reported_dG'], reproduced_dG='', difference='',
                            reported_SE=r['reported_SE'], reproduced_SE='', frame_spacing_ps=r['frame_spacing_ps'],
                            note='not reproduced (run missing)'))
            continue
        col = 'dG_chi2_10ps_d100' if r['frame_spacing_ps'] == '10' else 'dG_chi2_1ps_d100'
        d = float(g[col]) - float(r['reported_dG'])
        out.append(dict(run_folder=k, reported_dG=r['reported_dG'], reproduced_dG='%+.3f' % float(g[col]),
                        difference='%+.3f' % d, reported_SE=r['reported_SE'],
                        reproduced_SE='%.3f' % float(g['jk50_SE_1ps']), frame_spacing_ps=r['frame_spacing_ps'],
                        note=r['source']))
    p = os.path.join(REPO, 'tables', 'reproduced', 'comparison_with_reported.csv')
    with open(p, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    for o in out:
        print(f"{o['run_folder']:75s} reported {o['reported_dG']:>7s}  reproduced {o['reproduced_dG']:>7s}  "
              f"diff {o['difference']:>7s}  ({o['frame_spacing_ps']} ps)")
    diffs = [abs(float(o['difference'])) for o in out if o['difference']]
    print(f'{len(diffs)} of {len(out)} compared; max |difference| {max(diffs):.3f} kcal/mol')
    print('wrote', p)


if __name__ == '__main__':
    main()
