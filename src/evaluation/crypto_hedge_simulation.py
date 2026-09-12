"""
Walk-Forward Hedged P&L Simulation Engine for Cryptocurrency Risk Models.
Evaluates whether model crash probability signals translate into real portfolio
drawdown reduction, accounting for:
- 100% Long Bitcoin spot base portfolio
- 1.0x Short Perpetual Futures hedging overlay
- Binance perpetual taker trading fees (e.g., 5 bps entry, 5 bps exit)
- Execution slippage (e.g., 5 bps entry, 5 bps exit)
- Funding rate cash flow payments / receipts while holding short positions
- Schmitt-trigger hysteresis (dual enter/exit thresholds) to eliminate whipsaw churn
- Full threshold sensitivity sweep across theta in [0.10, 0.40]
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


class CryptoHedgeSimulator:
    """
    Simulates a walk-forward dynamic hedging strategy on Bitcoin spot holdings.
    Supports single fixed thresholds or dual-threshold Schmitt-trigger hysteresis.
    """

    def __init__(
        self,
        hedge_threshold: float = 0.20,
        enter_threshold: Optional[float] = None,
        exit_threshold: Optional[float] = None,
        taker_fee_bps: float = 5.0,
        slippage_bps: float = 5.0,
        include_funding: bool = True,
        initial_capital: float = 100000.0,
    ):
        self.hedge_threshold = hedge_threshold
        self.enter_threshold = enter_threshold if enter_threshold is not None else hedge_threshold
        self.exit_threshold = exit_threshold if exit_threshold is not None else self.enter_threshold
        # Total one-way friction = fee + slippage
        self.one_way_friction = (taker_fee_bps + slippage_bps) / 10000.0
        self.include_funding = include_funding
        self.initial_capital = initial_capital

    def simulate(
        self,
        df_forecasts: pd.DataFrame,
        df_features: pd.DataFrame,
        horizon: int = 1,
        enter_threshold: Optional[float] = None,
        exit_threshold: Optional[float] = None,
        btc_price_col: str = "BTC_PRICE",
        funding_col: str = "BTC_FUNDING_RATE",
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Simulates walk-forward hedging across all models for a specific forecast horizon.

        Args:
            df_forecasts: DataFrame with ['origin_idx', 'horizon', 'model', 'prob', 'realized']
            df_features: Master panel with DatetimeIndex, BTC_PRICE, and BTC_FUNDING_RATE.
            horizon: Forecast horizon to test (default 1d).
            enter_threshold: Probability threshold to enter hedge (defaults to instance setting).
            exit_threshold: Probability threshold to exit hedge (defaults to instance setting).

        Returns:
            (summary_metrics_df, daily_equity_curves_df)
        """
        th_enter = enter_threshold if enter_threshold is not None else self.enter_threshold
        th_exit = exit_threshold if exit_threshold is not None else self.exit_threshold

        sub_fc = df_forecasts[df_forecasts["horizon"] == horizon].copy()
        if sub_fc.empty:
            return pd.DataFrame(), pd.DataFrame()

        models = sub_fc["model"].unique()
        origins = sorted(sub_fc["origin_idx"].unique())

        prices = df_features[btc_price_col].values
        fundings = df_features[funding_col].values if funding_col in df_features.columns else np.zeros(len(prices))
        T = len(prices)

        records = []
        equity_dict = {}

        # 1. Unhedged Buy-and-Hold Baseline
        unhedged_equity = [self.initial_capital]
        origin_dates = []

        for i in range(len(origins) - 1):
            t_curr = origins[i]
            t_next = origins[i + 1]
            if t_next >= T:
                break

            p_curr = prices[t_curr]
            p_next = prices[t_next]
            ret_period = (p_next - p_curr) / p_curr
            unhedged_equity.append(unhedged_equity[-1] * (1.0 + ret_period))
            origin_dates.append(df_features.index[t_next])

        origin_dates.insert(0, df_features.index[origins[0]])
        equity_dict["Date"] = origin_dates
        equity_dict["Unhedged_BTC"] = unhedged_equity

        # Compute Unhedged baseline stats
        unhedged_arr = np.array(unhedged_equity)
        unhedged_ret = (unhedged_arr[-1] / unhedged_arr[0]) - 1.0
        unhedged_mdd = self._compute_max_drawdown(unhedged_arr)
        unhedged_sharpe, unhedged_sortino, unhedged_vol = self._compute_risk_adjusted_returns(unhedged_arr)

        thresh_label = f"{th_enter:.2f}" if th_enter == th_exit else f"Hyst[{th_exit:.2f}-{th_enter:.2f}]"

        records.append(
            {
                "Model": "Unhedged_Buy_and_Hold",
                "Hedge_Threshold": "N/A",
                "Total_Return_Pct": round(unhedged_ret * 100.0, 2),
                "Max_Drawdown_Pct": round(unhedged_mdd * 100.0, 2),
                "Drawdown_Reduction_Pct": 0.0,
                "Annualized_Vol_Pct": round(unhedged_vol * 100.0, 2),
                "Sharpe_Ratio": round(unhedged_sharpe, 2),
                "Sortino_Ratio": round(unhedged_sortino, 2),
                "Hedge_Days_Pct": 0.0,
                "Hedge_Flips": 0,
                "Friction_Cost_Pct": 0.0,
                "Funding_Cashflow_Pct": 0.0,
            }
        )

        # 2. Simulate for each model
        for m in models:
            m_fc = sub_fc[sub_fc["model"] == m].set_index("origin_idx")["prob"]
            hedged_equity = [self.initial_capital]

            hedge_state = False  # Is hedge currently active?
            total_friction_cash = 0.0
            total_funding_cash = 0.0
            hedge_periods = 0
            hedge_flips = 0

            for i in range(len(origins) - 1):
                t_curr = origins[i]
                t_next = origins[i + 1]
                if t_next >= T:
                    break

                prob = m_fc.get(t_curr, 0.0)

                # Schmitt-trigger hysteresis rule:
                # If currently hedged: exit only if prob drops below th_exit
                # If currently unhedged: enter only if prob meets or exceeds th_enter
                if hedge_state:
                    desired_hedge = prob >= th_exit
                else:
                    desired_hedge = prob >= th_enter

                p_curr = prices[t_curr]
                p_next = prices[t_next]
                raw_btc_ret = (p_next - p_curr) / p_curr

                # Friction incurred if hedge state changes
                friction = 0.0
                if desired_hedge != hedge_state:
                    friction = self.one_way_friction
                    total_friction_cash += hedged_equity[-1] * friction
                    hedge_flips += 1

                # Funding rate earned/paid if hedge is active
                funding_pnl = 0.0
                if desired_hedge:
                    hedge_periods += 1
                    days_elapsed = t_next - t_curr
                    if self.include_funding:
                        avg_funding_ann = float(np.mean(fundings[t_curr:t_next])) / 100.0
                        period_funding_rate = avg_funding_ann * (days_elapsed / 365.0)
                        funding_pnl = period_funding_rate
                        total_funding_cash += hedged_equity[-1] * funding_pnl

                # Portfolio return:
                if desired_hedge:
                    period_net_ret = 0.0 + funding_pnl - friction
                else:
                    period_net_ret = raw_btc_ret - friction

                hedged_equity.append(hedged_equity[-1] * (1.0 + period_net_ret))
                hedge_state = desired_hedge

            equity_dict[f"Hedged_{m}"] = hedged_equity

            h_arr = np.array(hedged_equity)
            h_ret = (h_arr[-1] / h_arr[0]) - 1.0
            h_mdd = self._compute_max_drawdown(h_arr)
            dd_reduction = unhedged_mdd - h_mdd
            h_sharpe, h_sortino, h_vol = self._compute_risk_adjusted_returns(h_arr)
            hedge_days_pct = (hedge_periods / max(len(origins) - 1, 1)) * 100.0

            records.append(
                {
                    "Model": m,
                    "Hedge_Threshold": thresh_label,
                    "Total_Return_Pct": round(h_ret * 100.0, 2),
                    "Max_Drawdown_Pct": round(h_mdd * 100.0, 2),
                    "Drawdown_Reduction_Pct": round(dd_reduction * 100.0, 2),
                    "Annualized_Vol_Pct": round(h_vol * 100.0, 2),
                    "Sharpe_Ratio": round(h_sharpe, 2),
                    "Sortino_Ratio": round(h_sortino, 2),
                    "Hedge_Days_Pct": round(hedge_days_pct, 1),
                    "Hedge_Flips": hedge_flips,
                    "Friction_Cost_Pct": round((total_friction_cash / self.initial_capital) * 100.0, 2),
                    "Funding_Cashflow_Pct": round((total_funding_cash / self.initial_capital) * 100.0, 2),
                }
            )

        summary_df = pd.DataFrame(records)
        equity_df = pd.DataFrame(equity_dict).set_index("Date")
        return summary_df, equity_df

    def sweep_thresholds(
        self,
        df_forecasts: pd.DataFrame,
        df_features: pd.DataFrame,
        thresholds: Optional[List[float]] = None,
        hysteresis_pairs: Optional[List[Tuple[float, float]]] = None,
        horizon: int = 1,
    ) -> pd.DataFrame:
        """
        Sweeps a grid of hedge thresholds and hysteresis pairs to evaluate parameter sensitivity.

        Returns:
            DataFrame containing performance across all threshold settings.
        """
        if thresholds is None:
            thresholds = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]

        if hysteresis_pairs is None:
            hysteresis_pairs = [(0.25, 0.15), (0.20, 0.12)]

        all_records = []

        # 1. Sweep single fixed thresholds
        for th in thresholds:
            df_res, _ = self.simulate(
                df_forecasts=df_forecasts,
                df_features=df_features,
                horizon=horizon,
                enter_threshold=th,
                exit_threshold=th,
            )
            # Exclude Unhedged row from duplicates
            sub_res = df_res[df_res["Model"] != "Unhedged_Buy_and_Hold"].copy()
            sub_res["Threshold_Type"] = "Fixed"
            sub_res["Param_Value"] = th
            all_records.append(sub_res)

        # 2. Test hysteresis pairs
        for enter_th, exit_th in hysteresis_pairs:
            df_res, _ = self.simulate(
                df_forecasts=df_forecasts,
                df_features=df_features,
                horizon=horizon,
                enter_threshold=enter_th,
                exit_threshold=exit_th,
            )
            sub_res = df_res[df_res["Model"] != "Unhedged_Buy_and_Hold"].copy()
            sub_res["Threshold_Type"] = "Hysteresis"
            sub_res["Param_Value"] = enter_th
            all_records.append(sub_res)

        if not all_records:
            return pd.DataFrame()

        return pd.concat(all_records, ignore_index=True)

    @staticmethod
    def _compute_max_drawdown(equity_curve: np.ndarray) -> float:
        peaks = np.maximum.accumulate(equity_curve)
        drawdowns = (peaks - equity_curve) / np.maximum(peaks, 1e-8)
        return float(np.max(drawdowns))

    @staticmethod
    def _compute_risk_adjusted_returns(
        equity_curve: np.ndarray,
        periods_per_year: float = 365.0 / 3.0,
        risk_free_rate: float = 0.04,
    ) -> Tuple[float, float, float]:
        rets = np.diff(equity_curve) / np.maximum(equity_curve[:-1], 1e-8)
        if len(rets) < 5 or np.std(rets) < 1e-8:
            return 0.0, 0.0, 0.0

        mean_ret = np.mean(rets) * periods_per_year
        vol = np.std(rets) * np.sqrt(periods_per_year)

        excess_ret = mean_ret - risk_free_rate
        sharpe = excess_ret / vol if vol > 1e-8 else 0.0

        downside_rets = rets[rets < 0]
        downside_vol = np.std(downside_rets) * np.sqrt(periods_per_year) if len(downside_rets) > 1 else vol
        sortino = excess_ret / downside_vol if downside_vol > 1e-8 else 0.0

        return float(sharpe), float(sortino), float(vol)
