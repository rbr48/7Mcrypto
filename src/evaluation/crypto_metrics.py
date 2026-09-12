"""
Verification Metrics and Proper Scoring Rules for Cryptocurrency Risk Models.
Includes Brier Score, Brier Skill Score (BSS), Logarithmic Score, ECE, PR-AUC,
Relative Economic Value, Diebold-Mariano Test, and Bootstrap BSS Confidence Intervals.
"""

from typing import Tuple
import numpy as np


def compute_brier_score(probs: np.ndarray, realized: np.ndarray) -> float:
    p = np.asarray(probs, dtype=float)
    y = np.asarray(realized, dtype=float)
    return float(np.mean((p - y) ** 2))


def compute_brier_skill_score(probs: np.ndarray, realized: np.ndarray, climatology_prob: float) -> float:
    """
    BSS = 1 - BS_model / BS_climatology.
    climatology_prob should be the training-set base rate (not test-set realized mean)
    to avoid information leakage in the denominator.
    """
    bs = compute_brier_score(probs, realized)
    p_clim = np.full_like(realized, climatology_prob, dtype=float)
    bs_clim = compute_brier_score(p_clim, realized)
    if bs_clim < 1e-8:
        return 0.0
    return float(1.0 - (bs / bs_clim))


def compute_logarithmic_score(probs: np.ndarray, realized: np.ndarray, eps: float = 1e-12) -> float:
    p = np.clip(np.asarray(probs, dtype=float), eps, 1.0 - eps)
    y = np.asarray(realized, dtype=float)
    return float(-np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p)))


def compute_expected_calibration_error(probs: np.ndarray, realized: np.ndarray, num_bins: int = 5) -> Tuple[float, np.ndarray]:
    p = np.asarray(probs, dtype=float)
    y = np.asarray(realized, dtype=float)
    bins = np.linspace(0.0, 1.0, num_bins + 1)
    ece = 0.0
    total_n = len(p)

    for i in range(num_bins):
        mask = (p >= bins[i]) & (p < bins[i + 1]) if i < num_bins - 1 else (p >= bins[i]) & (p <= bins[i + 1])
        bin_n = np.sum(mask)
        if bin_n > 0:
            bin_conf = np.mean(p[mask])
            bin_acc = np.mean(y[mask])
            ece += (bin_n / total_n) * np.abs(bin_acc - bin_conf)

    return float(ece), bins


def compute_pr_auc(probs: np.ndarray, realized: np.ndarray) -> float:
    p = np.asarray(probs, dtype=float)
    y = np.asarray(realized, dtype=float)
    if len(np.unique(y)) < 2:
        return 0.5

    thresholds = np.sort(np.unique(p))[::-1]
    precisions = []
    recalls = []

    for t in thresholds:
        pred = (p >= t).astype(int)
        tp = np.sum((pred == 1) & (y == 1))
        fp = np.sum((pred == 1) & (y == 0))
        fn = np.sum((pred == 0) & (y == 1))

        prec = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        precisions.append(prec)
        recalls.append(rec)

    precisions = np.array([1.0] + precisions + [0.0])
    recalls = np.array([0.0] + recalls + [1.0])
    # Trapezoidal integration compatible with NumPy 1.x and 2.x
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(precisions, recalls))
    return float(np.sum(0.5 * (precisions[:-1] + precisions[1:]) * np.diff(recalls)))


def compute_relative_value_score(probs: np.ndarray, realized: np.ndarray, cost_loss_ratio: float = 0.20) -> float:
    """
    Computes Richardson (2000) Relative Economic Value score:
    V(alpha) = (E_clim - E_forecast) / (E_clim - E_perfect)

    NOTE: This is a static decision-theoretic skill score on an idealized 2x2 contingency matrix.
    It measures expected cost reduction relative to climatology under fixed cost/loss assumptions,
    NOT realized portfolio dollar P&L or actual percentage drawdown avoided.
    """
    alpha = cost_loss_ratio
    p = np.asarray(probs, dtype=float)
    y = np.asarray(realized, dtype=float)
    s = np.mean(y)  # Base rate

    if s <= 0 or s >= 1:
        return 0.0

    # Decision rule: Hedge if predicted probability >= alpha
    action = (p >= alpha).astype(int)

    # Expected expenses
    # Expense matrix: Hedge & Crisis = C; Hedge & No Crisis = C; No Hedge & Crisis = L; No Hedge & No Crisis = 0
    # Normalized by L: C/L = alpha
    exp_forecast = np.mean(action * alpha + (1 - action) * y * 1.0)
    exp_clim = min(alpha, s)
    exp_perfect = s * alpha

    denom = exp_clim - exp_perfect
    if denom <= 1e-8:
        return 0.0

    val = (exp_clim - exp_forecast) / denom
    return float(np.clip(val, -1.0, 1.0))


