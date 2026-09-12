"""
Publication-Grade Visualization Generators for 4D Cryptocurrency Systemic Risk Model.
Generates:
1. figure_crypto_dgrs_trajectory.png (Latent Crypto Stress St with 95% CIs)
2. figure_crypto_propagation_heatmaps.png (Generalized IRF Pi_1 and Pi_7 Contagion Heatmaps)
3. figure_crypto_model_comparison.png (Out-of-Sample M0-M7 BSS with 95% Bootstrap CIs and DM Significance)
4. figure_crypto_hedged_equity.png (Walk-Forward Hedged Equity Curves vs. Buy & Hold BTC)
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Clean publication theme styling
BG_DARK = "#0a0c10"
PANEL_BG = "#12161f"
TEXT_COLOR = "#e1e7f0"
CYAN_ACCENT = "#00d2ff"
GOLD_ACCENT = "#ffd166"
CRIMSON_ACCENT = "#ef476f"
GREEN_ACCENT = "#06d6a0"


def setup_style():
    plt.style.use("dark_background")
    plt.rcParams.update(
        {
            "figure.facecolor": BG_DARK,
            "axes.facecolor": PANEL_BG,
            "axes.edgecolor": "#2a3245",
            "axes.labelcolor": TEXT_COLOR,
            "xtick.color": TEXT_COLOR,
            "ytick.color": TEXT_COLOR,
            "grid.color": "#1f2638",
            "grid.linestyle": "--",
            "grid.alpha": 0.6,
            "font.family": "sans-serif",
        }
    )


def plot_crypto_dgrs_trajectory(ci_df: pd.DataFrame, output_path: str = "results/figures/figure_crypto_dgrs_trajectory.png"):
    setup_style()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 6), dpi=300)

    dates = ci_df.index
    mean = ci_df["mean"].values
    lower = ci_df["lower_95"].values
    upper = ci_df["upper_95"].values

    ax.fill_between(dates, lower, upper, color=CYAN_ACCENT, alpha=0.18, label="95% Bayesian Credible Interval")
    ax.plot(dates, mean, color=CYAN_ACCENT, linewidth=1.8, label="Latent Systemic Crypto Stress State (S_t)")
    ax.axhline(0.0, color="#6b7c96", linestyle=":", alpha=0.7)
    ax.axhline(2.0, color=CRIMSON_ACCENT, linestyle="--", linewidth=1.2, label="Acute Systemic Liquidation Threshold (+2.0σ)")

    ax.set_title("4D-MGRFF: Latent Systemic Cryptocurrency Risk Trajectory (S_t) [EM-Estimated Q]", fontsize=14, pad=15, weight="bold", color=TEXT_COLOR)
    ax.set_xlabel("Date (24/7 Daily Snapshot)", fontsize=11, labelpad=10)
    ax.set_ylabel("Standardized Latent Stress (σ)", fontsize=11, labelpad=10)
    ax.legend(loc="upper left", framealpha=0.8, facecolor=PANEL_BG, edgecolor="#2a3245")
    ax.grid(True)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_crypto_propagation_heatmaps(df_pi_1: pd.DataFrame, df_pi_7: pd.DataFrame, output_path: str = "results/figures/figure_crypto_propagation_heatmaps.png"):
    setup_style()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

    cols = list(df_pi_1.columns)
    p = len(cols)

    for idx, (df, title) in enumerate([(df_pi_1, "1-Day Generalized IRF (Π₁)"), (df_pi_7, "7-Day Generalized IRF Decay (Π₇)")]):
        ax = axes[idx]
        im = ax.imshow(df.values, cmap="coolwarm", vmin=-1.0, vmax=1.0)

        ax.set_xticks(range(p))
        ax.set_yticks(range(p))
        ax.set_xticklabels(cols, rotation=45, ha="right", fontsize=9)
        ax.set_yticklabels(cols, fontsize=9)
        ax.set_title(title, fontsize=12, pad=12, weight="bold", color=TEXT_COLOR)

        # Annotate text values
        for i in range(p):
            for j in range(p):
                val = df.values[i, j]
                color = "black" if abs(val) < 0.4 else "white"
                ax.text(j, i, f"{val:+.2f}", ha="center", va="center", color=color, fontsize=8, weight="bold")

    fig.subplots_adjust(right=0.88)
    cbar_ax = fig.add_axes([0.90, 0.20, 0.02, 0.60])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label("Generalized IRF Coefficient (Pesaran-Shin)", color=TEXT_COLOR)

    fig.suptitle("4D-MGRFF: Cross-Asset Cryptocurrency Contagion Matrices — Generalized IRF (Π_h)", fontsize=15, y=0.98, weight="bold", color=TEXT_COLOR)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_crypto_model_comparison(perf_table: pd.DataFrame, output_path: str = "results/figures/figure_crypto_model_comparison.png"):
    setup_style()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(16, 7), dpi=300)

    horizons = perf_table["Horizon"].unique()
    models = perf_table["Model"].unique()
    
    n_h = len(horizons)
    n_m = len(models)
    width = 0.8 / n_m
    x_base = np.arange(n_h)

    palette = [CYAN_ACCENT, GOLD_ACCENT, "#ff7b00", GREEN_ACCENT, "#9d4edd", CRIMSON_ACCENT, "#3a86ff", "#ffffff"]

    has_ci = "BSS_CI_Lo" in perf_table.columns and "BSS_CI_Hi" in perf_table.columns
    has_dm = "DM_vs_Clim_pval" in perf_table.columns
    has_fdr = "DM_Sig_FDR" in perf_table.columns

    for i, m in enumerate(models):
        sub = perf_table[perf_table["Model"] == m]
        y_vals = []
        y_err_lo = []
        y_err_hi = []
        sig_markers = []

        for h in horizons:
            row = sub[sub["Horizon"] == h]
            if not row.empty:
                bss = row["BSS_vs_Clim"].values[0]
                y_vals.append(bss)

                if has_ci:
                    lo = row["BSS_CI_Lo"].values[0]
                    hi = row["BSS_CI_Hi"].values[0]
                    y_err_lo.append(bss - lo)
                    y_err_hi.append(hi - bss)
                else:
                    y_err_lo.append(0)
                    y_err_hi.append(0)

                # Prioritize FDR-corrected significance if present
                if has_fdr:
                    sig_markers.append(bool(row["DM_Sig_FDR"].values[0]))
                elif has_dm:
                    pval = row["DM_vs_Clim_pval"].values[0]
                    sig_markers.append(pval < 0.05 if not np.isnan(pval) else False)
                else:
                    sig_markers.append(False)
            else:
                y_vals.append(0.0)
                y_err_lo.append(0)
                y_err_hi.append(0)
                sig_markers.append(False)
        
        pos = x_base - 0.4 + (i + 0.5) * width
        color = palette[i % len(palette)]

        if has_ci:
            ax.bar(
                pos, y_vals, width=width, label=m, color=color, alpha=0.85, edgecolor="#2a3245",
                yerr=[y_err_lo, y_err_hi], ecolor="#aaaaaa", capsize=2, error_kw={"linewidth": 0.8},
            )
        else:
            ax.bar(pos, y_vals, width=width, label=m, color=color, alpha=0.85, edgecolor="#2a3245")

        # Add significance stars
        for j, (p_val_sig, yv) in enumerate(zip(sig_markers, y_vals)):
            if p_val_sig:
                star_y = yv + (y_err_hi[j] if has_ci else 0) + 0.015
                ax.text(pos[j], star_y, "★", ha="center", va="bottom", color=GOLD_ACCENT, fontsize=10, weight="bold")

    ax.set_xticks(x_base)
    ax.set_xticklabels(horizons, fontsize=11, weight="bold")
    ax.axhline(0.0, color="#6b7c96", linestyle=":", alpha=0.7)
    sig_label = "★ = Benjamini-Hochberg FDR q < 0.05" if has_fdr else "★ = DM p < 0.05"
    ax.set_title(f"4D-MGRFF Out-of-Sample Verification: BSS with 95% Bootstrap CI ({sig_label})", fontsize=13, pad=15, weight="bold", color=TEXT_COLOR)
    ax.set_xlabel("Forecast Horizon (h)", fontsize=11, labelpad=10)
    ax.set_ylabel("Brier Skill Score (Higher is Better)", fontsize=11, labelpad=10)
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0), framealpha=0.8, facecolor=PANEL_BG, edgecolor="#2a3245", fontsize=9)
    ax.grid(True, axis="y")

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_crypto_hedged_equity(equity_df: pd.DataFrame, output_path: str = "results/figures/figure_crypto_hedged_equity.png"):
    """
    Plots the walk-forward hedged equity curves vs. Unhedged Buy & Hold Bitcoin.
    """
    setup_style()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

    # Plot Unhedged BTC baseline
    if "Unhedged_BTC" in equity_df.columns:
        ax.plot(equity_df.index, equity_df["Unhedged_BTC"], color="#888888", linestyle="--", linewidth=1.8, label="Unhedged Buy & Hold BTC")

    # Priority models to highlight
    model_colors = {
        "Hedged_M5_LightGBM": CRIMSON_ACCENT,
        "Hedged_M4_DynamicAR": "#9d4edd",
        "Hedged_M7_Full4D": CYAN_ACCENT,
        "Hedged_M0_Persistence": GOLD_ACCENT,
    }

    for col in equity_df.columns:
        if col == "Unhedged_BTC":
            continue
        color = model_colors.get(col, "#555555")
        linewidth = 2.0 if col in model_colors else 1.0
        alpha = 0.9 if col in model_colors else 0.4
        label = col.replace("Hedged_", "Hedged: ")
        ax.plot(equity_df.index, equity_df[col], color=color, linewidth=linewidth, alpha=alpha, label=label)

    ax.set_title("Walk-Forward Hedged Equity Curves vs. Buy & Hold BTC (Including Frictions & Funding)", fontsize=13, pad=15, weight="bold", color=TEXT_COLOR)
    ax.set_xlabel("Date", fontsize=11, labelpad=10)
    ax.set_ylabel("Portfolio Value ($)", fontsize=11, labelpad=10)
    ax.legend(loc="upper left", framealpha=0.85, facecolor=PANEL_BG, edgecolor="#2a3245", fontsize=9)
    ax.grid(True)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_crypto_hedge_sensitivity(
    df_sweep: pd.DataFrame,
    output_path: str = "results/figures/figure_crypto_hedge_sensitivity.png",
):
    """
    Plots Max Drawdown and Net Total Return across hedge thresholds theta in [0.10, 0.40].
    Highlights the plateau of drawdown protection and the impact of hysteresis.
    """
    setup_style()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, dpi=300)

    # Filter fixed threshold rows
    df_fixed = df_sweep[df_sweep["Threshold_Type"] == "Fixed"].copy()

    key_models = ["M5_LightGBM", "M4_DynamicAR", "M0_Persistence", "M7_Full4D"]
    model_colors = {
        "M5_LightGBM": CRIMSON_ACCENT,
        "M4_DynamicAR": "#9d4edd",
        "M0_Persistence": GOLD_ACCENT,
        "M7_Full4D": CYAN_ACCENT,
    }

    # Top panel: Max Drawdown vs. Threshold
    for m in key_models:
        sub = df_fixed[df_fixed["Model"] == m].sort_values("Param_Value")
        if not sub.empty:
            color = model_colors.get(m, "#555555")
            ax1.plot(sub["Param_Value"], sub["Max_Drawdown_Pct"], marker="o", linewidth=2.0, color=color, label=f"{m}")

    # Unhedged baseline reference line
    ax1.axhline(51.32, color="#888888", linestyle="--", linewidth=1.5, label="Unhedged Buy & Hold (51.3%)")
    ax1.set_title("Hedge Threshold Sensitivity: Maximum Drawdown vs. Activation Threshold (θ)", fontsize=13, pad=12, weight="bold", color=TEXT_COLOR)
    ax1.set_ylabel("Max Drawdown (%) [Lower is Better]", fontsize=11, labelpad=8)
    ax1.legend(loc="lower right", framealpha=0.85, facecolor=PANEL_BG, edgecolor="#2a3245", fontsize=9)
    ax1.grid(True)

    # Bottom panel: Net Total Return vs. Threshold
    for m in key_models:
        sub = df_fixed[df_fixed["Model"] == m].sort_values("Param_Value")
        if not sub.empty:
            color = model_colors.get(m, "#555555")
            ax2.plot(sub["Param_Value"], sub["Total_Return_Pct"], marker="s", linewidth=2.0, color=color, label=f"{m}")

    ax2.axhline(16.48, color="#888888", linestyle="--", linewidth=1.5, label="Unhedged Buy & Hold (+16.5%)")

    # Plot Hysteresis points as special stars
    df_hyst = df_sweep[df_sweep["Threshold_Type"] == "Hysteresis"]
    for m in ["M5_LightGBM", "M0_Persistence"]:
        sub_h = df_hyst[df_hyst["Model"] == m]
        for _, row in sub_h.iterrows():
            ax1.scatter(row["Param_Value"], row["Max_Drawdown_Pct"], color="#00ffcc", marker="*", s=140, zorder=5)
            ax2.scatter(row["Param_Value"], row["Total_Return_Pct"], color="#00ffcc", marker="*", s=140, zorder=5)

    ax2.set_title("Hedge Threshold Sensitivity: Net Cumulative Return vs. Activation Threshold (θ)", fontsize=13, pad=12, weight="bold", color=TEXT_COLOR)
    ax2.set_xlabel("Crash Probability Activation Threshold (θ)", fontsize=11, labelpad=10)
    ax2.set_ylabel("Total Return Net of Frictions (%)", fontsize=11, labelpad=8)
    ax2.legend(loc="upper left", framealpha=0.85, facecolor=PANEL_BG, edgecolor="#2a3245", fontsize=9)
    ax2.grid(True)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")

