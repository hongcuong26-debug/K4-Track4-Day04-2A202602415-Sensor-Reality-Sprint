"""CLI runner for the fully synthetic Sensor Reality Sprint benchmark."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time

import numpy as np
import pandas as pd
import yaml

from .compensation import compensate_positions
from .metrics import association_swap_rate, mean_position_error, theory_error
from .plots import plot_compensation, plot_s1, plot_s2, plot_s3, plot_timeline
from .scenarios import s1_position, s2_position, s3_positions
from .sensors import camera_measure, lidar_measure


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "UNKNOWN"


def rng_pair(seed: int) -> tuple[np.random.Generator, np.random.Generator]:
    ss = np.random.SeedSequence(seed)
    a, b = ss.spawn(2)
    return np.random.default_rng(a), np.random.default_rng(b)


def run_s1(cfg: dict, t: np.ndarray, period: float) -> list[dict]:
    rows = []
    sigma_c, sigma_l = cfg["simulation"]["sigma_cam_m"], cfg["simulation"]["sigma_lidar_m"]
    for v in cfg["scenarios"]["S1"]["v_rel_mps"]:
        fn = lambda x, v=v: s1_position(x, float(v))
        for dt_ms in cfg["simulation"]["offsets_ms"]:
            dt = dt_ms / 1000.0
            for seed in cfg["simulation"]["seeds"]:
                rc, rl = rng_pair(int(seed)); cam = camera_measure(fn, t, sigma_c, rc); lid = lidar_measure(fn, t, dt, sigma_l, rl)
                truth = fn(t); valid = t >= dt
                exact = compensate_positions(lid, period, dt)
                minus = compensate_positions(lid, period, max(0.0, dt - 0.020))
                plus = compensate_positions(lid, period, dt + 0.020)
                th = theory_error(float(v), dt)
                rows.append(dict(data_kind="synthetic",scenario="S1",v_rel_mps=float(v),accel_mps2=np.nan,d_gap_m=np.nan,seed=int(seed),dt_ms=int(dt_ms),pos_error_m=mean_position_error(lid,truth,valid),theory_error_m=th,approx_gap_m=mean_position_error(lid,truth,valid)-th,assoc_swap_rate_pct=np.nan,residual_error_exact_m=mean_position_error(exact,truth,valid),residual_error_minus20_m=mean_position_error(minus,truth,valid),residual_error_plus20_m=mean_position_error(plus,truth,valid)))
    return rows


def run_s2(cfg: dict, t: np.ndarray, period: float) -> list[dict]:
    rows = []; sigma_l = cfg["simulation"]["sigma_lidar_m"]
    for v in cfg["scenarios"]["S2"]["v_rel_mps"]:
        for a in cfg["scenarios"]["S2"]["accel_mps2"]:
            fn = lambda x, v=v, a=a: s2_position(x, float(v), float(a))
            for dt_ms in cfg["simulation"]["offsets_ms"]:
                dt = dt_ms/1000.0
                for seed in cfg["simulation"]["seeds"]:
                    _, rl = rng_pair(int(seed)); lid = lidar_measure(fn,t,dt,sigma_l,rl); truth=fn(t); valid=t>=dt
                    exact=compensate_positions(lid,period,dt); minus=compensate_positions(lid,period,max(0,dt-.020)); plus=compensate_positions(lid,period,dt+.020)
                    th=theory_error(float(v),dt); pe=mean_position_error(lid,truth,valid)
                    rows.append(dict(data_kind="synthetic",scenario="S2",v_rel_mps=float(v),accel_mps2=float(a),d_gap_m=np.nan,seed=int(seed),dt_ms=int(dt_ms),pos_error_m=pe,theory_error_m=th,approx_gap_m=pe-th,assoc_swap_rate_pct=np.nan,residual_error_exact_m=mean_position_error(exact,truth,valid),residual_error_minus20_m=mean_position_error(minus,truth,valid),residual_error_plus20_m=mean_position_error(plus,truth,valid)))
    return rows


def run_s3(cfg: dict, t: np.ndarray, period: float) -> list[dict]:
    rows=[]; sigma_c=cfg["simulation"]["sigma_cam_m"]; sigma_l=cfg["simulation"]["sigma_lidar_m"]; v=float(cfg["scenarios"]["S3"]["v_rel_mps"])
    for gap in cfg["scenarios"]["S3"]["d_gap_m"]:
        fn=lambda x,gap=gap: s3_positions(x,v,float(gap))
        for dt_ms in cfg["simulation"]["offsets_ms"]:
            dt=dt_ms/1000.0
            for seed in cfg["simulation"]["seeds"]:
                rc,rl=rng_pair(int(seed)); cam=camera_measure(fn,t,sigma_c,rc); lid=lidar_measure(fn,t,dt,sigma_l,rl); truth=fn(t); valid=t>=dt
                rows.append(dict(data_kind="synthetic",scenario="S3",v_rel_mps=v,accel_mps2=np.nan,d_gap_m=float(gap),seed=int(seed),dt_ms=int(dt_ms),pos_error_m=mean_position_error(lid[valid],truth[valid]),theory_error_m=theory_error(v,dt),approx_gap_m=mean_position_error(lid[valid],truth[valid])-theory_error(v,dt),assoc_swap_rate_pct=association_swap_rate(cam[valid],lid[valid]),residual_error_exact_m=np.nan,residual_error_minus20_m=np.nan,residual_error_plus20_m=np.nan))
    return rows


def write_summary(df: pd.DataFrame, cfg: dict, path: Path) -> None:
    lines=["# Synthetic benchmark summary","","All values below were generated automatically from the synthetic benchmark. No real-sensor measurements are claimed.",""]
    lines += ["## S1 baseline vs temporal offset","","| v_rel (m/s) | Δt (ms) | pos_error mean ± std (m) | theory vΔt (m) |","|---:|---:|---:|---:|"]
    s1=df[df.scenario=="S1"]
    for (v,dt),g in s1.groupby(["v_rel_mps","dt_ms"]): lines.append(f"| {v:g} | {dt:d} | {g.pos_error_m.mean():.4f} ± {g.pos_error_m.std():.4f} | {g.theory_error_m.mean():.4f} |")
    lines += ["","## First offset above group reference threshold","",f"Reference threshold: pos_error > {cfg['thresholds']['pos_error_concern_m']:.2f} m (group assumption, not an industry standard).",""]
    for v,g in s1.groupby("v_rel_mps"):
        means=g.groupby("dt_ms").pos_error_m.mean(); hits=means[means>cfg["thresholds"]["pos_error_concern_m"]]
        lines.append(f"- v_rel={v:g} m/s: {int(hits.index[0]) if len(hits) else 'not reached'} ms")
    lines += ["","## S2 braking approximation gap","","| v_rel | accel | Δt | mean pos_error (m) | mean approx_gap (m) |","|---:|---:|---:|---:|---:|"]
    s2=df[df.scenario=="S2"]
    for (v,a,dt),g in s2.groupby(["v_rel_mps","accel_mps2","dt_ms"]): lines.append(f"| {v:g} | {a:g} | {dt:d} | {g.pos_error_m.mean():.4f} | {g.approx_gap_m.mean():.4f} |")
    lines += ["","## S3 association swap rate","","| d_gap (m) | Δt (ms) | mean swap rate (%) |","|---:|---:|---:|"]
    s3=df[df.scenario=="S3"]
    for (gap,dt),g in s3.groupby(["d_gap_m","dt_ms"]): lines.append(f"| {gap:g} | {dt:d} | {g.assoc_swap_rate_pct.mean():.2f} |")
    lines += ["","## Figures","","- [S1 error vs Δt](../figs/s1_error_vs_dt.png)","- [S2 approximation gap](../figs/s2_approx_gap.png)","- [S3 association heatmap](../figs/s3_assoc_heatmap.png)","- [Timeline example](../figs/timeline_example.png)","- [Compensation bar](../figs/compensation_bar.png)",""]
    path.write_text("\n".join(lines),encoding="utf-8")


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--config",required=True); args=p.parse_args(); start=time.time()
    cfg=yaml.safe_load(Path(args.config).read_text(encoding="utf-8")); root=Path(__file__).resolve().parents[2]
    for d in (root/"results",root/"figs",root/"logs"): d.mkdir(exist_ok=True)
    period=1.0/float(cfg["simulation"]["lidar_hz"]); duration=float(cfg["simulation"]["duration_s"]); t=np.arange(0.0,duration,period)
    rows=run_s1(cfg,t,period)+run_s2(cfg,t,period)+run_s3(cfg,t,period); df=pd.DataFrame(rows); df.to_csv(root/"results/results.csv",index=False)
    plot_s1(df,root/"figs/s1_error_vs_dt.png"); plot_s2(df,root/"figs/s2_approx_gap.png"); plot_s3(df,root/"figs/s3_assoc_heatmap.png"); plot_compensation(df,root/"figs/compensation_bar.png")
    rc,_=rng_pair(0); fn=lambda x:s1_position(x,10.0); cam=camera_measure(fn,t,0.0,rc); lid=lidar_measure(fn,t,0.150,0.0,np.random.default_rng(1)); plot_timeline(t,cam[:,0],lid[:,0],root/"figs/timeline_example.png")
    write_summary(df,cfg,root/"results/summary.md")
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"); runtime=time.time()-start
    log={"data_kind":"synthetic","config":cfg,"seeds":cfg["simulation"]["seeds"],"git_commit":git_commit(),"runtime_seconds":runtime,"generated_utc":stamp}
    (root/"logs"/f"run_{stamp}.log").write_text(json.dumps(log,indent=2),encoding="utf-8")
    print(f"Synthetic benchmark complete: {len(df)} rows in {runtime:.2f}s")

if __name__ == "__main__": main()
