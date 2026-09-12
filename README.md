# 4D-MGRFF: Cryptocurrency Systemic Risk Forecasting Framework

A specialized, mathematically rigorous implementation of the **4-Dimensional Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)** engineered for 24/7/365 continuous cryptocurrency markets, perpetual futures leverage dynamics, and cross-asset liquidity contagion.

---

## 1. Mathematical Architecture

The framework formalizes systemic cryptocurrency risk across four interconnected dimensions:

1. **Dimension 1 (Latent State $S_t$)**:
   Continuous systemic cryptocurrency stress extracted via a **Sign-Identified State-Space Model** with robust Huber Kalman filtering and Expectation-Maximization (EM) variance estimation:
   $$y_t = \Lambda S_t + \epsilon_t, \quad \epsilon_t \sim \mathcal{N}(0, R)$$
   $$S_t = \Phi S_{t-1} + \eta_t, \quad \eta_t \sim \mathcal{N}(0, Q)$$
   Subject to the strict identification anchor constraint:
   $$\lambda_{\text{DVOL}} > 0$$
   guaranteeing that surges in Bitcoin implied volatility unambiguously map to positive stress states, eliminating rotational indeterminacy and sign-inversion artifacts. State innovation variance $Q$ is estimated directly from data via EM iterations rather than arbitrary heuristics.

2. **Dimension 2 (Contemporaneous Interaction Network $A_t$)**:
   Empirical covariance network $\Sigma = \operatorname{Cov}(Z_t)$ capturing instantaneous co-movements across spot prices, perpetual funding rates, stablecoin depegging spreads, and equity/currency macro spillovers.

3. **Dimension 3 (Structural Propagation $\Pi_h$)**:
   Multi-horizon lead-lag impulse transmission based on **Generalized Impulse Response Functions (GIRF; Pesaran & Shin, 1998)**:
   $$\text{GIRF}_j(h) = \frac{\Phi^h \Sigma e_j}{\sqrt{\sigma_{jj}}}$$
   normalized such that transmission matrices $\Pi_h$ have exact unit diagonal ($\Pi_{h,jj} = 1.0$) and row-normalized coefficients $\in [-1.0, 1.0]$, avoiding unconstrained saturation artifacts.

4. **Dimension 4 (Temporal Horizon Dynamics $t+h$)**:
   Multi-step forecasting horizon evaluation for $h \in \{1, 3, 7, 14\}$ days, mapping the decay of predictability in continuous, algorithmically traded crypto markets.

---

## 2. Non-Circular Target & Point-in-Time Discipline

### 2.1 Non-Circular Drawdown Target Formulation
To avoid target circularity (e.g. using DVOL to forecast DVOL thresholds), the crisis target is defined as **realized forward maximum drawdown in Bitcoin spot price**:
$$\text{DD}_{t,h} = \max\left(0, 1 - \frac{\min_{\tau \in [t+1, t+h]} P_\tau}{P_t}\right)$$
$$\text{Target}_{t,h} = \mathbb{I}\left(\text{DD}_{t,h} \ge \theta_{t,h}^{(85)}\right)$$
where the crisis threshold $\theta_{t,h}^{(85)}$ is computed **strictly out-of-sample at each expanding-window origin $t$** using only historical training data, completely eliminating lookahead contamination.

### 2.2 Point-in-Time Database (Zero API Keys Required)
The acquisition layer ingests live and historical data from public endpoints with strict `event_time` and `publication_time` separation:
* **Deribit Public REST**: Bitcoin Implied Volatility Index (`DVOL`)
* **Binance Public REST**:
  * Spot Daily Closes: `BTCUSDT`, `ETHUSDT` (and `ETH_BTC_RATIO`)
  * Perpetual Futures 8-Hour Funding Rates: `BTC_FUNDING_RATE` (annualized %)
  * Stablecoin Parity Deviation: `STABLECOIN_DEPEG_BPS` (`USDCUSDT` deviation in bps)
* **FRED Macro Integration**: Trade-weighted USD index (`DTWEXBGS`) and S&P 500 volatility (`VIXCLS`) ingested with realistic multi-day publication lags.

---

## 3. Model Hierarchy (M0 to M7)

The backtesting tournament evaluates eight competitive probabilistic forecasting models:

