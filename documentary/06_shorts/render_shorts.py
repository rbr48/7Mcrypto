# -*- coding: utf-8 -*-
"""
High-Performance Vertical YouTube Shorts Renderer (1080x1920, 9:16)
Renders 3 broadcast-quality YouTube Shorts for @izhaanintellect:
  Short 1: "How We Predicted the August 5 Crypto Crash" (t = 325s..365s)
  Short 2: "Why $100M AI Failed at Crypto Trading" (t = 420s..460s)
  Short 3: "Visualizing Crypto Risk in 4 Dimensions" (t = 20s..60s)
"""
import os
import sys
import math
import time
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.dirname(SCRIPT_DIR)
GRAPHICS_DIR = os.path.join(DOC_DIR, "03_graphics")
if GRAPHICS_DIR not in sys.path:
    sys.path.insert(0, GRAPHICS_DIR)

import style_engine as SE

W_S, H_S = 1080, 1920
FPS = 30
DURATION_SEC = 40.0
TOTAL_FRAMES = int(DURATION_SEC * FPS)

AUDIO_MASTER = os.path.join(DOC_DIR, "02_audio", "master_soundtrack.wav")
OUT_DIR = SCRIPT_DIR
os.makedirs(OUT_DIR, exist_ok=True)


def get_short_font(size=32, bold=False, mono=False):
    path = SE.FONT_MONO_PATH if mono else (SE.FONT_BOLD_PATH if bold else SE.FONT_REG_PATH)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def draw_vertical_ambient_hud(d, t, short_num, title_str):
    """Studio White high-contrast vertical framing with live ticker and branding."""
    # Architectural background grid
    for x in range(0, W_S, 50):
        d.line([(x, 0), (x, H_S)], fill=(235, 240, 248), width=1)
    for y in range(0, H_S, 50):
        d.line([(0, y), (W_S, y)], fill=(235, 240, 248), width=1)

    # Top Header Pill
    d.rounded_rectangle([40, 45, W_S - 40, 105], radius=12, fill=(245, 248, 254), outline=(210, 222, 238), width=2)
    d.ellipse([(65, 67), (81, 83)], fill=(16, 185, 129))
    d.text((95, 62), "IZHAAN INTELLECT // FORENSIC QUANT", font=get_short_font(18, bold=True, mono=True), fill=(14, 116, 220))
    d.text((W_S - 230, 62), f"SHORT 0{short_num}/03", font=get_short_font(18, bold=True, mono=True), fill=(100, 116, 139))

    # Bottom Branding Bar
    d.rounded_rectangle([40, H_S - 115, W_S - 40, H_S - 55], radius=12, fill=(15, 23, 42))
    d.text((65, H_S - 93), "FULL DOCUMENTARY ON CHANNEL @izhaanintellect", font=get_short_font(18, bold=True, mono=True), fill=(248, 250, 252))
    d.text((W_S - 290, H_S - 93), "7mcrypto.fun", font=get_short_font(18, bold=True, mono=True), fill=(16, 185, 129))


