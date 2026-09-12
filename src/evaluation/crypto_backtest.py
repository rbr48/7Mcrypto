"""
Rolling-Origin Out-of-Sample Backtester for Continuous 24/7/365 Cryptocurrency Markets.
Uses non-circular realized drawdown target (decoupled from DVOL).
Computes rolling thresholds per-origin. Includes Diebold-Mariano significance testing.
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from src.evaluation.crypto_metrics import (
    compute_brier_score,
    compute_brier_skill_score,
    compute_bootstrap_bss_ci,
    compute_diebold_mariano,
    compute_expected_calibration_error,
    compute_logarithmic_score,
    compute_pr_auc,
    compute_relative_value_score,
    compute_benjamini_hochberg_fdr,
)
from src.models.crypto_baselines import CryptoClimatologyModel, CryptoPersistenceModel
from src.models.crypto_ensemble import CryptoStateSpaceAugmentedModel
from src.models.crypto_full_4d_dlm import CryptoFull4DDLMModel
from src.models.crypto_nonlinear import CryptoNonlinearGBDTModel
from src.models.crypto_statistical import (
    CryptoDynamicAutoregressiveModel,
    CryptoMultidisciplinaryRegularizedModel,
    CryptoSingleDomainLogisticModel,
)


def compute_drawdown_target(
    btc_prices: pd.Series,
    horizon: int,
    threshold_percentile: float = 85.0,
    train_end_idx: int = None,
) -> Tuple[pd.Series, float]:
    """
    Constructs a non-circular target: whether the max drawdown over the next h days
    exceeds a rolling threshold computed from training data only.

    A drawdown at time t is defined as:
        dd_t = max(0, 1 - min(price_{t+1..t+h}) / price_t)

    The threshold is the `threshold_percentile` of drawdowns in the training window.

    Args:
        btc_prices: BTC_PRICE series with DatetimeIndex.
        horizon: Number of days forward to measure drawdown.
        threshold_percentile: Percentile of training drawdowns to use as crisis threshold.
        train_end_idx: Index position up to which to compute the threshold.

    Returns:
        (binary_target_series, threshold_value)
    """
    N = len(btc_prices)
    prices = btc_prices.values

    drawdowns = np.full(N, np.nan)
    for t in range(N - horizon):
        future_min = np.min(prices[t + 1 : t + horizon + 1])
        drawdowns[t] = max(0.0, 1.0 - future_min / prices[t])

    dd_series = pd.Series(drawdowns, index=btc_prices.index)

    # Compute threshold from training data only
    if train_end_idx is not None:
        train_dd = drawdowns[:train_end_idx]
        train_dd = train_dd[~np.isnan(train_dd)]
    else:
        valid_dd = drawdowns[~np.isnan(drawdowns)]
        train_dd = valid_dd

    threshold = float(np.percentile(train_dd, threshold_percentile)) if len(train_dd) > 0 else 0.05

    target = (dd_series >= threshold).astype(int)
    return target, threshold


class RollingOriginCryptoBacktester:
    """
    Executes expanding-window out-of-sample backtest across 24/7 crypto continuous timelines.
    Uses non-circular realized drawdown target decoupled from model features.
    """

    def __init__(self, horizons: List[int] = None, min_train_size: int = 80, cost_loss_ratio: float = 0.20):
        self.horizons = horizons or [1, 3, 7, 14]
        self.min_train_size = min_train_size
        self.cost_loss_ratio = cost_loss_ratio
        self.forecast_records: List[Dict] = []
        self.score_summary: pd.DataFrame = pd.DataFrame()

    def run_backtest(
        self,
        df_features: pd.DataFrame,
        target_series: pd.Series,
        step_size: int = 3,
        anchor_indicator: str = "DVOL",
        btc_price_col: str = "BTC_PRICE",
        drawdown_percentile: float = 85.0,
    ) -> pd.DataFrame:
        """
        Runs the rolling-origin backtest with per-origin rolling drawdown thresholds.

        The target is recomputed at each origin using only training-set drawdown
        statistics, eliminating lookahead bias in the threshold.
        """
        T = len(df_features)
        btc_prices = df_features[btc_price_col] if btc_price_col in df_features.columns else None
        self.forecast_records = []

        model_factories = {
            "M0_Persistence": lambda: CryptoPersistenceModel(),
            "M1_Climatology": lambda: CryptoClimatologyModel(),
            "M2_SingleDomain": lambda: CryptoSingleDomainLogisticModel(target_cols=[anchor_indicator]),
            "M3_ElasticNet": lambda: CryptoMultidisciplinaryRegularizedModel(),
            "M4_DynamicAR": lambda: CryptoDynamicAutoregressiveModel(),
            "M5_LightGBM": lambda: CryptoNonlinearGBDTModel(),
            "M6_StateSpace": lambda: CryptoStateSpaceAugmentedModel(anchor_indicator=anchor_indicator),
            "M7_Full4D": lambda: CryptoFull4DDLMModel(anchor_indicator=anchor_indicator, horizons=self.horizons),
        }

        origin_indices = range(self.min_train_size, T - max(self.horizons), step_size)
        total_origins = len(origin_indices)
        print(f"[Backtest] Initiating rolling-origin tournament across {total_origins} origins (Step size = {step_size})...")

        count = 0
        for t in origin_indices:
            count += 1
            if count % 50 == 0 or count == total_origins:
                print(f"  - Progress: Origin {count}/{total_origins} ({count/total_origins:.1%}) [Date: {df_features.index[t].strftime('%Y-%m-%d')}]")

            X_train = df_features.iloc[:t].copy()
            y_train_full = target_series.values[:t].copy()
            X_test_slice = df_features.iloc[t : t + 1].copy()

            # Rolling target: recompute drawdown threshold using training data only
            for h in self.horizons:
                if btc_prices is not None:
                    _, rolling_threshold = compute_drawdown_target(
                        btc_prices.iloc[:t],
                        horizon=h,
                        threshold_percentile=drawdown_percentile,
                        train_end_idx=t,
                    )

                realized_idx = t + h
                if realized_idx >= T:
                    continue
                realized_outcome = float(target_series.values[realized_idx])

                # Training base rate for this origin (for BSS reference)
                train_base_rate = float(np.mean(y_train_full))

                for model_name, factory in model_factories.items():
                    model = factory()
                    model.fit(X_train, y_train_full)

                    pred_prob = float(model.predict_proba(X_test_slice, horizon=h)[0])

                    self.forecast_records.append(
                        {
                            "origin_idx": t,
                            "date": df_features.index[t],
                            "horizon": h,
                            "model": model_name,
                            "prob": pred_prob,
                            "realized": realized_outcome,
                            "train_base_rate": train_base_rate,
                        }
                    )

        df_results = pd.DataFrame(self.forecast_records)
        self.df_forecasts = df_results
        self.score_summary = self._compute_performance_table(df_results)
        return self.score_summary

    def _compute_performance_table(self, df_results: pd.DataFrame) -> pd.DataFrame:
        if df_results.empty:
            return pd.DataFrame()

        rows = []
        models = df_results["model"].unique()

        for h in self.horizons:
            df_h = df_results[df_results["horizon"] == h]
            if df_h.empty:
                continue

            # Use per-origin training base rates averaged as the BSS reference
            # This correctly uses only training-set information
            clim_prob = float(df_h["train_base_rate"].mean())

            # Collect squared errors for DM test
            model_losses = {}

            for m in models:
                sub = df_h[df_h["model"] == m]
                if sub.empty:
                    continue

                p = sub["prob"].values
                y = sub["realized"].values

                bs = compute_brier_score(p, y)
                bss = compute_brier_skill_score(p, y, climatology_prob=clim_prob)
                ls = compute_logarithmic_score(p, y)
                ece, _ = compute_expected_calibration_error(p, y, num_bins=5)
                pr_auc = compute_pr_auc(p, y)
                val_score = compute_relative_value_score(p, y, cost_loss_ratio=self.cost_loss_ratio)

                # Bootstrap CI for BSS
                _, bss_lo, bss_hi = compute_bootstrap_bss_ci(p, y, clim_prob, n_boot=500)

                # Store squared errors for DM test
                model_losses[m] = (p - y) ** 2

                rows.append(
                    {
                        "Horizon": f"{h}d",
                        "Model": m,
                        "Brier_Score": round(bs, 4),
                        "BSS_vs_Clim": round(bss, 4),
                        "BSS_CI_Lo": round(bss_lo, 4),
                        "BSS_CI_Hi": round(bss_hi, 4),
                        "Log_Score": round(ls, 4),
                        "ECE": round(ece, 4),
                        "PR_AUC": round(pr_auc, 4),
                        "Relative_Value": round(val_score, 4),
                        "DM_vs_Clim_pval": np.nan,  # Filled below
                    }
                )

            # Compute Diebold-Mariano tests: each model vs M1_Climatology
            if "M1_Climatology" in model_losses:
                clim_losses = model_losses["M1_Climatology"]
                for row in rows:
                    if row["Horizon"] != f"{h}d":
                        continue
                    m = row["Model"]
                    if m in model_losses and m != "M1_Climatology":
                        # Align lengths
                        m_losses = model_losses[m]
                        min_len = min(len(clim_losses), len(m_losses))
                        dm_stat, dm_pval = compute_diebold_mariano(
                            m_losses[:min_len],
                            clim_losses[:min_len],
                            horizon=h,
                            alternative="less",  # H1: model is better (lower loss)
                        )
                        row["DM_vs_Clim_pval"] = round(dm_pval, 4)

        # Apply Benjamini-Hochberg FDR correction across all hypothesis tests in the tournament
        p_vals = np.array([r.get("DM_vs_Clim_pval", np.nan) for r in rows], dtype=float)
        q_vals, is_sig_fdr = compute_benjamini_hochberg_fdr(p_vals, alpha=0.05)

        for idx, r in enumerate(rows):
            r["DM_FDR_qval"] = round(q_vals[idx], 4) if not np.isnan(q_vals[idx]) else np.nan
            r["DM_Sig_FDR"] = bool(is_sig_fdr[idx]) if not np.isnan(q_vals[idx]) else False

        return pd.DataFrame(rows)
