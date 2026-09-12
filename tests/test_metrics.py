"""Unit tests for crypto verification metrics and scoring rules."""

import numpy as np
import pytest

from src.evaluation.crypto_metrics import (
    compute_brier_score,
    compute_brier_skill_score,
    compute_logarithmic_score,
    compute_expected_calibration_error,
    compute_pr_auc,
    compute_relative_value_score,
    compute_diebold_mariano,
    compute_bootstrap_bss_ci,
)


def test_compute_brier_score():
    # Perfect predictions
    probs = np.array([1.0, 0.0, 1.0])
    realized = np.array([1, 0, 1])
    assert compute_brier_score(probs, realized) == pytest.approx(0.0)

    # Worst predictions
    probs_worst = np.array([0.0, 1.0, 0.0])
    assert compute_brier_score(probs_worst, realized) == pytest.approx(1.0)

    # Mixed predictions
    probs_half = np.array([0.5, 0.5])
    realized_half = np.array([1, 0])
    assert compute_brier_score(probs_half, realized_half) == pytest.approx(0.25)


def test_compute_brier_skill_score():
    realized = np.array([1, 0, 1, 0, 0])
    clim_prob = 0.4  # Matches base rate

    # Perfect forecast
    perfect_probs = realized.astype(float)
    bss_perfect = compute_brier_skill_score(perfect_probs, realized, clim_prob)
    assert bss_perfect == pytest.approx(1.0)

    # Climatology forecast
    clim_probs = np.full_like(realized, clim_prob, dtype=float)
    bss_clim = compute_brier_skill_score(clim_probs, realized, clim_prob)
    assert bss_clim == pytest.approx(0.0)

    # Poor forecast
    poor_probs = 1.0 - perfect_probs
    bss_poor = compute_brier_skill_score(poor_probs, realized, clim_prob)
    assert bss_poor < 0.0


def test_compute_logarithmic_score():
    probs = np.array([0.9, 0.1])
    realized = np.array([1, 0])
    ls = compute_logarithmic_score(probs, realized)
    expected = -0.5 * (np.log(0.9) + np.log(0.9))
    assert ls == pytest.approx(expected, rel=1e-3)

    # Extreme probabilities should not produce NaN or Inf
    extreme_probs = np.array([1.0, 0.0])
    ls_extreme = compute_logarithmic_score(extreme_probs, realized)
    assert not np.isnan(ls_extreme)
    assert not np.isinf(ls_extreme)


def test_compute_expected_calibration_error():
    probs = np.array([0.1, 0.2, 0.8, 0.9])
    realized = np.array([0, 0, 1, 1])
    ece, bins = compute_expected_calibration_error(probs, realized, num_bins=5)
    assert 0.0 <= ece <= 1.0
    assert len(bins) == 6


def test_compute_pr_auc():
    # Single class fallback
    assert compute_pr_auc(np.array([0.5, 0.6]), np.array([1, 1])) == 0.5

    # Perfect ranking
    probs = np.array([0.9, 0.8, 0.2, 0.1])
    realized = np.array([1, 1, 0, 0])
    pr_auc = compute_pr_auc(probs, realized)
    assert 0.8 <= pr_auc <= 1.0


def test_compute_relative_value_score():
    probs = np.array([0.9, 0.8, 0.1, 0.2])
    realized = np.array([1, 1, 0, 0])
    val = compute_relative_value_score(probs, realized, cost_loss_ratio=0.20)
    assert -1.0 <= val <= 1.0
    assert val > 0.0  # Decent forecast should yield positive economic value


def test_compute_diebold_mariano():
    # Identical losses -> stat = 0, pval = 1
    losses = np.array([0.1, 0.2, 0.15, 0.05, 0.3, 0.25])
    stat, pval = compute_diebold_mariano(losses, losses, horizon=1)
    assert stat == pytest.approx(0.0)
    assert pval == pytest.approx(1.0)

    # Model A clearly better (lower squared error)
    losses_a = np.array([0.01, 0.02, 0.01, 0.03, 0.02, 0.01, 0.02, 0.01])
    losses_b = np.array([0.25, 0.30, 0.20, 0.40, 0.35, 0.25, 0.30, 0.28])
    stat, pval = compute_diebold_mariano(losses_a, losses_b, horizon=1, alternative="less")
    assert stat < 0.0
    assert pval < 0.01

    # Multi-step horizon HAC standard error (h=7)
    stat_h7, pval_h7 = compute_diebold_mariano(losses_a, losses_b, horizon=7, alternative="less")
    assert not np.isnan(stat_h7)
    assert not np.isnan(pval_h7)

    # Small sample (<5) guard
    stat_small, pval_small = compute_diebold_mariano(np.array([0.1, 0.2]), np.array([0.2, 0.3]))
    assert stat_small == 0.0
    assert pval_small == 1.0


def test_compute_bootstrap_bss_ci():
    np.random.seed(42)
    realized = np.random.binomial(1, 0.2, size=100)
    probs = np.clip(realized * 0.5 + np.random.uniform(0, 0.3, size=100), 0.01, 0.99)
    clim_prob = 0.2

    point, lower, upper = compute_bootstrap_bss_ci(probs, realized, clim_prob, n_boot=200)
    assert lower <= upper
    # Point estimate should be between or very close to bounds
    assert lower <= point + 0.1
    assert upper >= point - 0.1
