"""Plot generation for the synthetic benchmark."""
from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_s1(df: pd.DataFrame, out: Path) -> None:
    sub = df[df.scenario == "S1"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for v, g in sub.groupby("v_rel_mps"):
        agg = g.groupby("dt_ms").pos_error_m.agg(["mean", "std"]).reset_index()
        ax.errorbar(agg.dt_ms, agg["mean"], yerr=agg["std"], marker="o", label=f"synthetic v_rel={v:g} m/s")
        x = np.array(sorted(agg.dt_ms.unique()))
        ax.plot(x, v * x / 1000.0, linestyle="--", label=f"theory {v:g} m/s")
    ax.set_xlabel("Time offset Δt (ms)")
    ax.set_ylabel("Mean position error (m)")
    ax.set_title("S1 synthetic position error vs time offset")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out, dpi=160); plt.close(fig)


def plot_s2(df: pd.DataFrame, out: Path) -> None:
    sub = df[df.scenario == "S2"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for (v, a), g in sub.groupby(["v_rel_mps", "accel_mps2"]):
        agg = g.groupby("dt_ms")[["pos_error_m", "theory_error_m"]].mean().reset_index()
        ax.plot(agg.dt_ms, agg.pos_error_m, marker="o", label=f"observed v={v:g}, a={a:g}")
        ax.plot(agg.dt_ms, agg.theory_error_m, linestyle="--", label=f"vΔt v={v:g}")
    ax.set_xlabel("Time offset Δt (ms)"); ax.set_ylabel("Position error (m)")
    ax.set_title("S2 constant acceleration: observed vs initial vΔt")
    ax.grid(True, alpha=0.3); ax.legend(fontsize=7, ncol=2)
    fig.tight_layout(); fig.savefig(out, dpi=160); plt.close(fig)


def plot_s3(df: pd.DataFrame, out: Path) -> None:
    sub = df[df.scenario == "S3"]
    pivot = sub.groupby(["d_gap_m", "dt_ms"]).assoc_swap_rate_pct.mean().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    im = ax.imshow(pivot.values, aspect="auto", origin="lower")
    ax.set_xticks(range(len(pivot.columns)), [f"{int(x)} ms" for x in pivot.columns])
    ax.set_yticks(range(len(pivot.index)), [f"{x:g} m" for x in pivot.index])
    ax.set_xlabel("Time offset Δt"); ax.set_ylabel("Target gap d_gap")
    ax.set_title("S3 synthetic nearest-neighbor association swap rate (%)")
    fig.colorbar(im, ax=ax, label="Swap rate (%)")
    fig.tight_layout(); fig.savefig(out, dpi=160); plt.close(fig)


def plot_timeline(t: np.ndarray, camera_x: np.ndarray, lidar_x: np.ndarray, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(t, camera_x, label="synthetic camera at t")
    ax.plot(t, lidar_x, label="synthetic LiDAR stamped t, sampled t−150 ms")
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Longitudinal position x (m)")
    ax.set_title("Synthetic timeline example: v_rel=10 m/s, Δt=150 ms")
    ax.grid(True, alpha=0.3); ax.legend(); fig.tight_layout(); fig.savefig(out, dpi=160); plt.close(fig)


def plot_compensation(df: pd.DataFrame, out: Path) -> None:
    sub = df[(df.scenario == "S1") & (df.dt_ms > 0)]
    agg = sub.groupby("dt_ms")[["pos_error_m", "residual_error_exact_m", "residual_error_minus20_m", "residual_error_plus20_m"]].mean()
    x = np.arange(len(agg)); width = 0.2
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.bar(x - 1.5*width, agg.pos_error_m, width, label="before")
    ax.bar(x - 0.5*width, agg.residual_error_exact_m, width, label="comp exact Δt")
    ax.bar(x + 0.5*width, agg.residual_error_minus20_m, width, label="comp Δt−20 ms")
    ax.bar(x + 1.5*width, agg.residual_error_plus20_m, width, label="comp Δt+20 ms")
    ax.set_xticks(x, [f"{int(v)} ms" for v in agg.index])
    ax.set_xlabel("True time offset Δt"); ax.set_ylabel("Mean position error (m)")
    ax.set_title("Synthetic S1 compensation (mean over 5, 10, 20 m/s)")
    ax.legend(fontsize=8); ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(out, dpi=160); plt.close(fig)