| Model ID | Model Name | Description |
|---|---|---|
| **M0** | `M0_Persistence` | Naive persistence benchmark ($P_{t+h} = y_t$) |
| **M1** | `M1_Climatology` | Unconditional historical base rate reference |
| **M2** | `M2_SingleDomain` | Univariate logistic regression on DVOL |
| **M3** | `M3_ElasticNet` | Multidisciplinary Ridge/ElasticNet regularized logistic model |
| **M4** | `M4_DynamicAR` | Autoregressive model with dynamic parameter adaptation |
| **M5** | `M5_LightGBM` | 100-tree Gradient Boosted Decision Tree (LightGBM) |
| **M6** | `M6_StateSpace` | Logistic regression augmented with DGRS latent state $S_t$ (Dimension 1 isolated) |
| **M7** | `M7_Full4D` | Complete 4D Dynamic Linear Model (State $S_t$ + GIRF $\Pi_h$ + logistic calibration) |

---

## 4. Verification Battery & Scoring Rules

Models are verified strictly on out-of-sample forecasts across expanding windows:
* **Brier Score (BS)** and **Brier Skill Score (BSS)** against training-set climatology
* **Logarithmic Score** (Negative Log-Likelihood)
* **Expected Calibration Error (ECE)** with 5 equal-probability bins
* **Precision-Recall AUC (PR-AUC)** for imbalanced tail events
* **Richardson (2000) Relative Economic Value $V(\alpha)$**: A static decision-theoretic cost-loss score ($\alpha = 0.20$) measuring theoretical expense reduction on an idealized $2\times 2$ contingency matrix relative to climatology (**not** a portfolio P&L metric)
* **Diebold-Mariano (DM) Tests** with Newey-West HAC standard errors for multi-step forecasts
* **Benjamini-Hochberg False Discovery Rate (FDR)**: Corrects for multiple testing across all 28 hypothesis tests in the tournament ($q < 0.05$)
* **Block Bootstrap 95% Confidence Intervals** for BSS

---

## 5. Empirical Out-of-Sample Verification

Summary performance from the continuous rolling-origin backtest (292 origins, step size = 3 days):

| Horizon | Model | Brier Score | BSS vs Clim | 95% Bootstrap CI | PR-AUC | Rel. Value $V$ | DM Raw $p$ | FDR $q$-val | FDR Sig? |
|---|---|---|---|---|---|---|---|---|---|
| **1d** | **M4 DynamicAR** | 0.1162 | +0.0756 | `[+0.0421, +0.1074]` | 0.4294 | 0.4593 | **0.0000** | **0.0000** | **YES** ★ |
| **1d** | **M5 LightGBM** | **0.0940** | **+0.2523** | `[+0.0078, +0.4156]` | **0.5428** | **0.4767** | **0.0040** | **0.0373** | **YES** ★ |
| **1d** | `M0 Persistence` | 0.0974 | +0.2248 | `[-0.1585, +0.5181]` | 0.7039 | 0.6221 | 0.0654 | 0.3815 | No |
| **1d** | `M7 Full4D` | 0.1253 | +0.0030 | `[-0.0549, +0.0542]` | 0.1978 | 0.1163 | 0.3004 | 0.7905 | No |
| **3d** | **M4 DynamicAR** | 0.1279 | +0.0011 | `[-0.0164, +0.0226]` | 0.1725 | -0.0227 | **0.0002** | **0.0028** | **YES** ★ |
| **3d** | `M5 LightGBM` | 0.1250 | +0.0238 | `[-0.1528, +0.1867]` | 0.3584 | 0.2670 | 0.3388 | 0.7905 | No |
| **7d** | All Models | $\ge 0.1228$ | $\le -0.0146$ | — | $\le 0.3837$ | $\le 0.1646$ | $\ge 0.1675$ | $\ge 0.7817$ | No |
| **14d** | All Models | $\ge 0.1335$ | $\le -0.0238$ | — | $\le 0.2356$ | $\le -0.0056$ | $\ge 0.0991$ | $\ge 0.5550$ | No |

★ indicates statistical significance surviving Benjamini-Hochberg False Discovery Rate control ($q < 0.05$).

---

## 6. Walk-Forward Hedged P&L Simulation

To evaluate whether crash probability forecasts translate into real portfolio drawdown reduction, an out-of-sample hedging simulation was run across all 292 origins:
* **Base Portfolio**: 100% Long Bitcoin spot ($100,000 capital).
* **Overlay**: Open 1.0x short perpetual futures hedge whenever model crash probability $P_t \ge 0.20$.
* **Frictions Modeled**: Binance 5 bps taker fee + 5 bps execution slippage (10 bps round-trip) per hedge transition.
* **Funding Cash Flows**: Actual 8-hour perpetual funding payments/receipts applied daily.

