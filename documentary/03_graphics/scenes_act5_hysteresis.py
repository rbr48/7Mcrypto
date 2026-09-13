# -*- coding: utf-8 -*-
"""
Procedural Scene Renderers — ACT 5: THE ONE-BIT TRAP & HYSTERESIS (Scenes 136 - 155)
1080p 30 FPS cinematic motion graphics for @izhaanintellect.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import style_engine as SE

W, H = SE.W, SE.H


def draw_header(d, title, sub):
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT 5 // ONE-BIT TRAP & HYSTERESIS")
    f_t = SE.get_font(40, bold=True)
    f_s = SE.get_font(20, mono=True)
    d.text((80, 85), title, font=f_t, fill=SE.TEXT_WHITE)
    d.text((82, 140), sub, font=f_s, fill=SE.CYAN)
    d.line([(80, 175), (W - 80, 175)], fill=SE.BORDER_CYAN, width=1)


def s_136_sensitivity_sweep_grid(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "CRITICAL THRESHOLD SENSITIVITY SWEEP", "SYSTEMATICALLY SWEEPING ACTIVATION THRESHOLD theta FROM 0.10 TO 0.40")

    thresholds = ["0.10", "0.15", "0.20 (BASE)", "0.25", "0.30", "0.35", "0.40"]
    x0, y0 = 120, 240
    col_w = (W - 240) // len(thresholds)

    f_th = SE.get_font(20, bold=True, mono=True)
    f_lbl = SE.get_font(15, mono=True)

    d.text((120, 205), "TESTED THRESHOLD PARAMETERS (theta):", font=SE.get_font(20, bold=True), fill=SE.GOLD)

    for i, th in enumerate(thresholds):
        bx = x0 + i * col_w
        is_base = "BASE" in th
        border_col = SE.GOLD if is_base else SE.BORDER_CYAN
        fill_col = SE.BG_TINT_GOLD if is_base else SE.BG_PANEL

        d.rounded_rectangle([bx + 6, y0, bx + col_w - 6, y0 + 440], radius=8, fill=fill_col, outline=border_col, width=2 if is_base else 1)
        d.text((bx + 14, y0 + 18), th, font=f_th, fill=SE.GOLD if is_base else SE.CYAN)

        progress = (t / max(0.1, dur * 0.8)) * (len(thresholds) + 1)
        active = (i <= progress)
        dot_col = SE.GREEN if active else SE.TEXT_MUTED

        d.ellipse([(bx + col_w // 2 - 8, y0 + 80), (bx + col_w // 2 + 8, y0 + 96)], fill=dot_col)
        status_txt = "ANALYZED" if active else "QUEUED"
        d.text((bx + 18, y0 + 120), status_txt, font=f_lbl, fill=dot_col)

        if active:
            d.text((bx + 14, y0 + 190), "WALK-FORWARD", font=SE.get_font(12, mono=True), fill=SE.TEXT_MUTED)
            d.text((bx + 14, y0 + 220), "292 ROLLING", font=SE.get_font(14, bold=True, mono=True), fill=SE.TEXT_WHITE)
            d.text((bx + 14, y0 + 250), "ORIGINS", font=SE.get_font(12, mono=True), fill=SE.TEXT_MUTED)
            d.line([(bx + 14, y0 + 295), (bx + col_w - 20, y0 + 295)], fill=SE.BORDER_CYAN)
            d.text((bx + 14, y0 + 320), "10 BPS FEE", font=SE.get_font(13, mono=True), fill=SE.DANGER_RED)
            d.text((bx + 14, y0 + 350), "ACTIVE", font=SE.get_font(14, bold=True, mono=True), fill=SE.GREEN)

    d.text((120, H - 210), "OBJECTIVE: DETERMINE WHETHER M0'S +477% AND M5'S +420% ARE GENUINE OR ARTIFACTS OF alpha = 0.20.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_137_m0_frozen_anomaly(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE M0 FROZEN ANOMALY: A SHOCKING DISCOVERY", "EXACT IDENTICAL PERFORMANCE AT EVERY SINGLE THRESHOLD VALUE")

    d.rounded_rectangle([120, 230, W - 120, H - 240], radius=10, fill=SE.BG_PANEL, outline=SE.DANGER_RED, width=2)

    headers = ["THRESHOLD (theta)", "NET RETURN", "MAX DRAWDOWN", "TOTAL HEDGE FLIPS", "FRICTION LOSS"]
    f_h = SE.get_font(17, bold=True, mono=True)
    f_v = SE.get_font(20, mono=True)

    col_xs = [160, 540, 860, 1200, 1520]
    for idx, h_txt in enumerate(headers):
        d.text((col_xs[idx], 260), h_txt, font=f_h, fill=SE.CYAN)
    d.line([(140, 305), (W - 140, 305)], fill=SE.BORDER_CYAN, width=2)

    rows = [
        ("theta = 0.10", "+477.79%", "-12.89%", "38 FLIPS", "-10.14%"),
        ("theta = 0.15", "+477.79%", "-12.89%", "38 FLIPS", "-10.14%"),
        ("theta = 0.20", "+477.79%", "-12.89%", "38 FLIPS", "-10.14%"),
        ("theta = 0.30", "+477.79%", "-12.89%", "38 FLIPS", "-10.14%"),
        ("theta = 0.40", "+477.79%", "-12.89%", "38 FLIPS", "-10.14%"),
    ]

    for r_idx, (c0, c1, c2, c3, c4) in enumerate(rows):
        y = 340 + r_idx * 64
        d.rectangle([140, y - 8, W - 140, y + 42], fill=SE.BG_TINT_RED if r_idx % 2 == 0 else SE.BG_PANEL)
        d.text((col_xs[0], y), c0, font=f_v, fill=SE.GOLD)
        d.text((col_xs[1], y), c1, font=f_v, fill=SE.DANGER_RED)
        d.text((col_xs[2], y), c2, font=f_v, fill=SE.DANGER_RED)
        d.text((col_xs[3], y), c3, font=f_v, fill=SE.DANGER_RED)
        d.text((col_xs[4], y), c4, font=f_v, fill=SE.DANGER_RED)

    d.text((140, H - 210), "ZERO ELASTICITY: NOT A SINGLE FLIP OR RETURN BASIS POINT CHANGES ACROSS THE ENTIRE SPECTRUM!", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_138_zero_elasticity_revealed(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "ZERO THRESHOLD ELASTICITY EXPOSED", "d(PERFORMANCE) / d(theta) == 0.000000 // A MATHEMATICAL RED FLAG")

    # Flatline derivative oscilloscope
    SE.draw_waveform_oscilloscope(
        d, t, 180, 250, W - 360, 240,
        freq=0.0, amp=0, col=SE.DANGER_RED,
        title="FIRST DERIVATIVE d(HEDGE_RETURN) / d(theta) == 0.000000 (TOTAL INERTIA)", deadband=None
    )

    d.text((180, H - 210), "MATHEMATICAL IMPOSSIBILITY: A TRUE PROBABILITY MODEL MUST RESPOND AS CUTOFF THRESHOLD MOVES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_139_code_dissection_m0(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SOURCE CODE FORENSICS // CRYPTO_BASELINES.PY", "DISSECTING THE MATHEMATICAL ROOT CAUSE OF THE FROZEN SIGNAL")

    term_bg = (248, 250, 254) if SE.THEME == "LIGHT" else (8, 12, 18)
    title_bg = (235, 240, 248) if SE.THEME == "LIGHT" else (18, 28, 44)
    term_border = (205, 218, 235) if SE.THEME == "LIGHT" else SE.CYAN

    d.rounded_rectangle([120, 220, W - 120, H - 240], radius=8, fill=term_bg, outline=term_border, width=2)
    d.rectangle([120, 220, W - 120, 265], fill=title_bg)
    d.ellipse([(140, 236), (154, 250)], fill=SE.DANGER_RED)
    d.ellipse([(164, 236), (178, 250)], fill=SE.GOLD)
    d.ellipse([(188, 236), (202, 250)], fill=SE.GREEN)
    d.text((220, 233), "src/models/crypto_baselines.py — PersistenceModel.predict_proba()", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)

    lines = [
        ("def predict_proba(self, h: int = 1):", SE.CYAN),
        ("    decay = np.exp(-0.05 * (h - 1))   # exponential decay to baseline", SE.TEXT_MUTED),
        ("    if h == 1:                         # 1-DAY HORIZON:", SE.GOLD),
        ("        decay = 1.0                    # EXACT EXP(0) = 1.0", SE.GREEN),
        ("    ", SE.TEXT_WHITE),
        ("    # The fatal collapse:", SE.DANGER_RED),
        ("    prob = 0.99 if last_state == 1 else 0.01", SE.DANGER_RED),
        ("    return prob", SE.CYAN),
    ]

    f_c = SE.get_font(22, mono=True)
    for i, (line_txt, col) in enumerate(lines):
        if "prob = 0.99" in line_txt:
            d.rectangle([140, 280 + i * 40, W - 140, 318 + i * 40], fill=SE.BG_TINT_RED)
        d.text((160, 282 + i * 40), line_txt, font=f_c, fill=col)

    d.text((120, H - 210), "ROOT CAUSE FOUND: PROBABILITY WAS HARDCODED TO 0.99 OR 0.01. IT WAS A 1-BIT REGISTER ALL ALONG!", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_140_the_one_bit_formula(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE 1-BIT REGISTER COLLAPSE", "P(t) in { 0.01 , 0.99 } // TOTAL LOSS OF PROBABILITY CONTINUUM")

    d.rounded_rectangle([180, 240, W // 2 - 40, H - 240], radius=12, fill=SE.BG_PANEL, outline=SE.GREEN, width=2)
    d.text((220, 280), "STATE 0: CALM REGIME", font=SE.get_font(24, bold=True, mono=True), fill=SE.GREEN)
    d.text((220, 370), "P(CRASH) = 0.01", font=SE.get_font(52, bold=True, mono=True), fill=SE.TEXT_WHITE)
    d.text((220, 470), "STRICTLY BELOW 0.10, 0.20, 0.30, 0.40", font=SE.get_font(18, mono=True), fill=SE.TEXT_MUTED)
    d.text((220, 520), "HEDGE ALWAYS OFF", font=SE.get_font(24, bold=True, mono=True), fill=SE.GREEN)

    d.rounded_rectangle([W // 2 + 40, 240, W - 180, H - 240], radius=12, fill=SE.BG_PANEL, outline=SE.DANGER_RED, width=2)
    d.text((W // 2 + 80, 280), "STATE 1: CRISIS REGIME", font=SE.get_font(24, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W // 2 + 80, 370), "P(CRASH) = 0.99", font=SE.get_font(52, bold=True, mono=True), fill=SE.TEXT_WHITE)
    d.text((W // 2 + 80, 470), "STRICTLY ABOVE 0.10, 0.20, 0.30, 0.40", font=SE.get_font(18, mono=True), fill=SE.TEXT_MUTED)
    d.text((W // 2 + 80, 520), "HEDGE ALWAYS ON", font=SE.get_font(24, bold=True, mono=True), fill=SE.DANGER_RED)

    d.text((180, H - 200), "BECAUSE 0.01 < THETA < 0.99 FOR ALL REASONABLE THRESHOLDS, M0'S TRADING LEDGER NEVER CHANGED.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_141_the_light_switch_analogy(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE LIGHT SWITCH VS THE DIMMER DIAL", "WHY A BINARY PERSISTENCE RULE CANNOT BE USED FOR REAL RISK CONTROL")

    # Rotary Dimmer Dial (Left) vs Broken Binary Switch (Right)
    dial_rot = (t * 0.8) % 1.0
    SE.draw_speedometer_gauge(d, dial_rot * 100, 0.0, 100.0, "CONTINUOUS DIMMER DIAL", "% CALIB", W // 4 + 40, H // 2 + 10, 130, SE.CYAN)

    d.rounded_rectangle([W // 2 + 40, 240, W - 160, H - 240], radius=10, fill=SE.BG_TINT_RED, outline=SE.DANGER_RED, width=2)
    d.text((W // 2 + 80, 280), "M0 BROKEN LIGHT SWITCH", font=SE.get_font(24, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W // 2 + 80, 360), "CANNOT BE TUNED OR CALIBRATED", font=SE.get_font(20, bold=True), fill=SE.TEXT_WHITE)
    d.text((W // 2 + 80, 420), "Institutions cannot set risk tolerance.", font=SE.get_font(18), fill=SE.TEXT_MUTED)
    d.text((W // 2 + 80, 470), "Its apparent victory was a lucky artifact of crypto's multi-day autocorrelation.", font=SE.get_font(16, mono=True), fill=SE.GOLD)

    d.text((160, H - 200), "REAL RISK MANAGEMENT REQUIRES A TUNABLE DIMMER DIAL — NOT AN UNCONTROLLABLE BINARY SWITCH.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_142_m0_fdr_failure_recall(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE BENJAMINI-HOCHBERG VERDICT ON M0", "STATISTICALLY INDISTINGUISHABLE FROM RANDOM GUESSING (q = 0.4578)")

    pvals = [0.0000, 0.0040, 0.4578, 0.7905]
    SE.draw_pvalue_fdr_plot(d, pvals, q_val=0.05, x=180, y=240, w=W - 360, h=H - 480, t=t)

    d.text((180, H - 200), "M0 PERSISTENCE FAILED FDR CONTROL WITH q = 0.4578 (46% FALSE DISCOVERY RATE). IT IS STATISTICALLY DEAD.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_143_m5_plateau_chart(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE M5 LIGHTGBM ROBUSTNESS PLATEAU", "MAINTAINS 32% TO 39% DRAWDOWN REDUCTION ACROSS THE ENTIRE THRESHOLD SPECTRUM")

    categories = ["0.10", "0.15", "0.20", "0.25", "0.30", "0.35", "0.40"]
    values = [32.4, 35.8, 38.4, 38.1, 35.2, 33.1, 32.0]
    colors = [SE.CYAN] * 7

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=45.0,
        x=180, y=240, w=W - 360, h=H - 480,
        t=t, dur=dur, colors=colors
    )
    d.text((180, H - 200), "STEADY RISK ABSORPTION: 32% - 39% OF MARKET CRASH SEVERITY CONSISTENTLY ERASED ACROSS ALL THRESHOLDS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_144_m5_tunable_dial(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE ONLY TUNABLE RISK CONTROLLER", "M5 PRODUCES A CONTINUOUS, CALIBRATED POSTERIOR PROBABILITY")

    SE.draw_speedometer_gauge(d, 38.38, 0.0, 50.0, "M5 CRASH ABSORPTION", "PP SAVED", W // 4 + 40, H // 2 + 10, 130, SE.GREEN)

    d.rounded_rectangle([W // 2 + 40, 240, W - 160, H - 240], radius=10, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
    d.text((W // 2 + 80, 280), "REAL QUANTITATIVE ELASTICITY:", font=SE.get_font(22, bold=True, mono=True), fill=SE.CYAN)
    d.text((W // 2 + 80, 350), "- Hedge days smoothly decrease from 48% to 18%", font=SE.get_font(18, mono=True), fill=SE.GOLD)
    d.text((W // 2 + 80, 400), "- Friction drag drops from 22.4% down to 8.2%", font=SE.get_font(18, mono=True), fill=SE.GREEN)
    d.text((W // 2 + 80, 450), "- Downside capture remains tightly bounded", font=SE.get_font(18, mono=True), fill=SE.CYAN)
    d.text((W // 2 + 80, 520), "Institutional risk officers have a true control surface.", font=SE.get_font(18, bold=True), fill=SE.TEXT_WHITE)

    d.text((160, H - 200), "CONTINUOUS CONTROL: M5 IS THE ONLY MODEL THAT OFFERS A PREDICTIVE, CALIBRATED DIAL FOR RISK OFFICERS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_145_baseline_inertia_explained(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE COMPRESSION COLLAPSE OF OTHER MODELS", "M1, M2, M3, M6, AND M7 CEASE TRADING AT theta >= 0.25")

    categories = ["M1 UNCOND", "M2 LOGISTIC", "M3 MULTI-LOG", "M6 2D-DLM", "M7 4D-DLM", "M5 LIGHTGBM"]
    values = [0, 0, 0, 0, 0, 36]  # Hedge days at theta = 0.30
    colors = [SE.DANGER_RED, SE.DANGER_RED, SE.DANGER_RED, SE.DANGER_RED, SE.DANGER_RED, SE.GREEN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=40,
        x=180, y=240, w=W - 360, h=H - 480,
        t=t, dur=dur, colors=colors
    )
    d.text((180, H - 200), "PROBABILITY COMPRESSION: LINEAR & STATE-SPACE MODELS FLATTEN EXTREMES, CEASING TRADES AT THETA >= 0.25.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_146_schmitt_trigger_diagram(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "ELECTRICAL ENGINEERING HYSTERESIS: SCHMITT TRIGGER", "REPLACING THE SINGLE THRESHOLD WITH A DUAL-BAND CONTROL DEAD-ZONE")

    cx, cy = W // 2, H // 2 + 10
    w_box, h_box = 720, 300
    d.rounded_rectangle([cx - w_box // 2, cy - h_box // 2, cx + w_box // 2, cy + h_box // 2], radius=10, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)

    # Threshold lines
    d.line([(cx - 150, cy - h_box // 2 + 30), (cx - 150, cy + h_box // 2 - 30)], fill=SE.GREEN, width=2)
    d.text((cx - 270, cy + h_box // 2 - 25), "EXIT THRESHOLD: P <= 0.15", font=SE.get_font(16, bold=True, mono=True), fill=SE.GREEN)

    d.line([(cx + 150, cy - h_box // 2 + 30), (cx + 150, cy + h_box // 2 - 30)], fill=SE.DANGER_RED, width=2)
    d.text((cx + 70, cy - h_box // 2 + 10), "ENTER THRESHOLD: P >= 0.25", font=SE.get_font(16, bold=True, mono=True), fill=SE.DANGER_RED)

    # Deadband
    d.rectangle([cx - 150, cy - 70, cx + 150, cy + 70], fill=SE.BG_TINT_GOLD, outline=SE.GOLD, width=1)
    d.text((cx - 130, cy - 12), "HYSTERESIS DEADBAND [0.15, 0.25]", font=SE.get_font(16, bold=True, mono=True), fill=SE.GOLD)
    d.text((cx - 110, cy + 16), "MAINTAIN CURRENT POSITION", font=SE.get_font(14, mono=True), fill=SE.TEXT_WHITE)

    d.text((160, H - 200), "DUAL-BAND STABILITY: REQUIRES CONVINCING PROBABILITY TO ENTER (0.25) AND TO EXIT (0.15).", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_147_hysteresis_oscilloscope_run(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "TAMING THE PROBABILITY FLICKER", "SIGNALS OSCILLATING AT 19.9% AND 20.1% ARE LOCKED INTO PLACE")

    # Oscilloscope with deadband
    SE.draw_waveform_oscilloscope(
        d, t * 2.0, 180, 240, W - 360, 240,
        freq=2.2, amp=40, col=SE.CYAN,
        title="SIGNAL HOVERING INSIDE HYSTERESIS DEADBAND — ZERO POSITION FLIPS TRIGGERED",
        deadband=(0.15, 0.25)
    )

    d.text((180, H - 200), "ZERO CHURN: MARGINAL OSCILLATIONS INSIDE [0.15, 0.25] PRESERVE STATE, SAVING THOUSANDS IN FEES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_148_flips_slashed_46(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "10 FLIPS INSTANTLY ELIMINATED", "TRADING CHURN SLASHED FROM 56 TRANSITIONS DOWN TO 46")

    categories = ["SINGLE THRESHOLD (theta = 0.20)", "SCHMITT HYSTERESIS [0.15, 0.25]"]
    values = [56, 46]
    colors = [SE.DANGER_RED, SE.GREEN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=70,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "18% REDUCTION IN TRADING TURNOVER: 10 COSTLY ROUND-TRIP WHIPSAWS ARE COMPLETELY FILTERED OUT.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_149_friction_saved_379(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "+3.79% CAPITAL PRESERVED FROM FEES", "TOTAL EXCHANGE FRICTION LOSS COLLAPSES FROM 16.37% TO 12.58%")

    categories = ["OLD FRICTION DRAG (56 FLIPS)", "NEW FRICTION DRAG (46 FLIPS)", "NET CAPITAL PRESERVED"]
    values = [16.37, 12.58, 3.79]
    colors = [SE.DANGER_RED, SE.CYAN, SE.GREEN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=20.0,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "+3.79% COMPOUNDED DIRECTLY TO PORTFOLIO NAV: REAL CASH DIVERTED FROM EXCHANGES BACK TO INVESTORS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_evidence_badge(d, 4, "SCHMITT HYSTERESIS SAVES +3.79% CAPITAL", "FLIPS: 56 -> 46 (ZERO DRAWDOWN PENALTY)")
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_150_drawdown_untouched(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE CRITICAL DISCOVERY: ZERO PROTECTION LOST", "MAXIMUM DRAWDOWN REMAINS LOCKED AT EXACTLY 12.95%")

    SE.draw_speedometer_gauge(d, 12.95, 0.0, 50.0, "BEFORE HYSTERESIS DD", "%", W // 4 + 40, H // 2 + 10, 130, SE.GREEN)
    SE.draw_speedometer_gauge(d, 12.95, 0.0, 50.0, "WITH HYSTERESIS DD", "%", 3 * W // 4 - 40, H // 2 + 10, 130, SE.GREEN)

    d.text((160, H - 200), "PERFECT RISK INTEGRITY: DOWNSIDE CRASH PROTECTION REMAINED AT EXACTLY 12.95%. ZERO SACRIFICE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_151_sortino_ratio_strength(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SORTINO RATIO SURGES TO 3.91", "DOWNSIDE VOLATILITY COLLAPSES WHILE RETENTION RISES")

    categories = ["UNHEDGED BITCOIN", "M5 BASE (THETA = 0.20)", "M5 HYSTERESIS [0.15, 0.25]"]
    values = [0.38, 3.78, 3.91]
    colors = [SE.DANGER_RED, SE.CYAN, SE.GREEN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=4.5,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "A 10X LEAP IN DOWNSIDE-ADJUSTED QUALITY: SORTINO 3.91 RANKS IN THE TOP 1% OF ALL INSTITUTIONAL STRATEGIES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_152_regime_stability(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "REGIME STABILITY CERTIFIED", "ELIMINATING ONE-DAY NOISE FLIPS TO PRESERVE MACRO CONTINUITY")

    # Flow diagram showing regime preservation
    steps = [
        ("CALM REGIME", "SPOT 100% UNHEDGED"),
        ("ENTRY HURDLE", "P >= 0.25 HIGH CONFIDENCE"),
        ("DEFENSE HOLD", "LOCKED IN SOLID BLOCK"),
        ("EXIT HURDLE", "P <= 0.15 VOL RECEDES")
    ]
    step_active = min(3, int(t * 1.8))
    SE.draw_flow_diagram(d, steps, step_active, x=120, y=300, w=W - 240, h=180, t=t)

    d.text((120, H - 210), "DISCIPLINED EXECUTION: HEDGES ACTIVATE DECISIVELY AND HOLD FIRM UNTIL VOLATILITY STRUCTURALLY SUBSIDES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_153_the_quant_triumph(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE COMPLETE QUANTITATIVE TRIUMPH", "HOW RIGOROUS SCIENTIFIC METHODOLOGY RESCUED MACHINE LEARNING")

    # 3 Checkmark Cards
    pillars = [
        ("STATISTICAL SKILL", "SURVIVES FDR (q=0.0373)", "REAL ALPHA", SE.GREEN),
        ("CRASH PROTECTION", "-12.95% MAX DRAWDOWN", "38.38 PP SAVED", SE.CYAN),
        ("EXECUTION ENGINE", "SCHMITT HYSTERESIS", "3.91 SORTINO", SE.GOLD)
    ]
    cw = (W - 280) // 3
    for i, (p_tit, p_sub, p_tag, p_col) in enumerate(pillars):
        bx = 140 + i * cw
        d.rounded_rectangle([bx + 8, 250, bx + cw - 8, H - 240], radius=10, fill=SE.BG_PANEL, outline=p_col, width=2)
        d.text((bx + 20, 280), p_tit, font=SE.get_font(18, bold=True, mono=True), fill=p_col)
        d.text((bx + 20, 360), p_sub, font=SE.get_font(22, bold=True), fill=SE.TEXT_WHITE)
        d.line([(bx + 20, 440), (bx + cw - 28, 440)], fill=SE.BORDER_CYAN)
        d.text((bx + 20, 480), p_tag, font=SE.get_font(16, bold=True, mono=True), fill=p_col)

    d.text((140, H - 200), "THE SCIENTIFIC VERDICT: AI DID NOT FAIL — NAIVE UN-HYSTERESISED EXECUTION FAILED. FIXED WITH RIGOR.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_154_hysteresis_rule_certified(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PRODUCTION ARCHITECTURE CERTIFIED", "4D-MGRFF + SCHMITT TRIGGER HYSTERESIS READY FOR INSTITUTIONAL DEPLOYMENT")

    # Radar profile for production readiness
    categories = ["FDR SURVIVAL", "DRAWDOWN SHIELD", "FEE EFFICIENCY", "REGIME STABILITY"]
    values = [1.00, 0.94, 0.88, 0.96]
    SE.draw_radar_spider_chart(d, categories, values, W // 2, H // 2 + 20, 180, t, col=SE.GREEN, label="PRODUCTION READINESS")

    d.text((W // 2 - 320, H - 200), "CERTIFIED PRODUCTION PROTOCOL: MATHEMATICALLY PROVEN, POINT-IN-TIME CLEAN, AND FRICTION-ROBUST.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_155_act6_transition(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT VI // CODA & THE VERDICT")

    cx, cy = W // 2, H // 2
    d.text((cx - 360, cy - 60), "ACT VI: CODA & THE VERDICT", font=SE.get_font(54, bold=True), fill=SE.TEXT_WHITE)
    d.text((cx - 380, cy + 30), "THE THREE LAWS OF QUANTITATIVE INTEGRITY", font=SE.get_font(24, mono=True), fill=SE.CYAN)
    d.line([(cx - 380, cy + 85), (cx + 380, cy + 85)], fill=SE.BORDER_CYAN, width=2)

    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
