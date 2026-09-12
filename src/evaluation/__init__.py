"""Evaluation module for 4D-MGRFF cryptocurrency risk forecasting."""

from src.evaluation.crypto_metrics import (
    compute_brier_score,
    compute_brier_skill_score,
    compute_logarithmic_score,
    compute_expected_calibration_error,
    compute_pr_auc,
    compute_relative_value_score,
    compute_diebold_mariano,
    compute_bootstrap_bss_ci,
    compute_benjamini_hochberg_fdr,
)
from src.evaluation.crypto_backtest import (
    RollingOriginCryptoBacktester,
    compute_drawdown_target,
)
from src.evaluation.crypto_hedge_simulation import CryptoHedgeSimulator
from src.evaluation.crypto_plotting import (
    plot_crypto_dgrs_trajectory,
    plot_crypto_propagation_heatmaps,
    plot_crypto_model_comparison,
    plot_crypto_hedged_equity,
    plot_crypto_hedge_sensitivity,
)

__all__ = [
    "compute_brier_score",
    "compute_brier_skill_score",
    "compute_logarithmic_score",
    "compute_expected_calibration_error",
    "compute_pr_auc",
    "compute_relative_value_score",
    "compute_diebold_mariano",
    "compute_bootstrap_bss_ci",
    "compute_benjamini_hochberg_fdr",
    "RollingOriginCryptoBacktester",
    "compute_drawdown_target",
    "CryptoHedgeSimulator",
    "plot_crypto_dgrs_trajectory",
    "plot_crypto_propagation_heatmaps",
    "plot_crypto_model_comparison",
    "plot_crypto_hedged_equity",
    "plot_crypto_hedge_sensitivity",
]
