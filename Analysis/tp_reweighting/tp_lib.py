"""tp_lib.py - Tiwary-Parrinello reweighting of the W417 / W399 chi1-chi2 WT-MetaD runs.

The functions below are the ones that produced the reported per-run values, copied without
changes in the arithmetic from the authors' analysis code:
  - read_hills, read_colvar, reconstruct, masks, dG_ratio: scripts/B3_B11_tp_reweight.py
  - dG_tp: scripts/A1_unify_free_energies.py
  - blocks, jackknife: scripts/revision_2026-10-06/CX18_rerun_readout.py
The only change is that the readers accept gzip files (.gz), as stored in this repository.

Method (Tiwary & Parrinello, J. Phys. Chem. B 2015, 119, 736).
  - The bias V(s, t) is rebuilt from the run's own HILLS on a periodic 360 x 360 grid
    (stretched-Gaussian kernels with the PLUMED cutoff, FFT convolution), c(t) every 100 ps.
  - Each COLVAR frame gets the bias of the hills deposited strictly before it, then the
    weight exp[(V - c(t)) / kT].
  - dG(IN - OUT) = -kT ln(P_IN / P_OUT), with IN = chi2 > 0 and OUT = chi2 < 0 over all chi1,
    or with the canonical rotamer cores (|chi1| > 150 deg; OUT -120 < chi2 < -55 deg,
    IN 60 < chi2 < 120 deg).
"""
import gzip
import io

import numpy as np
import pandas as pd

KT = 8.314462618e-3 * 300.0          # 2.494339 kJ/mol
BETA = 1.0 / KT
KT_KJ = KT
KJ2KCAL = 1.0 / 4.184
KT_KCAL = KT * KJ2KCAL
A_STR, B_STR, DP2 = 1.00193418799744762, -0.00193418799744762, 6.25   # PLUMED stretched Gaussian, cutoff 6.25
NG = 360
DTCHK = 100.0
G = 10.0                              # bias factor of every production run (checked against HILLS in read_hills)


def slurp(path):
    with open(path, 'rb', buffering=1 << 23) as f:
        raw = f.read()
    return gzip.decompress(raw) if path.endswith('.gz') else raw


def read_table(path, ncol):
    return pd.read_csv(io.BytesIO(slurp(path)), sep=r'\s+', comment='#', header=None,
                       usecols=list(range(ncol)), dtype=np.float64, engine='c').values


def read_hills(path):
    d = read_table(path, 7)
    nzero = int((d[:, 5] == 0.0).sum())
    d = d[d[:, 5] != 0.0]
    d = d[np.argsort(d[:, 0], kind='stable')]
    t = d[:, 0]
    biasf = sorted(set(map(float, d[:, 6])))
    if biasf != [G]:
        raise ValueError(f'{path}: bias factor {biasf}, expected {G}')
    info = dict(n_hills=int(len(t)), n_zero_height_skipped=nzero, t_first=float(t[0]), t_last=float(t[-1]),
                n_dup_times=int(len(t) - len(np.unique(t))), biasf=biasf, h_first=float(d[0, 5]))
    return t, d[:, 1].copy(), d[:, 2].copy(), d[:, 5].copy(), (float(d[0, 3]), float(d[0, 4])), info


def read_colvar(path):
    d = read_table(path, 3)
    t = d[:, 0]
    _, first = np.unique(t, return_index=True)     # drop duplicated times (restarts), keep the first
    ndup = len(t) - len(first)
    d = d[np.sort(first)]
    d = d[np.argsort(d[:, 0], kind='stable')]
    return d[:, 0].copy(), d[:, 1].copy(), d[:, 2].copy(), dict(n_rows_raw=int(len(t)), n_dup_dropped=int(ndup),
                                                                n_rows=int(len(d)))


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def kexact(dx, dy, sig):
    dp2 = 0.5 * ((dx / sig[0]) ** 2 + (dy / sig[1]) ** 2)
    return np.where(dp2 < DP2, A_STR * np.exp(-dp2) + B_STR, 0.0)


def kernel_fft(sig):
    d = 2 * np.pi / NG
    off = np.fft.fftfreq(NG) * NG * d
    X, Y = np.meshgrid(off, off, indexing='xy')   # [iy, ix]
    return np.fft.rfft2(kexact(X, Y, sig))


def bilinear(V, x, y):
    d = 2 * np.pi / NG
    u = (x + np.pi) / d
    v = (y + np.pi) / d
    i0 = np.floor(u).astype(int)
    j0 = np.floor(v).astype(int)
    fu = u - i0
    fv = v - j0
    i0 %= NG
    j0 %= NG
    i1 = (i0 + 1) % NG
    j1 = (j0 + 1) % NG
    return ((1 - fu) * (1 - fv) * V[j0, i0] + fu * (1 - fv) * V[j0, i1]
            + (1 - fu) * fv * V[j1, i0] + fu * fv * V[j1, i1])