| Model | Total Return | Max Drawdown | Drawdown Reduction | Annualized Vol | Sharpe Ratio | Sortino Ratio | Hedge Active | Friction Drag | Funding Cashflow |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Unhedged Buy & Hold** | **+16.48%** | **51.32%** | **0.00%** | **42.36%** | **0.26** | **0.45** | 0.0% | 0.00% | 0.00% |
| **M5 LightGBM** | **+420.69%** | **12.95%** | **+38.38%** | **31.61%** | **2.22** | **3.78** | 19.9% | -16.37% | +5.91% |
| **M4 DynamicAR** | **+353.29%** | **21.68%** | **+29.65%** | **37.07%** | **1.78** | **3.20** | 12.4% | -5.59% | +3.58% |
| `M0 Persistence` | +477.79% | 12.89% | +38.43% | 35.97% | 2.11 | 3.84 | 16.5% | -10.14% | +6.08% |
| `M7 Full4D` | +48.69% | 51.32% | 0.00% | 39.38% | 0.51 | 0.83 | 10.3% | -1.72% | +2.29% |
| `M2 SingleDomain` | +13.95% | 51.32% | 0.00% | 41.26% | 0.24 | 0.39 | 3.4% | -0.88% | +0.09% |

---

## 7. Empirical Limitations & Single-Regime Scope

1. **Regime Homogeneity**: The evaluation sample (January 2024 to September 2026) covers an ETF launch and halving secular bull/consolidation market. The model's behavior during a structural multi-year crypto winter (such as 2018 or 2022) is unverified due to public REST API historical depth limits.
2. **Horizon Boundary**: Statistical significance and positive skill collapse beyond $h=3$ days. In 24/7 continuous crypto markets, daily lead-lag signals are arbitraged within 24–72 hours.
3. **M7 Model Role**: M7 (Full 4D DLM) is ineffective as a binary directional classifier. Its utility lies in **counterfactual macro stress testing and structural contagion mapping ($\Pi_h$)**, not tactical execution.

---

## 8. Directory Layout

```
4d-crypto-risk/
├── data/
│   └── processed/
│       └── crypto_risk_database.db         # SQLite Point-in-Time Database
├── src/
│   ├── acquisition/
│   │   ├── crypto_ingestor.py              # Binance/Deribit automated fetcher
│   │   └── schema.py                       # Strict Point-in-Time schema & query_as_of
│   ├── statespace/
│   │   └── crypto_dgrs.py                  # Sign-Identified DGRS (EM Q, Huber filtering)
│   ├── models/
│   │   ├── crypto_baselines.py             # M0 Persistence & M1 Climatology
│   │   ├── crypto_statistical.py           # M2 SingleDomain, M3 ElasticNet, M4 DynamicAR
│   │   ├── crypto_nonlinear.py             # M5 LightGBM GBDT
│   │   ├── crypto_ensemble.py              # M6 State-Space Augmented Logistic
│   │   └── crypto_full_4d_dlm.py           # M7 Full 4D DLM with Generalized IRF
│   └── evaluation/
│       ├── crypto_backtest.py              # Rolling-origin tournament & rolling drawdown target
│       ├── crypto_metrics.py               # BSS, ECE, PR-AUC, DM test, Bootstrap CI, FDR
│       ├── crypto_hedge_simulation.py      # Walk-forward P&L simulator with fees & funding
│       └── crypto_plotting.py              # Dark publication-theme figures generator
├── tests/
│   ├── test_metrics.py                     # Tests for scoring rules & DM tests
│   ├── test_hedge_simulation.py            # Tests for FDR correction & hedge simulator
│   ├── test_statespace.py                  # Tests for polarity anchor & EM estimation
│   ├── test_models.py                      # Tests for M0-M7 output bounds & GIRF properties
│   ├── test_target.py                      # Tests for drawdown calculation & rolling isolation
│   └── test_schema.py                      # Tests for Point-in-Time non-leaking queries
├── results/
│   ├── tables/                             # Performance and Hedged P&L verification tables
│   └── figures/                            # Trajectory, heatmap, and equity curve figures
├── pyproject.toml                          # Project metadata & dependencies
├── run_crypto_pipeline.py                  # Master pipeline runner
└── README.md
```

---

## 9. Execution & Testing

### Run the Master Pipeline
```bash
python run_crypto_pipeline.py
```

### Run the Test Suite
```bash
python -m pytest -v
```
