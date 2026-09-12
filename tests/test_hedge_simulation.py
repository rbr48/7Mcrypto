"""Unit tests for Benjamini-Hochberg FDR correction and Hedged P&L Simulator."""

import numpy as np
import pandas as pd
import pytest

from src.evaluation.crypto_metrics import compute_benjamini_hochberg_fdr
from src.evaluation.crypto_hedge_simulation import CryptoHedgeSimulator


def test_benjamini_hochberg_fdr_basic():
    # Empty case
    q_empty, sig_empty = compute_benjamini_hochberg_fdr(np.array([]))
    assert len(q_empty) == 0

    # Monotonicity and significance
    p_vals = np.array([0.001, 0.004, 0.03, 0.20, 0.80])
    q_vals, is_sig = compute_benjamini_hochberg_fdr(p_vals, alpha=0.05)

    assert len(q_vals) == 5
    # q-values must be >= p-values
    assert np.all(q_vals >= p_vals - 1e-10)
    # The smallest p-value should be significant
    assert is_sig[0] is True or is_sig[0] == 1

    # NaN preservation
    p_with_nan = np.array([0.001, np.nan, 0.05])
    q_nan, sig_nan = compute_benjamini_hochberg_fdr(p_with_nan, alpha=0.05)
    assert np.isnan(q_nan[1])
    assert sig_nan[1] is False or sig_nan[1] == 0


def test_crypto_hedge_simulator_execution():
    dates = pd.date_range("2024-01-01", periods=20, freq="D")
    prices = [100.0, 102.0, 101.0, 95.0, 90.0, 92.0, 96.0, 100.0, 105.0, 110.0] * 2
    fundings = [10.0] * 20  # 10% annualized

    df_features = pd.DataFrame(
        {"BTC_PRICE": prices, "BTC_FUNDING_RATE": fundings},
        index=dates,
    )

    # Synthetic forecast records for 2 models
    records = []
    for origin in range(0, 18, 2):
        records.append({"origin_idx": origin, "horizon": 1, "model": "ModelA", "prob": 0.35, "realized": 1.0})
        records.append({"origin_idx": origin, "horizon": 1, "model": "ModelB", "prob": 0.05, "realized": 0.0})

    df_fc = pd.DataFrame(records)

    sim = CryptoHedgeSimulator(
        hedge_threshold=0.20,
        taker_fee_bps=5.0,
        slippage_bps=5.0,
        include_funding=True,
        initial_capital=10000.0,
    )

    summary_df, equity_df = sim.simulate(df_fc, df_features, horizon=1)

    assert not summary_df.empty
    assert not equity_df.empty
    assert "Unhedged_Buy_and_Hold" in summary_df["Model"].values
    assert "ModelA" in summary_df["Model"].values
    assert "ModelB" in summary_df["Model"].values

    # ModelA has prob=0.35 > threshold=0.20 -> active hedge days > 0
    row_a = summary_df[summary_df["Model"] == "ModelA"].iloc[0]
    assert row_a["Hedge_Days_Pct"] > 0.0

    # ModelB has prob=0.05 < threshold=0.20 -> no hedge
    row_b = summary_df[summary_df["Model"] == "ModelB"].iloc[0]
    assert row_b["Hedge_Days_Pct"] == 0.0

    # Check required columns
    expected_cols = {
        "Model", "Total_Return_Pct", "Max_Drawdown_Pct", "Drawdown_Reduction_Pct",
        "Annualized_Vol_Pct", "Sharpe_Ratio", "Sortino_Ratio", "Friction_Cost_Pct",
    }
    assert expected_cols.issubset(set(summary_df.columns))


def test_crypto_hedge_simulator_hysteresis_reduces_flips():
    # Construct an oscillating probability series: 0.22, 0.18, 0.22, 0.18, ...
    dates = pd.date_range("2024-01-01", periods=10, freq="D")
    prices = [100.0] * 10
    df_features = pd.DataFrame({"BTC_PRICE": prices, "BTC_FUNDING_RATE": [0.0] * 10}, index=dates)

    records = []
    for origin in range(0, 8, 1):
        prob = 0.22 if origin % 2 == 0 else 0.18
        records.append({"origin_idx": origin, "horizon": 1, "model": "FlickerModel", "prob": prob, "realized": 0.0})
    df_fc = pd.DataFrame(records)

    sim = CryptoHedgeSimulator(initial_capital=10000.0)

    # 1. Without hysteresis (fixed threshold = 0.20): flips on almost every step
    df_fixed, _ = sim.simulate(df_fc, df_features, enter_threshold=0.20, exit_threshold=0.20)
    flips_fixed = df_fixed[df_fixed["Model"] == "FlickerModel"]["Hedge_Flips"].values[0]

    # 2. With hysteresis (enter=0.25, exit=0.15): prob never reaches 0.25 to enter, so 0 flips
    df_hyst, _ = sim.simulate(df_fc, df_features, enter_threshold=0.25, exit_threshold=0.15)
    flips_hyst = df_hyst[df_hyst["Model"] == "FlickerModel"]["Hedge_Flips"].values[0]

    assert flips_fixed > 0
    assert flips_hyst == 0
    assert flips_hyst < flips_fixed


def test_crypto_hedge_simulator_sweep():
    dates = pd.date_range("2024-01-01", periods=10, freq="D")
    prices = [100.0, 95.0, 90.0, 85.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0]
    df_features = pd.DataFrame({"BTC_PRICE": prices, "BTC_FUNDING_RATE": [5.0] * 10}, index=dates)

    records = []
    for origin in range(0, 8, 1):
        records.append({"origin_idx": origin, "horizon": 1, "model": "M_Test", "prob": 0.25, "realized": 1.0})
    df_fc = pd.DataFrame(records)

    sim = CryptoHedgeSimulator()
    sweep_df = sim.sweep_thresholds(
        df_forecasts=df_fc,
        df_features=df_features,
        thresholds=[0.15, 0.20, 0.30],
        hysteresis_pairs=[(0.25, 0.15)],
    )

    assert not sweep_df.empty
    assert set(sweep_df["Threshold_Type"].unique()) == {"Fixed", "Hysteresis"}
    assert len(sweep_df) == 4  # 3 fixed + 1 hysteresis

