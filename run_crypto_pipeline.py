"""
4D-MGRFF: Master Cryptocurrency Systemic Risk Pipeline.
End-to-end execution of:
1. Point-in-Time Crypto Data Ingestion (Deribit DVOL, Binance Spot & Funding, Stablecoin Depegging)
2. Sign-Identified DGRS Latent Stress Filtering (lambda_DVOL > 0, EM-estimated Q)
3. Non-Circular Realized Drawdown Target Construction (decoupled from DVOL)
4. Rolling-Origin Out-of-Sample Model Tournament (M0 to M7 across h in {1, 3, 7, 14} days)
5. Empirical Generalized IRF Cross-Asset Contagion Matrices (Pi_1 and Pi_7)
6. Diebold-Mariano Significance Testing and Bootstrap Confidence Intervals
7. Publication Figures and Verification Tables Export
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd

# Add repo root to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.acquisition.schema import CryptoPointInTimeDatabase
from src.acquisition.crypto_ingestor import CryptoDataIngestor
from src.statespace.crypto_dgrs import SignIdentifiedCryptoDGRS
from src.models.crypto_full_4d_dlm import CryptoFull4DDLMModel
from src.evaluation.crypto_backtest import RollingOriginCryptoBacktester, compute_drawdown_target
from src.evaluation.crypto_hedge_simulation import CryptoHedgeSimulator
from src.evaluation.crypto_plotting import (
    plot_crypto_dgrs_trajectory,
    plot_crypto_propagation_heatmaps,
    plot_crypto_model_comparison,
    plot_crypto_hedged_equity,
    plot_crypto_hedge_sensitivity,
)


def run_crypto_risk_pipeline():
    print("=" * 80)
    print(" 4D-MGRFF: CRYPTOCURRENCY SYSTEMIC RISK EMPIRICAL PIPELINE ")
    print("=" * 80)

    # 1. Initialize Point-in-Time Database & Ingestion
    db_path = "data/processed/crypto_risk_database.db"
    db = CryptoPointInTimeDatabase(db_path=db_path)
    ingestor = CryptoDataIngestor(db=db)

    fred_db_path = "../4d-global-risk/data/processed/global_risk_database.db"
    print("\n[Phase 1] Executing Real-Data Ingestion from Binance, Deribit, and FRED...")
    if not os.path.exists(fred_db_path):
        print(f"  [!] WARNING: 4d-global-risk database not found at '{fred_db_path}'")
        print("    Macro features (DTWEXBGS, VIXCLS) will be excluded from the model.")
    df_aligned = ingestor.run_ingestion_pipeline(fred_db_path=fred_db_path)

    print(f"\n[Phase 2] Aligned Cryptocurrency Systemic Risk Panel:")
    print(f"  - Sample Range       : {df_aligned.index.min().strftime('%Y-%m-%d')} to {df_aligned.index.max().strftime('%Y-%m-%d')}")
    print(f"  - Total Observations : {len(df_aligned)} consecutive 24/7 daily periods")
    print(f"  - Features           : {list(df_aligned.columns)}")

    if ingestor.dvol_is_proxy:
        print("  [!] DVOL is fully proxied by BTC_REALIZED_VOL (Deribit API unavailable)")

    # 2. Construct Non-Circular Drawdown Target
    # Uses BTC_PRICE realized drawdowns — completely decoupled from DVOL features.
    # The threshold is computed per-origin inside the backtester using only training data.
    print("\n[Phase 2b] Constructing Non-Circular Realized Drawdown Target...")
    max_horizon = 14
    btc_prices = df_aligned["BTC_PRICE"]
    target_event, global_threshold = compute_drawdown_target(
        btc_prices,
        horizon=max_horizon,
        threshold_percentile=85.0,
        train_end_idx=len(btc_prices),  # Full-sample for display only; backtester uses rolling
    )
    base_rate = float(np.nanmean(target_event))
    print(f"  - Target Definition  : BTC max drawdown over next {max_horizon}d exceeds rolling 85th percentile")
    print(f"  - Global Threshold   : {global_threshold:.4%} drawdown (display only — backtester uses per-origin)")
    print(f"  - Historical Base Rate: {base_rate:.2%}")
    print(f"  - NOTE: Target is decoupled from DVOL — eliminates circularity bias")

    # 3. Rolling-Origin Out-of-Sample Backtest
    print("\n[Phase 3] Executing 24/7 Rolling-Origin Backtest (Non-Circular Target)...")
    backtester = RollingOriginCryptoBacktester(
        horizons=[1, 3, 7, 14],
        min_train_size=80,
        cost_loss_ratio=0.20,
    )

    perf_table = backtester.run_backtest(
        df_features=df_aligned,
        target_series=target_event,
        step_size=3,
        anchor_indicator="DVOL",
        btc_price_col="BTC_PRICE",
        drawdown_percentile=85.0,
    )

    # 4. Export Performance Tables
    os.makedirs("results/tables", exist_ok=True)
    perf_table.to_csv("results/tables/table_crypto_performance.csv", index=False)
    try:
        perf_table.to_markdown("results/tables/table_crypto_performance.md", index=False)
    except Exception:
        pass

    print("\n" + "=" * 80)
    print(" TABLE: CRYPTOCURRENCY OUT-OF-SAMPLE VERIFICATION PERFORMANCE ")
    print("=" * 80)
    print(perf_table.to_string(index=False))

    # Highlight DM and FDR significance
    sig_models = perf_table[perf_table["DM_vs_Clim_pval"] < 0.05]
    if not sig_models.empty:
        print("\n  * Raw Diebold-Mariano tests beating climatology (p < 0.05):")
        for _, row in sig_models.iterrows():
            fdr_str = f" [FDR q = {row['DM_FDR_qval']:.4f} {'SIG' if row['DM_Sig_FDR'] else 'NOT sig after FDR'}]" if "DM_FDR_qval" in row else ""
            print(f"    - {row['Model']} at {row['Horizon']}: BSS = {row['BSS_vs_Clim']:.4f} (raw p = {row['DM_vs_Clim_pval']:.4f}){fdr_str}")

    fdr_models = perf_table[perf_table.get("DM_Sig_FDR", False) == True]
    if not fdr_models.empty:
        print("\n  * Models surviving Benjamini-Hochberg False Discovery Rate (FDR q < 0.05):")
        for _, row in fdr_models.iterrows():
            print(f"    - {row['Model']} at {row['Horizon']}: BSS = {row['BSS_vs_Clim']:.4f} (q = {row['DM_FDR_qval']:.4f})")
    else:
        print("\n  [!] Notice: No model survives Benjamini-Hochberg FDR correction across all 28 hypothesis tests.")

    # 4b. Walk-Forward Hedged P&L Simulation (Real Frictions & Funding)
    print("\n[Phase 3b] Simulating Walk-Forward Dynamic Hedging Overlay (1d Horizon)...")
    simulator = CryptoHedgeSimulator(
        hedge_threshold=0.20,
        taker_fee_bps=5.0,
        slippage_bps=5.0,
        include_funding=True,
        initial_capital=100000.0,
    )

    # 1. Base run at theta = 0.20
    hedge_summary, hedge_equity = simulator.simulate(
        df_forecasts=backtester.df_forecasts,
        df_features=df_aligned,
        horizon=1,
    )

    # 2. Hysteresis anti-churn run (Enter = 0.25, Exit = 0.15)
    hyst_summary, hyst_equity = simulator.simulate(
        df_forecasts=backtester.df_forecasts,
        df_features=df_aligned,
        horizon=1,
        enter_threshold=0.25,
        exit_threshold=0.15,
    )

    # Combine key comparisons into the headline P&L table
    m5_hyst = hyst_summary[hyst_summary["Model"] == "M5_LightGBM"].copy()
    m5_hyst["Model"] = "M5_LightGBM (Hysteresis 0.15-0.25)"
    combined_pnl = pd.concat([hedge_summary, m5_hyst], ignore_index=True)

    combined_pnl.to_csv("results/tables/table_crypto_hedged_pnl.csv", index=False)
    try:
        combined_pnl.to_markdown("results/tables/table_crypto_hedged_pnl.md", index=False)
    except Exception:
        pass

    print("\n" + "=" * 80)
    print(" TABLE: WALK-FORWARD HEDGED P&L & DRAWDOWN REDUCTION (1-Day Horizon) ")
    print(" (Includes Binance 5bps taker fee + 5bps slippage + funding cash flows) ")
    print("=" * 80)
    print(combined_pnl.to_string(index=False))

    plot_crypto_hedged_equity(hedge_equity, output_path="results/figures/figure_crypto_hedged_equity.png")

    # 3. Comprehensive Threshold Sensitivity Sweep
    print("\n[Phase 3c] Running Threshold Sensitivity Sweep (theta in [0.10, 0.40] + Hysteresis)...")
    sweep_df = simulator.sweep_thresholds(
        df_forecasts=backtester.df_forecasts,
        df_features=df_aligned,
        thresholds=[0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        hysteresis_pairs=[(0.25, 0.15), (0.20, 0.12)],
        horizon=1,
    )
    sweep_df.to_csv("results/tables/table_crypto_hedge_sensitivity.csv", index=False)
    try:
        sweep_df.to_markdown("results/tables/table_crypto_hedge_sensitivity.md", index=False)
    except Exception:
        pass

    plot_crypto_hedge_sensitivity(sweep_df, output_path="results/figures/figure_crypto_hedge_sensitivity.png")

    print("\n[Phase 4] Estimating Generalized IRF Contagion Matrices (Pesaran-Shin Pi_h)...")
    m7 = CryptoFull4DDLMModel(anchor_indicator="DVOL", horizons=[1, 7])
    m7.fit(df_aligned, target_event.values)

    pi_1 = m7.get_propagation_matrix(horizon=1)
    pi_7 = m7.get_propagation_matrix(horizon=7)

    cols = list(df_aligned.columns)
    df_pi_1 = pd.DataFrame(np.round(pi_1, 3), index=cols, columns=cols)
    df_pi_7 = pd.DataFrame(np.round(pi_7, 3), index=cols, columns=cols)

    df_pi_1.to_csv("results/tables/table_crypto_propagation_h1.csv")
    df_pi_7.to_csv("results/tables/table_crypto_propagation_h7.csv")

    print("\n" + "=" * 80)
    print(" GENERALIZED IRF MATRIX (Pi_1: 1-Day Lead-Lag Impulse Transmission) ")
    print("=" * 80)
    print(df_pi_1.to_string())

    # Verify diagonals are exactly 1.0
    diag_check = np.allclose(np.diag(pi_1), 1.0, atol=1e-10) and np.allclose(np.diag(pi_7), 1.0, atol=1e-10)
    print(f"\n  Diagonal = 1.0 check: {'PASS' if diag_check else 'FAIL'}")

    # 6. Export Visualizations
    print("\n[Phase 5] Generating Publication Figures for Cryptocurrency Domain...")
    os.makedirs("results/figures", exist_ok=True)
    dgrs = SignIdentifiedCryptoDGRS(anchor_indicator="DVOL")
    dgrs.fit(df_aligned)
    _, _, ci_df = dgrs.smooth(df_aligned)

    plot_crypto_dgrs_trajectory(ci_df, output_path="results/figures/figure_crypto_dgrs_trajectory.png")
    plot_crypto_propagation_heatmaps(df_pi_1, df_pi_7, output_path="results/figures/figure_crypto_propagation_heatmaps.png")
    plot_crypto_model_comparison(perf_table, output_path="results/figures/figure_crypto_model_comparison.png")

    print("\n" + "=" * 80)
    print(" SUCCESS: 4D Cryptocurrency Systemic Risk Pipeline Complete! ")
    print("=" * 80)
    return perf_table, df_pi_1, df_pi_7


if __name__ == "__main__":
    run_crypto_risk_pipeline()