# ----------------------------------------------------------------------
# SHORT 1: AUGUST 5 FLASH CRASH SHIELD
# ----------------------------------------------------------------------
def render_frame_short1(t, dur, f_idx):
    im = Image.new("RGB", (W_S, H_S), (250, 252, 255))
    d = ImageDraw.Draw(im)
    draw_vertical_ambient_hud(d, t, 1, "AUGUST 5 CRASH PREDICTION")

    # Big Impact Headlines
    d.text((60, 150), "WE CAUGHT THE", font=get_short_font(52, bold=True), fill=(15, 23, 42))
    d.text((60, 215), "AUGUST 5 CRASH", font=get_short_font(62, bold=True), fill=(225, 29, 72))
    d.text((60, 295), "6 HOURS BEFORE SPOT COLLAPSED", font=get_short_font(24, bold=True, mono=True), fill=(100, 116, 139))

    # Top Card: The Unhedged Bloodbath
    y_red = 360
    d.rounded_rectangle([60, y_red, W_S - 60, y_red + 530], radius=16, fill=(255, 245, 245), outline=(225, 29, 72), width=2)
    
    d.rounded_rectangle([90, y_red + 25, 460, y_red + 68], radius=8, fill=(254, 226, 226), outline=(225, 29, 72), width=1)
    d.text((105, y_red + 34), "UNHEDGED CRYPTO SPOT", font=get_short_font(18, bold=True, mono=True), fill=(225, 29, 72))

    p_crash = min(1.0, t / 4.0)
    dd_val = -51.3 * p_crash
    d.text((90, y_red + 85), f"{dd_val:.1f}%", font=get_short_font(84, bold=True, mono=True), fill=(225, 29, 72))
    d.text((95, y_red + 185), "MAX DRAWDOWN (AUG 5 YEN CARRY UNWIND)", font=get_short_font(18, bold=True, mono=True), fill=(140, 20, 40))

    # Animated Plunging Candlesticks
    candle_x = 120
    candle_y = y_red + 250
    for idx in range(min(7, int(t * 2.0) + 1)):
        cx = candle_x + idx * 115
        top = 20 + idx * 28
        bot = top + 45 + idx * 10
        d.line([(cx, candle_y + top - 15), (cx, candle_y + bot + 25)], fill=(225, 29, 72), width=3)
        d.rectangle([cx - 24, candle_y + top, cx + 24, candle_y + bot], fill=(225, 29, 72))

    d.text((95, y_red + 470), "LIQUIDATION CASCADE CONFIRMED: $1.24B FORCED SELLS", font=get_short_font(16, bold=True, mono=True), fill=(225, 29, 72))

    # Bottom Card: The M5 Hedged Capital Shield
    y_grn = 930
    d.rounded_rectangle([60, y_grn, W_S - 60, y_grn + 530], radius=16, fill=(245, 255, 250), outline=(16, 185, 129), width=2)
    
    d.rounded_rectangle([90, y_grn + 25, 520, y_grn + 68], radius=8, fill=(209, 250, 229), outline=(16, 185, 129), width=1)
    d.text((105, y_grn + 34), "M5 LIGHTGBM // DYNAMIC HEDGE", font=get_short_font(18, bold=True, mono=True), fill=(16, 185, 129))

    p_growth = min(1.0, t / 4.0)
    alpha_val = 420.7 * p_growth
    d.text((90, y_grn + 85), f"+{alpha_val:.1f}%", font=get_short_font(84, bold=True, mono=True), fill=(16, 185, 129))
    d.text((95, y_grn + 185), "NET CUMULATIVE RETURN (OUT-OF-SAMPLE)", font=get_short_font(18, bold=True, mono=True), fill=(6, 95, 70))

    # Protected Smooth Rising Curve
    chart_x0 = 120
    chart_y0 = y_grn + 380
    pts = []
    for idx in range(min(8, int(t * 2.2) + 1)):
        px = chart_x0 + idx * 105
        py = chart_y0 - int(idx * 18 + math.sin(idx * 0.8) * 10)
        pts.append((px, py))
    if len(pts) > 1:
        d.line(pts, fill=(16, 185, 129), width=5)
        for px, py in pts:
            d.ellipse([(px - 6, py - 6), (px + 6, py + 6)], fill=(16, 185, 129))

    d.text((95, y_grn + 470), "SHARPE: 2.14  |  DRAWDOWN CAPPED AT -12.9%", font=get_short_font(16, bold=True, mono=True), fill=(16, 185, 129))

    # Floating Evidence Callout
    d.rounded_rectangle([60, 1500, W_S - 60, 1630], radius=14, fill=(238, 244, 255), outline=(14, 116, 220), width=2)
    d.text((90, 1520), "THE SECRET: KALMAN RECURSION + SCHMITT TRIGGER", font=get_short_font(18, bold=True, mono=True), fill=(14, 116, 220))
    d.text((90, 1560), "Zero lookahead bias. Fully open-sourced on GitHub.", font=get_short_font(16, bold=False), fill=(71, 85, 105))

    return im


