# -*- coding: utf-8 -*-
"""
High-CTR A/B YouTube Thumbnail Suite for @izhaanintellect
Generates 3 broadcast-grade 1920x1080 thumbnail variants:
  Variant A: Editorial White (Vox/Bloomberg split: -51.3% crash vs +420.7% hedged)
  Variant B: Cyber Quant Lab (4D Tesseract wireframe, Kalman telemetry, golden HUD)
  Variant C: 1-Bit Heuristic Showdown ($100M Overfit AI crossed out vs 1-line Schmitt Trigger)
"""
import os
import sys
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.dirname(SCRIPT_DIR)
GRAPHICS_DIR = os.path.join(DOC_DIR, "03_graphics")
if GRAPHICS_DIR not in sys.path:
    sys.path.insert(0, GRAPHICS_DIR)

import style_engine as SE

OUT_A = os.path.join(SCRIPT_DIR, "THUMBNAIL_A_EDITORIAL_WHITE.png")
OUT_B = os.path.join(SCRIPT_DIR, "THUMBNAIL_B_CYBER_TESSERACT.png")
OUT_C = os.path.join(SCRIPT_DIR, "THUMBNAIL_C_1BIT_SHOWDOWN.png")


def render_thumbnail_a(out_path=OUT_A):
    """
    Variant A: Editorial White (Vox / Bloomberg Quicktake style)
    High contrast split: -51.3% Crash vs +420.7% Protected Alpha
    """
    im = Image.new("RGB", (SE.W, SE.H), (250, 252, 255))
    d = ImageDraw.Draw(im)

    # Clean architectural grid
    for x in range(0, SE.W, 60):
        d.line([(x, 0), (x, SE.H)], fill=(232, 238, 246), width=1)
    for y in range(0, SE.H, 60):
        d.line([(0, y), (SE.W, y)], fill=(232, 238, 246), width=1)

    # Channel Tag Banner
    d.rounded_rectangle([80, 50, 680, 105], radius=10, fill=(238, 244, 255), outline=(14, 116, 220), width=2)
    d.ellipse([(105, 70), (125, 90)], fill=(16, 185, 129))
    d.text((140, 63), "IZHAAN INTELLECT // FORENSIC RISK LAB", font=SE.get_font(22, bold=True, mono=True), fill=(14, 116, 220))

    # Huge Headline with impactful hierarchy
    f_badge = SE.get_font(26, bold=True, mono=True)
    f_huge = SE.get_font(102, bold=True)
    f_sub = SE.get_font(38, bold=True)
    f_kpi_val = SE.get_font(76, bold=True, mono=True)
    f_kpi_lbl = SE.get_font(22, bold=True, mono=True)

    d.text((80, 130), "THE 4D CODE THAT", font=f_huge, fill=(15, 23, 42))
    d.text((80, 240), "CRACKED CRYPTO RISK", font=f_huge, fill=(14, 116, 220))

    # Subtitle tag
    d.text((85, 365), "WHY 99% OF TRADERS BLED TO DEATH ON AUGUST 5, 2024", font=f_sub, fill=(100, 116, 139))

    # Left Split Card: The Bloodbath (-51.3% Spot)
    x0_red, y0_red, x1_red, y1_red = 80, 440, 920, 980
    SE.draw_glass_panel(d, x0_red, y0_red, x1_red - x0_red, y1_red - y0_red, radius=20, fill=(255, 245, 245), outline=(225, 29, 72))
    
    # Red Warning Badge
    d.rounded_rectangle([x0_red + 30, y0_red + 25, x0_red + 430, y0_red + 70], radius=8, fill=(254, 226, 226), outline=(225, 29, 72), width=2)
    d.text((x0_red + 45, y0_red + 34), "WARNING // UNHEDGED SPOT", font=f_badge, fill=(225, 29, 72))

    # Red Crash metric
    d.text((x0_red + 30, y0_red + 90), "-51.3%", font=f_kpi_val, fill=(225, 29, 72))
    d.text((x0_red + 35, y0_red + 185), "MAX DRAWDOWN (AUG 5 YEN SHOCK)", font=f_kpi_lbl, fill=(140, 20, 40))

    # Drawn Red plunging candlestick chart
    candle_x = x0_red + 480
    candle_y = y0_red + 80
    candles = [
        (0, 40, -10, 60, False),
        (50, 55, 20, 90, False),
        (100, 85, 40, 160, False),
        (150, 150, 110, 280, False),
        (200, 260, 210, 390, False),
    ]
    for cx, c_top, c_wtop, c_wbot, is_up in candles:
        # Wick
        d.line([(candle_x + cx, candle_y + c_wtop), (candle_x + cx, candle_y + c_wbot)], fill=(225, 29, 72), width=3)
        # Body
        d.rectangle([candle_x + cx - 16, candle_y + c_top, candle_x + cx + 16, candle_y + c_wbot - 20], fill=(225, 29, 72))

    d.text((x0_red + 35, y0_red + 240), "SHARPE: 0.81  |  VOLATILITY: 78.4%", font=SE.get_font(20, bold=True, mono=True), fill=(100, 116, 139))
    d.text((x0_red + 35, y0_red + 275), "LIQUIDATION CASCADE CONFIRMED", font=SE.get_font(18, bold=True, mono=True), fill=(225, 29, 72))

    # Right Split Card: The Shield (+420.7% M5 Hedged)
    x0_grn, y0_grn, x1_grn, y1_grn = 1000, 440, 1840, 980
    SE.draw_glass_panel(d, x0_grn, y0_grn, x1_grn - x0_grn, y1_grn - y0_grn, radius=20, fill=(245, 255, 250), outline=(16, 185, 129))

    # Green Shield Badge
    d.rounded_rectangle([x0_grn + 30, y0_grn + 25, x0_grn + 480, y0_grn + 70], radius=8, fill=(209, 250, 229), outline=(16, 185, 129), width=2)
    d.text((x0_grn + 45, y0_grn + 34), "M5 LIGHTGBM // DYNAMIC HEDGE", font=f_badge, fill=(16, 185, 129))

    # Green Alpha metric
    d.text((x0_grn + 30, y0_grn + 90), "+420.7%", font=f_kpi_val, fill=(16, 185, 129))
    d.text((x0_grn + 35, y0_grn + 185), "NET CUMULATIVE RETURN (OUT-OF-SAMPLE)", font=f_kpi_lbl, fill=(6, 95, 70))

    # Green protected curve
    chart_x0 = x0_grn + 460
    curve_pts = [
        (chart_x0, y0_grn + 320),
        (chart_x0 + 70, y0_grn + 290),
        (chart_x0 + 150, y0_grn + 240),
        (chart_x0 + 230, y0_grn + 170),
        (chart_x0 + 310, y0_grn + 90),
    ]
    for i in range(len(curve_pts) - 1):
        d.line([curve_pts[i], curve_pts[i+1]], fill=(16, 185, 129), width=6)
        d.ellipse([(curve_pts[i][0]-6, curve_pts[i][1]-6), (curve_pts[i][0]+6, curve_pts[i][1]+6)], fill=(16, 185, 129))
    d.ellipse([(curve_pts[-1][0]-8, curve_pts[-1][1]-8), (curve_pts[-1][0]+8, curve_pts[-1][1]+8)], fill=(16, 185, 129))

    d.text((x0_grn + 35, y0_grn + 240), "SHARPE: 2.14  |  DRAWDOWN: -12.9%", font=SE.get_font(20, bold=True, mono=True), fill=(100, 116, 139))
    d.text((x0_grn + 35, y0_grn + 275), "YEN CRASH SHIELD ACTIVE (100% SECURED)", font=SE.get_font(18, bold=True, mono=True), fill=(16, 185, 129))

    # Bottom Official URL Banner
    d.rectangle([0, 1030, SE.W, SE.H], fill=(15, 23, 42))
    d.text((80, 1042), "OFFICIAL THESIS LAB: 7mcrypto.izhaanintellect.fun  |  GITHUB: github.com/rbr48/7Mcrypto", font=SE.get_font(18, bold=True, mono=True), fill=(248, 250, 252))
    d.text((1550, 1042), "VERIFIED REPRODUCIBLE", font=SE.get_font(18, bold=True, mono=True), fill=(16, 185, 129))

    im.save(out_path, "PNG", quality=95)
    print(f"[OK] Rendered Thumbnail A (Editorial White): {out_path}")


