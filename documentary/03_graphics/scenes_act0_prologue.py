# -*- coding: utf-8 -*-
"""
Procedural Scene Renderers — ACT 0: PROLOGUE & HOOK (Scenes 001 - 025)
1080p 30 FPS cinematic motion graphics for @izhaanintellect.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import style_engine as SE

W, H = SE.W, SE.H


def draw_header(d, title, sub):
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT 0 // PROLOGUE")
    f_t = SE.get_font(44, bold=True)
    f_s = SE.get_font(20, mono=True)
    d.text((80, 85), title, font=f_t, fill=SE.TEXT_WHITE)
    d.text((82, 140), sub, font=f_s, fill=SE.CYAN)
    d.line([(80, 175), (W - 80, 175)], fill=SE.BORDER_CYAN, width=1)


def s_001_channel_ident(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d, spacing=70, alpha=25)
    SE.render_tesseract_frame(im, d, t, cx=W//2, cy=H//2 - 40, scale=170)

    prog = min(1.0, t / 1.0)
    pulse = (math.sin(t * 5.0) + 1.0) * 0.5
    f_main = SE.get_font(int(54 + pulse * 2), bold=True)
    f_sub = SE.get_font(20, mono=True)

    title = "IZHAAN INTELLECT"
    bbox = d.textbbox((0, 0), title, font=f_main)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw)//2, H - 230), title, font=f_main, fill=SE.TEXT_WHITE)

    sub = "THEORETICAL PHYSICS • QUANTITATIVE FINANCE • HIGHER DIMENSIONS"
    bbox_s = d.textbbox((0, 0), sub, font=f_sub)
    tw_s = bbox_s[2] - bbox_s[0]
    d.text(((W - tw_s)//2, H - 165), sub, font=f_sub, fill=SE.CYAN)
    return im


def s_002_glitch_warning(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SYSTEMIC LIQUIDATION EVENT DETECTED", "METRIC INTEGRITY ALERT // BITCOIN DRAWDOWN")

    d.rounded_rectangle([160, 230, W // 2 - 40, H - 240], radius=10, fill=SE.BG_TINT_RED, outline=SE.DANGER_RED, width=2)
    d.text((200, 260), "CRITICAL RISK CASCADE", font=SE.get_font(28, bold=True), fill=SE.DANGER_RED)

    f_body = SE.get_font(18, mono=True)
    lines = [
        "EVENT: 2024-03 -> 2026-09",
        "ASSET: BITCOIN (BTC/USDT)",
        "PEAK PRICE: $73,750 USD",
        "TROUGH PRICE: $35,900 USD",
        "MAX REALIZED DD: -51.32%",
        "STATUS: CRISIS LEVEL 5"
    ]
    for i, l in enumerate(lines):
        d.text((200, 330 + i * 36), f">> {l}", font=f_body, fill=SE.TEXT_WHITE if i < 4 else SE.DANGER_RED)

    SE.draw_waveform_oscilloscope(
        d, t, W // 2 + 20, 230, W // 2 - 180, H - 470,
        freq=2.8, amp=55, col=SE.DANGER_RED,
        title="LIQUIDATION CASCADE SHOCKWAVE", deadband=None
    )

    SE.draw_news_ticker(d, "EMERGENCY: SYSTEMIC CASCADE DETECTED ACROSS GLOBAL CRYPTO EXCHANGES", source="REUTERS WIRE", t=t)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_003_51pct_crash_reveal(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "BITCOIN UNHEDGED TRAJECTORY", "PEAK-TO-TROUGH DISASTER: -51.32% PORTFOLIO LOSS")

    # Animated crash line
    pts = []
    n_pts = 60
    revealed = min(n_pts, int((t / max(0.1, dur * 0.85)) * n_pts) + 5)
    for i in range(revealed):
        x = 120 + int(i * (W - 240) / n_pts)
        frac = i / n_pts
        if frac < 0.25:
            val = 0.5 + frac * 1.5
        else:
            val = 0.875 - (frac - 0.25) * 1.1 + math.sin(i * 0.8) * 0.04
        y = int(240 + (1.0 - val) * 480)
        pts.append((x, y))

    if len(pts) > 1:
        poly = [(pts[0][0], H - 180)] + pts + [(pts[-1][0], H - 180)]
        d.polygon(poly, fill=SE.BG_TINT_RED)
        d.line(pts, fill=SE.DANGER_RED, width=4)
        # Glowing head dot
        hx, hy = pts[-1]
        d.ellipse([(hx - 7, hy - 7), (hx + 7, hy + 7)], fill=SE.DANGER_RED, outline=SE.TEXT_WHITE, width=2)

    # Dynamic animated drawdown odometer counter
    prog = min(1.0, t / max(0.1, dur * 0.8))
    cur_dd = -51.32 * (prog ** 1.4)
    f_stat = SE.get_font(52, bold=True, mono=True)
    d.text((W - 580, 260), f"{cur_dd:6.2f}% MAX DD", font=f_stat, fill=SE.DANGER_RED)
    f_sub = SE.get_font(20, mono=True)
    d.text((W - 580, 330), "UNHEDGED CAPITAL DESTROYED", font=f_sub, fill=SE.TEXT_MUTED)
    return im


def s_004_liquidation_cascade(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "EXCHANGE LIQUIDATION ENGINE", "DERIVATIVES ORDERBOOK DEPTH WIPEOUT")

    prog = min(1.0, t / max(0.1, dur * 0.75))
    liq_amt = int(prog * 1480)
    d.text((160, 240), f"${liq_amt:,} MILLION LIQUIDATED", font=SE.get_font(52, bold=True, mono=True), fill=SE.DANGER_RED)

    SE.draw_orderbook_depth(d, x=160, y=340, w=W - 320, h=H - 580, t=t)

    SE.draw_news_ticker(d, "DERIVATIVES ALERT: OVER $1.48 BILLION IN LONG POSITIONS LIQUIDATED", source="COINDESK TERMINAL", t=t)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_005_panic_telemetry(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PANIC INDICATOR TELEMETRY", "MULTI-ASSET CROSS-MARKET STRESS VECTORS")

    # Live gauges for DVOL and VIX
    dvol_pulse = 72.0 + math.sin(t * 3.0) * 16.5
    vix_pulse = 32.0 + math.cos(t * 2.8) * 8.2
    SE.draw_speedometer_gauge(d, dvol_pulse, 40.0, 120.0, "DERIBIT 30D DVOL", unit=" VOL", cx=W//4 + 40, cy=H//2 + 40, radius=130, col=SE.DANGER_RED)
    SE.draw_speedometer_gauge(d, vix_pulse, 10.0, 60.0, "CBOE VIX INDEX", unit=" PTS", cx=3*W//4 - 40, cy=H//2 + 40, radius=130, col=SE.GOLD)

    # Telemetry data strips
    d.rounded_rectangle([W//2 - 180, 240, W//2 + 180, H - 220], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)
    f_lbl = SE.get_font(18, bold=True, mono=True)
    d.text((W//2 - 150, 260), "FUNDING RATE:", font=f_lbl, fill=SE.TEXT_MUTED)
    d.text((W//2 - 150, 295), "-0.0482% / 8H", font=SE.get_font(28, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W//2 - 150, 360), "ETH/BTC RATIO:", font=f_lbl, fill=SE.TEXT_MUTED)
    d.text((W//2 - 150, 395), "0.0381 RATIO", font=SE.get_font(28, bold=True, mono=True), fill=SE.CYAN)
    d.text((W//2 - 150, 460), "ORDERBOOK SPREAD:", font=f_lbl, fill=SE.TEXT_MUTED)
    d.text((W//2 - 150, 495), "4.82 BPS SPREAD", font=SE.get_font(28, bold=True, mono=True), fill=SE.GOLD)
    return im


def s_006_central_bank_promise(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE CENTRAL BANK PROMISE", "DECIMAL-POINT PRECISION IN UNPRECEDENTED CRISES")

    # Central Bank State Space Flow Architecture
    steps = [
        ("MACRO SENSORS", "FRED Yields + VIX Feeds"),
        ("KALMAN FILTER", "Unobserved Fever Latent State"),
        ("CONTAGION TENSOR", "Pesaran-Shin Impulse Matrix"),
        ("CAPITAL SHIELD", "Preemptive Liquidity Injection")
    ]
    active_step = int((t * 1.5) % len(steps))
    SE.draw_flow_diagram(d, steps, active_step, 120, 260, W - 240, 280, t)

    f_quote = SE.get_font(22, mono=True)
    d.text((140, H - 200), "\"Macroprudential state-space models claim to forecast systemic crisis before market collapse.\"", font=f_quote, fill=SE.CYAN)
    return im


def s_007_state_space_equations(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "DYNAMIC LINEAR STATE-SPACE ARCHITECTURE", "HAMILTON (1994) / WEST & HARRISON (1997)")

    steps = [
        ("STATE x_t", "G_t * x_{t-1} + w_t"),
        ("OBSERVE y_t", "F_t * x_t + v_t"),
        ("INNOVATION v_t", "y_t - F_t * x_{t|t-1}"),
        ("GAIN K_t", "P F^T (F P F^T + R)^{-1}")
    ]
    active_step = int((t * 1.2) % len(steps))
    SE.draw_flow_diagram(d, steps, active_step, 100, 240, W - 200, 260, t)

    # Dynamic waveform below
    SE.draw_waveform_oscilloscope(d, t, 100, 520, W - 200, 180, freq=1.5, amp=0.7, col=SE.CYAN, title="KALMAN FILTER ESTIMATION NOISE PROCESS")
    return im


def s_008_kalman_origins(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "KALMAN FILTERING (R.E. KALMAN, 1960)", "FROM APOLLO LUNAR NAVIGATION TO FINANCIAL CONTAGION")

    SE.draw_radar_spider_chart(
        d,
        ["APOLLO GUIDANCE", "RADAR TRACKING", "ORBIT ESTIMATION", "MACROPRUDENTIAL"],
        [0.98, 0.92, 0.95, 0.85],
        W // 2, H // 2 + 10, 180, t,
        col=SE.CYAN, label="KALMAN APPLICATIONS"
    )

    d.text((140, H - 200), "OPTIMAL MINIMUM MEAN-SQUARED ERROR ESTIMATOR IN GAUSSIAN NOISE // HAMILTON (1994)", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_009_hypercube_glimpse(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE FOURTH DIMENSION: HYPERSPACE", "PROJECTING 4-MANIFOLDS INTO 1-DIMENSIONAL EXECUTION")
    SE.render_tesseract_frame(im, d, t * 1.4, cx=W//2, cy=H//2 + 30, scale=230)
    return im


def s_010_academic_illusion(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE ACADEMIC MIRAGE", "WHY 90% RETROSPECTIVE ACCURACY GUARANTEES LIVE COLLAPSE")

    SE.draw_speedometer_gauge(d, 91.4, 0.0, 100.0, "PAPER CLAIMED FIT", "% IN-SMPL", W // 4 + 40, H // 2 + 10, 130, SE.DANGER_RED)

    d.rounded_rectangle([W // 2 + 40, 240, W - 160, H - 240], radius=10, fill=SE.BG_PANEL, outline=SE.DANGER_RED, width=2)
    d.text((W // 2 + 80, 280), "METHODOLOGICAL PATHOLOGY:", font=SE.get_font(22, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W // 2 + 80, 350), "- Circular volatility targeting: DVOL predicting DVOL", font=SE.get_font(18, mono=True), fill=SE.TEXT_WHITE)
    d.text((W // 2 + 80, 400), "- Full-sample lookahead: 2026 data leaking into 2024", font=SE.get_font(18, mono=True), fill=SE.GOLD)
    d.text((W // 2 + 80, 450), "- Multi-testing bias: Cherry-picked unadjusted p-values", font=SE.get_font(18, mono=True), fill=SE.TEXT_MUTED)
    d.text((W // 2 + 80, 520), "RESULT: TOTAL BANKRUPTCY IN LIVE TRADING", font=SE.get_font(20, bold=True, mono=True), fill=SE.DANGER_RED)

    d.text((160, H - 200), "THE ACADEMIC MIRAGE: 90% RETROSPECTIVE FIT COLLAPSES WHEN SUBJECTED TO HONEST OUT-OF-SAMPLE TESTING.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_011_live_exchange_pipe(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "POINT-IN-TIME INGESTION INFRASTRUCTURE", "STRICT AS-OF QUERY ENGINE // ZERO TIME TRAVEL")

    steps = [
        ("BINANCE SPOT", "TICK & DEPTH FEED"),
        ("DERIBIT DVOL", "IMPLIED VOLATILITY"),
        ("FRED YIELDS", "VIX & 10Y TREASURY"),
        ("SQLITE PIT DB", "AS-OF QUERY ENGINE")
    ]
    step_active = min(3, int(t * 1.8))
    SE.draw_flow_diagram(d, steps, step_active, x=120, y=280, w=W - 240, h=180, t=t)

    SE.draw_waveform_oscilloscope(
        d, t, 160, 490, W - 320, 160,
        freq=2.2, amp=35, col=SE.GREEN,
        title="LIVE INGESTION WEBSOCKET PACKET STREAM (0 MS LATENCY)", deadband=None
    )
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_012_970_day_history(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "970 CONTINUOUS TRADING DAYS", "JANUARY 17, 2024 -> SEPTEMBER 12, 2026")

    SE.draw_animated_bar_chart(
        d,
        ["JAN 2024 (INCEPTION)", "OCT 2024 (EXPANDING)", "MAY 2025 (OUT-OF-SAMPLE)", "SEP 2026 (FINAL AUDIT)"],
        [180.0, 420.0, 710.0, 970.0],
        1000.0,
        120, 240, W - 240, 260, t, dur,
        colors=[SE.CYAN, SE.CYAN, SE.GOLD, SE.GREEN]
    )

    # Dynamic rolling test origin counter
    cur_orig = int(min(292, (t / max(0.1, dur * 0.75)) * 292))
    d.rounded_rectangle([120, 530, W - 120, H - 200], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN)
    d.text((160, 560), f"EXPANDING-WINDOW TEST ORIGINS: {cur_orig:03d} / 292", font=SE.get_font(36, bold=True, mono=True), fill=SE.CYAN)
    d.text((160, 620), "STEP SIZE = 3 DAYS // STRICT TEST-TRAIN TEMPORAL SEPARATION", font=SE.get_font(20, mono=True), fill=SE.TEXT_MUTED)
    return im


def s_013_circularity_teaser(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE CIRCULARITY TRAP DETECTED", "DVOL IMPULSES FEEDING REFLEXIVE PRICE DISASTER")

    stages = [
        ("DVOL SPIKE", "Implied Volatility"),
        ("PERP BASIS", "Negative Funding"),
        ("LIQUIDATIONS", "Margin Cascades"),
        ("SPOT DUMP", "Market Selloff")
    ]
    SE.draw_circular_feedback_loop(d, stages, t, cx=W//2, cy=H//2 + 30, radius=180)
    return im


def s_014_the_hedged_solution(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "WALK-FORWARD PERPETUAL HEDGE OVERLAY", "HOLDING 100% BITCOIN SPOT + DYNAMIC 1.0X SHORT")

    # Dual animated equity curves
    n_pts = 60
    revealed = min(n_pts, int((t / max(0.1, dur * 0.85)) * n_pts) + 2)
    green_pts = []
    red_pts = []
    for i in range(revealed):
        x = 140 + int(i * (W - 280) / n_pts)
        frac = i / n_pts
        # Hedged curve climbs
        y_g = H - 240 - int((frac ** 0.85) * 360 + math.sin(i * 0.5) * 12)
        # Unhedged curve dives
        y_r = H - 240 - int(240 - frac * 160 + math.sin(i * 0.6) * 20) if frac < 0.3 else H - 240 - int(240 - (frac - 0.3) * 320)
        green_pts.append((x, y_g))
        red_pts.append((x, y_r))

    if len(green_pts) > 1:
        d.line(green_pts, fill=SE.GREEN, width=4)
        d.line(red_pts, fill=SE.DANGER_RED, width=3)
        hx_g, hy_g = green_pts[-1]
        hx_r, hy_r = red_pts[-1]
        d.ellipse([(hx_g - 6, hy_g - 6), (hx_g + 6, hy_g + 6)], fill=SE.GREEN)
        d.ellipse([(hx_r - 6, hy_r - 6), (hx_r + 6, hy_r + 6)], fill=SE.DANGER_RED)

    # Dynamic readout badge
    prog = min(1.0, t / max(0.1, dur * 0.8))
    m5_ret = 16.48 + (420.69 - 16.48) * (prog ** 1.3)
    d.text((W - 620, 240), f"M5 HEDGE: +{m5_ret:.1f}%", font=SE.get_font(32, bold=True, mono=True), fill=SE.GREEN)
    d.text((W - 620, 290), "UNHEDGED: -51.32% DD", font=SE.get_font(26, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W - 620, 335), "SHIELD: +38.38 PP SAVED", font=SE.get_font(20, mono=True), fill=SE.CYAN)
    return im


def s_015_plot_twist_teaser(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE UNCOMFORTABLE PLOT TWIST", "WHY MACHINE LEARNING WAS HUMILIATED BY A DUMB RULE")

    SE.draw_animated_bar_chart(
        d,
        ["M0 PERSISTENCE (1-BIT)", "M5 LIGHTGBM (AI)", "UNHEDGED BITCOIN"],
        [477.82, 420.69, 16.48],
        520.0,
        140, 250, W - 280, 260, t, dur,
        colors=[SE.GOLD, SE.CYAN, SE.DANGER_RED]
    )

    d.rounded_rectangle([140, 540, W - 140, H - 200], radius=8, fill=SE.BG_PANEL, outline=SE.GOLD, width=1)
    d.text((180, 570), "THE FORENSIC QUESTION: DID AI TRULY FAIL?", font=SE.get_font(26, bold=True, mono=True), fill=SE.GOLD)
    d.text((180, 620), "Why did a single line of persistence out-return multi-million parameter machine learning?", font=SE.get_font(20), fill=SE.TEXT_WHITE)
    return im


def s_016_mandelbrot_ghost(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "VOLATILITY CLUSTERING (MANDELBROT, 1963)", "\"LARGE CHANGES TEND TO BE FOLLOWED BY LARGE CHANGES\"")

    SE.draw_waveform_oscilloscope(
        d, t, 160, 250, W - 320, 250,
        freq=3.2, amp=60, col=SE.GOLD,
        title="MANDELBROT FAT-TAIL CLUSTERING WAVEFORM (NON-GAUSSIAN BURSTS)"
    )

    d.text((160, H - 200), "STYLIZED FACT: EXTREME SHOCKS CLUSTER TEMPORALLY — CREATING THE PERSISTENCE ILLUSION.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_017_hysteresis_preview(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SCHMITT-TRIGGER HYSTERESIS FILTER", "ELIMINATING BOUNDARY FEE CHURN IN LIVE TRADING")

    # Upper and lower threshold lines
    y_hi = 360
    y_lo = 540
    d.line([(120, y_hi), (W - 120, y_hi)], fill=SE.DANGER_RED, width=2)
    d.line([(120, y_lo), (W - 120, y_lo)], fill=SE.GREEN, width=2)
    d.text((W - 380, y_hi - 30), "ENTER HEDGE: P >= 0.25", font=SE.get_font(18, mono=True), fill=SE.DANGER_RED)
    d.text((W - 380, y_lo + 10), "EXIT HEDGE: P <= 0.15", font=SE.get_font(18, mono=True), fill=SE.GREEN)

    # Shaded deadband
    d.rectangle([120, y_hi, W - 120, y_lo], fill=(15, 30, 45, 100))
    d.text((W//2 - 140, 440), "HYSTERESIS DEADBAND (NO CHURN)", font=SE.get_font(20, mono=True), fill=SE.CYAN)
    return im


def s_018_title_sequence_a(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d, spacing=50, alpha=40)
    SE.render_tesseract_frame(im, d, t * 1.1, cx=W//2, cy=H//2 - 60, scale=200)

    f_title = SE.get_font(72, bold=True)
    d.text((W//2 - 390, H - 240), "THE 51% ILLUSION", font=f_title, fill=SE.TEXT_WHITE)
    return im


def s_019_title_sequence_b(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT SPECIAL REPORT", act_str="DOCUMENTARY FEATURE")

    # Rotating 4D hypercube backdrop
    SE.render_tesseract_frame(im, d, t * 1.25, cx=W//2, cy=H//2 - 40, scale=220)

    d.rounded_rectangle([120, H - 240, W - 120, H - 120], radius=8, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)
    d.text((160, H - 220), "WHY CENTRAL BANK MATHEMATICS FAILED CRYPTO", font=SE.get_font(38, bold=True), fill=SE.GOLD)
    d.text((165, H - 165), "(AND THE ONE-BIT TRAP THAT SAVED A REAL PORTFOLIO)", font=SE.get_font(24, mono=True), fill=SE.CYAN)
    return im


def s_020_radar_scan_intro(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE 4D HYPERSPACE SYSTEMIC SCAN", "OBSERVING SIMULTANEOUS DIMENSIONS")

    cx, cy = W//2, H//2 + 30
    for r in (80, 160, 240, 320):
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=SE.BORDER_CYAN, width=1)
    d.line([(cx, cy - 320), (cx, cy + 320)], fill=SE.CYAN, width=1)
    d.line([(cx - 320, cy), (cx + 320, cy)], fill=SE.CYAN, width=1)

    # Dynamic rotating radar needle
    ang = t * 2.5
    rx = cx + int(math.cos(ang) * 320)
    ry = cy + int(math.sin(ang) * 320)
    d.line([(cx, cy), (rx, ry)], fill=SE.CYAN, width=3)

    d.text((cx - 60, cy - 350), "LIQUIDITY", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)
    d.text((cx + 340, cy - 10), "DERIVATIVES", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)
    d.text((cx - 60, cy + 330), "TAIL VOLATILITY", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)
    d.text((cx - 420, cy - 10), "MACRO SPILLOVER", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)
    return im


def s_021_price_fallacy(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE SPOT PRICE FALLACY", "LAGGING INDICATORS CANNOT WARN OF CASCADE LIQUIDATIONS")

    # Live crashing candlestick chart
    SE.draw_candlestick_chart(d, 120, 240, W - 240, 420, t, dur, trend="crash")

    # Warning alert box
    d.rounded_rectangle([W - 740, 260, W - 140, 370], radius=8, fill=SE.BG_TINT_RED, outline=SE.DANGER_RED, width=2)
    d.text((W - 710, 280), "THE SPOT PRICE FALLACY:", font=SE.get_font(20, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W - 710, 318), "When spot drops on the screen, orderbook depth has", font=SE.get_font(18), fill=SE.TEXT_WHITE)
    d.text((W - 710, 342), "already evaporated. Retrospective metrics guarantee death.", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)
    return im


def s_022_funding_fallacy(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE FUNDING RATE BLINDSPOT", "OFF-CHAIN LEVERAGE INVISIBLE TO PERPETUAL SWAPS")

    # Live funding waveform with deadband
    SE.draw_waveform_oscilloscope(d, t, 120, 240, W - 240, 420, freq=1.6, amp=0.8, col=SE.GOLD, title="8-HOUR PERPETUAL FUNDING RATE OSCILLATION", deadband=(-0.4, 0.4))

    d.rounded_rectangle([W - 740, 260, W - 140, 370], radius=8, fill=SE.BG_TINT_GOLD, outline=SE.GOLD, width=2)
    d.text((W - 710, 280), "OFF-CHAIN LEVERAGE BLINDSPOT:", font=SE.get_font(20, bold=True, mono=True), fill=SE.GOLD)
    d.text((W - 710, 318), "Off-shore OTC lending and basis repo agreements hide true", font=SE.get_font(18), fill=SE.TEXT_WHITE)
    d.text((W - 710, 342), "counterparty exposure until forced liquidations ignite.", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)
    return im


def s_023_macro_silos(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "INSTITUTIONAL DISCIPLINARY SILOS", "WALL STREET MACRO VS CRYPTO NATIVE ARCHITECTURE")

    # Dual split screen: Left Wall Street, Right Crypto Native
    cx = W//2
    # Left: Wall Street
    vix_v = 36.5 + math.sin(t * 3.0) * 8.0
    SE.draw_speedometer_gauge(d, vix_v, 10.0, 60.0, "WALL STREET (CBOE VIX)", unit=" PTS", cx=cx - 400, cy=H//2 + 30, radius=130, col=SE.CYAN)
    d.text((cx - 560, H - 220), "TRADITIONAL MACRO: BLIND TO DERIBIT GAMMA SQUEEZES", font=SE.get_font(16, bold=True, mono=True), fill=SE.TEXT_MUTED)

    # Right: Crypto Native
    SE.draw_orderbook_depth(d, cx + 50, 240, cx - 170, 380, t)
    d.text((cx + 70, H - 220), "CRYPTO NATIVE: BLIND TO 10Y TREASURY DISCOUNT SHOCKS", font=SE.get_font(16, bold=True, mono=True), fill=SE.TEXT_MUTED)

    # Center disconnect symbol
    d.line([(cx, 240), (cx, H - 200)], fill=SE.DANGER_RED, width=2)
    d.text((cx - 40, H//2 - 10), "SILO", font=SE.get_font(22, bold=True, mono=True), fill=SE.DANGER_RED)
    return im


def s_024_enter_4d_mgrff(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "ENTER 4D-MGRFF ARCHITECTURE", "MULTIDISCIPLINARY GENERALIZED RISK FORECAST FRAMEWORK")

    # Center rotating 4D tesseract
    cx, cy = W//2, H//2 + 20
    SE.render_tesseract_frame(im, d, t * 1.2, cx=cx, cy=cy, scale=210)

    # 4 Orbiting asset nodes
    nodes = [
        ("MICROSTRUCTURE", "BINANCE L2 DEPTH"),
        ("DERIVATIVES", "FUNDING & BASIS"),
        ("TAIL RISK", "DERIBIT 30D DVOL"),
        ("MACRO SPILLOVER", "FRED 10Y & VIX")
    ]
    r_orbit = 340
    for i, (title, sub) in enumerate(nodes):
        ang = i * (math.pi / 2) + t * 0.4
        px = cx + int(math.cos(ang) * r_orbit)
        py = cy + int(math.sin(ang) * r_orbit)
        d.line([(cx, cy), (px, py)], fill=SE.BORDER_CYAN, width=1)
        d.rounded_rectangle([px - 110, py - 35, px + 110, py + 35], radius=6, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
        d.text((px - 95, py - 22), title, font=SE.get_font(14, bold=True), fill=SE.TEXT_WHITE)
        d.text((px - 95, py + 4), sub, font=SE.get_font(11, mono=True), fill=SE.CYAN)
    return im


def s_025_act1_transition(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT I // THE ARCHITECTURE")

    # Expanding concentric portal rings
    cx, cy = W//2, H//2 - 20
    for i in range(5):
        r = int(70 + i * 80 + ((t * 80) % 80))
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=SE.CYAN, width=2)

    SE.render_tesseract_frame(im, d, t * 1.5, cx=cx, cy=cy, scale=120)

    d.rounded_rectangle([180, H - 240, W - 180, H - 120], radius=8, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
    d.text((220, H - 220), "ACT I: THE CENTRAL BANK MACHINE", font=SE.get_font(42, bold=True), fill=SE.TEXT_WHITE)
    d.text((225, H - 165), "ESTIMATING THE UNOBSERVABLE FEVER OF CRASHES VIA KALMAN FILTERS", font=SE.get_font(22, mono=True), fill=SE.CYAN)
    return im
