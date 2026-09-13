# -*- coding: utf-8 -*-
"""
Procedural Scene Renderers — ACT 1: THE CENTRAL BANK MATH (Scenes 026 - 055)
1080p 30 FPS cinematic motion graphics for @izhaanintellect.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import style_engine as SE

W, H = SE.W, SE.H


def draw_header(d, title, sub):
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT 1 // CENTRAL BANK MATH")
    f_t = SE.get_font(42, bold=True)
    f_s = SE.get_font(20, mono=True)
    d.text((80, 85), title, font=f_t, fill=SE.TEXT_WHITE)
    d.text((82, 140), sub, font=f_s, fill=SE.CYAN)
    d.line([(80, 175), (W - 80, 175)], fill=SE.BORDER_CYAN, width=1)


def s_026_four_pillars_grid(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE FOUR MULTIDISCIPLINARY PILLARS", "SIMULTANEOUS CROSS-DOMAIN OBSERVATION")

    # 4-Pillar animated radar profile
    SE.draw_radar_spider_chart(
        d,
        ["MICROSTRUCTURE", "DERIVATIVES", "TAIL VOL", "MACRO YIELDS"],
        [0.88, 0.75, 0.92, 0.65],
        W//2, H//2 + 30, 180, t,
        col=SE.CYAN,
        label="4D-MGRFF SPIDER PROFILE"
    )

    # Corner metric summaries
    d.text((120, 240), "PILLAR I: BINANCE L2 DEPTH", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    d.text((120, 270), "BID/ASK SPREAD & SLIPPAGE", font=SE.get_font(14, mono=True), fill=SE.TEXT_MUTED)

    d.text((W - 400, 240), "PILLAR II: PERP BASIS", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    d.text((W - 400, 270), "8H FUNDING CASH FLOWS", font=SE.get_font(14, mono=True), fill=SE.TEXT_MUTED)

    d.text((120, H - 220), "PILLAR III: DERIBIT DVOL", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((120, H - 190), "FORWARD IMPLIED VOLATILITY", font=SE.get_font(14, mono=True), fill=SE.TEXT_MUTED)

    d.text((W - 400, H - 220), "PILLAR IV: CBOE & FRED", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    d.text((W - 400, H - 190), "VIX FEAR + 10Y TREASURY", font=SE.get_font(14, mono=True), fill=SE.TEXT_MUTED)
    return im


def s_027_pillar_1_liquidity(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PILLAR 1 // ORDERBOOK DEPTH & MICROSTRUCTURE", "BINANCE SPOT LEVEL 2 DEPTH ASYMMETRY")

    # Real-time Level 2 orderbook depth curve
    SE.draw_orderbook_depth(d, 120, 240, W - 240, 420, t)

    d.rounded_rectangle([W - 680, 260, W - 140, 360], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN)
    d.text((W - 650, 280), "AS-OF DEPTH SUMMARY:", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    d.text((W - 650, 315), "Bid liquidity vaporizes 4.2x faster than asks during panic.", font=SE.get_font(16), fill=SE.TEXT_WHITE)
    return im


def s_028_pillar_2_derivatives(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PILLAR 2 // DERIVATIVES LEVERAGE VELOCITY", "BINANCE BTCUSDT 8-HOUR PERPETUAL FUNDING RATE")

    # Oscilloscope showing funding rate oscillations and negative spikes
    SE.draw_waveform_oscilloscope(
        d, t, 120, 240, W - 240, 420,
        freq=1.4, amp=0.8, col=SE.GOLD,
        title="8-HOUR PERPETUAL FUNDING RATE OSCILLATION",
        deadband=(-0.35, 0.35)
    )

    d.text((150, H - 190), "NEUTRAL THRESHOLD (0.01%)  //  EXTREME FLUSH (-0.048%)", font=SE.get_font(20, bold=True, mono=True), fill=SE.GOLD)
    return im


def s_029_pillar_3_volatility(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PILLAR 3 // DERIBIT 30-DAY DVOL (IMPLIED VOLATILITY)", "FORWARD OPTION-IMPLIED 30-DAY VARIANCE")

    # Live DVOL gauge with sweeping needle
    dvol_val = 74.5 + math.sin(t * 3.5) * 18.0
    SE.draw_speedometer_gauge(d, dvol_val, 30.0, 130.0, "DERIBIT 30D DVOL", unit=" VOL", cx=W//2, cy=H//2 + 20, radius=170, col=SE.DANGER_RED)

    d.rounded_rectangle([180, H - 230, W - 180, H - 150], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN)
    d.text((220, H - 205), "OPTION SKEW ALERT: Massive put skew premium signals institutional delta hedging.", font=SE.get_font(22, mono=True), fill=SE.TEXT_WHITE)
    return im


def s_030_pillar_4_macro(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PILLAR 4 // MACROECONOMIC SPILLOVER ANCHOR", "CBOE VIXCLS + 10-YEAR US TREASURY CONSTANT MATURITY")

    # Dual live macro gauges
    vix_val = 38.57 + math.sin(t * 2.5) * 4.0
    yield_val = 4.28 + math.cos(t * 2.0) * 0.15
    SE.draw_speedometer_gauge(d, vix_val, 10.0, 60.0, "CBOE VIX INDEX", unit=" PTS", cx=W//4 + 40, cy=H//2 + 30, radius=140, col=SE.CYAN)
    SE.draw_speedometer_gauge(d, yield_val, 2.0, 6.0, "10Y US TREASURY", unit=" %", cx=3*W//4 - 40, cy=H//2 + 30, radius=140, col=SE.GOLD)

    d.text((W//4 - 100, H - 200), "WALL STREET FEAR GAUGE", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_MUTED)
    d.text((3*W//4 - 180, H - 200), "GLOBAL RISK-FREE DISCOUNT RATE", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_MUTED)
    return im


def s_031_latent_state_concept(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE UNOBSERVABLE FEVER: LATENT STATE S_t", "LIKE BODY TEMPERATURE: OBSERVABLE VIA SYMPTOMS")

    cx, cy = W//2, H//2 + 20
    # Core glowing latent node
    pulse = (math.sin(t * 4.0) + 1.0) * 0.5
    r = int(70 + pulse * 20)
    d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(30, 80, 120), outline=SE.CYAN, width=3)
    d.text((cx - 30, cy - 15), "S_t", font=SE.get_font(36, bold=True, mono=True), fill=SE.TEXT_WHITE)

    # Radiating symptom arrows
    symp = ["FUNDING", "DVOL", "VIX", "DEPTH"]
    for i, s in enumerate(symp):
        ang = i * (math.pi / 2) + (math.pi / 4)
        px = cx + int(math.cos(ang) * 220)
        py = cy + int(math.sin(ang) * 220)
        d.line([(cx, cy), (px, py)], fill=SE.BORDER_CYAN, width=2)
        d.ellipse([(px - 40, py - 40), (px + 40, py + 40)], fill=SE.BG_PANEL, outline=SE.GOLD)
        d.text((px - 32, py - 10), s, font=SE.get_font(15, bold=True, mono=True), fill=SE.TEXT_WHITE)
    return im


def s_032_kalman_prediction(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "KALMAN STEP 1: A-PRIORI TIME UPDATE", "PROJECTING STATE COVARIANCE FORWARD INTO UNCERTAINTY")

    # Animated covariance ellipse projection
    cx, cy = W//2 - 200, H//2 + 40
    # Prior state ellipse at t-1
    d.ellipse([(cx - 80, cy - 50), (cx + 80, cy + 50)], outline=SE.BORDER_CYAN, width=2)
    d.text((cx - 40, cy - 10), "x_{t-1|t-1}", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_MUTED)

    # Projected forward state at t
    prog = min(1.0, t * 1.4)
    target_x = cx + int(prog * 450)
    target_y = cy - int(math.sin(prog * math.pi) * 60)
    # Expanding uncertainty envelope
    rx = int(80 + prog * 60)
    ry = int(50 + prog * 40)
    d.line([(cx, cy), (target_x, target_y)], fill=SE.GOLD, width=3)
    d.ellipse([(target_x - rx, target_y - ry), (target_x + rx, target_y + ry)], fill=SE.BG_TINT_BLUE, outline=SE.CYAN, width=2)
    d.ellipse([(target_x - 6, target_y - 6), (target_x + 6, target_y + 6)], fill=SE.CYAN)
    d.text((target_x - 45, target_y - 12), "x_{t|t-1}", font=SE.get_font(20, bold=True, mono=True), fill=SE.TEXT_WHITE)

    # Formula badge
    d.rounded_rectangle([W - 640, 240, W - 100, 420], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN)
    d.text((W - 610, 260), "STATE PROJECTION EQUATION:", font=SE.get_font(16, bold=True, mono=True), fill=SE.GOLD)
    d.text((W - 610, 295), "x_{t|t-1} = G_{t} x_{t-1|t-1}", font=SE.get_font(28, bold=True, mono=True), fill=SE.TEXT_WHITE)
    d.text((W - 610, 350), "P_{t|t-1} = G P G^T + Q_t", font=SE.get_font(24, bold=True, mono=True), fill=SE.CYAN)
    return im


def s_033_kalman_innovation(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "KALMAN STEP 2: MEASUREMENT INNOVATION", "THE DIFFERENCE BETWEEN WHAT WAS PREDICTED AND REALITY")

    # Oscilloscope showing actual market feed vs prior prediction
    x0, y0, w0, h0 = 120, 240, W - 240, 420
    d.rounded_rectangle([x0, y0, x0 + w0, y0 + h0], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)

    pts_pred = []
    pts_actual = []
    cy = y0 + h0 // 2
    n_pts = 70
    revealed = min(n_pts, int((t / max(0.1, dur * 0.8)) * n_pts) + 2)

    for i in range(revealed):
        px = x0 + 40 + int(i * (w0 - 80) / n_pts)
        frac = i / n_pts
        y_p = cy - int(math.sin(frac * math.pi * 3.0 + t * 2.0) * 90)
        # Actual has unexpected jump / shock
        shock = 80 if (25 < i < 45) else 0
        y_a = y_p - shock + int(math.cos(i * 0.8) * 15)
        pts_pred.append((px, y_p))
        pts_actual.append((px, y_a))
        # Draw vertical innovation vector error lines
        if i % 6 == 0:
            d.line([(px, y_p), (px, y_a)], fill=SE.DANGER_RED, width=2)

    if len(pts_pred) > 1:
        d.line(pts_pred, fill=SE.CYAN, width=2)
        d.line(pts_actual, fill=SE.GOLD, width=3)

    d.text((x0 + 60, y0 + 30), "ACTUAL MARKET SENSOR y_t (GOLD)", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    d.text((x0 + 60, y0 + 60), "PRIOR MODEL PREDICTION F_t x_{t|t-1} (CYAN)", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    d.text((x0 + 60, y0 + 90), "INNOVATION RESIDUAL v_t (RED SPREAD)", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    return im


def s_034_kalman_gain(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "KALMAN STEP 3: OPTIMAL KALMAN GAIN K_t", "BALANCING SENSOR TRUST AGAINST PROCESS UNCERTAINTY")

    terms = [
        ("K_t", "Optimal Gain", "Determines how heavily latent stress S_t updates from today's market feed.", SE.CYAN),
        ("P_prior", "State Variance", "Estimated uncertainty of prior latent stress estimate before observing today's price.", SE.GOLD),
        ("F_t", "Factor Loadings", "Observation matrix linking latent stress S_t to the 4 observable market pillars.", SE.GREEN),
        ("R_t", "Sensor Noise", "Observation error covariance; during flash crashes, Huber loss expands R_t to filter noise.", SE.DANGER_RED)
    ]
    SE.draw_formula_dissection_card(
        d, "DYNAMIC KALMAN FILTER GAIN EQUATION",
        "K_t = P_{t|t-1} * F_t' * [F_t * P_{t|t-1} * F_t' + R_t]^(-1)",
        terms, x=160, y=230, w=W - 320, h=470
    )
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_035_huber_robustness_curve(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "HUBER M-ESTIMATION LOSS FUNCTION", "SMOOTH L2 QUADRATIC CORE TRANSITIONING TO ROBUST L1 LINEAR TAILS")
    SE.draw_waveform_oscilloscope(d, t, 180, 240, W - 360, H - 480, freq=1.4, amp=45, col=SE.CYAN, title="HUBER PSEUDO-RESIDUALS // CLAMPED LEVERAGE POINTS")
    d.text((180, H - 200), "OUTLIER RESISTANCE: FLASH CRASHES CANNOT ROTATE LATENT TRAJECTORIES UNBOUNDEDLY.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
def _old_s_035(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "HUBER ROBUST LOSS ADAPTATION", "SUPPRESSING LEVERAGE FLASH-CRASH OUTLIER SHOCKS")

    # Plot Huber loss curve vs Quadratic
    cx, cy = W//2, H//2 + 50
    pts_quad = []
    pts_huber = []
    for x in range(-300, 301, 5):
        val_x = x / 100.0
        y_q = cy - int((val_x ** 2) * 40)
        pts_quad.append((cx + x, max(220, y_q)))
        k = 1.35
        if abs(val_x) <= k:
            loss_h = 0.5 * (val_x ** 2)
        else:
            loss_h = k * abs(val_x) - 0.5 * (k ** 2)
        y_h = cy - int(loss_h * 55)
        pts_huber.append((cx + x, max(220, y_h)))

    d.line(pts_quad, fill=SE.DANGER_RED, width=2)
    d.line(pts_huber, fill=SE.GREEN, width=4)
    d.text((cx + 120, 260), "QUADRATIC LOSS (EXPLODES ON FLASH CRASHES)", font=SE.get_font(18, mono=True), fill=SE.DANGER_RED)
    d.text((cx + 120, 320), "HUBER LOSS (LINEAR RESISTANCE TO OUTLIERS)", font=SE.get_font(18, mono=True), fill=SE.GREEN)
    return im


def s_036_em_q_estimation(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "EXPECTATION-MAXIMIZATION Q ESTIMATION", "ESTIMATING INNOVATION COVARIANCE ITERATIVELY")

    # Animated EM log-likelihood convergence curve
    x0, y0, w0, h0 = 140, 240, W - 280, 420
    d.rounded_rectangle([x0, y0, x0 + w0, y0 + h0], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)

    pts_ll = []
    revealed = min(14, int((t / max(0.1, dur * 0.8)) * 14) + 1)
    for it in range(revealed):
        px = x0 + 80 + int(it * (w0 - 160) / 14)
        # Log likelihood climbing to maximum
        ll = -1200.0 + (850.0 * (1.0 - math.exp(-it * 0.45)))
        py = y0 + h0 - 70 - int((ll + 1200.0) / 900.0 * 280)
        pts_ll.append((px, py))

    if len(pts_ll) > 1:
        d.line(pts_ll, fill=SE.GREEN, width=4)
        for px, py in pts_ll:
            d.ellipse([(px - 5, py - 5), (px + 5, py + 5)], fill=SE.GREEN)

    d.text((x0 + 80, y0 + 35), "EM LOG-LIKELIHOOD CONVERGENCE (14 ITERATIONS)", font=SE.get_font(22, bold=True, mono=True), fill=SE.GREEN)
    d.text((x0 + 80, y0 + 75), "OPTIMAL Q ESTIMATE: Q = 0.0184 (DATA-DRIVEN) VS HARDCODED 0.05", font=SE.get_font(18, mono=True), fill=SE.CYAN)
    return im


def s_037_polarity_constraint(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "IDENTIFICATION & POLARITY CONSTRAINTS", "LOCKING OBSERVATION MATRIX FACTOR LOADINGS: F_{1,1} >= 0")
    categories = ["BTC SPOT", "DERIBIT DVOL", "REALIZED VOL", "FRED 10Y"]
    values = [1.0, 0.82, 0.74, 0.65]
    SE.draw_radar_spider_chart(d, categories, values, W // 2, H // 2 + 10, 180, t, col=SE.GOLD, label="POLARITY LOADINGS")
    d.text((W // 2 - 300, H - 200), "IDENTIFICATION LOCKED: RESOLVING ROTATIONAL AND SIGN INDETERMINACY IN EM ITERATIONS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
def _old_s_037(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SIGN IDENTIFICATION & POLARITY LOCK", "PREVENTING MARKOV CHAIN SIGN-INVERSION IN LATENT SPACE")

    factors = [
        ("DVOL VOLATILITY", "+1 (POSITIVE)", "Crisis increases implied volatility", SE.GREEN),
        ("ORDERBOOK SPREAD", "+1 (POSITIVE)", "Crisis widens bid/ask spreads", SE.GREEN),
        ("CBOE VIX", "+1 (POSITIVE)", "Crisis amplifies equity fear index", SE.GREEN),
        ("PERP FUNDING", "-1 (NEGATIVE)", "Crisis drives funding deeply negative", SE.DANGER_RED)
    ]
    for i, (name, sign, desc, col) in enumerate(factors):
        y = 240 + i * 105
        d.rounded_rectangle([140, y, W - 140, y + 85], radius=8, fill=SE.BG_PANEL, outline=col, width=2)
        d.text((180, y + 16), name, font=SE.get_font(22, bold=True), fill=SE.TEXT_WHITE)
        d.text((180, y + 50), desc, font=SE.get_font(15, mono=True), fill=SE.TEXT_MUTED)
        # Lock badge
        d.rounded_rectangle([W - 380, y + 18, W - 180, y + 66], radius=6, fill=col)
        d.text((W - 360, y + 26), f"SIGN: {sign[:2]}", font=SE.get_font(20, bold=True, mono=True), fill=SE.TEXT_WHITE)
    return im


def s_038_dgrs_trajectory_full(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "ESTIMATED LATENT FEVER TRAJECTORY: DGRS(t)", "SMOOTHED CONTINUOUS SYSTEMIC RISK INDEX OVER 970 DAYS")
    SE.draw_candlestick_chart(d, x=180, y=240, w=W - 360, h=H - 480, t=t, dur=dur, trend="crash")
    d.text((180, H - 200), "THE LATENT SHIELD: DGRS(t) MAPS UNSEEN SYSTEMIC TENSION UNDERNEATH DECEPTIVELY CALM SPOT PRICES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
def _old_s_038(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "DGRS LATENT SYSTEMIC STRESS S_t (2024-2026)", "EM-ESTIMATED Q // KALMAN SMOOTHED RECONSTRUCTION")

    # Dynamic sweeping trajectory curve
    pts = []
    n = 120
    revealed = min(n, int((t / max(0.1, dur * 0.85)) * n) + 2)
    for i in range(revealed):
        x = 120 + int(i * (W - 240) / n)
        frac = i / n
        base_s = 0.65 - frac * 0.35
        if 0.45 < frac < 0.55:
            base_s += math.sin((frac - 0.45) * 10.0 * math.pi) * 0.45
        y = int(240 + (1.0 - base_s) * 440)
        pts.append((x, y))

    if len(pts) > 1:
        d.line(pts, fill=SE.CYAN, width=3)
        hx, hy = pts[-1]
        d.ellipse([(hx - 6, hy - 6), (hx + 6, hy + 6)], fill=SE.CYAN)

    d.text((W - 480, 260), "CURRENT STRESS: 0.22 (LOW)", font=SE.get_font(24, bold=True, mono=True), fill=SE.GREEN)
    return im


def s_039_august_2024_spike(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "ZOOM-IN: AUGUST 5, 2024 LIQUIDATION", "YEN CARRY COLLAPSE SENDS DGRS S_t TO +2.85 SIGMA")

    # Candlestick crash chart on left
    SE.draw_candlestick_chart(d, 120, 240, W//2 + 40, 420, t, dur, trend="crash")

    # Gauge on right showing 2.85 Sigma peak stress
    SE.draw_speedometer_gauge(d, 2.85, 0.0, 3.5, "PEAK SYSTEMIC STRESS", unit=" SIGMA", cx=3*W//4, cy=H//2 + 20, radius=140, col=SE.DANGER_RED)
    d.text((3*W//4 - 180, H - 200), "YEN CARRY COLLAPSE // BTC $64K -> $49K", font=SE.get_font(16, bold=True, mono=True), fill=SE.TEXT_MUTED)
    return im


def s_040_credible_intervals(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "BAYESIAN 95% CREDIBLE CORRIDORS", "S_t +/- 1.96 * SQRT(P_{t|t}) ESTIMATION UNCERTAINTY")

    pts_hi = []
    pts_lo = []
    pts_mid = []
    for i in range(80):
        x = 120 + int(i * (W - 240) / 80)
        mid = H//2 + int(math.sin(i * 0.12 + t * 2.0) * 80)
        band = int(45 + math.sin(i * 0.25) * 18)
        pts_hi.append((x, mid - band))
        pts_lo.append((x, mid + band))
        pts_mid.append((x, mid))

    poly = pts_hi + pts_lo[::-1]
    d.polygon(poly, fill=SE.BG_TINT_BLUE)
    d.line(pts_hi, fill=SE.BORDER_CYAN, width=1)
    d.line(pts_lo, fill=SE.BORDER_CYAN, width=1)
    d.line(pts_mid, fill=SE.CYAN, width=3)
    d.text((160, 270), "SHADED REGION: 95% BAYESIAN POSTERIOR CREDIBLE CORRIDOR", font=SE.get_font(20, bold=True, mono=True), fill=SE.CYAN)
    return im


def s_041_tesseract_rotation_fast(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "4D TENSOR EMBEDDING SPACE", "HIGH-SPEED ISOCLINIC DOUBLE ROTATION")
    SE.render_tesseract_frame(im, d, t * 2.2, cx=W//2, cy=H//2 + 30, scale=240)
    return im


def s_042_so4_plane_projection(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SPECIAL ORTHOGONAL GROUP SO(4)", "6 INDEPENDENT PLANES OF ROTATION (XY, XZ, XW, YZ, YW, ZW)")
    SE.render_tesseract_frame(im, d, t * 1.5, cx=W//2, cy=H//2 + 30, scale=210)
    return im


def s_043_hyperplane_slicing(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "DIMENSIONAL CROSS-SECTIONS", "OBSERVING 3D SHADOWS OF 4D GEOMETRY OVER TIME")

    # Animated slicing plane
    cx, cy = W//2, H//2 + 20
    SE.render_tesseract_frame(im, d, t * 1.1, cx=cx, cy=cy, scale=170)
    # Slicing line
    slice_y = cy + int(math.sin(t * 2.5) * 140)
    d.line([(cx - 300, slice_y), (cx + 300, slice_y)], fill=SE.GOLD, width=3)
    d.text((cx + 120, slice_y - 25), "HYPERPLANE SLICE W = const", font=SE.get_font(16, bold=True, mono=True), fill=SE.GOLD)

    d.text((160, H - 210), "Just as a 3D sphere passes through Flatland as an expanding circle,", font=SE.get_font(22), fill=SE.TEXT_WHITE)
    d.text((160, H - 170), "a 4D crisis manifold passes through crypto orderbooks as volatility.", font=SE.get_font(22, bold=True), fill=SE.CYAN)
    return im


def s_044_terminal_diagnostics(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "KALMAN STABILITY & SPECTRAL RADIUS", "VERIFYING MATRIX G EIGENVALUES LIE STRICTLY INSIDE THE UNIT CIRCLE")

    cx, cy = W//2, H//2 + 30
    d.ellipse([(cx - 180, cy - 180), (cx + 180, cy + 180)], fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=2)
    d.line([(cx, cy - 200), (cx, cy + 200)], fill=SE.BORDER_CYAN, width=1)
    d.line([(cx - 200, cy), (cx + 200, cy)], fill=SE.BORDER_CYAN, width=1)

    # Rotating eigenvalue constellation
    eigs = [(0.42, 0.28), (0.42, -0.28), (-0.35, 0.15), (0.12, -0.45)]
    for rx, ry in eigs:
        ang = t * 0.6
        nx = rx * math.cos(ang) - ry * math.sin(ang)
        ny = rx * math.sin(ang) + ry * math.cos(ang)
        px = cx + int(nx * 180)
        py = cy + int(ny * 180)
        d.ellipse([(px - 8, py - 8), (px + 8, py + 8)], fill=SE.CYAN, outline=SE.TEXT_WHITE, width=2)

    d.text((cx + 195, cy - 10), "UNIT CIRCLE |lambda| = 1", font=SE.get_font(18, mono=True), fill=SE.TEXT_MUTED)
    d.text((140, H - 200), "SPECTRAL RADIUS rho(G) = 0.505 < 1.0 -> STRICTLY ASYMPTOTICALLY STABLE", font=SE.get_font(20, bold=True, mono=True), fill=SE.GREEN)
    return im


def s_045_bic_model_selection(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "BAYESIAN INFORMATION CRITERION (BIC)", "MODEL SELECTION: PENALIZING EXCESS LATENT FACTORS")

    SE.draw_animated_bar_chart(
        d,
        ["1-FACTOR DGRS (OPTIMAL)", "2-FACTOR DGRS", "3-FACTOR DGRS"],
        [4812.4, 4651.1, 4319.8],
        5000.0,
        140, 260, W - 280, 260, t, dur,
        colors=[SE.GREEN, SE.GOLD, SE.DANGER_RED]
    )

    d.rounded_rectangle([140, 550, W - 140, H - 200], radius=8, fill=SE.BG_PANEL, outline=SE.GREEN, width=1)
    d.text((180, 575), "SELECTION VERDICT: 1-Factor DGRS minimizes BIC at -4,812.4.", font=SE.get_font(22, bold=True, mono=True), fill=SE.GREEN)
    d.text((180, 615), "Excess factors add empirical noise without expanding explanatory power.", font=SE.get_font(18), fill=SE.TEXT_MUTED)
    return im


def s_046_one_factor_optimality(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "FACTOR EXPLAINED VARIANCE RATIO", "ONE LATENT FACTOR EXPLAINS 73.4% OF SYSTEMIC COVARIANCE")

    SE.draw_animated_bar_chart(
        d,
        ["FACTOR 1 (SYSTEMIC FEVER)", "FACTOR 2 (ETH BETA)", "FACTOR 3 (MACRO NOISE)", "FACTOR 4 (IDIOSYNCRATIC)"],
        [73.4, 14.2, 7.8, 4.6],
        100.0,
        140, 260, W - 280, 280, t, dur,
        colors=[SE.CYAN, SE.BORDER_CYAN, SE.BORDER_CYAN, SE.BORDER_CYAN]
    )
    return im


def s_047_crypto_vs_fiat_diff(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "CRYPTO LIQUIDITY VS FIAT BANKING", "CONTINUOUS 24/7/365 TRADING MEETS FRACTIONAL RESERVE CYCLES")
    categories = ["SETTLEMENT SPEED", "TRADING HOURS", "LEVERAGE UNWIND", "CIRCUIT BREAKERS"]
    values_crypto = [0.95, 1.00, 0.90, 0.05]
    SE.draw_radar_spider_chart(d, categories, values_crypto, W // 2, H // 2 + 10, 180, t, col=SE.DANGER_RED, label="CRYPTO DYNAMICS")
    d.text((W // 2 - 320, H - 200), "NO BAILOUTS, NO PAUSE: CRYPTO LIQUIDATIONS OCCUR AT THE SPEED OF BLOCK PROPAGATION.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
def _old_s_047(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "CONTINUOUS CRYPTO VS TRADITIONAL FIAT", "THE REASON CENTRAL BANK ASSUMPTIONS COLLAPSE")

    # Top: Fiat Banking (segmented closed schedule)
    d.rounded_rectangle([140, 260, W - 140, 390], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN)
    d.text((180, 280), "TRADITIONAL FIAT BANKING (FEDWIRE / CHIPS):", font=SE.get_font(20, bold=True, mono=True), fill=SE.TEXT_MUTED)
    d.text((180, 320), "Closed weekends • Closed overnight • Circuit breakers • T+2 Settlement", font=SE.get_font(22), fill=SE.TEXT_WHITE)

    # Bottom: Crypto 24/7/365 (continuous neon stream)
    d.rounded_rectangle([140, 420, W - 140, 550], radius=8, fill=SE.BG_TINT_BLUE, outline=SE.CYAN, width=2)
    d.text((180, 440), "CRYPTO DERIVATIVES ENGINE (BINANCE / DERIBIT):", font=SE.get_font(20, bold=True, mono=True), fill=SE.CYAN)
    d.text((180, 480), "24/7/365 Continuous • Autonomous liquidation bots • Instant T+0 Margin Calls", font=SE.get_font(22, bold=True), fill=SE.TEXT_WHITE)
    return im


def s_048_continuous_clearing(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "ALGORITHMIC CONTINUOUS CLEARING", "AUTONOMOUS LIQUIDATION BOTS FIRING ON EVERY BLOCK")

    # Order stream oscilloscope
    SE.draw_waveform_oscilloscope(d, t, 120, 240, W - 240, 340, freq=2.2, amp=0.85, col=SE.DANGER_RED, title="HIGH-FREQUENCY LIQUIDATION BURST ENGINE")
    SE.draw_news_ticker(d, "SUNDAY 3:00 AM FLASH CASCADE: $320M MARGIN AUTO-DELEVERAGED IN 18 SECONDS", source="DERIBIT API", t=t)
    return im


def s_049_central_bank_blindness(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "CENTRAL BANK BLIND SPOTS", "WHY CENTRAL BANKERS MISS ON-CHAIN LIQUIDATION CLIFFS")
    SE.draw_speedometer_gauge(d, 82.5, 0.0, 100.0, "TRADITIONAL MODEL BLINDNESS", "% INERT", W // 4 + 40, H // 2 + 10, 130, SE.DANGER_RED)
    SE.draw_speedometer_gauge(d, 96.0, 0.0, 100.0, "4D-MGRFF ON-CHAIN CAPTURE", "% DETECT", 3 * W // 4 - 40, H // 2 + 10, 130, SE.GREEN)
    d.text((160, H - 200), "MACRO MODELS ASSUME LENDERS OF LAST RESORT. CRYPTO PROTOCOLS RECOGNIZE ONLY LIQUIDATION CODE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
def _old_s_049(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE CENTRAL BANK BLINDSPOT", "CALIBRATED FOR T+2 SETTLEMENT, DEPLOYED ON T+0 REALITY")

    cx, cy = W//2, H//2 + 20
    for r in (80, 160, 240):
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=SE.BORDER_CYAN, width=1)
    # Sweeping radar needle showing missed shock
    ang = t * 2.0
    d.line([(cx, cy), (cx + int(math.cos(ang) * 240), cy + int(math.sin(ang) * 240))], fill=SE.GOLD, width=2)
    d.text((cx - 120, cy - 10), "WEEKEND BLINDSPOT", font=SE.get_font(20, bold=True, mono=True), fill=SE.DANGER_RED)

    d.text((160, H - 200), "Central bank math expects friction and human pause. Crypto executes instantly.", font=SE.get_font(24, bold=True), fill=SE.TEXT_WHITE)
    return im


def s_050_synthetic_vs_real(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SYNTHETIC MONTE CARLO VS REALITY", "SYNTHETIC GAUSSIAN RUNS FAIL TO CAPTURE DEFI LIQUIDATION SPIRALS")
    SE.draw_waveform_oscilloscope(d, t, 180, 240, W - 360, H - 480, freq=2.0, amp=50, col=SE.DANGER_RED, title="POISSON JUMP DEFI SPIRAL DYNAMICS (HEAVY FAT TAILS)")
    d.text((180, H - 200), "THE FAT-TAIL TRUTH: CRYPTO CORRELATIONS EXPLODE TOWARDS 1.0 EXACTLY WHEN LIQUIDITY EVAPORATES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
def _old_s_050(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "VERIFIED DATASET INTEGRITY", "ZERO SYNTHETIC SIMULATION ARTIFACTS")

    # 4 Data source verification cards
    sources = [
        ("BINANCE SPOT L2", "Live orderbook depth & spread ticks", SE.CYAN),
        ("BINANCE PERPETUAL", "8-Hour historical funding & basis", SE.GOLD),
        ("DERIBIT 30D DVOL", "Option implied forward variance", SE.DANGER_RED),
        ("FRED ST. LOUIS", "VIXCLS & 10Y Constant Maturity Yield", SE.GREEN)
    ]
    for i, (name, desc, col) in enumerate(sources):
        y = 240 + i * 105
        d.rounded_rectangle([140, y, W - 140, y + 85], radius=8, fill=SE.BG_PANEL, outline=col, width=2)
        d.text((180, y + 16), name, font=SE.get_font(22, bold=True), fill=SE.TEXT_WHITE)
        d.text((180, y + 50), desc, font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)
        # Checkmark badge
        d.text((W - 320, y + 26), "[VERIFIED 100%]", font=SE.get_font(18, bold=True, mono=True), fill=col)
    return im


def s_051_state_vector_snapshot(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "ONLINE STATE VECTOR EXTRACTION", "LIVE RUNTIME METRICS EMITTED BY KALMAN SMOOTHER")

    # Triple live telemetry gauges
    SE.draw_speedometer_gauge(d, 0.42, 0.0, 1.0, "LATENT STRESS S_t", unit="", cx=W//4, cy=H//2 + 20, radius=120, col=SE.CYAN)
    SE.draw_speedometer_gauge(d, 0.18, -0.5, 0.5, "STRESS VELOCITY dS/dt", unit="", cx=W//2, cy=H//2 + 20, radius=120, col=SE.GOLD)
    SE.draw_speedometer_gauge(d, 0.0034, 0.0, 0.02, "ERROR COVARIANCE P_t", unit="", cx=3*W//4, cy=H//2 + 20, radius=120, col=SE.GREEN)
    return im


def s_052_huber_residual_plot(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "OUTLIER ATTENUATION IN ACTION", "HUBER ADAPTIVE WEIGHTS CLIPPING FLASH SHOCKS BY 62%")

    # Scatter plot of residuals with threshold line
    x0, y0, w0, h0 = 140, 240, W - 280, 420
    d.rounded_rectangle([x0, y0, x0 + w0, y0 + h0], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)

    cy = y0 + h0 // 2
    d.line([(x0 + 40, cy), (x0 + w0 - 40, cy)], fill=SE.BORDER_CYAN, width=1)
    # Threshold cutoff lines
    d.line([(x0 + 40, cy - 100), (x0 + w0 - 40, cy - 100)], fill=SE.GOLD, width=2)
    d.line([(x0 + 40, cy + 100), (x0 + w0 - 40, cy + 100)], fill=SE.GOLD, width=2)
    d.text((x0 + 60, cy - 125), "HUBER OUTLIER THRESHOLD k = 1.345", font=SE.get_font(15, bold=True, mono=True), fill=SE.GOLD)

    # Scatter points
    for i in range(40):
        px = x0 + 60 + int(i * (w0 - 120) / 40)
        res = math.sin(i * 1.8) * 70 + (140 if i in (12, 28) else 0)
        py = cy - int(res)
        is_clipped = abs(res) > 100
        col = SE.DANGER_RED if is_clipped else SE.GREEN
        d.ellipse([(px - 5, py - 5), (px + 5, py + 5)], fill=col)

    d.text((180, H - 190), "62% OF FLASH-CRASH SPIKES CLIPPED TO PROTECT FILTER INTEGRITY", font=SE.get_font(20, bold=True, mono=True), fill=SE.GREEN)
    return im


def s_053_mathematical_hubris(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE DANGER OF MATHEMATICAL HUBRIS", "AN IMMACULATE MODEL CAN STILL LEAD TO COMPLETE LIQUIDATION")

    # Pulsing 4D tesseract
    SE.render_tesseract_frame(im, d, t * 1.8, cx=W//2, cy=H//2 - 20, scale=200)

    d.rounded_rectangle([160, H - 240, W - 160, H - 120], radius=8, fill=SE.BG_TINT_RED, outline=SE.DANGER_RED, width=2)
    d.text((200, H - 220), "MATHEMATICAL PERFECTION DOES NOT EQUAL SURVIVAL", font=SE.get_font(32, bold=True), fill=SE.DANGER_RED)
    d.text((200, H - 165), "Now comes the real test: Can this math map contagion before it strikes live capital?", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)
    return im


def s_054_contagion_teaser(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PREVIEWING THE 7-ASSET CONTAGION MATRIX", "MAPPING DIRECTED SPILLOVERS ACROSS TRADFI AND DEFI")
    matrix_teaser = [
        [1.0, -0.38, -0.25, 0.21],
        [-0.12, 1.0, -0.18, 0.09],
        [-0.20, -0.15, 1.0, -0.14],
        [0.21, 0.09, -0.14, 1.0]
    ]
    labels = ["BTC", "ETH/BTC", "DVOL", "FUND"]
    SE.draw_matrix_heatmap(d, matrix_teaser, labels, labels, x=220, y=240, w=W - 440, h=H - 480, t=t, highlight_cell=(0, 1))
    d.text((220, H - 200), "COMING IN ACT II: FULL 7x7 CONTAGION MATRIX AND GENERALIZED IMPULSE RESPONSES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
def _old_s_054(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PREPARING THE CONTAGION ENGINE", "WHERE DOES THE SHOCK TRANSMIT FIRST?")

    # 7-node network topology preview
    nodes = ["BTC", "ETH/BTC", "DVOL", "VIX", "10Y", "FUNDING", "DEPTH"]
    cx, cy = W//2, H//2 + 20
    r_net = 220
    pts = []
    for i, name in enumerate(nodes):
        ang = i * (2 * math.pi / len(nodes)) + t * 0.3
        px = cx + int(math.cos(ang) * r_net)
        py = cy + int(math.sin(ang) * r_net)
        pts.append((px, py, name))

    for i in range(len(pts)):
        for j in ((i + 1) % len(pts), (i + 3) % len(pts)):
            d.line([(pts[i][0], pts[i][1]), (pts[j][0], pts[j][1])], fill=SE.BORDER_CYAN, width=1)

    for px, py, name in pts:
        d.ellipse([(px - 36, py - 36), (px + 36, py + 36)], fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
        d.text((px - 25, py - 10), name[:5], font=SE.get_font(13, bold=True, mono=True), fill=SE.TEXT_WHITE)
    return im


def s_055_act2_transition(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT II // THE CONTAGION MATRIX")

    # Concentric portal rings
    cx, cy = W//2, H//2 - 20
    for i in range(5):
        r = int(70 + i * 80 + ((t * 80) % 80))
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=SE.CYAN, width=2)

    SE.render_tesseract_frame(im, d, t * 1.5, cx=cx, cy=cy, scale=120)

    d.rounded_rectangle([180, H - 240, W - 180, H - 120], radius=8, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
    d.text((220, H - 220), "ACT II: THE CONTAGION MATRIX", font=SE.get_font(42, bold=True), fill=SE.TEXT_WHITE)
    d.text((225, H - 165), "MAPPING SHOCK TRANSMISSION WITHOUT CHOLESKY ORDERING BIAS", font=SE.get_font(22, mono=True), fill=SE.CYAN)
    return im