def render_thumbnail_b(out_path=OUT_B):
    """
    Variant B: Cyber Quant Lab (Bloomberg Terminal / Sci-Fi Quant Matrix)
    Features glowing 4D hypercube tesseract, Kalman Gain telemetry, and high-tech typography.
    """
    im = Image.new("RGB", (SE.W, SE.H), (6, 10, 18))
    d = ImageDraw.Draw(im)

    # Dark cyber grid
    for x in range(0, SE.W, 50):
        d.line([(x, 0), (x, SE.H)], fill=(15, 26, 44), width=1)
    for y in range(0, SE.H, 50):
        d.line([(0, y), (SE.W, y)], fill=(15, 26, 44), width=1)

    # 4D Hypercube Tesseract in center-right
    cx, cy = 1350, 520
    theta_xw, theta_zw, theta_xy = 1.85, 1.25, 0.75
    proj_pts = []
    depths = []
    for v in SE.TESS_VERTS:
        vr = SE.rotate_4d(v, theta_xw=1.85, theta_zw=1.25, theta_yw=0.45, theta_xy=0.75)
        px, py, p4 = SE.project_4d_to_2d(vr, scale=360, cx=cx, cy=cy)
        proj_pts.append((px, py))
        depths.append(p4)

    # Draw glow layers for edges
    for i, j in SE.TESS_EDGES:
        p1, p2 = proj_pts[i], proj_pts[j]
        avg_d = (depths[i] + depths[j]) * 0.5
        alpha = max(0.2, min(1.0, (avg_d + 1.2) / 2.4))
        r_col = int(14 * alpha + 0 * (1 - alpha))
        g_col = int(165 * alpha + 40 * (1 - alpha))
        b_col = int(233 * alpha + 80 * (1 - alpha))
        d.line([p1, p2], fill=(r_col, g_col, b_col), width=int(3 + alpha * 3))

    for idx, (px, py) in enumerate(proj_pts):
        d_val = depths[idx]
        alpha = max(0.2, min(1.0, (d_val + 1.2) / 2.4))
        r = int(7 + alpha * 6)
        d.ellipse([(px - r - 2, py - r - 2), (px + r + 2, py + r + 2)], fill=(14, 165, 233))
        d.ellipse([(px - r, py - r), (px + r, py + r)], fill=(255, 255, 255))

    # Left Content HUD Panel
    x0, y0, x1, y1 = 70, 70, 940, 990
    SE.draw_glass_panel(d, x0, y0, x1 - x0, y1 - y0, radius=24, fill=(10, 18, 32), outline=(14, 165, 233))

    # Live Telemetry Header
    d.text((x0 + 40, y0 + 35), "SYS_STATUS // CALIBRATED 4D MANIFOLD", font=SE.get_font(20, bold=True, mono=True), fill=(14, 165, 233))
    d.ellipse([(x0 + 480, y0 + 40), (x0 + 494, y0 + 54)], fill=(16, 185, 129))

    # Headline
    f_huge = SE.get_font(100, bold=True)
    f_gold = SE.get_font(95, bold=True)
    d.text((x0 + 40, y0 + 80), "THE 4-D", font=f_huge, fill=(248, 250, 252))
    d.text((x0 + 40, y0 + 190), "CRASH CODE", font=f_gold, fill=(245, 158, 11))

    # Teaser sentence
    d.text((x0 + 40, y0 + 310), "CAUGHT THE AUG 5 SHOCK 6 HOURS EARLY", font=SE.get_font(32, bold=True), fill=(226, 232, 240))

    # Math Card: Kalman Gain & GIRF shock (Compact HUD)
    math_box = [x0 + 35, y0 + 370, x0 + 805, y0 + 560]
    SE.draw_glass_panel(d, math_box[0], math_box[1], math_box[2]-math_box[0], math_box[3]-math_box[1], radius=14, fill=(12, 22, 38), outline=(14, 165, 233))
    d.text((math_box[0] + 25, math_box[1] + 18), "RECURSIVE FILTERING // KALMAN GAIN INNOVATION", font=SE.get_font(16, bold=True, mono=True), fill=(14, 165, 233))
    d.text((math_box[0] + 25, math_box[1] + 55), "K_t = P_{t|t-1} H_t^T (H_t P_{t|t-1} H_t^T + R_t)^{-1}", font=SE.get_font(26, bold=True, mono=True), fill=(248, 250, 252))
    d.line([(math_box[0] + 25, math_box[1] + 105), (math_box[2] - 25, math_box[1] + 105)], fill=(25, 45, 75), width=1)
    d.text((math_box[0] + 25, math_box[1] + 120), "GENERALIZED IMPULSE RESPONSE FUNCTION (GIRF):", font=SE.get_font(15, bold=True, mono=True), fill=(245, 158, 11))
    d.text((math_box[0] + 25, math_box[1] + 148), "\u03a0_h = \u03c3_ii^{-1/2} A_h \u03a3 e_i  (ORDER-INVARIANT)", font=SE.get_font(22, bold=True, mono=True), fill=(16, 185, 129))

    # Key Stat Blocks
    d.rounded_rectangle([x0 + 35, y0 + 590, x0 + 410, y0 + 750], radius=14, fill=(15, 28, 48), outline=(14, 165, 233), width=1)
    d.text((x0 + 55, y0 + 605), "OOS SHARPE RATIO", font=SE.get_font(18, bold=True, mono=True), fill=(148, 163, 184))
    d.text((x0 + 55, y0 + 645), "2.14", font=SE.get_font(64, bold=True, mono=True), fill=(16, 185, 129))
    d.text((x0 + 55, y0 + 715), "BENCHMARK: 0.81 (SPOT)", font=SE.get_font(16, bold=True, mono=True), fill=(100, 116, 139))

    d.rounded_rectangle([x0 + 430, y0 + 590, x0 + 805, y0 + 750], radius=14, fill=(15, 28, 48), outline=(245, 158, 11), width=1)
    d.text((x0 + 450, y0 + 605), "DD COMPRESSION", font=SE.get_font(18, bold=True, mono=True), fill=(148, 163, 184))
    d.text((x0 + 450, y0 + 645), "-74.9%", font=SE.get_font(64, bold=True, mono=True), fill=(245, 158, 11))
    d.text((x0 + 450, y0 + 715), "-51.3% -> -12.9% COLLAPSE", font=SE.get_font(16, bold=True, mono=True), fill=(100, 116, 139))

    # Official verification stamp
    SE.draw_evidence_badge(d, 4, "PESARAN & SHIN GIRF INVARIANT", "FORMALLY PROVEN", x=x0 + 35, y=y0 + 780)

    # Bottom Cyber Banner
    d.rectangle([0, 1030, SE.W, SE.H], fill=(10, 18, 32))
    d.text((80, 1042), "IZHAAN INTELLECT // FORENSIC QUANT RESEARCH // FULL CODE ON GITHUB", font=SE.get_font(18, bold=True, mono=True), fill=(148, 163, 184))
    d.text((1500, 1042), "7MCRYPTO.IZHAANINTELLECT.FUN", font=SE.get_font(18, bold=True, mono=True), fill=(14, 165, 233))

    im.save(out_path, "PNG", quality=95)
    print(f"[OK] Rendered Thumbnail B (Cyber Tesseract): {out_path}")


