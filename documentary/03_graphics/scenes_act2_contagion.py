# -*- coding: utf-8 -*-
"""
Procedural Scene Renderers — ACT 2: THE GENERALIZED CONTAGION MATRIX (Scenes 056 - 085)
1080p 30 FPS cinematic motion graphics for @izhaanintellect.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import style_engine as SE

W, H = SE.W, SE.H


def draw_header(d, title, sub):
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT 2 // CONTAGION MATRIX")
    f_t = SE.get_font(42, bold=True)
    f_s = SE.get_font(20, mono=True)
    d.text((80, 85), title, font=f_t, fill=SE.TEXT_WHITE)
    d.text((82, 140), sub, font=f_s, fill=SE.CYAN)
    d.line([(80, 175), (W - 80, 175)], fill=SE.BORDER_CYAN, width=1)


def s_056_network_topology(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "INTER-MARKET CONTAGION TOPOLOGY", "DIRECTED NETWORK GRAPH ACROSS 7 SYSTEMIC ASSETS")

    cx, cy = W // 2, H // 2 + 20
    nodes = ["VIX", "DGS10", "BTC_PRICE", "ETH_BTC", "DVOL", "REAL_VOL", "FUNDING"]
    rad = 220
    pts = []
    for i, name in enumerate(nodes):
        ang = i * (2 * math.pi / len(nodes)) + t * 0.15
        px = cx + int(math.cos(ang) * rad)
        py = cy + int(math.sin(ang) * rad)
        pts.append((px, py, name))

    pulse_idx = int(t * 3) % len(pts)
    for i in range(len(pts)):
        for j in ((i + 1) % len(pts), (i + 3) % len(pts)):
            col = SE.GOLD if i == pulse_idx else SE.BORDER_CYAN
            w_line = 3 if i == pulse_idx else 1
            d.line([(pts[i][0], pts[i][1]), (pts[j][0], pts[j][1])], fill=col, width=w_line)

    for i, (px, py, name) in enumerate(pts):
        halo_col = SE.BG_TINT_GOLD if i == pulse_idx else SE.BG_PANEL
        outline_col = SE.GOLD if i == pulse_idx else SE.CYAN
        d.ellipse([(px - 44, py - 44), (px + 44, py + 44)], fill=halo_col, outline=outline_col, width=2)
        d.text((px - 32, py - 10), name[:7], font=SE.get_font(13, bold=True, mono=True), fill=SE.TEXT_WHITE)

    d.text((120, H - 220), "7-ASSET DIRECTED STATE GRAPH // 42 SIMULTANEOUS CROSS-TRANSMISSION CHANNELS", font=SE.get_font(18, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_057_cholesky_problem(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE CHOLESKY DECOMPOSITION TRAP", "ORTHOGONALIZED IRF IMPOSES ARBITRARY CAUSAL ORDERING")

    cx1, cx2, cy = W // 4 + 60, 3 * W // 4 - 60, H // 2 + 10
    sz = 5
    cs = 44

    d.text((cx1 - (sz * cs) // 2, cy - (sz * cs) // 2 - 40), "CHOLESKY FACTOR L (LOWER TRIANGULAR)", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    for r in range(sz):
        for c in range(sz):
            bx = cx1 - (sz * cs) // 2 + c * cs
            by = cy - (sz * cs) // 2 + r * cs
            if c > r:
                d.rectangle([bx, by, bx + cs - 4, by + cs - 4], fill=SE.BG_TINT_RED, outline=SE.DANGER_RED, width=1)
                d.text((bx + 14, by + 12), "0", font=SE.get_font(16, bold=True, mono=True), fill=SE.DANGER_RED)
            else:
                d.rectangle([bx, by, bx + cs - 4, by + cs - 4], fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)
                d.text((bx + 10, by + 12), f"L{r}{c}", font=SE.get_font(12, mono=True), fill=SE.TEXT_MUTED)

    d.text((cx2 - (sz * cs) // 2, cy - (sz * cs) // 2 - 40), "PESARAN-SHIN COVARIANCE SIGMA (FULL)", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    for r in range(sz):
        for c in range(sz):
            bx = cx2 - (sz * cs) // 2 + c * cs
            by = cy - (sz * cs) // 2 + r * cs
            d.rectangle([bx, by, bx + cs - 4, by + cs - 4], fill=SE.BG_PANEL, outline=SE.GREEN, width=1)
            d.text((bx + 8, by + 12), f"s{r}{c}", font=SE.get_font(12, mono=True), fill=SE.CYAN)

    d.text((120, H - 230), "WARNING: FORCING UPPER TRIANGLE TO ZERO ASSUMES CRYPTO ASSETS CANNOT SIMULTANEOUSLY FEED BACK.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((120, H - 200), "IN A 24/7 INTERNET SPEED MARKET, ORDERING-DEPENDENCE INTRODUCES 80% ARTIFACT ERRORS.", font=SE.get_font(16, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_058_order_permutation_error(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PERMUTATION INSTABILITY", "SHUFFLING VARIABLE ORDER ALTERS TRADITIONAL IRF BY UP TO 80%")

    d.rounded_rectangle([160, 240, W // 2 - 40, H - 240], radius=8, fill=SE.BG_PANEL, outline=SE.DANGER_RED, width=2)
    d.text((200, 280), "ORDERING A: [VIX -> BTC -> DVOL]", font=SE.get_font(22, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((200, 360), "VIX -> BTC SHOCK RESPONSE:", font=SE.get_font(18, mono=True), fill=SE.TEXT_MUTED)
    d.text((200, 410), "-0.62", font=SE.get_font(64, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((200, 500), "SEVERE IMMEDIATE SYSTEMIC CRASH", font=SE.get_font(16, mono=True), fill=SE.TEXT_WHITE)

    d.rounded_rectangle([W // 2 + 40, 240, W - 160, H - 240], radius=8, fill=SE.BG_PANEL, outline=SE.DANGER_RED, width=2)
    d.text((W // 2 + 80, 280), "ORDERING B: [BTC -> VIX -> DVOL]", font=SE.get_font(22, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W // 2 + 80, 360), "VIX -> BTC SHOCK RESPONSE:", font=SE.get_font(18, mono=True), fill=SE.TEXT_MUTED)
    d.text((W // 2 + 80, 410), "-0.12", font=SE.get_font(64, bold=True, mono=True), fill=SE.GOLD)
    d.text((W // 2 + 80, 500), "MINIMAL NEGLIGIBLE IMPACT DETECTED", font=SE.get_font(16, mono=True), fill=SE.TEXT_WHITE)

    diff_val = 0.50 + 0.05 * math.sin(t * 3.0)
    SE.draw_speedometer_gauge(d, diff_val, 0.0, 1.0, "ORDERING SENSITIVITY", "BIAS", W // 2, H // 2 + 20, 80, SE.DANGER_RED)

    d.text((160, H - 210), "SAME DATA, SAME DATES, SAME RESIDUALS — BUT DIFFERENT ORDERING FLIPS CONCLUSIONS 5X.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_059_pesaran_shin_paper(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PESARAN & SHIN (1998) BREAKTHROUGH", "GENERALIZED IMPULSE RESPONSE ANALYSIS IN LINEAR MULTIVARIATE MODELS")

    hl_prog = max(0.0, min(1.0, (t - 0.4) / max(0.1, dur * 0.7)))
    SE.draw_archival_paper(
        d,
        journal_str="JOURNAL OF ECONOMETRICS 58 (1998) 17–29",
        title_str="Generalized Impulse Response Analysis in Linear Multivariate Models",
        authors_str="M. Hashem Pesaran (Cambridge) & Yongcheol Shin (Edinburgh)",
        quote_str="The proposed approach does not require orthogonalisation of shocks and is invariant to the ordering of the variables.",
        highlight_frac=hl_prog,
        box=(140, 230, W - 140, H - 210)
    )
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_060_girf_formula_reveal(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE GENERALIZED IRF OPERATOR", "NON-ORTHOGONALIZED SHOCK PROPAGATION TENSOR")

    terms = [
        ("Pi_h", "Propagation Matrix", "Invariant cross-variable contagion tensor at forecast horizon h.", SE.CYAN),
        ("Sigma", "Covariance", "Full historical covariance matrix; integrates joint volatility shocks.", SE.GOLD),
        ("Phi_h", "VAR Dynamics", "Dynamic impulse coefficient matrix from Vector Autoregressive lag structure.", SE.GREEN),
        ("diag^-1/2", "Normalization", "Normalizes diagonal self-impacts to exactly 1.00 across all assets.", SE.DANGER_RED)
    ]
    SE.draw_formula_dissection_card(
        d, "PESARAN-SHIN (1998) ORDER-INVARIANT FORMULATION",
        "Pi_h = Sigma * Phi_h' * [diag(Sigma)]^(-1/2)",
        terms, x=160, y=230, w=W - 320, h=470
    )
    SE.draw_evidence_badge(d, 1, "ORDER INVARIANCE PROVED (7! = 5,040 ORDERINGS)", "DIAGONAL SELF-IMPACT = 1.0000")
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_061_propagation_matrix_h1(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "EMPIRICAL PROPAGATION MATRIX Pi_1 (HORIZON = 1 DAY)", "ESTIMATED FROM 970 DAYS OF LIVE CRYPTO & MACRO FEEDS")

    matrix_7x7 = [
        [1.000, -0.381, -0.245, -0.312, -0.098, -0.042, +0.210],
        [-0.120, 1.000, -0.180, -0.145, -0.065, -0.021, +0.089],
        [-0.195, -0.145, 1.000, +0.512, +0.285, +0.065, -0.142],
        [-0.210, -0.180, +0.512, 1.000, +0.340, +0.085, -0.110],
        [-0.112, -0.450, +0.312, +0.285, 1.000, +0.145, -0.085],
        [-0.040, -0.025, +0.065, +0.085, +0.145, 1.000, +0.015],
        [+0.210, +0.089, -0.142, -0.110, -0.085, +0.015, 1.000]
    ]
    labels = ["BTC", "ETH/BTC", "DVOL", "RVOL", "VIX", "10Y", "FUND"]

    SE.draw_matrix_heatmap(
        d, matrix_7x7, labels, labels,
        x=160, y=220, w=W - 320, h=H - 450,
        t=t, highlight_cell=(4, 1)
    )
    d.text((160, H - 200), "PROVEN MATHEMATICAL MAP: EMPIRICALLY REPRODUCIBLE DIRECTED SHOCK RESPONSES AT h=1.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_062_diagonal_normalization(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "DIAGONAL NORMALIZATION VERIFIED", "ALL SELF-IMPULSE DIAGONAL COEFFICIENTS EQUAL 1.0000 EXACT")

    assets = ["BTC_PRICE", "ETH_BTC", "DVOL", "REAL_VOL", "VIX", "DGS10", "FUNDING"]
    card_w = (W - 280) // 7
    for i, asset in enumerate(assets):
        bx = 140 + i * card_w
        active = (t / max(0.1, dur * 0.7)) > (i / 7)
        border_col = SE.GREEN if active else SE.BORDER_CYAN
        fill_col = SE.BG_TINT_GREEN if active else SE.BG_PANEL

        d.rounded_rectangle([bx + 4, 300, bx + card_w - 4, 520], radius=8, fill=fill_col, outline=border_col, width=2)
        d.text((bx + 12, 330), asset[:7], font=SE.get_font(14, bold=True, mono=True), fill=SE.TEXT_WHITE)
        d.text((bx + 12, 400), "1.0000", font=SE.get_font(22, bold=True, mono=True), fill=SE.GREEN if active else SE.TEXT_MUTED)
        d.text((bx + 12, 460), "LOCKED", font=SE.get_font(12, mono=True), fill=SE.CYAN if active else SE.TEXT_MUTED)

    d.text((140, H - 220), "PIPELINE VERIFICATION TEST: PASSED. DIAGONAL SELF-IMPACT = 1.0000 (0.00% ERROR).", font=SE.get_font(22, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_063_heatmap_render_h1(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "GENERALIZED CONTAGION HEATMAP", "COLOR SPECTRUM: DIVERGING NEGATIVE (RED) TO POSITIVE (GREEN)")

    matrix_7x7 = [
        [1.000, -0.381, -0.245, -0.312, -0.098, -0.042, +0.210],
        [-0.120, 1.000, -0.180, -0.145, -0.065, -0.021, +0.089],
        [-0.195, -0.145, 1.000, +0.512, +0.285, +0.065, -0.142],
        [-0.210, -0.180, +0.512, 1.000, +0.340, +0.085, -0.110],
        [-0.112, -0.450, +0.312, +0.285, 1.000, +0.145, -0.085],
        [-0.040, -0.025, +0.065, +0.085, +0.145, 1.000, +0.015],
        [+0.210, +0.089, -0.142, -0.110, -0.085, +0.015, 1.000]
    ]
    labels = ["BTC", "ETH/BTC", "DVOL", "RVOL", "VIX", "10Y", "FUND"]

    scan_col = int(t * 4) % 7
    SE.draw_matrix_heatmap(
        d, matrix_7x7, labels, labels,
        x=200, y=220, w=W - 400, h=H - 450,
        t=t, highlight_cell=(4, scan_col)
    )
    d.text((200, H - 200), "DIVERGING HEATMAP: NEGATIVE VALUES EXPAND DOWNSIDE; POSITIVE VALUES AMPLIFY SPIKES.", font=SE.get_font(18, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_064_vix_to_ethbtc_shock(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "KEY TRANSMISSION PATHWAY: VIX -> ETH/BTC", "WALL STREET EQUITY PANIC PUNISHES ALTCOIN RATIOS BY -0.45")

    vix_val = 18.0 + 17.0 * min(1.0, t * 1.5)
    SE.draw_speedometer_gauge(d, vix_val, 10.0, 45.0, "CBOE VIX SHOCK", "PTS", W // 4 + 40, H // 2 + 10, 130, SE.DANGER_RED)

    SE.draw_waveform_oscilloscope(
        d, t, 3 * W // 4 - 260, H // 2 - 130, 460, 260,
        freq=1.8, amp=55, col=SE.DANGER_RED,
        title="ETH / BTC SPREAD DISSOLUTION (-0.45)", deadband=None
    )

    cx = W // 2
    d.line([(cx - 70, H // 2 + 10), (cx + 50, H // 2 + 10)], fill=SE.GOLD, width=4)
    d.polygon([(cx + 60, H // 2 + 10), (cx + 40, H // 2 - 8), (cx + 40, H // 2 + 28)], fill=SE.GOLD)
    d.text((cx - 40, H // 2 - 35), "-0.45", font=SE.get_font(28, bold=True, mono=True), fill=SE.DANGER_RED)

    d.text((140, H - 200), "INSTITUTIONAL RISK RETREAT: WHEN TRADITIONAL EQUITIES CRASH, SPECULATIVE ALTS BLEED TO BITCOIN.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_065_institutional_flight(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE DUAL FLIGHT-TO-SAFETY PROTOCOL", "WHY BITCOIN OUTPERFORMS ALTCOINS DURING MACRO CRISES")

    flight_steps = [
        ("STAGE 1: ALTCOIN PANIC", "SPECULATIVE ALTS DUMP INTO BTC"),
        ("STAGE 2: BTC HARVESTING", "BTC EXCHANGED FOR CASH & T-BILLS"),
        ("STAGE 3: TOTAL DELEVERAGE", "COLLATERAL RETREATS TO MONEY MARKET")
    ]
    step_active = min(2, int(t * 1.5))
    SE.draw_flow_diagram(d, flight_steps, step_active, x=140, y=280, w=W - 280, h=180, t=t)

    d.rounded_rectangle([140, 500, W - 140, H - 220], radius=8, fill=SE.BG_PANEL, outline=SE.GOLD, width=2)
    d.text((180, 530), "MECHANICAL ASYMMETRY:", font=SE.get_font(22, bold=True, mono=True), fill=SE.GOLD)
    d.text((180, 570), "BTC acts as the 'crypto reserve currency' during early shockwaves, buffering losses", font=SE.get_font(20), fill=SE.TEXT_WHITE)
    d.text((180, 610), "before secondary liquidation drags spot Bitcoin downward in Stage 2.", font=SE.get_font(20), fill=SE.TEXT_WHITE)

    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_066_realized_to_implied_vol(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "VOLATILITY COUPLING: REALIZED -> DVOL (+0.51)", "DERIBIT OPTIONS VOLATILITY CONVERGING WITH SPOT SWINGS")

    SE.draw_waveform_oscilloscope(
        d, t, 160, 240, W - 320, 180,
        freq=1.4, amp=40, col=SE.GREEN,
        title="HISTORICAL REALIZED VOLATILITY (BINANCE 24H TICK)", deadband=None
    )
    SE.draw_waveform_oscilloscope(
        d, t + 0.1, 160, 460, W - 320, 180,
        freq=1.4, amp=48, col=SE.CYAN,
        title="DERIBIT DVOL 30-DAY FORWARD IMPLIED VOLATILITY (COUPLING = +0.512)", deadband=None
    )

    d.text((160, H - 200), "HIGH STRUCTURAL COUPLING (+0.512): REALIZED CRASHES TRANSMIT DIRECTLY INTO OPTIONS PREMIUMS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_067_eth_btc_price_lead(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SPOT PRICE TO RATIO SPILLOVER: -0.38", "BITCOIN CORRECTIONS AMPLIFY SPECULATIVE LOSSES IN ALTS")

    SE.draw_candlestick_chart(d, x=160, y=240, w=W // 2 - 200, h=H - 480, t=t, dur=dur, trend="bearish")
    d.text((180, 255), "BITCOIN SPOT PRICE (PULLBACK -15%)", font=SE.get_font(16, bold=True, mono=True), fill=SE.DANGER_RED)

    SE.draw_candlestick_chart(d, x=W // 2 + 40, y=240, w=W // 2 - 200, h=H - 480, t=t * 1.2, dur=dur, trend="bearish")
    d.text((W // 2 + 60, 255), "ETH / BTC CROSS RATIO (PULLBACK -28%)", font=SE.get_font(16, bold=True, mono=True), fill=SE.DANGER_RED)

    d.text((160, H - 210), "ASYMMETRIC BETA: FOR EVERY 1.0% BTC DROPS, ETH/BTC CONTRACTS BY -0.38% (CROSS SPILLOVER).", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_068_propagation_matrix_h7(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "EMPIRICAL PROPAGATION MATRIX Pi_7 (HORIZON = 7 DAYS)", "SHOCK DISSIPATION AND EQUILIBRIUM CONVERGENCE")

    matrix_h7 = [
        [0.420, -0.082, -0.045, -0.062, -0.018, -0.012, +0.035],
        [-0.025, 0.380, -0.030, -0.025, -0.015, -0.008, +0.012],
        [-0.040, -0.025, 0.450, +0.095, +0.052, +0.012, -0.024],
        [-0.035, -0.028, +0.095, 0.410, +0.060, +0.015, -0.018],
        [-0.020, -0.075, +0.052, +0.060, 0.440, +0.025, -0.015],
        [-0.008, -0.005, +0.012, +0.015, +0.025, 0.510, +0.005],
        [+0.035, +0.012, -0.024, -0.018, -0.015, +0.005, 0.480]
    ]
    labels = ["BTC", "ETH/BTC", "DVOL", "RVOL", "VIX", "10Y", "FUND"]

    SE.draw_matrix_heatmap(
        d, matrix_h7, labels, labels,
        x=200, y=220, w=W - 400, h=H - 450,
        t=t, highlight_cell=None
    )
    d.text((200, H - 200), "DAMPENING DYNAMICS: BY DAY 7, CROSS-ASSET SHOCK SPILLOVERS SUBSIDE BELOW 0.10.", font=SE.get_font(18, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_069_horizon_decay_dynamics(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "IRF TEMPORAL DECAY CURVE", "HALF-LIFE OF INTER-EXCHANGE SYSTEMIC SHOCKS = 48 TO 72 HOURS")

    pts = []
    x_start, x_end = 180, W - 220
    y_base = H - 260
    for h in range(1, 15):
        x = x_start + int((h - 1) * (x_end - x_start) / 13)
        decay_val = math.exp(-(h - 1) * 0.28)
        y = y_base - int(decay_val * 320)
        pts.append((x, y))

    if len(pts) > 1:
        d.line(pts, fill=SE.CYAN, width=4)
        for (x, y) in pts:
            d.ellipse([(x - 5, y - 5), (x + 5, y + 5)], fill=SE.GOLD, outline=SE.TEXT_WHITE)

    hl_x = x_start + int(2 * (x_end - x_start) / 13)
    d.line([(hl_x, 260), (hl_x, y_base)], fill=SE.DANGER_RED, width=2)
    d.text((hl_x + 15, 300), "HALF-LIFE TAU = 48 - 72H", font=SE.get_font(20, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((hl_x + 15, 335), "SHOCK DISSIPATES BY 50%", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)

    d.text((180, H - 200), "ANALYTIC HALF-LIFE: tau = ln(2) / lambda ~= 2.47 DAYS. FAST EQUILIBRATION DISCOURAGES LONG-TERM TIMING.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_070_no_saturation_artifacts(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "NUMERICAL INTEGRITY: ZERO SATURATION", "PREVENTING ARTIFICIAL +/-0.99 CLIPPING IN EIGENSPACE")

    categories = ["MAX COEFF", "MIN COEFF", "SPECTRAL RAD", "COND NUM / 10", "RESIDUAL COV"]
    values = [0.51, 0.45, 0.68, 0.35, 0.42]
    colors = [SE.CYAN, SE.DANGER_RED, SE.GOLD, SE.GREEN, SE.BORDER_CYAN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=1.0,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "NUMERICAL PROOF: EIGENVALUES STRICTLY BOUNDED IN STABLE UNIT DISK [|lambda| <= 0.682 < 1.0].", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_071_tesseract_unfolding(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "UNFOLDING 4D NETWORKS (CORPUS HYPERCUBUS)", "MAPPING 8 BOUNDING 3-CELLS INTO SYSTEMIC GRAPH NODES")

    scale = int(220 + 20 * math.sin(t * 1.5))
    SE.render_tesseract_frame(im, d, t * 1.2, cx=W // 2, cy=H // 2 + 20, scale=scale)

    d.text((W // 2 - 320, H - 200), "CORPUS HYPERCUBUS PROJECTION // 16 VERTICES, 32 EDGES, 24 FACES, 8 CUBES", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_072_clifford_torus_motion(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "CLIFFORD TORUS ISOMETRY", "SURFACE OF CONSTANT CURVATURE IN 4-SPACE DYNAMICS")

    scale = int(240 + 25 * math.cos(t * 1.8))
    SE.render_tesseract_frame(im, d, t * 1.8, cx=W // 2, cy=H // 2 + 20, scale=scale)

    d.text((W // 2 - 280, H - 200), "FLAT RIEMANNIAN METRIC: EMBEDDING 4-VARIATE RISK SURFACES INTO R^4", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_073_liquidity_drain_pathway(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE LIQUIDITY VORTEX", "OPTIONS MARKET MAKERS WITHDRAWING SPOT BIDS")

    SE.draw_orderbook_depth(d, x=180, y=240, w=W - 360, h=H - 480, t=t)

    d.text((180, H - 200), "SPREAD EXPLOSION: AS DVOL SPIKES, TOP-OF-BOOK SPREAD BLOWS OUT FROM 5 BPS TO 80 BPS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_074_deribit_delta_hedging(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "NEGATIVE GAMMA CONTAGION", "DYNAMIC DELTA HEDGING ACCELERATING SPOT DOWNSIDE CASCADES")

    stages = [
        "SPOT PRICE DROPS",
        "DEALERS SHORT GAMMA",
        "DELTA SALES ACCELERATE",
        "ORDERBOOK THINS OUT"
    ]
    SE.draw_circular_feedback_loop(d, stages, t=t, cx=W // 2, cy=H // 2 + 20, radius=180)

    d.text((160, H - 200), "FEEDBACK SPIRAL: OPTIONS DEALERS MUST MECHANICALLY DUMP UNDERLYING DELTA AS SPOT FALLS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_075_funding_inversion_cue(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "FUNDING INVERSION SIGNALS", "PERP BASIS DIPS NEGATIVE: RETAIL AGGRESSIVELY PANIC SHORTS")

    SE.draw_waveform_oscilloscope(
        d, t, 180, 250, W - 360, 240,
        freq=1.6, amp=60, col=SE.DANGER_RED,
        title="BINANCE BTCUSDT PERPETUAL 8-HOUR FUNDING RATE (INVERTING NEGATIVE)", deadband=None
    )

    d.text((180, H - 210), "WHEN PERPETUAL BASIS GOES DEEP NEGATIVE, HEDGERS EARN CASH FLOWS TO REMAIN PROTECTED.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_076_the_macro_anchor(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE MACRO GRAVITATIONAL ANCHOR", "US TREASURY YIELDS SETTING THE LIQUIDITY TIDE FOR ALL SPECULATION")

    y_val = 4.10 + 0.55 * min(1.0, t * 1.2)
    SE.draw_speedometer_gauge(d, y_val, 3.5, 5.2, "10Y US TREASURY (DGS10)", "%", W // 4 + 40, H // 2 + 10, 130, SE.GOLD)

    liq_val = 82.0 - 45.0 * min(1.0, t * 1.2)
    SE.draw_speedometer_gauge(d, liq_val, 20.0, 100.0, "CRYPTO SPECULATIVE LIQUIDITY", "INDEX", 3 * W // 4 - 40, H // 2 + 10, 130, SE.CYAN)

    d.text((180, H - 200), "WHEN 10-YEAR YIELDS SURGE, RISK-FREE COST OF CAPITAL SOARS, TRIGGERING CRYPTO REDEMPTIONS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_077_contagion_summary_card(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "STRUCTURAL CONTAGION ENGINE CERTIFIED", "PESARAN-SHIN Pi_h MATRIX VALIDATED AS RIGOROUS RISK MAP")

    categories = ["EIGEN VALUE STABILITY", "PERMUTATION INVARIANCE", "MICRO-CROSS COUPLING", "MACRO INTEGRATION"]
    values = [0.94, 1.00, 0.88, 0.91]
    SE.draw_radar_spider_chart(d, categories, values, W // 2, H // 2 + 20, 180, t, col=SE.CYAN, label="CONTAGION FIDELITY")

    d.text((W // 2 - 320, H - 200), "MATHEMATICALLY SOUND: AN OBJECTIVE, ORDERING-FREE RISK PROPAGATION ENGINE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_078_the_academic_confidence(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE ILLUSION OF SCIENTIFIC TRIUMPH", "THE EQUATIONS MATCHED THEORY... SO WE PREPARED TO TRADE")

    steps = [
        ("STAGE 1: ECONOMIC THEORY", "PESARAN-SHIN 1998"),
        ("STAGE 2: MATRIX CALIBRATION", "970 DAYS OF TICKS"),
        ("STAGE 3: IMPULSE VALIDATION", "ZERO ORDERING BIAS"),
        ("STAGE 4: TRADING EXECUTION", "PREPARING HEDGES")
    ]
    step_active = min(3, int(t * 1.8))
    SE.draw_flow_diagram(d, steps, step_active, x=120, y=300, w=W - 240, h=180, t=t)

    d.text((120, H - 210), "\"WE HAVE A 4D CONTAGION TENSOR. NOW LET US CONVERT IT INTO A PROFITABLE HEDGE.\"", font=SE.get_font(20, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_079_trading_signal_conversion(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "CONVERTING STRUCTURAL TENSORS INTO TRADES", "ESTIMATING EXCEEDANCE PROBABILITY P(CRASH) IN NEXT h DAYS")

    cx, cy = W // 2, H // 2 + 30
    w_curve, h_curve = 700, 260
    d.rounded_rectangle([cx - w_curve // 2, cy - h_curve // 2, cx + w_curve // 2, cy + h_curve // 2], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)

    pts = []
    x0, x1 = cx - w_curve // 2 + 40, cx + w_curve // 2 - 40
    y_base = cy + h_curve // 2 - 30
    for i in range(100):
        x = x0 + int(i * (x1 - x0) / 99)
        z = (i - 30) / 18.0
        dens = math.exp(-0.5 * z * z)
        y = y_base - int(dens * 180)
        pts.append((x, y))

    if len(pts) > 1:
        d.line(pts, fill=SE.CYAN, width=3)

    th_x = x0 + int(50 * (x1 - x0) / 99)
    d.line([(th_x, cy - h_curve // 2 + 20), (th_x, y_base)], fill=SE.DANGER_RED, width=2)
    d.text((th_x + 10, cy - h_curve // 2 + 30), "CRITICAL THRESHOLD theta = 0.20", font=SE.get_font(16, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((th_x + 10, cy - h_curve // 2 + 60), "P(CRASH >= 85TH PCT) -> HEDGE ACTIVE", font=SE.get_font(13, mono=True), fill=SE.GOLD)

    d.text((140, H - 200), "DECISION RULE: WHEN POSTERIOR PROBABILITY EXCEEDS 20%, TRIGGER 1.0X SHORT DERIVATIVES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_080_live_test_launch(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "TOURNAMENT LAUNCH: 8 MODELS IN THE ARENA", "M0 PERSISTENCE TO M7 FULL 4D DLM ACROSS 292 EXPANDING WINDOWS")

    d.rounded_rectangle([140, 240, W - 140, H - 260], radius=10, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
    d.text((180, 280), "WALK-FORWARD ROLLING TIMELINE // 292 RE-ESTIMATIONS", font=SE.get_font(22, bold=True, mono=True), fill=SE.CYAN)

    t_prog = min(1.0, t / max(0.1, dur * 0.8))
    cur_origin = int(1 + 291 * t_prog)
    d.text((180, 360), f"ORIGIN T_0: {cur_origin:03d} / 292", font=SE.get_font(52, bold=True, mono=True), fill=SE.GOLD)

    bar_w = W - 360
    d.rectangle([180, 460, 180 + bar_w, 485], fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)
    d.rectangle([180, 460, 180 + int(bar_w * t_prog), 485], fill=SE.CYAN)

    d.text((180, 520), "MODELS EVALUATED: M0, M1, M2, M3, M4, M5, M6, M7 // 4 HORIZONS (1d, 3d, 7d, 14d)", font=SE.get_font(18, mono=True), fill=SE.TEXT_WHITE)
    d.text((180, H - 210), "ZERO LOOKAHEAD LEAKAGE: ALL HYPERPARAMETERS AND THRESHOLDS LOCKED STRICTLY AS-OF T_0.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_081_first_results_shock(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE INITIAL LEADERBOARD SHOCK", "M2 SINGLE-DOMAIN LOGISTIC CLAIMS BRIER SKILL SCORE = +0.322")

    categories = ["M0 PERSIST", "M1 UNCOND", "M2 LOGISTIC", "M3 MULTI-LOG", "M4 DYN-AR", "M5 LIGHTGBM", "M6 2D-DLM", "M7 4D-DLM"]
    values = [0.08, 0.00, 0.322, 0.14, 0.18, 0.25, 0.02, 0.03]
    colors = [SE.TEXT_MUTED, SE.TEXT_MUTED, SE.GREEN, SE.TEXT_MUTED, SE.CYAN, SE.GOLD, SE.TEXT_MUTED, SE.DANGER_RED]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=0.40,
        x=160, y=240, w=W - 320, h=H - 480,
        t=t, dur=dur, colors=colors
    )
    d.text((160, H - 200), "ANOMALY: M2 (A SIMPLE SINGLE-VARIABLE LOGISTIC) APPARENTLY CRUSHED THE 4D CENTRAL BANK MODEL.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_082_suspicion_arises(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SCIENTIFIC SKEPTICISM", "WHY WOULD A NAIVE 1-VARIABLE MODEL BEAT A 4-DIMENSIONAL MANIFOLD?")

    categories = ["DATA COMPLEXITY", "THEORETICAL RIGOR", "FEATURE DIVERSITY", "REPORTED SKILL"]
    values_m2 = [0.20, 0.15, 0.15, 0.95]
    values_m7 = [0.90, 0.95, 0.92, 0.12]

    SE.draw_radar_spider_chart(d, categories, values_m2, W // 4 + 40, H // 2 + 10, 130, t, col=SE.DANGER_RED, label="M2 LOGISTIC")
    SE.draw_radar_spider_chart(d, categories, values_m7, 3 * W // 4 - 40, H // 2 + 10, 130, t, col=SE.CYAN, label="M7 4D-DLM")

    d.text((140, H - 200), "AN UNCOMFORTABLE DISCREPANCY: EITHER OCCAM'S RAZOR IS EXTREME... OR THE METHODOLOGY IS RIGGED.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_083_code_audit_begins(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "FORENSIC CODE INSPECTION", "DISSECTING TARGET VARIABLE DEFINITIONS IN SRC/MODELS")

    term_bg = (245, 248, 252) if SE.THEME == "LIGHT" else (10, 15, 22)
    title_bg = (230, 238, 248) if SE.THEME == "LIGHT" else (18, 28, 44)
    term_border = (200, 215, 235) if SE.THEME == "LIGHT" else SE.CYAN

    d.rounded_rectangle([140, 230, W - 140, H - 230], radius=8, fill=term_bg, outline=term_border, width=2)
    d.rectangle([140, 230, W - 140, 275], fill=title_bg)
    d.ellipse([(160, 246), (174, 260)], fill=SE.DANGER_RED)
    d.ellipse([(184, 246), (198, 260)], fill=SE.GOLD)
    d.ellipse([(208, 246), (222, 260)], fill=SE.GREEN)
    d.text((245, 243), "src/models/crypto_tournament.py — Target Variable Extraction Audit", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)

    lines = [
        ("def construct_crisis_labels(df, quantile=0.85):", SE.CYAN),
        ("    # Auditing feature input matrix:", SE.TEXT_MUTED),
        ("    X = df[['DVOL', 'BTC_PRICE', 'REAL_VOL', 'VIX']].values", SE.TEXT_WHITE),
        ("    ", SE.TEXT_WHITE),
        ("    # Inspecting target variable formulation line by line...", SE.GOLD),
        ("    # Scan beam active on line 42", SE.DANGER_RED)
    ]
    for idx, (txt, col) in enumerate(lines):
        d.text((180, 310 + idx * 42), txt, font=SE.get_font(22, mono=True), fill=col)

    d.text((180, H - 200), "LINE-BY-LINE REVERSE ENGINEERING: VERIFYING HOW Y_t WAS LABELED ACROSS THE TRAINING SET.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_084_smoking_gun_found(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE SMOKING GUN: CIRCULARITY DETECTED", "y = (dvol >= quantile(0.85)) // PREDICTING DVOL WITH DVOL")

    pulse_col = SE.DANGER_RED if int(t * 4) % 2 == 0 else (255, 100, 100)
    d.rounded_rectangle([160, 240, W - 160, 480], radius=10, fill=SE.BG_TINT_RED, outline=pulse_col, width=3)
    d.text((200, 270), "CRITICAL METHODOLOGICAL BUG UNCOVERED:", font=SE.get_font(22, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((200, 330), "y_target = (df['DVOL'] >= df['DVOL'].quantile(0.85))", font=SE.get_font(36, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((200, 410), "FATAL FLAW: PREDICTING DERIBIT DVOL USING DERIBIT DVOL AS THE MAIN REGRESSOR!", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)

    d.rounded_rectangle([160, 510, W - 160, H - 230], radius=8, fill=SE.BG_PANEL, outline=SE.GOLD, width=1)
    d.text((200, 535), "THE ILLUSION EXPLAINED:", font=SE.get_font(20, bold=True, mono=True), fill=SE.GOLD)
    d.text((200, 570), "Because volatility is highly autocorrelated, the model merely predicted that high volatility", font=SE.get_font(20), fill=SE.TEXT_WHITE)
    d.text((200, 605), "persists into the next day — an obvious tautology offering zero forward hedging alpha.", font=SE.get_font(20), fill=SE.TEXT_WHITE)

    d.text((160, H - 200), "A STATISTICAL MIRAGE: ACADEMIC FINANCE TEEMS WITH PAPERS THAT FALL INTO THIS EXACT TRAP.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_085_act3_transition(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT III // THE CIRCULARITY TRAP")

    cx, cy = W // 2, H // 2
    d.text((cx - 420, cy - 60), "ACT III: THE TRAP OF CIRCULARITY", font=SE.get_font(52, bold=True), fill=SE.TEXT_WHITE)
    d.text((cx - 380, cy + 30), "HOW ACADEMIC FINANCE TRICKS ITSELF & THE FDR MASSACRE", font=SE.get_font(24, mono=True), fill=SE.CYAN)
    d.line([(cx - 420, cy + 85), (cx + 420, cy + 85)], fill=SE.BORDER_CYAN, width=2)

    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
