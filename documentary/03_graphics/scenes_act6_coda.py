# -*- coding: utf-8 -*-
"""
Procedural Scene Renderers — ACT 6: CODA & THE VERDICT (Scenes 156 - 165)
1080p 30 FPS cinematic motion graphics for @izhaanintellect.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import style_engine as SE

W, H = SE.W, SE.H


def draw_header(d, title, sub):
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT 6 // CODA & VERDICT")
    f_t = SE.get_font(40, bold=True)
    f_s = SE.get_font(20, mono=True)
    d.text((80, 85), title, font=f_t, fill=SE.TEXT_WHITE)
    d.text((82, 140), sub, font=f_s, fill=SE.CYAN)
    d.line([(80, 175), (W - 80, 175)], fill=SE.BORDER_CYAN, width=1)


def s_156_institutional_verdict(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE INSTITUTIONAL VERDICT", "THREE GROUND-TRUTH LESSONS FROM 970 DAYS OF REAL CRYPTO DATA")

    pillars = [
        ("LESSON 1", "M7 IS A MACRO SIMULATOR", "State-space models model structural contagion and DeFi liquidations — not fast directional trading triggers.", SE.CYAN),
        ("LESSON 2", "THE 1-DAY PREDICTIVE LIMIT", "Predicting 7-day crashes from public tick data is statistically indistinguishable from chance.", SE.GOLD),
        ("LESSON 3", "EXECUTION DOMINATES MATH", "Friction, exchange fee tiers, and Schmitt-trigger hysteresis separate live alpha from bankruptcy.", SE.GREEN)
    ]

    card_w = (W - 240) // 3
    for i, (p_num, p_title, p_desc, p_col) in enumerate(pillars):
        x = 120 + i * card_w
        active = (t / max(0.1, dur * 0.7)) > (i / 3)
        fill_col = SE.BG_TINT_GREEN if (active and i == 2) else (SE.BG_TINT_GOLD if (active and i == 1) else (SE.BG_TINT_CYAN if active else SE.BG_PANEL))
        d.rounded_rectangle([x + 8, 250, x + card_w - 8, H - 240], radius=10, fill=fill_col, outline=p_col if active else SE.BORDER_CYAN, width=2)
        d.text((x + 24, 280), p_num, font=SE.get_font(18, bold=True, mono=True), fill=p_col)
        d.text((x + 24, 330), p_title, font=SE.get_font(20, bold=True), fill=SE.TEXT_WHITE)
        d.line([(x + 24, 400), (x + card_w - 24, 400)], fill=SE.BORDER_CYAN, width=1)

        words = p_desc.split()
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 26:
                lines.append(" ".join(cur_line))
                cur_line = []
        if cur_line:
            lines.append(" ".join(cur_line))

        for l_idx, line in enumerate(lines):
            d.text((x + 24, 430 + l_idx * 32), line, font=SE.get_font(16), fill=SE.TEXT_WHITE)

    d.text((120, H - 210), "THE SCIENTIFIC CORE: GROUNDED EMPIRICISM TRUMPS THEORETICAL ASSUMPTIONS EVERY SINGLE TIME.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_157_lesson_1_m7_role(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "LESSON 1: THE TRUE PURPOSE OF M7 4D-DLM", "NOT A HEDGE TRIGGER // A MULTI-VARIABLE MACRO STRESS-TEST ENGINE")

    # Radar profile for macro stress-testing
    categories = ["YIELD SENSITIVITY", "DEFI CONTAGION", "COUNTERFACTUALS", "SYSTEMIC RISK"]
    values = [0.94, 0.91, 0.88, 0.96]
    SE.draw_radar_spider_chart(d, categories, values, W // 2, H // 2 + 20, 180, t, col=SE.CYAN, label="M7 FLIGHT SIMULATOR")

    d.text((W // 2 - 340, H - 200), "M7 IS A POLICY FLIGHT SIMULATOR FOR CENTRAL BANKS AND PROTOCOL ARCHITECTS — NOT A TRADING TRIGGER.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_158_girf_irreplaceable(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "IRF IMPULSE MATRICES: INDISPENSABLE FOR DEFI", "GENERALIZED IMPULSE RESPONSE FUNCTIONS MODEL PROTOCOL RUNS")

    cx, cy = W // 2, H // 2 + 10
    nodes = [
        ("BINANCE SPOT", -260, -80, SE.GOLD),
        ("DERIBIT DVOL", 0, -140, SE.CYAN),
        ("FRED DGS10", 260, -80, SE.GREEN),
        ("PERP FUNDING", -140, 120, SE.DANGER_RED),
        ("DEFI LIQUIDATIONS", 140, 120, SE.TEXT_WHITE),
    ]

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            p1 = (cx + nodes[i][1], cy + nodes[i][2])
            p2 = (cx + nodes[j][1], cy + nodes[j][2])
            d.line([p1, p2], fill=SE.BORDER_CYAN, width=1)

    pulse_idx = int(t * 3) % len(nodes)
    for idx, (label, ox, oy, col) in enumerate(nodes):
        px, py = cx + ox, cy + oy
        is_pulse = (idx == pulse_idx)
        fill_c = SE.BG_TINT_GOLD if is_pulse else SE.BG_PANEL
        d.ellipse([(px - 45, py - 45), (px + 45, py + 45)], fill=fill_c, outline=col, width=3 if is_pulse else 2)
        d.text((px - 35, py - 10), label.split()[0], font=SE.get_font(13, bold=True, mono=True), fill=col)

    d.text((160, H - 200), "GIRF MAPS SYSTEMIC TRANSMISSION VELOCITY ACROSS CEFI ORDERBOOKS AND ON-CHAIN COLLATERAL POOLS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_159_lesson_2_horizon_limit(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "LESSON 2: THE 1-DAY FORECAST BOUNDARY", "WHY PREDICTING 7-DAY CRYPTO CRASHES USING PUBLIC DATA IS MATHEMATICAL ILLUSION")

    categories = ["1-DAY (SIGNAL: BSS=+0.25)", "3-DAY (DECAY: BSS=+0.08)", "7-DAY (NOISE: BSS=-0.04)", "14-DAY (NOISE: BSS=-0.08)"]
    values = [0.2523, 0.0812, -0.0415, -0.0820]
    colors = [SE.GREEN, SE.GOLD, SE.DANGER_RED, SE.DANGER_RED]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=0.30,
        x=180, y=240, w=W - 360, h=H - 480,
        t=t, dur=dur, colors=colors
    )
    d.text((180, H - 200), "INFORMATION HALFLIFE: CRYPTO EFFICIENCY ERASES PUBLIC TICK SIGNAL BEYOND 24-72 HOURS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_160_lesson_3_execution_king(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "LESSON 3: EXECUTION IS KING", "HOW 10 BPS OF FRICTION CAN DESTROY A MILLION-DOLLAR STATISTICAL EDGE")

    categories = ["THEORETICAL PAPER BACKTEST", "UN-HYSTERESISED LIVE TRADING", "SCHMITT HYSTERESIS ENGINE"]
    values = [520.0, 420.69, 458.50]
    colors = [SE.TEXT_MUTED, SE.DANGER_RED, SE.GREEN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=550.0,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "EXECUTION IS YOUR STRATEGY: WITHOUT HYSTERESIS DEADZONES, YOUR ALPHA FEEDS THE EXCHANGE ORDERBOOK.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_161_github_open_science(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "100% OPEN SCIENCE // REPRODUCIBLE REPOSITORY", "31 UNIT TESTS // SQLITE POINT-IN-TIME DB // WALK-FORWARD HEDGE SIMULATOR")

    term_bg = (248, 250, 254) if SE.THEME == "LIGHT" else (8, 12, 18)
    title_bg = (235, 240, 248) if SE.THEME == "LIGHT" else (18, 28, 44)
    term_border = (205, 218, 235) if SE.THEME == "LIGHT" else SE.CYAN

    d.rounded_rectangle([140, 230, W - 140, H - 240], radius=8, fill=term_bg, outline=term_border, width=2)
    d.rectangle([140, 230, W - 140, 275], fill=title_bg)
    d.text((160, 243), "rbr48 / 7Mcrypto — git status (31 passed tests)", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)

    lines = [
        ("pytest tests/ -v", SE.CYAN),
        ("======================== 31 passed in 4.82s ========================", SE.GREEN),
        ("test_schema.py::test_pit_separation                      PASSED [ 12%]", SE.TEXT_WHITE),
        ("test_dlm.py::test_kalman_filter_4d                       PASSED [ 38%]", SE.TEXT_WHITE),
        ("test_backtest.py::test_benjamini_hochberg_fdr            PASSED [ 64%]", SE.TEXT_WHITE),
        ("test_hedge_simulation.py::test_friction_and_hysteresis    PASSED [100%]", SE.GREEN),
        ("All 970 daily records from Binance, Deribit, and FRED verified pit-clean.", SE.GOLD),
    ]

    for i, (l_txt, col) in enumerate(lines):
        d.text((170, 300 + i * 40), l_txt, font=SE.get_font(20, mono=True), fill=col)

    d.text((170, 620), "OFFICIAL GITHUB REPOSITORY: HTTPS://GITHUB.COM/RBR48/7MCRYPTO", font=SE.get_font(24, bold=True, mono=True), fill=SE.CYAN)
    d.text((140, H - 200), "COMPLETE REPRODUCIBILITY: RUN 'pytest tests/' TO VALIDATE EVERY EQUATION LOCALLY ON YOUR MACHINE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_162_clone_and_verify(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "DO NOT TRUST US // VERIFY FOR YOURSELF", "EVERY ROW, EQUATION, AND SIMULATION IS PUBLIC AND RUNNABLE")

    d.rounded_rectangle([180, 240, W - 180, H - 240], radius=10, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)
    d.text((230, 280), "THE QUANT AUDIT PROTOCOL:", font=SE.get_font(26, bold=True), fill=SE.TEXT_WHITE)

    steps = [
        ("1. CLONE REPOSITORY", "git clone https://github.com/rbr48/7Mcrypto.git", SE.GOLD),
        ("2. RUN SIMULATION", "python -m src.evaluation.crypto_hedge_simulation", SE.GOLD),
        ("3. INTERACTIVE QUANT LAB", "https://7mcrypto.izhaanintellect.fun/", SE.CYAN),
        ("4. MAIN RESEARCH PORTAL", "https://izhaanintellect.fun/", SE.GREEN)
    ]
    for idx, (s_tit, s_cmd, s_col) in enumerate(steps):
        y = 350 + idx * 65
        d.text((230, y), s_tit, font=SE.get_font(16, bold=True, mono=True), fill=SE.TEXT_MUTED)
        d.text((230, y + 24), s_cmd, font=SE.get_font(22, bold=True, mono=True), fill=s_col)

    d.text((180, H - 200), "ZERO CURVE FITTING. ZERO DATA SNOOPING. COMPLETE MATHEMATICAL AND CODE TRANSPARENCY.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_163_channel_mission(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE IZHAAN INTELLECT MISSION", "BRINGING INSTITUTIONAL RIGOR & HOLLYWOOD-GRADE VISUALS TO FINANCE")

    d.rounded_rectangle([180, 240, W - 180, H - 240], radius=12, fill=SE.BG_PANEL, outline=SE.GOLD, width=2)
    d.text((240, 290), "IZHAAN INTELLECT", font=SE.get_font(52, bold=True), fill=SE.TEXT_WHITE)
    d.text((242, 360), "QUANTITATIVE RESEARCH // HIGH-DIMENSIONAL FINANCE // OPEN SCIENCE", font=SE.get_font(20, mono=True), fill=SE.GOLD)

    d.line([(240, 400), (W - 240, 400)], fill=SE.BORDER_CYAN, width=1)

    manifesto = [
        "In an internet filled with hype, fake screenshots, and backtest illusions,",
        "we build genuine code, test against genuine market friction, and trace",
        "every single number to its mathematical origin.",
        "",
        "If you value truth over hype and rigor over noise — you are in the right place."
    ]

    for idx, m_line in enumerate(manifesto):
        d.text((240, 430 + idx * 34), m_line, font=SE.get_font(20), fill=SE.TEXT_WHITE if idx != 4 else SE.CYAN)

    d.text((180, H - 200), "OFFICIAL CHANNEL MISSION: DEMOCRATIZING INSTITUTIONAL-GRADE FINANCIAL DATA SCIENCE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_164_tesseract_final_dissolve(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "BEYOND THE THIRD DIMENSION", "THE MATHEMATICAL ARCHITECTURE OF FINANCIAL REGIMES")

    scale = int(240 + 30 * math.sin(t * 1.5))
    SE.render_tesseract_frame(im, d, t * 1.4, cx=W // 2, cy=H // 2 + 10, scale=scale)

    for r in (340, 420, 500):
        d.ellipse([(W // 2 - r, H // 2 + 10 - r), (W // 2 + r, H // 2 + 10 + r)], outline=SE.BORDER_CYAN, width=1)

    d.text((W // 2 - 320, H - 200), "4D-MGRFF: MULTIVARIATE GENERALIZED RISK FORECASTING FRAMEWORK // IZHAAN INTELLECT", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_165_outro_community(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // TRANSMISSION COMPLETE", act_str="END OF BROADCAST")

    cx = W // 2
    d.text((cx - 360, 220), "THANK YOU FOR WATCHING", font=SE.get_font(48, bold=True), fill=SE.TEXT_WHITE)
    d.text((cx - 430, 290), "SUBSCRIBE TO IZHAAN INTELLECT FOR MORE QUANT DOCUMENTARIES", font=SE.get_font(22, mono=True), fill=SE.CYAN)

    # Animated YouTube Subscribe Button
    sub_w, sub_h = 320, 64
    sub_x, sub_y = cx - sub_w // 2, 355
    d.rounded_rectangle([sub_x, sub_y, sub_x + sub_w, sub_y + sub_h], radius=32, fill=(225, 29, 72))
    d.text((sub_x + 55, sub_y + 14), "SUBSCRIBE", font=SE.get_font(28, bold=True), fill=(255, 255, 255))

    bell_x = sub_x + sub_w + 25
    d.rounded_rectangle([bell_x, sub_y, bell_x + 64, sub_y + sub_h], radius=32, fill=SE.BG_PANEL, outline=SE.GOLD, width=2)
    d.text((bell_x + 22, sub_y + 14), "#", font=SE.get_font(28, bold=True), fill=SE.GOLD)

    # All official links
    d.rounded_rectangle([cx - 480, 460, cx + 480, 670], radius=10, fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=2)
    d.text((cx - 440, 490), "MAIN PORTAL:   https://izhaanintellect.fun/", font=SE.get_font(20, bold=True, mono=True), fill=SE.TEXT_WHITE)
    d.text((cx - 440, 545), "THESIS LAB:    https://7mcrypto.izhaanintellect.fun/", font=SE.get_font(20, bold=True, mono=True), fill=SE.CYAN)
    d.text((cx - 440, 600), "GITHUB REPO:   https://github.com/rbr48/7Mcrypto", font=SE.get_font(20, bold=True, mono=True), fill=SE.GOLD)

    d.text((cx - 380, H - 200), "LIKE, COMMENT, AND SHARE IF YOU ENJOY HIGH-RIGOR DATA SCIENCE", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_MUTED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