def render_thumbnail_c(out_path=OUT_C):
    """
    Variant C: 1-Bit Heuristic Showdown
    '$100M Overfit AI' crossed out vs 1-Line Schmitt Trigger Rule
    """
    im = Image.new("RGB", (SE.W, SE.H), (250, 252, 255))
    d = ImageDraw.Draw(im)

    # Clean architectural grid
    for x in range(0, SE.W, 60):
        d.line([(x, 0), (x, SE.H)], fill=(232, 238, 246), width=1)
    for y in range(0, SE.H, 60):
        d.line([(0, y), (SE.W, y)], fill=(232, 238, 246), width=1)

    # Channel Tag Banner
    d.rounded_rectangle([80, 50, 680, 105], radius=10, fill=(238, 244, 255), outline=(14, 116, 220), width=2)
    d.ellipse([(105, 70), (125, 90)], fill=(16, 185, 129))
    d.text((140, 63), "IZHAAN INTELLECT // FORENSIC QUANT LAB", font=SE.get_font(22, bold=True, mono=True), fill=(14, 116, 220))

    # Huge Provocative Headline
    f_huge = SE.get_font(98, bold=True)
    f_sub = SE.get_font(36, bold=True)
    d.text((80, 125), "HOW A 1-BIT RULE", font=f_huge, fill=(15, 23, 42))
    d.text((80, 230), "BEAT WALL STREET'S AI", font=f_huge, fill=(225, 29, 72))
    d.text((85, 350), "THE SHOCKING CODE FORENSICS OF 7 MACHINE LEARNING MODELS", font=f_sub, fill=(100, 116, 139))

    # Left Card: $100M Neural Network (CROSSED OUT IN RED)
    x0_l, y0_l, x1_l, y1_l = 80, 420, 920, 980
    SE.draw_glass_panel(d, x0_l, y0_l, x1_l - x0_l, y1_l - y0_l, radius=20, fill=(255, 245, 245), outline=(225, 29, 72))
    
    d.rounded_rectangle([x0_l + 30, y0_l + 25, x0_l + 440, y0_l + 70], radius=8, fill=(254, 226, 226), outline=(225, 29, 72), width=2)
    d.text((x0_l + 45, y0_l + 34), "M7 DEEP LSTM // OVERFIT", font=SE.get_font(24, bold=True, mono=True), fill=(225, 29, 72))

    d.text((x0_l + 30, y0_l + 90), "-12.9% LOSS", font=SE.get_font(72, bold=True, mono=True), fill=(225, 29, 72))
    d.text((x0_l + 35, y0_l + 175), "54,000 PARAMETERS // 8 LAYERS", font=SE.get_font(20, bold=True, mono=True), fill=(100, 116, 139))

    # Simulated complex neural network layer nodes
    nn_x0 = x0_l + 60
    nn_y0 = y0_l + 220
    cols = 5
    rows = 4
    for c in range(cols):
        for r in range(rows):
            px = nn_x0 + c * 70
            py = nn_y0 + r * 50
            d.ellipse([(px-8, py-8), (px+8, py+8)], fill=(225, 29, 72))
            if c < cols - 1:
                for nr in range(rows):
                    npx = nn_x0 + (c + 1) * 70
                    npy = nn_y0 + nr * 50
                    d.line([(px, py), (npx, npy)], fill=(254, 202, 202), width=1)

    # Giant RED 'X' over the neural net
    d.line([(x0_l + 40, y0_l + 200), (x0_l + 440, y0_l + 420)], fill=(225, 29, 72), width=8)
    d.line([(x0_l + 440, y0_l + 200), (x0_l + 40, y0_l + 420)], fill=(225, 29, 72), width=8)
    d.text((x0_l + 35, y0_l + 480), "FAILURE: CURSE OF DIMENSIONALITY", font=SE.get_font(20, bold=True, mono=True), fill=(225, 29, 72))

    # Right Card: 1-Bit Schmitt Trigger Rule (WINNER)
    x0_r, y0_r, x1_r, y1_r = 1000, 420, 1840, 980
    SE.draw_glass_panel(d, x0_r, y0_r, x1_r - x0_r, y1_r - y0_r, radius=20, fill=(245, 255, 250), outline=(16, 185, 129))

    d.rounded_rectangle([x0_r + 30, y0_r + 25, x0_r + 480, y0_r + 70], radius=8, fill=(209, 250, 229), outline=(16, 185, 129), width=2)
    d.text((x0_r + 45, y0_r + 34), "M5 + SCHMITT HYSTERESIS // 1-BIT", font=SE.get_font(24, bold=True, mono=True), fill=(16, 185, 129))

    d.text((x0_r + 30, y0_r + 90), "+420.7% ALPHA", font=SE.get_font(72, bold=True, mono=True), fill=(16, 185, 129))
    d.text((x0_r + 35, y0_r + 175), "SHARPE: 2.14  |  DRAWDOWN: -12.9%", font=SE.get_font(20, bold=True, mono=True), fill=(6, 95, 70))

    # Code Box displaying the elegant 1-line rule
    code_box = [x0_r + 35, y0_r + 220, x0_r + 770, y0_r + 440]
    d.rounded_rectangle(code_box, radius=12, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    d.text((code_box[0] + 25, code_box[1] + 20), "# THE ENTIRE TRADING EDGE:", font=SE.get_font(18, bold=True, mono=True), fill=(100, 116, 139))
    d.text((code_box[0] + 25, code_box[1] + 60), "if p_stress > 0.30:", font=SE.get_font(28, bold=True, mono=True), fill=(245, 158, 11))
    d.text((code_box[0] + 70, code_box[1] + 105), "hedge_ratio = 1.0", font=SE.get_font(28, bold=True, mono=True), fill=(16, 185, 129))
    d.text((code_box[0] + 25, code_box[1] + 150), "elif p_stress < 0.15:", font=SE.get_font(28, bold=True, mono=True), fill=(245, 158, 11))
    d.text((code_box[0] + 70, code_box[1] + 190), "hedge_ratio = 0.0", font=SE.get_font(28, bold=True, mono=True), fill=(14, 165, 233))

    d.text((x0_r + 35, y0_r + 480), "ZERO LOOKAHEAD  |  ZERO WHIPSAW TRADING", font=SE.get_font(20, bold=True, mono=True), fill=(16, 185, 129))

    # Bottom Banner
    d.rectangle([0, 1030, SE.W, SE.H], fill=(15, 23, 42))
    d.text((80, 1042), "RESEARCH PAPER: 7mcrypto.izhaanintellect.fun  |  FULL CODE REPOSITORY ON GITHUB", font=SE.get_font(18, bold=True, mono=True), fill=(248, 250, 252))
    d.text((1550, 1042), "IZHAAN INTELLECT", font=SE.get_font(18, bold=True, mono=True), fill=(16, 185, 129))

    im.save(out_path, "PNG", quality=95)
    print(f"[OK] Rendered Thumbnail C (1-Bit Showdown): {out_path}")


def main():
    print("=" * 70)
    print("GENERATING 3 HIGH-CTR A/B YOUTUBE THUMBNAILS (1920x1080)")
    print("=" * 70)
    render_thumbnail_a()
    render_thumbnail_b()
    render_thumbnail_c()
    print("=" * 70)
    print("ALL 3 THUMBNAIL VARIANTS READY FOR A/B TESTING.")


if __name__ == "__main__":
    main()