def c_of(V):
    a1 = BETA * G / (G - 1.0) * V
    a2 = BETA / (G - 1.0) * V
    m1 = a1.max()
    m2 = a2.max()
    return KT * (m1 + np.log(np.exp(a1 - m1).sum()) - m2 - np.log(np.exp(a2 - m2).sum()))


def reconstruct(ht, hx, hy, hh, sig, ft, fx, fy):
    """Running V at frames (strictly earlier hills) and c(t) at frames."""
    d = 2 * np.pi / NG
    ix = np.rint((hx + np.pi) / d).astype(int) % NG
    iy = np.rint((hy + np.pi) / d).astype(int) % NG
    Kf = kernel_fft(sig)
    acc = np.zeros((NG, NG))
    fac = (G - 1.0) / G
    tmax = max(ht.max(), ft.max())
    chk = np.arange(0.0, tmax + DTCHK + 1e-9, DTCHK)
    cchk = np.zeros(len(chk))
    Vf = np.zeros(len(ft))
    p = 0
    Vgrid_last = None
    for k in range(len(chk)):
        t0 = chk[k]
        q = np.searchsorted(ht, t0, side='left')      # hills with t_j < t0
        if q > p:
            np.add.at(acc, (iy[p:q], ix[p:q]), hh[p:q])
            p = q
        V = fac * np.fft.irfft2(np.fft.rfft2(acc) * Kf, s=(NG, NG))
        cchk[k] = c_of(V)
        if k == len(chk) - 1:
            Vgrid_last = V
            break
        t1 = chk[k + 1]
        fa = np.searchsorted(ft, t0, side='left')
        fb = np.searchsorted(ft, t1, side='left')
        if fb > fa:
            Vh = bilinear(V, fx[fa:fb], fy[fa:fb])
            q2 = np.searchsorted(ht, t1, side='left')
            if q2 > q:
                dx = wrap(fx[fa:fb, None] - hx[None, q:q2])
                dy = wrap(fy[fa:fb, None] - hy[None, q:q2])
                K = kexact(dx, dy, sig)
                K *= (ht[None, q:q2] < ft[fa:fb, None])
                Vh = Vh + fac * (K * hh[None, q:q2]).sum(axis=1)
            Vf[fa:fb] = Vh
    cf = np.interp(ft, chk, cchk)
    return Vf, cf, chk, cchk, Vgrid_last


def masks(x, y):
    xd = np.degrees(x)
    yd = np.degrees(y)
    core = np.abs(xd) > 150.0
    mout = core & (yd > -120.0) & (yd < -55.0)
    minn = core & (yd > 60.0) & (yd < 120.0)
    return mout, minn, (yd > 0), (yd < 0)


def dG_ratio(lw, a, b, sel):
    """-kT ln(sum_a w / sum_b w) over frames in sel, kcal/mol (rotamer-window estimate: a = IN, b = OUT)."""
    s = sel
    if not s.any():
        return np.nan
    m = lw[s].max()
    w = np.exp(lw - m)
    wa = w[a & s].sum()
    wb = w[b & s].sum()
    if wa <= 0 or wb <= 0:
        return np.nan
    return float(-KT_KCAL * np.log(wa / wb))


def dG_tp(t, c2, rb, lo=None, hi=None):
    """dG(IN - OUT) in kcal/mol with IN = chi2 > 0, OUT = chi2 < 0; rb = V - c(t) in kJ/mol."""
    m = np.ones(len(t), bool)
    if lo is not None:
        m &= t >= lo
    if hi is not None:
        m &= t <= hi
    if m.sum() < 100:
        return float('nan')
    w = np.exp((rb[m] - rb[m].max()) / KT_KJ)
    wi = w[c2[m] > 0].sum(); wo = w[c2[m] < 0].sum()
    if wi <= 0 or wo <= 0:
        return float('nan')
    return float(-KT_KJ * np.log(wi / wo) * KJ2KCAL)


def blocks(lo, hi, length):
    e = list(np.arange(lo, hi + 1e-6, length))
    if e[-1] < hi - 1e-6:
        e.append(hi)
    return e


def jackknife(t, sel, est, edges):
    """Leave-one-block-out jackknife standard error of est over the blocks given by edges."""
    th = []
    for k in range(len(edges) - 1):
        a, b = edges[k], edges[k + 1]
        inb = (t >= a) & ((t < b) if k < len(edges) - 2 else (t <= b))
        th.append(est(sel & ~inb))
    v = np.array(th)
    if not np.all(np.isfinite(v)):
        return float('nan')
    n = len(v)
    return float(np.sqrt((n - 1.0) / n * ((v - v.mean()) ** 2).sum()))