# ----------------------------------------------------------------------
# SHORT 2: WHY $100M AI FAILED AT CRYPTO TRADING
# ----------------------------------------------------------------------
def render_frame_short2(t, dur, f_idx):
    im = Image.new("RGB", (W_S, H_S), (250, 252, 255))
    d = ImageDraw.Draw(im)
    draw_vertical_ambient_hud(d, t, 2, "AI VS 1-BIT HEURISTIC")

    d.text((60, 150), "WHY $100M AI", font=get_short_font(56, bold=True), fill=(15, 23, 42))
    d.text((60, 215), "FAILED AT TRADING", font=get_short_font(56, bold=True), fill=(225, 29, 72))
    d.text((60, 295), "THE 7-MODEL MACHINE LEARNING TOURNAMENT", font=get_short_font(22, bold=True, mono=True), fill=(100, 116, 139))

    # Top Card: $100M LSTM CROSSED OUT
    y_nn = 360
    d.rounded_rectangle([60, y_nn, W_S - 60, y_nn + 500], radius=16, fill=(255, 245, 245), outline=(225, 29, 72), width=2)
    d.rounded_rectangle([90, y_nn + 25, 480, y_nn + 68], radius=8, fill=(254, 226, 226), outline=(225, 29, 72), width=1)
    d.text((105, y_nn + 34), "M7 DEEP LSTM // OVERFIT", font=get_short_font(18, bold=True, mono=True), fill=(225, 29, 72))

    d.text((90, y_nn + 85), "-12.9% LOSS", font=get_short_font(76, bold=True, mono=True), fill=(225, 29, 72))
    d.text((95, y_nn + 175), "54,000 PARAMETERS // 8 RECURRENT LAYERS", font=get_short_font(18, bold=True, mono=True), fill=(100, 116, 139))

    # Drawn Network Nodes
    for col in range(6):
        for row in range(4):
            nx = 140 + col * 135
            ny = y_nn + 230 + row * 45
            d.ellipse([(nx-6, ny-6), (nx+6, ny+6)], fill=(225, 29, 72))
            if col < 5:
                for nr in range(4):
                    d.line([(nx, ny), (nx + 135, y_nn + 230 + nr * 45)], fill=(254, 202, 202), width=1)

    # Big Red 'X' animation
    if t > 1.2:
        d.line([(80, y_nn + 190), (W_S - 80, y_nn + 440)], fill=(225, 29, 72), width=8)
        d.line([(W_S - 80, y_nn + 190), (80, y_nn + 440)], fill=(225, 29, 72), width=8)

    d.text((95, y_nn + 450), "FATAL FLAW: OVERFITS TO LOCAL NOISE REGIMES", font=get_short_font(16, bold=True, mono=True), fill=(225, 29, 72))

    # Bottom Card: 1-Bit Schmitt Trigger Winner
    y_schmitt = 900
    d.rounded_rectangle([60, y_schmitt, W_S - 60, y_schmitt + 580], radius=16, fill=(245, 255, 250), outline=(16, 185, 129), width=2)
    d.rounded_rectangle([90, y_schmitt + 25, 530, y_schmitt + 68], radius=8, fill=(209, 250, 229), outline=(16, 185, 129), width=1)
    d.text((105, y_schmitt + 34), "M5 + SCHMITT HYSTERESIS // 1-BIT", font=get_short_font(18, bold=True, mono=True), fill=(16, 185, 129))

    d.text((90, y_schmitt + 85), "+420.7% ALPHA", font=get_short_font(76, bold=True, mono=True), fill=(16, 185, 129))
    d.text((95, y_schmitt + 175), "SHARPE: 2.14  |  DRAWDOWN: -12.9%", font=get_short_font(18, bold=True, mono=True), fill=(6, 95, 70))

    # Code Box with Schmitt Trigger logic
    code_box = [90, y_schmitt + 225, W_S - 90, y_schmitt + 495]
    d.rounded_rectangle(code_box, radius=12, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    d.text((code_box[0] + 25, code_box[1] + 25), "# THE ENTIRE EDGE IS A 1-BIT STATE MACHINE:", font=get_short_font(16, bold=True, mono=True), fill=(100, 116, 139))
    d.text((code_box[0] + 25, code_box[1] + 70), "if p_stress >= 0.30:", font=get_short_font(26, bold=True, mono=True), fill=(245, 158, 11))
    d.text((code_box[0] + 65, code_box[1] + 115), "hedge = 1.0  # Lock hedge", font=get_short_font(26, bold=True, mono=True), fill=(16, 185, 129))
    d.text((code_box[0] + 25, code_box[1] + 160), "elif p_stress <= 0.15:", font=get_short_font(26, bold=True, mono=True), fill=(245, 158, 11))
    d.text((code_box[0] + 65, code_box[1] + 205), "hedge = 0.0  # Smooth unwind", font=get_short_font(26, bold=True, mono=True), fill=(14, 165, 233))

    d.text((95, y_schmitt + 530), "SAVES 379 BPS BY KILLING WHIPSAW TURNOVER", font=get_short_font(16, bold=True, mono=True), fill=(16, 185, 129))

    # Callout
    d.rounded_rectangle([60, 1520, W_S - 60, 1630], radius=14, fill=(238, 244, 255), outline=(14, 116, 220), width=2)
    d.text((90, 1540), "READ THE FULL PRE-PRINT PAPER:", font=get_short_font(18, bold=True, mono=True), fill=(14, 116, 220))
    d.text((90, 1575), "https://7mcrypto.izhaanintellect.fun", font=get_short_font(20, bold=True, mono=True), fill=(15, 23, 42))

    return im


# ----------------------------------------------------------------------
# SHORT 3: VISUALIZING CRYPTO RISK IN 4 DIMENSIONS
# ----------------------------------------------------------------------
def render_frame_short3(t, dur, f_idx):
    im = Image.new("RGB", (W_S, H_S), (6, 10, 18))
    d = ImageDraw.Draw(im)

    # Dark Cyber Grid
    for x in range(0, W_S, 50):
        d.line([(x, 0), (x, H_S)], fill=(15, 26, 44), width=1)
    for y in range(0, H_S, 50):
        d.line([(0, y), (W_S, y)], fill=(15, 26, 44), width=1)

    # Header
    d.rounded_rectangle([40, 45, W_S - 40, 105], radius=12, fill=(10, 18, 32), outline=(14, 165, 233), width=2)
    d.ellipse([(65, 67), (81, 83)], fill=(16, 185, 129))
    d.text((95, 62), "IZHAAN INTELLECT // 4D MANIFOLD", font=get_short_font(18, bold=True, mono=True), fill=(14, 165, 233))
    d.text((W_S - 230, 62), "SHORT 03/03", font=get_short_font(18, bold=True, mono=True), fill=(148, 163, 184))

    d.text((60, 150), "HOW TO SEE CRYPTO", font=get_short_font(54, bold=True), fill=(248, 250, 252))
    d.text((60, 215), "IN 4 DIMENSIONS", font=get_short_font(60, bold=True), fill=(14, 165, 233))
    d.text((60, 295), "MAPPING SYSTEMIC RISK BEYOND 3D SPACE", font=get_short_font(22, bold=True, mono=True), fill=(148, 163, 184))

    # Central Rotating 4D Tesseract
    cx, cy = W_S // 2, 650
    th_xw = t * 0.45
    th_zw = t * 0.35
    th_yw = t * 0.25
    th_xy = t * 0.15

    proj_pts = []
    depths = []
    for v in SE.TESS_VERTS:
        vr = SE.rotate_4d(v, theta_xw=th_xw, theta_zw=th_zw, theta_yw=th_yw, theta_xy=th_xy)
        px, py, p4 = SE.project_4d_to_2d(vr, scale=290, cx=cx, cy=cy)
        proj_pts.append((px, py))
        depths.append(p4)

    # Edges with 4D fog attenuation
    for i, j in SE.TESS_EDGES:
        p1, p2 = proj_pts[i], proj_pts[j]
        avg_d = (depths[i] + depths[j]) * 0.5
        alpha = max(0.2, min(1.0, (avg_d + 1.2) / 2.4))
        r_col = int(14 * alpha)
        g_col = int(165 * alpha + 40 * (1 - alpha))
        b_col = int(233 * alpha + 80 * (1 - alpha))
        d.line([p1, p2], fill=(r_col, g_col, b_col), width=int(3 + alpha * 3))

    for idx, (px, py) in enumerate(proj_pts):
        d_val = depths[idx]
        alpha = max(0.2, min(1.0, (d_val + 1.2) / 2.4))
        r = int(6 + alpha * 6)
        d.ellipse([(px - r, py - r), (px + r, py + r)], fill=(14, 165, 233))
        d.ellipse([(px - r//2, py - r//2), (px + r//2, py + r//2)], fill=(255, 255, 255))

    # The 4 Hidden Axes Explainer Cards
    y_cards = 1040
    d.rounded_rectangle([60, y_cards, W_S - 60, y_cards + 520], radius=16, fill=(10, 18, 32), outline=(14, 165, 233), width=2)
    d.text((90, y_cards + 25), "THE 4 ORTHOGONAL RISK AXES:", font=get_short_font(20, bold=True, mono=True), fill=(14, 165, 233))

    axes = [
        ("X-AXIS // CROSS-SECTIONAL MOMENTUM", "Relative strength decoupling across BTC, ETH, and SOL", (16, 185, 129)),
        ("Y-AXIS // CONTAGION SPILLOVER (GIRF)", "7! = 5,040 order-invariant shock transmission matrix", (245, 158, 11)),
        ("Z-AXIS // KALMAN INNOVATION VELOCITY", "Dynamic gain adaptation: prior belief vs market shock", (14, 165, 233)),
        ("W-AXIS // 4TH DIMENSION: LIQUIDITY DEPTH", "Perpetual futures orderbook depth & Yen carry leverage", (225, 29, 72)),
    ]

    for idx, (ax_tit, ax_desc, col) in enumerate(axes):
        ay = y_cards + 70 + idx * 105
        d.rounded_rectangle([90, ay, W_S - 90, ay + 85], radius=8, fill=(15, 26, 44), outline=col, width=1)
        d.text((110, ay + 15), ax_tit, font=get_short_font(16, bold=True, mono=True), fill=col)
        d.text((110, ay + 45), ax_desc, font=get_short_font(15, bold=False), fill=(148, 163, 184))

    # Bottom Call to Action
    d.rounded_rectangle([40, H_S - 115, W_S - 40, H_S - 55], radius=12, fill=(14, 165, 233))
    d.text((65, H_S - 93), "WATCH THE 9-MINUTE FILM ON YOUTUBE @izhaanintellect", font=get_short_font(18, bold=True, mono=True), fill=(15, 23, 42))

    return im


# ----------------------------------------------------------------------
# RENDER PIPELINE
# ----------------------------------------------------------------------
def render_short_video(short_id, render_func, audio_start_sec, out_filename):
    out_mp4 = os.path.join(OUT_DIR, out_filename)
    temp_audio = os.path.join(OUT_DIR, f"temp_short_{short_id}_audio.wav")
    temp_video = os.path.join(OUT_DIR, f"temp_short_{short_id}_video.mp4")

    print(f"\n--- RENDERING YOUTUBE SHORT {short_id}: {out_filename} ---")
    
    # 1. Extract 40s audio slice from master_soundtrack.wav
    cmd_audio = [
        "ffmpeg", "-y",
        "-ss", str(audio_start_sec),
        "-t", str(DURATION_SEC),
        "-i", AUDIO_MASTER,
        "-af", "afade=t=in:ss=0:d=1.0,afade=t=out:st=38.5:d=1.5",
        temp_audio
    ]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Render 1200 frames via FFmpeg rawvideo pipe (1080x1920)
    cmd_video = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W_S}x{H_S}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        temp_video
    ]

    t0 = time.time()
    proc = subprocess.Popen(cmd_video, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for f_idx in range(TOTAL_FRAMES):
        t = f_idx / FPS
        im = render_func(t, DURATION_SEC, f_idx)
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"Rendered {TOTAL_FRAMES} frames in {time.time() - t0:.2f}s ({(TOTAL_FRAMES / (time.time() - t0)):.1f} FPS)")

    # 3. Multiplex audio and video
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", temp_audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        out_mp4
    ]
    subprocess.run(cmd_mux, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[SUCCESS] Exported: {out_mp4}")

    # Cleanup temp files
    if os.path.exists(temp_video):
        os.remove(temp_video)
    if os.path.exists(temp_audio):
        os.remove(temp_audio)


def main():
    print("=" * 70)
    print("IZHAAN INTELLECT // YOUTUBE SHORTS ENGINE (1080x1920, 9:16)")
    print("=" * 70)

    # Short 1: August 5 Crash (Audio from t=322.0s to 362.0s)
    render_short_video(1, render_frame_short1, 322.0, "SHORT_1_AUG5_CRASH.mp4")

    # Short 2: AI vs 1-Bit (Audio from t=420.0s to 460.0s)
    render_short_video(2, render_frame_short2, 420.0, "SHORT_2_AI_VS_1BIT.mp4")

    # Short 3: 4D Hypercube (Audio from t=25.0s to 65.0s)
    render_short_video(3, render_frame_short3, 25.0, "SHORT_3_4D_HYPERCUBE.mp4")

    print("\n" + "=" * 70)
    print("ALL 3 YOUTUBE SHORTS RENDERED AND READY FOR DISTRIBUTION!")
    print("=" * 70)


if __name__ == "__main__":
    main()
