"""Unit tests for non-circular realized drawdown target construction."""

import numpy as np
import pandas as pd
import pytest

from src.evaluation.crypto_backtest import compute_drawdown_target


def test_drawdown_target_monotonic_increasing():
    # If price monotonically rises, all drawdowns are 0
    dates = pd.date_range("2024-01-01", periods=20, freq="D")
    prices = pd.Series(np.linspace(100, 200, 20), index=dates)

    target, threshold = compute_drawdown_target(prices, horizon=3, threshold_percentile=85.0)
    # Threshold is 0.0, target is all 1s or 0s consistently without error
    assert isinstance(threshold, float)
    assert len(target) == len(prices)


def test_drawdown_target_sharp_crash():
    # Construct series with known 25% crash on day 5
    dates = pd.date_range("2024-01-01", periods=15, freq="D")
    price_vals = [100.0] * 5 + [75.0] * 5 + [80.0] * 5
    prices = pd.Series(price_vals, index=dates)

    target, threshold = compute_drawdown_target(prices, horizon=3, threshold_percentile=80.0)
    # Day 4 forward looks ahead into the 75.0 price (25% drawdown)
    # Target values must be 0 or 1
    assert set(np.unique(target.values)).issubset({0, 1})
    assert threshold > 0.0
    assert 1 in target.values


def test_drawdown_target_rolling_threshold_isolation():
    # Test that train_end_idx isolates future data from threshold computation
    dates = pd.date_range("2024-01-01", periods=50, freq="D")
    # Low volatility early, extreme crash late
    price_vals = [100.0 + np.sin(i) * 2 for i in range(30)] + [100.0 * (0.5 ** (i - 29)) for i in range(30, 50)]
    prices = pd.Series(price_vals, index=dates)

    # Threshold with only early data
    _, thresh_early = compute_drawdown_target(prices, horizon=3, threshold_percentile=85.0, train_end_idx=25)
    # Threshold with full data (including extreme crashes)
    _, thresh_full = compute_drawdown_target(prices, horizon=3, threshold_percentile=85.0, train_end_idx=50)

    # Extreme crash in late period must not have contaminated thresh_early
    assert thresh_early < thresh_full
