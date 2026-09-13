# -*- coding: utf-8 -*-
"""
Narration Script Beats — "THE 51% ILLUSION: Why Central Bank Math Failed Crypto (And What Actually Worked)"
Official Documentary for YouTube channel @izhaanintellect.

88 Narration Beats structured across 7 Acts.
Voice: Google Gemini TTS 'Charon' (Informative, authoritative documentary voice).
Timing: Calibrated to produce a 9.0 to 9.5 minute finished film runtime (strictly within 8-10 min).
"""

# Format: (beat_id, act_index, text_to_speak, pause_after_sec)
BEATS = [
    # ------------------------------------------------------------- ACT 0: PROLOGUE & HOOK ---
    ("p_01", 0, "In cryptocurrency, surviving a crash is not about courage.", 0.4),
    ("p_02", 0, "It is about mathematical survival.", 0.5),
    ("p_03", 0, "Over the last two years, an unhedged Bitcoin investor watched their portfolio endure a devastating fifty-one point three percent maximum drawdown.", 0.5),
    ("p_04", 0, "Billions in leveraged capital evaporated within hours across global liquidation engines.", 0.4),
    ("p_05", 0, "Yet if you consult central banks and academic economists, they claim the solution has existed for decades.", 0.5),
    ("p_06", 0, "They point to Dynamic Linear State-Space Models, Kalman filters, and multidimensional contagion matrices.", 0.5),
    ("p_07", 0, "The exact mathematical architecture used by the European Central Bank and the Federal Reserve to monitor systemic collapse.", 0.6),
    ("p_08", 0, "So, we decided to do what academic papers rarely do.", 0.4),
    ("p_09", 0, "We connected this central bank math directly to live tick-by-tick feeds from Binance, Deribit, and the Federal Reserve.", 0.5),
    ("p_10", 0, "What we uncovered was a masterclass in quantitative illusion, a hidden trap of statistical circularity, and a shocking plot twist where artificial intelligence was humiliated by a one-line rule.", 0.9),

    # ------------------------------------------------ ACT 1: THE CENTRAL BANK MATH ---
    ("a1_01", 1, "To understand systemic risk, you must first understand why standard financial indicators fail.", 0.5),
    ("a1_02", 1, "Looking only at price is like looking exclusively in a rearview mirror.", 0.4),
    ("a1_03", 1, "Monitoring funding rates alone blinds you to institutional macro contagion.", 0.5),
    ("a1_04", 1, "This is why macroeconomists designed the Four-Dimensional Multidisciplinary Risk Framework.", 0.5),
    ("a1_05", 1, "Instead of viewing risk as a single number, it measures reality across four fundamental pillars.", 0.5),
    ("a1_06", 1, "First: Liquidity and microstructure—measuring order book depth and bid-ask slippage.", 0.4),
    ("a1_07", 1, "Second: Derivatives leverage—tracking perpetual funding rates and open interest velocity.", 0.4),
    ("a1_08", 1, "Third: Tail-risk volatility—incorporating Deribit thirty-day implied volatility, or DVOL.", 0.5),
    ("a1_09", 1, "And fourth: Macroeconomic spillovers—measuring Wall Street's VIX and US Treasury yields.", 0.5),
    ("a1_10", 1, "The core hypothesis is that systemic stress cannot be observed directly.", 0.5),
    ("a1_11", 1, "Like gravity or temperature, it is a latent hidden variable—denoted mathematically as S-sub-t.", 0.5),
    ("a1_12", 1, "Using an Expectation-Maximization Kalman Filter, the algorithm extracts this latent stress signal in real time.", 0.5),
    ("a1_13", 1, "To survive wild crypto flash crashes, it employs Huber-robust observation loss functions that prevent extreme outlier noise from poisoning the estimate.", 0.5),
    ("a1_14", 1, "On paper, this state-space architecture is mathematically flawless. But in finance, elegance is never a substitute for truth.", 0.9),

    # ---------------------------------------- ACT 2: THE GENERALIZED CONTAGION MATRIX ---
    ("a2_01", 2, "Once systemic stress is estimated, the central bank framework attempts its most ambitious feat: forecasting contagion pathways.", 0.5),
    ("a2_02", 2, "If a shock strikes one corner of the financial system, where does the damage travel next?", 0.5),
    ("a2_03", 2, "Traditional econometrics uses Vector Autoregression with Cholesky decomposition.", 0.4),
    ("a2_04", 2, "However, Cholesky ordering forces an arbitrary hierarchy: you must guess which asset moves first.", 0.5),
    ("a2_05", 2, "If you shuffle the order of variables, your contagion results completely change.", 0.5),
    ("a2_06", 2, "To solve this, our pipeline implements Pesaran-Shin Generalized Impulse Response Functions.", 0.5),
    ("a2_07", 2, "Generalized IRFs integrate across the entire historical covariance matrix, producing transmission coefficients that are completely invariant to variable ordering.", 0.6),
    ("a2_08", 2, "The resulting propagation matrix, Pi-sub-h, reveals fascinating empirical truths about the crypto economy.", 0.5),
    ("a2_09", 2, "First, the diagonal elements are normalized to exactly one point zero, verifying structural symmetry.", 0.5),
    ("a2_10", 2, "Second, when a panic shock strikes Wall Street's VIX, it does not strike Bitcoin spot prices first.", 0.5),
    ("a2_11", 2, "Instead, it transmits an immediate negative shock of minus zero-point-four-five directly into the Ethereum-Bitcoin ratio.", 0.5),
    ("a2_12", 2, "When macro panic hits, institutional investors flee altcoins into Bitcoin first, treating Bitcoin as the digital reserve asset before exiting into fiat cash.", 0.6),
    ("a2_13", 2, "Meanwhile, Bitcoin realized volatility feeds into Deribit options implied volatility with a massive positive coefficient of plus zero-point-five-one.", 0.5),
    ("a2_14", 2, "The contagion map was pristine. But when we used this model to trade live capital, catastrophe struck.", 0.9),

    # -------------------------------------------- ACT 3: THE TRAP OF CIRCULARITY ---
    ("a3_01", 3, "Here lies the darkest trap in quantitative financial research: statistical circularity.", 0.5),
    ("a3_02", 3, "In the original academic papers proposing this framework, the target variable was defined as: DVOL exceeding its eighty-fifth percentile.", 0.5),
    ("a3_03", 3, "Think carefully about what that means.", 0.4),
    ("a3_04", 3, "One of the most heavily weighted inputs entering the model was... Deribit DVOL.", 0.5),
    ("a3_05", 3, "The model was not predicting an economic crisis. It was predicting whether today's volatility would look like yesterday's volatility.", 0.5),
    ("a3_06", 3, "That is not predictive alpha. That is an academic tautology.", 0.6),
    ("a3_07", 3, "Worse still, previous backtests computed the eighty-fifth percentile threshold across the entire historical dataset simultaneously.", 0.5),
    ("a3_08", 3, "This allowed market conditions from twenty-twenty-six to leak into training sets evaluated in twenty-twenty-four.", 0.5),
    ("a3_09", 3, "In our audit, we dismantled this illusion completely.", 0.4),
    ("a3_10", 3, "First, we redefined the target to forward maximum drawdown of Bitcoin spot price, completely isolated from any volatility feature.", 0.5),
    ("a3_11", 3, "Second, we enforced rolling per-origin thresholds, guaranteeing zero lookahead leakage.", 0.5),
    ("a3_12", 3, "And third, we applied the Benjamini-Hochberg False Discovery Rate correction across all twenty-eight tournament hypothesis tests.", 0.5),
    ("a3_13", 3, "The result was a total statistical bloodbath.", 0.5),
    ("a3_14", 3, "Twenty-five out of twenty-eight model tests failed completely. At horizons of seven and fourteen days, every single model collapsed to zero skill.", 0.9),

    # ---------------------------------------- ACT 4: THE TRUE WALK-FORWARD HEDGE ---
    ("a4_01", 4, "Only two models survived multiple-testing correction at the one-day horizon: Autoregressive Model Four and LightGBM Model Five.", 0.5),
    ("a4_02", 4, "Now came the true test: Can statistical skill generate real-world risk protection?", 0.5),
    ("a4_03", 4, "Most backtests make a fatal assumption: zero transaction fees, zero slippage, and instant execution.", 0.5),
    ("a4_04", 4, "We built a full walk-forward trading simulator that mimics institutional capital execution.", 0.5),
    ("a4_05", 4, "The strategy holds one hundred percent Bitcoin spot.", 0.4),
    ("a4_06", 4, "Whenever the model's crash probability breaches a twenty percent threshold, it opens a one-to-one short perpetual futures hedge on Binance.", 0.5),
    ("a4_07", 4, "Crucially, every single hedge flip pays ten basis points of trading friction: five basis points taker fee, plus five basis points execution slippage.", 0.5),
    ("a4_08", 4, "And while the hedge remains open, the portfolio pays or receives actual daily perpetual funding rates.", 0.5),
    ("a4_09", 4, "The empirical results were extraordinary.", 0.4),
    ("a4_10", 4, "Unhedged Bitcoin Buy and Hold produced a modest sixteen point five percent total return, but inflicted a devastating fifty-one point three percent drawdown.", 0.5),
    ("a4_11", 4, "The Machine Learning model, LightGBM, achieved a total return of four hundred and twenty point seven percent net of all fees.", 0.5),
    ("a4_12", 4, "Its Sharpe ratio soared to two point twenty-two.", 0.4),
    ("a4_13", 4, "And most importantly: it crushed the maximum drawdown from fifty-one point three percent down to just twelve point nine-five percent.", 0.5),
    ("a4_14", 4, "A staggering thirty-eight percentage point reduction in portfolio destruction. But the simulator had one more shocking secret.", 0.9),

    # ----------------------------------- ACT 5: THE ONE-BIT TRAP & HYSTERESIS ---
    ("a5_01", 5, "When we inspected the leaderboard, Model Five had not won first place in raw return.", 0.5),
    ("a5_02", 5, "First place belonged to Model Zero: Persistence. A completely naive one-line baseline that delivered four hundred and seventy-seven percent return.", 0.5),
    ("a5_03", 5, "How could naive persistence beat artificial intelligence?", 0.4),
    ("a5_04", 5, "The answer was trading friction.", 0.4),
    ("a5_05", 5, "The machine learning model flipped between hedged and unhedged fifty-six times, burning sixteen point four percent of its capital in fee drag.", 0.5),
    ("a5_06", 5, "Whenever probability hovered near twenty percent, it whipsawed in and out of the order book.", 0.5),
    ("a5_07", 5, "Meanwhile, naive persistence stayed hedged in solid blocks, riding the well-known phenomenon of volatility clustering discovered by Benoit Mandelbrot.", 0.5),
    ("a5_08", 5, "Yet when we swept activation thresholds from ten to forty percent, an astonishing anomaly emerged.", 0.5),
    ("a5_09", 5, "Model Zero produced the exact same four hundred and seventy-seven percent return at every single threshold.", 0.5),
    ("a5_10", 5, "In the source code, at horizon one, the persistence formula collapses to an inelastic one-bit signal: emitting only zero-point-zero-one or zero-point-nine-nine.", 0.6),
    ("a5_11", 5, "Persistence is not a tunable risk model; it is an uncalibrated light switch that fails false discovery rate testing completely.", 0.5),
    ("a5_12", 5, "To fix LightGBM's churn, we implemented electrical engineering Schmitt-Trigger Hysteresis: enter the hedge above twenty-five percent, exit only below fifteen percent.", 0.6),
    ("a5_13", 5, "This simple filter eliminated ten unnecessary flips, saving nearly four percentage points in friction while locking maximum drawdown at twelve point nine-five percent.", 0.5),
    ("a5_14", 5, "And across the entire threshold sweep from ten to thirty percent, drawdown reduction forms a rock-solid thirty-eight point four percent plateau.", 0.9),

    # ------------------------------------------------ ACT 6: CODA & THE VERDICT ---
    ("c_01", 6, "So, what is the ultimate verdict on central bank math in cryptocurrency?", 0.5),
    ("c_02", 6, "The Four-Dimensional State-Space Model is useless as a binary trading trigger. It is too smooth for crypto's non-linear flash liquidations.", 0.5),
    ("c_03", 6, "However, as a structural macro stress simulator, its Generalized Impulse Response matrices are irreplaceable for institutional treasury risk.", 0.5),
    ("c_04", 6, "Second: Machine learning delivers genuine, statistically verified forecast skill—but only at the one-day horizon.", 0.5),
    ("c_05", 6, "And third: In quantitative finance, mathematical skill is worthless without execution engineering.", 0.5),
    ("c_06", 6, "Without hysteresis and transaction friction modeling, your theoretical edge will evaporate in the live order book.", 0.5),
    ("c_07", 6, "The entire framework—all thirty-one unit tests, the Point-in-Time SQLite database, and the hedge simulator—is fully open-sourced in the repository below.", 0.5),
    ("c_08", 6, "This is Izhaan Intellect. Subscribe for mathematically honest science, and we will see you in the next dimension.", 1.5),
]
