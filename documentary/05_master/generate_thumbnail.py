# -*- coding: utf-8 -*-
"""
High-CTR Cinematic YouTube Thumbnail Generator for Izhaan Intellect
Generates 1080p (1920x1080) broadcast thumbnails in both:
1. Editorial White Theme (Vox / Financial Times / Bloomberg Quicktake)
2. Cyber Dark Theme (Bloomberg Terminal / Quant Lab)
Features 4D tesseract wireframe, official branding, and verified website links.
"""
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw

GRAPHICS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_graphics"))
if GRAPHICS_DIR not in sys.path:
    sys.path.insert(0, GRAPHICS_DIR)

import style_engine as SE

OUT_WHITE = os.path.abspath(os.path.join(os.path.dirname(__file__), "THUMBNAIL_IZHAAN_INTELLECT_WHITE.png"))
OUT_DARK = os.path.abspath(os.path.join(os.path.dirname(__file__), "THUMBNAIL_IZHAAN_INTELLECT_DARK.png"))
OUT_DEFAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "THUMBNAIL_IZHAAN_INTELLECT_4D_CRYPTO_RISK.png"))


def render_thumb(is_light=True, out_path=OUT_WHITE):
    # Palette
    if is_light:
        bg_col = (250, 252, 255)
        grid_col = (232, 238, 246)
        panel_fill = (245, 248, 253, 245)
        border_col = (210, 222, 238)
        text_dark = (15, 23, 42)
        text_muted = (100, 116, 139)
        blue = (14, 116, 220)
        gold = (195, 125, 10)
        red = (225, 29, 72)
        green = (16, 160, 80)
        card_red_bg = (254, 242, 242)
        card_green_bg = (240, 253, 244)
    else:
        bg_col = (5, 8, 15)
        grid_col = (18, 28, 44)
        panel_fill = (8, 14, 24, 220)
        border_col = (30, 80, 120)
        text_dark = (242, 246, 252)
        text_muted = (120, 138, 160)
        blue = (48, 209, 235)
        gold = (255, 204, 0)
        red = (255, 59, 48)
        green = (52, 199, 89)
        card_red_bg = (35, 12, 18)
        card_green_bg = (15, 38, 28)

    im = Image.new("RGB", (SE.W, SE.H), bg_col)
    d = ImageDraw.Draw(im)

    # Grid
    for x in range(0, SE.W, 55):
        d.line([(x, 0), (x, SE.H)], fill=grid_col, width=1)
    for y in range(0, SE.H, 55):
        d.line([(0, y), (SE.W, y)], fill=grid_col, width=1)

    # 4D Tesseract on right side
    cx, cy = 1380, 540
    theta_xw, theta_zw, theta_xy = 1.6, 1.1, 0.7
    proj_pts = []
    depths = []
    for v in SE.TESS_VERTS:
        vr = SE.rotate_4d(v, theta_xw, theta_zw, theta_xy)
        px, py, p4 = SE.project_4d_to_2d(vr, scale=330, cx=cx, cy=cy)
        proj_pts.append((px, py))
        depths.append(p4)

    for i, j in SE.TESS_EDGES:
        p1, p2 = proj_pts[i], proj_pts[j]
        avg_d = (depths[i] + depths[j]) * 0.5
        if is_light:
            col = (int(14 + avg_d * 10), int(95 + avg_d * 30), int(195 + avg_d * 40))
        else:
            col = (int(40 + avg_d * 180), int(140 + avg_d * 110), int(210 + avg_d * 45))
        d.line([p1, p2], fill=col, width=4 if is_light else 3)

    for idx, (px, py) in enumerate(proj_pts):
        r = 8
        if is_light:
            d.ellipse([(px - r, py - r), (px + r, py + r)], fill=text_dark, outline=blue, width=2)
        else:
            d.ellipse([(px - r, py - r), (px + r, py + r)], fill=blue, outline=(255, 255, 255), width=2)

    # Main Left Panel
    d.rounded_rectangle([70, 75, 960, 1005], radius=16, fill=panel_fill, outline=border_col, width=2)

    # Channel Tag
    d.rounded_rectangle([110, 115, 520, 165], radius=8, fill=(235, 242, 252) if is_light else (18, 30, 50), outline=blue, width=1)
    d.ellipse([(128, 133), (144, 149)], fill=green)
    d.text((158, 127), "IZHAAN INTELLECT // FORENSIC QUANT", font=SE.get_font(18, bold=True, mono=True), fill=blue)

    # Headlines
    f_huge = SE.get_font(94, bold=True)
    f_sub = SE.get_font(40, bold=True)

    d.text((110, 195), "THE 51% CRASH", font=f_huge, fill=text_dark)
    d.text((110, 295), "ILLUSION", font=f_huge, fill=gold)

    d.line([(110, 420), (920, 420)], fill=border_col, width=2)
    d.text((110, 445), "HOW A 1-BIT RULE BEAT AI", font=f_sub, fill=blue)

    # Cards
    d.rounded_rectangle([110, 530, 480, 715], radius=10, fill=card_red_bg, outline=red, width=2)
    d.text((130, 550), "UNHEDGED SPOT BITCOIN", font=SE.get_font(17, bold=True, mono=True), fill=text_muted)
    d.text((130, 590), "-51.32%", font=SE.get_font(58, bold=True, mono=True), fill=red)
    d.text((130, 670), "MAXIMUM DRAWDOWN", font=SE.get_font(16, mono=True), fill=text_dark)

    d.rounded_rectangle([520, 530, 920, 715], radius=10, fill=card_green_bg, outline=green, width=2)
    d.text((540, 550), "4D WALK-FORWARD HEDGE", font=SE.get_font(17, bold=True, mono=True), fill=text_muted)
    d.text((540, 590), "+420.69%", font=SE.get_font(58, bold=True, mono=True), fill=green)
    d.text((540, 670), "NET RETURN (HEDGED)", font=SE.get_font(16, mono=True), fill=text_dark)

    # Links badge
    d.text((110, 765), "THESIS PORTAL: HTTPS://7MCRYPTO.IZHAANINTELLECT.FUN/", font=SE.get_font(21, bold=True, mono=True), fill=gold)
    d.text((110, 810), "GITHUB: HTTPS://GITHUB.COM/RBR48/7MCRYPTO (31 TESTS PASSED)", font=SE.get_font(18, mono=True), fill=text_muted)
    d.text((110, 850), "PORTAL: HTTPS://IZHAANINTELLECT.FUN/", font=SE.get_font(18, mono=True), fill=blue)

    # Watch CTA button
    btn_y = 910
    d.rounded_rectangle([110, btn_y, 490, btn_y + 55], radius=8, fill=blue)
    d.text((135, btn_y + 14), "FULL QUANT DOCUMENTARY", font=SE.get_font(20, bold=True), fill=(255, 255, 255))

    # Corner brackets
    m = 35
    sz = 24
    d.line([(m, m), (m + sz, m)], fill=blue, width=2)
    d.line([(m, m), (m, m + sz)], fill=blue, width=2)
    d.line([(SE.W - m, m), (SE.W - m - sz, m)], fill=blue, width=2)
    d.line([(SE.W - m, m), (SE.W - m, m + sz)], fill=blue, width=2)
    d.line([(m, SE.H - m), (m + sz, SE.H - m)], fill=blue, width=2)
    d.line([(m, SE.H - m), (m, SE.H - m - sz)], fill=blue, width=2)
    d.line([(SE.W - m, SE.H - m), (SE.W - m - sz, SE.H - m)], fill=blue, width=2)
    d.line([(SE.W - m, SE.H - m), (SE.W - m, SE.H - m - sz)], fill=blue, width=2)

    im.save(out_path, quality=95)
    print(f"Generated Thumbnail: {out_path}")


def main():
    render_thumb(is_light=True, out_path=OUT_WHITE)
    render_thumb(is_light=False, out_path=OUT_DARK)
    render_thumb(is_light=True, out_path=OUT_DEFAULT)


if __name__ == "__main__":
    main()
