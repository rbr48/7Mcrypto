# -*- coding: utf-8 -*-
"""
Procedural Scene Renderers — ACT 3: THE TRAP OF CIRCULARITY (Scenes 086 - 110)
1080p 30 FPS cinematic motion graphics for @izhaanintellect.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import style_engine as SE

W, H = SE.W, SE.H


def draw_header(d, title, sub):
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT 3 // CIRCULARITY TRAP")
    f_t = SE.get_font(42, bold=True)
    f_s = SE.get_font(20, mono=True)
    d.text((80, 85), title, font=f_t, fill=SE.TEXT_WHITE)
    d.text((82, 140), sub, font=f_s, fill=SE.CYAN)
    d.line([(80, 175), (W - 80, 175)], fill=SE.BORDER_CYAN, width=1)


def s_086_circularity_definition(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "STATISTICAL CIRCULARITY DEFINED", "REGRESSING A FEATURE ON A MONOTONIC TRANSFORMATION OF ITSELF")

    stages = [
        "INPUT: DERIBIT DVOL",
        "LOGISTIC ESTIMATOR",
        "TARGET: DVOL >= 85%",
        "FEEDBACK LEAKAGE"
    ]
    SE.draw_circular_feedback_loop(d, stages, t=t, cx=W // 2, cy=H // 2 + 10, radius=190)

    d.text((160, H - 210), "MATHEMATICAL TAUTOLOGY: Y = I(X >= c). THE MODEL NEVER PREDICTS A CASCADE; IT MERELY REGRESSES ON SELF.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_087_target_diagram_old(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE ORIGINAL FLAWED SPECIFICATION", "DVOL (INPUT) -> MODEL -> DVOL >= 85TH PERCENTILE (TARGET)")

    # 3-step pipeline with fatal feedback arrow
    steps = [
        ("FEATURE INPUT", "DERIBIT DVOL(t)"),
        ("LOGISTIC MODEL", "P = sigma(w*X + b)"),
        ("TARGET VARIABLE", "DVOL(t+1) >= 85TH PCT")
    ]
    SE.draw_flow_diagram(d, steps, active_step=int(t * 1.5) % 3, x=160, y=280, w=W - 320, h=160, t=t)

    # Big red circular loop returning from target to input
    d.arc([220, 360, W - 220, 620], start=0, end=180, fill=SE.DANGER_RED, width=3)
    d.polygon([(220, 480), (200, 510), (240, 510)], fill=SE.DANGER_RED)
    d.text((W // 2 - 160, 630), "<< CIRCULAR INFORMATION LOOP <<", font=SE.get_font(20, bold=True, mono=True), fill=SE.DANGER_RED)

    d.text((160, H - 200), "FATAL CONTAMINATION: PREDICTING TOMORROW'S TEMPERATURE USING TODAY'S THERMOMETER.", font=SE.get_font(18, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_088_fake_alpha_exposed(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE ILLUSION OF PREDICTIVE ALPHA", "WHY ACADEMIC CLAIMS OF 90% ACCURACY EVAPORATE IN LIVE CAPITAL")

    # Dual Speedometer: In-Sample Accuracy vs Forward Out-Of-Sample Edge
    SE.draw_speedometer_gauge(d, 91.5, 0.0, 100.0, "IN-SAMPLE FIT (TAUTOLOGY)", "%", W // 4 + 40, H // 2 + 10, 130, SE.DANGER_RED)
    SE.draw_speedometer_gauge(d, 0.2, 0.0, 100.0, "FORWARD REAL ALPHA", "%", 3 * W // 4 - 40, H // 2 + 10, 130, SE.CYAN)

    d.text((160, H - 200), "PREDICTING AUTOCORRELATED TIME SERIES WITH ITS OWN VALUE IS TRIVIAL, BUT OFFERS ZERO REAL TRADING EDGE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_089_lookahead_leak_card(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "LOOKAHEAD BIAS: FULL-SAMPLE LEAKAGE", "85TH PERCENTILE COMPUTED ACROSS ENTIRE HISTORICAL DATASET")

    # Timeline with future data scanning backward
    d.rounded_rectangle([160, 240, W - 160, H - 260], radius=10, fill=SE.BG_PANEL, outline=SE.DANGER_RED, width=2)
    d.text((200, 280), "FULL-SAMPLE QUANTILE CONTAMINATION:", font=SE.get_font(22, bold=True, mono=True), fill=SE.DANGER_RED)

    # Timeline bar
    tx0, tx1 = 200, W - 200
    ty = 400
    d.line([(tx0, ty), (tx1, ty)], fill=SE.BORDER_CYAN, width=4)

    # Points on timeline
    d.ellipse([(tx0 + 100 - 10, ty - 10), (tx0 + 100 + 10, ty + 10)], fill=SE.CYAN)
    d.text((tx0 + 70, ty + 25), "2024 TRAINING", font=SE.get_font(16, mono=True), fill=SE.CYAN)

    d.ellipse([(tx1 - 150 - 10, ty - 10), (tx1 - 150 + 10, ty + 10)], fill=SE.DANGER_RED)
    d.text((tx1 - 190, ty + 25), "2026 CRASH REALIZATION", font=SE.get_font(16, mono=True), fill=SE.DANGER_RED)

    # Scanbeam backward from 2026 to 2024
    scan_pos = tx1 - 150 - int((tx1 - tx0 - 250) * (t / max(0.1, dur * 0.8)) % (tx1 - tx0 - 250))
    d.line([(scan_pos, ty - 40), (scan_pos, ty + 40)], fill=SE.GOLD, width=3)
    d.text((scan_pos - 90, ty - 70), "<< FUTURE LEAK <<", font=SE.get_font(16, bold=True, mono=True), fill=SE.GOLD)

    d.text((200, 520), "COMPUTING QUANTILE(0.85) ON ENTIRE DATAFRAME ALLOWS 2026 CRASHES TO INFLUENCE 2024 LABELS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((160, H - 200), "A LETHAL CODE FLAW: UNREALIZED VOLATILITY LEAKED DIRECTLY INTO MODEL WEIGHT ESTIMATION.", font=SE.get_font(18, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_090_time_travel_crime(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "TIME-TRAVELER PREDICTION ANOMALY", "TEST-SET INFORMATION FLOWING BACKWARD INTO MODEL TRAINING")

    # Animated reverse wave
    SE.draw_waveform_oscilloscope(
        d, -t * 1.5, 180, 260, W - 360, 240,
        freq=2.0, amp=60, col=SE.DANGER_RED,
        title="TIME-REVERSED CONTAMINATION VECTOR (TEST SET -> TRAIN SET)", deadband=None
    )

    d.text((180, H - 210), "WHEN CODE 'LOOKS INTO THE FUTURE', EVEN A RANDOM NUMBER GENERATOR LOOKS LIKE GENIUS ALPHA.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_091_dismantling_the_rig(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE THREE LAWS OF SCIENTIFIC INTEGRITY", "ERADICATING CIRCULARITY, LEAKAGE, AND MULTI-TESTING CHERRY-PICKING")

    laws = [
        ("LAW 1: DECOUPLED SPOT DRAWDOWN", "TARGET = SPOT BTC MAXIMUM DRAWDOWN OVER HORIZON h", "ELIMINATES DVOL CIRCULARITY"),
        ("LAW 2: EXPANDING-ORIGIN THRESHOLD", "85TH PERCENTILE RE-ESTIMATED STRICTLY ON PAST DATA", "ELIMINATES LOOKAHEAD LEAK"),
        ("LAW 3: BENJAMINI-HOCHBERG FDR", "CORRECTING ACROSS ALL 28 TOURNAMENT HYPOTHESIS TESTS", "ELIMINATES P-HACKING")
    ]
    card_w = (W - 280) // 3
    for i, (l_head, l_sub, l_ben) in enumerate(laws):
        bx = 140 + i * card_w
        active = (t / max(0.1, dur * 0.7)) > (i / 3)
        border_col = SE.GREEN if active else SE.BORDER_CYAN
        fill_col = SE.BG_TINT_GREEN if active else SE.BG_PANEL

        d.rounded_rectangle([bx + 8, 250, bx + card_w - 8, H - 240], radius=8, fill=fill_col, outline=border_col, width=2)
        d.text((bx + 20, 280), f"RULE 0{i+1}", font=SE.get_font(16, bold=True, mono=True), fill=SE.GOLD)
        d.text((bx + 20, 330), l_head, font=SE.get_font(20, bold=True), fill=SE.TEXT_WHITE)
        d.text((bx + 20, 420), l_sub, font=SE.get_font(14, mono=True), fill=SE.CYAN)
        d.line([(bx + 20, 480), (bx + card_w - 28, 480)], fill=SE.BORDER_CYAN)
        d.text((bx + 20, 510), l_ben, font=SE.get_font(15, bold=True, mono=True), fill=SE.GREEN if active else SE.TEXT_MUTED)

    d.text((140, H - 200), "THREE NON-NEGOTIABLE PROTOCOLS: COMPLETE MATHEMATICAL AND EMPIRICAL DISINFECTION.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_092_rule_1_target_decouple(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "RULE 1: FORWARD SPOT MAX DRAWDOWN TARGET", "Y_t = I( max_{1<=k<=h} (P_t - P_{t+k})/P_t >= theta_t )")

    # Candlestick chart showing forward drawdown zone
    SE.draw_candlestick_chart(d, x=180, y=240, w=W - 360, h=H - 480, t=t, dur=dur, trend="bearish")

    # Shaded evaluation window [t+1, t+h]
    wx = 180 + int((W - 360) * 0.65)
    d.rectangle([wx, 240, wx + 180, H - 240], fill=SE.BG_TINT_GOLD, outline=SE.GOLD, width=1)
    d.text((wx + 15, 260), "WINDOW [t+1, t+h]", font=SE.get_font(14, bold=True, mono=True), fill=SE.GOLD)
    d.text((wx + 15, 290), "MAX DRAWDOWN", font=SE.get_font(12, mono=True), fill=SE.TEXT_WHITE)

    d.text((180, H - 200), "CLEAN SEPARATION: SPOT BITCOIN PRICE ALONE DETERMINES THE DRAWDOWN TARGET (ZERO DVOL INPUT).", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_093_rule_2_rolling_threshold(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "RULE 2: ROLLING EXPANDING THRESHOLD", "RE-ESTIMATING 85TH PERCENTILE AS-OF ORIGIN T_0")

    # Rolling origin visualization
    d.rounded_rectangle([160, 240, W - 160, H - 260], radius=10, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
    d.text((200, 280), "STRICT POINT-IN-TIME THRESHOLD CALCULATION:", font=SE.get_font(22, bold=True, mono=True), fill=SE.CYAN)

    bx0, bx1 = 200, W - 200
    by = 420
    d.line([(bx0, by), (bx1, by)], fill=SE.BORDER_CYAN, width=4)

    # Expanding frontier
    frontier_x = bx0 + int((bx1 - bx0) * min(1.0, 0.3 + 0.6 * (t / max(0.1, dur * 0.8))))
    d.rectangle([bx0, by - 30, frontier_x, by + 30], fill=SE.BG_TINT_GREEN, outline=SE.GREEN, width=2)
    d.text((bx0 + 20, by - 55), "AVAILABLE TRAINING HISTORY (T <= T_0)", font=SE.get_font(16, bold=True, mono=True), fill=SE.GREEN)

    d.line([(frontier_x, by - 50), (frontier_x, by + 50)], fill=SE.GOLD, width=3)
    d.text((frontier_x - 60, by + 65), "ORIGIN T_0", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)

    d.text((frontier_x + 30, by - 20), "UNTOUCHED FUTURE (T > T_0) -> ZERO LEAKAGE", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)

    d.text((160, H - 200), "POINT-IN-TIME RIGOR: AS CRASHES OCCUR IN REAL TIME, THE CRISIS THRESHOLD EVOLVES DYNAMICALLY.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_094_rule_3_fdr_control(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "RULE 3: BENJAMINI-HOCHBERG FDR CONTROL", "PREVENTING CHERRY-PICKED p-VALUES ACROSS 28 TESTS")

    # Draw p-value FDR plot
    pvals = [0.0000, 0.0002, 0.0040, 0.0910, 0.1250, 0.2200, 0.3100, 0.4578, 0.5550, 0.6840, 0.7817, 0.7905]
    SE.draw_pvalue_fdr_plot(d, pvals, q_val=0.05, x=180, y=240, w=W - 360, h=H - 480, t=t)

    d.text((180, H - 200), "FALSE DISCOVERY RATE CONTROL: ENFORCING BOUNDARY (k/m)*alpha. ONLY 3 TESTS LIE BELOW LINE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_095_fdr_mathematics(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE BENJAMINI-HOCHBERG EQUATION (1995)", "RANKING p-VALUES: p_{(1)} <= p_{(2)} <= ... <= p_{(m)}")

    d.rounded_rectangle([160, 240, W - 160, 480], radius=10, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
    d.text((200, 270), "CRITICAL REJECTION CRITERION:", font=SE.get_font(22, bold=True, mono=True), fill=SE.GOLD)
    d.text((200, 330), "p_(k) <= (k / m) * alpha_FDR,   WHERE alpha = 0.05, m = 28", font=SE.get_font(38, bold=True, mono=True), fill=SE.CYAN)
    d.text((200, 410), "FIND LARGEST INDEX k*. REJECT ALL NULL HYPOTHESES H_(1), ..., H_(k*).", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)

    d.text((160, H - 210), "HARVARD & STANFORD GOLD STANDARD: GUARANTEES THAT NO MORE THAN 5% OF ACCEPTED CLAIMS ARE FALSE POSITIVES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_096_rerunning_tournament(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "RERUNNING THE TOURNAMENT ACROSS 292 ORIGINS", "EXPANDING WINDOW EVALUATION OF ALL 8 MODELS")

    # 8x4 matrix of test cells ticking through
    models = ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7"]
    horizons = ["1-DAY", "3-DAY", "7-DAY", "14-DAY"]

    cw = (W - 320) // len(horizons)
    rh = 42
    oy = 250

    for j, h_lbl in enumerate(horizons):
        d.text((240 + j * cw, oy), h_lbl, font=SE.get_font(16, bold=True, mono=True), fill=SE.GOLD)

    total_cells = len(models) * len(horizons)
    active_cell = int(t * 12) % total_cells

    for i, m_lbl in enumerate(models):
        y = oy + 40 + i * rh
        d.text((160, y + 10), m_lbl, font=SE.get_font(16, bold=True, mono=True), fill=SE.CYAN)
        for j in range(len(horizons)):
            cell_idx = i * len(horizons) + j
            bx = 230 + j * cw
            is_cur = (cell_idx == active_cell)
            fill_col = SE.BG_TINT_GOLD if is_cur else SE.BG_PANEL
            border_col = SE.GOLD if is_cur else SE.BORDER_CYAN
            d.rectangle([bx, y, bx + cw - 12, y + rh - 6], fill=fill_col, outline=border_col, width=1)
            txt_col = SE.GREEN if (i in (4, 5) and j == 0) else (SE.CYAN if cell_idx < active_cell else SE.TEXT_MUTED)
            d.text((bx + 20, y + 8), "COMPUTING..." if is_cur else ("VERIFIED" if cell_idx < active_cell else "QUEUED"), font=SE.get_font(12, mono=True), fill=txt_col)

    d.text((160, H - 200), "TOTAL COMPUTE MATRIX: 8 MODELS x 4 HORIZONS x 292 RE-ESTIMATION STEPS = 9,344 MODEL FITS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_097_m2_collapse(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE SUDDEN COLLAPSE OF M2 SINGLE-DOMAIN", "CONFIRMING THE CIRCULARITY HYPOTHESIS")

    # Side-by-side bar comparison: Circular (+0.322) vs Honest (-0.0056)
    categories = ["CIRCULAR TARGET (FLAWED)", "HONEST SPOT DRAWDOWN (DISINFECTED)"]
    values = [0.322, -0.0056]
    colors = [SE.DANGER_RED, SE.GREEN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=0.40,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "SMOKING GUN CONFIRMED: M2'S +0.322 SCORE WAS 100% ARTIFICIAL TAUTOLOGY. REAL SKILL = -0.0056.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_098_fdr_rejection_slaughter(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE STATISTICAL SLAUGHTER", "25 OUT OF 28 TOURNAMENT HYPOTHESIS TESTS FAIL FDR CONTROL")

    # Big dramatic numbers
    d.rounded_rectangle([160, 240, W // 2 - 40, H - 240], radius=10, fill=SE.BG_TINT_RED, outline=SE.DANGER_RED, width=2)
    d.text((200, 280), "REJECTED HYPOTHESES (NOISE)", font=SE.get_font(22, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((200, 360), "25", font=SE.get_font(120, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((200, 520), "89.3% OF CLAIMED STATISTICAL SKILL FAILED FDR AUDIT", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)

    d.rounded_rectangle([W // 2 + 40, 240, W - 160, H - 240], radius=10, fill=SE.BG_TINT_GREEN, outline=SE.GREEN, width=2)
    d.text((W // 2 + 80, 280), "SURVIVING HYPOTHESES (SIGNAL)", font=SE.get_font(22, bold=True, mono=True), fill=SE.GREEN)
    d.text((W // 2 + 80, 360), "03", font=SE.get_font(120, bold=True, mono=True), fill=SE.GREEN)
    d.text((W // 2 + 80, 520), "SURVIVES BENJAMINI-HOCHBERG AT alpha = 0.05", font=SE.get_font(16, mono=True), fill=SE.CYAN)

    d.text((160, H - 200), "RIGOROUS CLEANSING: ONLY 3 SIGNALS ACROSS 28 TESTS PROVE STATISTICALLY GENUINE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_evidence_badge(d, 2, "25/28 MODELS FAILED FDR CORRECTION", "FDR q-VALUE >= 0.55 (SPURIOUS NOISE)")
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_099_horizon_collapse_7d(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "HORIZON = 7 DAYS: ZERO STATISTICAL SKILL", "ALL 8 MODELS INDISTINGUISHABLE FROM CLIMATOLOGY")

    categories = ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7"]
    values = [-0.01, 0.00, -0.04, -0.02, -0.01, +0.02, -0.03, -0.04]
    colors = [SE.DANGER_RED] * 8

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=0.10,
        x=180, y=240, w=W - 360, h=H - 480,
        t=t, dur=dur, colors=colors
    )
    d.text((180, H - 200), "ALL 7-DAY BRIER SKILL SCORES <= 0.02 // FDR q-VALUES >= 0.7817 (TOTAL NOISE REGIME).", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_100_horizon_collapse_14d(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "HORIZON = 14 DAYS: TOTAL EXTINCTION", "PREDICTING A CRYPTO CRASH TWO WEEKS AWAY IS STATISTICAL NOISE")

    categories = ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7"]
    values = [-0.05, -0.02, -0.08, -0.06, -0.04, -0.03, -0.07, -0.09]
    colors = [SE.DANGER_RED] * 8

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=0.10,
        x=180, y=240, w=W - 360, h=H - 480,
        t=t, dur=dur, colors=colors
    )
    d.text((180, H - 200), "14-DAY FORECASTING EXTINCTION: ALL MODELS PERFORM WORSE THAN SIMPLE UNCONDITIONAL BASELINE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_101_the_two_survivors(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE TWO VALIDATED SURVIVORS", "SURVIVING BENJAMINI-HOCHBERG FDR CONTROL AT alpha = 0.05")

    # Two podium cards
    d.rounded_rectangle([160, 240, W // 2 - 40, H - 240], radius=10, fill=SE.BG_TINT_GREEN, outline=SE.GREEN, width=2)
    d.text((200, 280), "SURVIVOR 1: M4 DYNAMIC-AR", font=SE.get_font(24, bold=True, mono=True), fill=SE.GREEN)
    d.text((200, 350), "HORIZON: 1-DAY & 3-DAY", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)
    d.text((200, 410), "DM p-VALUE: 0.0000", font=SE.get_font(28, bold=True, mono=True), fill=SE.CYAN)
    d.text((200, 460), "FDR q-VALUE: 0.0000 (PASSED)", font=SE.get_font(22, bold=True, mono=True), fill=SE.GREEN)

    d.rounded_rectangle([W // 2 + 40, 240, W - 160, H - 240], radius=10, fill=SE.BG_TINT_GOLD, outline=SE.GOLD, width=2)
    d.text((W // 2 + 80, 280), "SURVIVOR 2: M5 LIGHTGBM", font=SE.get_font(24, bold=True, mono=True), fill=SE.GOLD)
    d.text((W // 2 + 80, 350), "HORIZON: 1-DAY SHORTRANGE", font=SE.get_font(20, mono=True), fill=SE.TEXT_WHITE)
    d.text((W // 2 + 80, 410), "BSS: +0.2523 (ARENA LEADER)", font=SE.get_font(28, bold=True, mono=True), fill=SE.GOLD)
    d.text((W // 2 + 80, 460), "FDR q-VALUE: 0.0373 (PASSED)", font=SE.get_font(22, bold=True, mono=True), fill=SE.GREEN)

    d.text((160, H - 200), "AUTHENTIC DISCOVERY: TWO INDEPENDENT ARCHITECTURES PROVE ROBUST UNDER RIGID TESTING.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_102_m4_stats_card(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "M4 DYNAMIC-AR VERIFIED PERFORMANCE", "DIEBOLD-MARIANO p = 0.0000 // FDR q = 0.0000")

    # M4 Speedometer Gauges: Diebold Mariano test & FDR q-val
    SE.draw_speedometer_gauge(d, 0.0000, 0.0, 0.05, "DM TEST p-VAL", "PROB", W // 4 + 40, H // 2 + 10, 130, SE.GREEN)
    SE.draw_speedometer_gauge(d, 0.0000, 0.0, 0.05, "BENJAMINI-HOCHBERG q-VAL", "FDR", 3 * W // 4 - 40, H // 2 + 10, 130, SE.CYAN)

    d.text((160, H - 200), "M4 PROVES THAT HISTORICAL DRAWDOWN MOMENTUM TRANSMITS A HIGH-INTEGRITY 24H RESIDUAL SIGNAL.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_103_m5_stats_card(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "M5 LIGHTGBM VERIFIED PERFORMANCE", "OUT-OF-SAMPLE BRIER SKILL SCORE = +0.2523 (HIGHEST IN ARENA)")

    SE.draw_speedometer_gauge(d, 0.2523, 0.0, 0.40, "BRIER SKILL SCORE", "BSS", W // 4 + 40, H // 2 + 10, 130, SE.GOLD)
    SE.draw_speedometer_gauge(d, 0.0373, 0.0, 0.05, "FDR q-VALUE (< 0.05)", "q", 3 * W // 4 - 40, H // 2 + 10, 130, SE.GREEN)

    d.text((160, H - 200), "M5 LIGHTGBM EXTRACTS NON-LINEAR CROSS-DERIVATIVE SIGNALS, ACHIEVING OUT-OF-SAMPLE SKILL BSS = +0.2523.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_104_bootstrap_confidence_ci(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "BOOTSTRAP 95% CONFIDENCE INTERVALS", "M5 95% CI: [+0.0078, +0.4156] STRICTLY EXCLUDES ZERO")

    # Bootstrap Resampling Bell Curve
    cx, cy = W // 2, H // 2 + 30
    w_box, h_box = 760, 260
    d.rounded_rectangle([cx - w_box // 2, cy - h_box // 2, cx + w_box // 2, cy + h_box // 2], radius=10, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)

    pts = []
    x0, x1 = cx - w_box // 2 + 60, cx + w_box // 2 - 60
    y_base = cy + h_box // 2 - 30
    for i in range(100):
        x = x0 + int(i * (x1 - x0) / 99)
        z = (i - 55) / 16.0
        dens = math.exp(-0.5 * z * z)
        y = y_base - int(dens * 170)
        pts.append((x, y))

    if len(pts) > 1:
        d.line(pts, fill=SE.GREEN, width=3)

    # Zero line on left
    zero_x = x0 + int(20 * (x1 - x0) / 99)
    d.line([(zero_x, cy - h_box // 2 + 20), (zero_x, y_base)], fill=SE.DANGER_RED, width=2)
    d.text((zero_x - 35, cy - h_box // 2 + 30), "ZERO LINE", font=SE.get_font(14, bold=True, mono=True), fill=SE.DANGER_RED)

    # 95% CI Band
    ci_low = x0 + int(24 * (x1 - x0) / 99)
    ci_high = x0 + int(86 * (x1 - x0) / 99)
    d.line([(ci_low, y_base + 12), (ci_high, y_base + 12)], fill=SE.GOLD, width=4)
    d.text((ci_low, y_base + 22), "[+0.0078", font=SE.get_font(14, bold=True, mono=True), fill=SE.GOLD)
    d.text((ci_high - 60, y_base + 22), "+0.4156]", font=SE.get_font(14, bold=True, mono=True), fill=SE.GOLD)

    d.text((160, H - 200), "1,000 BOOTSTRAP DRAWS: 95% CONFIDENCE INTERVAL STRICTLY SITS ABOVE ZERO. STATISTICALLY AUTHENTIC.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_105_m7_dlm_failure(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "M7 CENTRAL BANK DLM CLASSIFIER RESULT", "BRIER SKILL SCORE = +0.0030 // FDR q = 0.7905 (NOT SIGNIFICANT)")

    SE.draw_speedometer_gauge(d, 0.0030, 0.0, 0.20, "M7 BRIER SKILL", "BSS", W // 4 + 40, H // 2 + 10, 130, SE.DANGER_RED)
    SE.draw_speedometer_gauge(d, 0.7905, 0.0, 1.0, "FDR q-VALUE (FAIL)", "q", 3 * W // 4 - 40, H // 2 + 10, 130, SE.DANGER_RED)

    d.text((160, H - 200), "THE FLAGSHIP CENTRAL BANK MODEL FAILS AS A BINARY TRADING PREDICTOR: q = 0.7905 (79% NOISE PROBABILITY).", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_106_why_m7_failed_direction(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "WHY STATE-SPACE SMOOTHING FAILS TRADING", "KALMAN SMOOTHING ASSUMES GAUSSIAN DYNAMICS // CRYPTO IS POISSON-JUMP")

    # Kalman smooth curve (top) vs Flash crash discontinuous cliff (bottom)
    SE.draw_waveform_oscilloscope(
        d, t, 160, 240, W - 320, 180,
        freq=0.8, amp=35, col=SE.CYAN,
        title="KALMAN CONTINUOUS FILTERED STATE (SMOOTH GAUSSIAN ASSUMPTION)", deadband=None
    )
    SE.draw_waveform_oscilloscope(
        d, t, 160, 460, W - 320, 180,
        freq=2.8, amp=65, col=SE.DANGER_RED,
        title="REALITY: CRYPTO POISSON-JUMP LIQUIDATION SPIKES", deadband=None
    )

    d.text((160, H - 200), "THE KALMAN PARADOX: THE KALMAN FILTER SMOOTHS OUT THE VERY FLASH CRASHES IT SEEKS TO DETECT.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_107_the_cold_truth(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE UNFORGIVING TRUTH", "CRYPTO MARKET EFFICIENCY ABSORBS MACRO SIGNALS WITHIN 24 TO 72 HOURS")

    # Information half-life decay bar
    categories = ["1-DAY (SIGNAL)", "2-DAYS (DECAY)", "3-DAYS (BORDER)", "7-DAYS (NOISE)", "14-DAYS (NOISE)"]
    values = [0.2523, 0.1240, 0.0812, 0.0030, -0.0415]
    colors = [SE.GREEN, SE.CYAN, SE.GOLD, SE.DANGER_RED, SE.DANGER_RED]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=0.30,
        x=180, y=240, w=W - 360, h=H - 480,
        t=t, dur=dur, colors=colors
    )
    d.text((180, H - 200), "MARKET EFFICIENCY LAW: ANYONE CLAIMING MULTI-WEEK TIMING ALPHA ON PUBLIC TICK FEEDS IS SELLING FICTION.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_108_from_stats_to_pnl(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "FROM STATISTICAL SCORE TO REAL CAPITAL", "DOES STATISTICAL SKILL ACTUALLY PROTECT REAL MONEY?")

    # 4-stage bridge from math to capital
    steps = [
        ("STATISTICAL BSS", "+0.2523 SCORE"),
        ("SIGNAL CONVERSION", "P >= 0.20 THRESHOLD"),
        ("PERPETUAL EXECUTION", "1.0X SHORT OVERLAY"),
        ("NET PORTFOLIO P&L", "SHARPE & DRAWDOWN")
    ]
    step_active = min(3, int(t * 1.8))
    SE.draw_flow_diagram(d, steps, step_active, x=120, y=300, w=W - 240, h=180, t=t)

    d.text((120, H - 210), "TESTING IN LIVE CAPITAL: DOES A SURVIVING FDR SIGNAL CONVERT INTO ACTUAL RISK-ADJUSTED WEALTH?", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_109_simulation_prep(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "CONSTRUCTING THE REALISTIC HEDGE ENGINE", "100% BTC SPOT + 1.0X BINANCE SHORT PERPETUAL OVERLAY")

    # Schematic cards: Spot Asset + Derivative Overlay + Friction Engine
    cards = [
        ("PORTFOLIO BASE", "100% SPOT BITCOIN", "HELD CONTINUOUSLY // ZERO TAXABLE DISPOSAL", SE.CYAN),
        ("HEDGE OVERLAY", "1.0X BINANCE SHORT PERP", "OPENED ONLY WHEN P(CRASH) >= 0.20", SE.GOLD),
        ("MARKET FRICTION", "10 BPS ROUND-TRIP", "5 BPS TAKER FEE + 5 BPS SLIPPAGE PER FLIP", SE.DANGER_RED),
        ("CASH FLOW HARVEST", "LIVE 8H FUNDING", "RECEIVE OR PAY ACTUAL PERPETUAL BASIS", SE.GREEN)
    ]
    cw = (W - 280) // 4
    for i, (c_tit, c_sub, c_desc, c_col) in enumerate(cards):
        bx = 140 + i * cw
        d.rounded_rectangle([bx + 6, 260, bx + cw - 6, H - 240], radius=8, fill=SE.BG_PANEL, outline=c_col, width=2)
        d.text((bx + 18, 290), c_tit, font=SE.get_font(15, bold=True, mono=True), fill=SE.TEXT_MUTED)
        d.text((bx + 18, 340), c_sub, font=SE.get_font(18, bold=True), fill=c_col)
        d.line([(bx + 18, 410), (bx + cw - 24, 410)], fill=SE.BORDER_CYAN)
        d.text((bx + 18, 440), c_desc, font=SE.get_font(13, mono=True), fill=SE.TEXT_WHITE)

    d.text((140, H - 200), "ZERO DELUSIONS: EVERY BASIS POINT OF EXCHANGE TAKER FEES AND SLIPPAGE IS FULLY DEDUCTED.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_110_act4_transition(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT IV // THE WALK-FORWARD HEDGE")

    cx, cy = W // 2, H // 2
    d.text((cx - 420, cy - 60), "ACT IV: THE WALK-FORWARD HEDGE", font=SE.get_font(52, bold=True), fill=SE.TEXT_WHITE)
    d.text((cx - 360, cy + 30), "SAVING CAPITAL FROM THE 51% DRAWDOWN", font=SE.get_font(24, mono=True), fill=SE.CYAN)
    d.line([(cx - 420, cy + 85), (cx + 420, cy + 85)], fill=SE.BORDER_CYAN, width=2)

    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