def compute_diebold_mariano(
    losses_a: np.ndarray,
    losses_b: np.ndarray,
    horizon: int = 1,
    alternative: str = "two-sided",
) -> Tuple[float, float]:
    """
    Diebold-Mariano test for equal predictive accuracy.
    Uses Newey-West HAC standard errors for multi-step forecasts (h > 1).

    Args:
        losses_a: Squared forecast errors from model A.
        losses_b: Squared forecast errors from model B.
        horizon: Forecast horizon h (for HAC bandwidth = h - 1).
        alternative: 'two-sided', 'less' (A better), or 'greater' (B better).

    Returns:
        (dm_statistic, p_value)
    """
    d = np.asarray(losses_a, dtype=float) - np.asarray(losses_b, dtype=float)
    n = len(d)
    if n < 5:
        return 0.0, 1.0

    d_mean = np.mean(d)

    # Newey-West HAC variance estimator with bandwidth = max(h-1, 0)
    bandwidth = max(horizon - 1, 0)
    gamma_0 = np.mean((d - d_mean) ** 2)

    gamma_sum = 0.0
    for k in range(1, bandwidth + 1):
        weight = 1.0 - k / (bandwidth + 1)  # Bartlett kernel
        gamma_k = np.mean((d[k:] - d_mean) * (d[:-k] - d_mean))
        gamma_sum += 2.0 * weight * gamma_k

    var_d = (gamma_0 + gamma_sum) / n
    if var_d < 1e-12:
        return 0.0, 1.0

    dm_stat = d_mean / np.sqrt(var_d)

    # p-value from standard normal approximation
    from scipy.stats import norm

    if alternative == "two-sided":
        p_val = 2.0 * norm.sf(np.abs(dm_stat))
    elif alternative == "less":
        p_val = norm.cdf(dm_stat)
    else:  # "greater"
        p_val = norm.sf(dm_stat)

    return float(dm_stat), float(p_val)


def compute_bootstrap_bss_ci(
    probs: np.ndarray,
    realized: np.ndarray,
    climatology_prob: float,
    n_boot: int = 1000,
    alpha: float = 0.05,
    block_size: int = 10,
) -> Tuple[float, float, float]:
    """
    Block bootstrap confidence interval for Brier Skill Score.

    Returns:
        (bss_point, bss_lower, bss_upper)
    """
    p = np.asarray(probs, dtype=float)
    y = np.asarray(realized, dtype=float)
    n = len(p)

    bss_point = compute_brier_skill_score(p, y, climatology_prob)

    rng = np.random.RandomState(42)
    bss_boot = np.zeros(n_boot)

    n_blocks = max(n // block_size, 1)

    for b in range(n_boot):
        # Block bootstrap: sample contiguous blocks to preserve serial dependence
        block_starts = rng.randint(0, max(n - block_size, 1), size=n_blocks)
        indices = np.concatenate([np.arange(s, min(s + block_size, n)) for s in block_starts])[:n]
        if len(indices) < 5:
            indices = rng.randint(0, n, size=n)

        p_b = p[indices]
        y_b = y[indices]
        bss_boot[b] = compute_brier_skill_score(p_b, y_b, climatology_prob)

    lower = float(np.percentile(bss_boot, 100 * alpha / 2))
    upper = float(np.percentile(bss_boot, 100 * (1 - alpha / 2)))

    return bss_point, lower, upper


def compute_benjamini_hochberg_fdr(p_values: np.ndarray, alpha: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
    """
    Benjamini-Hochberg (1995) False Discovery Rate (FDR) procedure.
    Controls the expected proportion of false discoveries across multiple hypothesis tests.

    Args:
        p_values: 1D array of p-values.
        alpha: False discovery rate significance threshold (default 0.05).

    Returns:
        (adjusted_q_values, is_significant_mask)
    """
    p = np.asarray(p_values, dtype=float)
    n = len(p)
    if n == 0:
        return np.array([]), np.array([], dtype=bool)

    valid_mask = ~np.isnan(p)
    valid_p = p[valid_mask]
    m = len(valid_p)

    if m == 0:
        return np.full(n, np.nan), np.zeros(n, dtype=bool)

    # Sort valid p-values
    sort_idx = np.argsort(valid_p)
    sorted_p = valid_p[sort_idx]

    # Compute raw q-values: q_i = p_(i) * m / rank_i
    ranks = np.arange(1, m + 1)
    q_raw = sorted_p * (m / ranks)

    # Enforce monotonicity backwards: q_(i) <= q_(i+1)
    q_sorted = np.minimum.accumulate(q_raw[::-1])[::-1]
    q_sorted = np.clip(q_sorted, 0.0, 1.0)

    # Re-order to original valid positions
    q_valid = np.zeros(m)
    q_valid[sort_idx] = q_sorted

    # Reconstruct full array with NaNs preserved
    q_values = np.full(n, np.nan)
    q_values[valid_mask] = q_valid

    is_sig = np.zeros(n, dtype=bool)
    is_sig[valid_mask] = q_valid < alpha

    return q_values, is_sig

