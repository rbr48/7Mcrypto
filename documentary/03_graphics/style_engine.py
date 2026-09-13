# -*- coding: utf-8 -*-
"""
Izhaan Intellect Cinematic Visual Engine & Quant HUD Toolkit
Hollywood/Netflix-grade procedural 1080p motion graphics renderer.
Provides dark-mode cyber aesthetics, 4D hypercube projections, CRT scanlines,
kinetic typography, financial charts, and official channel watermarking.
"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FPS = 30

# Theme configuration: "LIGHT" (Editorial White / Vox / Financial Times) or "DARK" (Cyber Terminal)
THEME = os.getenv("DOCUMENTARY_THEME", "LIGHT").upper()

if THEME == "LIGHT":
    BG_DARK = (250, 252, 255)       # Studio Paper White
    BG_PANEL = (242, 246, 252)      # Soft floating slate card panel
    CYAN = (14, 116, 220)           # Electric Cobalt Blue
    GOLD = (195, 125, 10)           # Refined Editorial Amber
    DANGER_RED = (225, 29, 72)      # Crimson Red
    GREEN = (16, 160, 80)           # Emerald Green
    TEXT_WHITE = (15, 23, 42)       # Obsidian Charcoal (main headlines)
    TEXT_MUTED = (100, 116, 139)    # Slate Grey (body/secondary)
    GRID_LINE = (232, 238, 246)     # Architectural drafting lines
    BORDER_CYAN = (210, 222, 238)   # Clean structural card borders
    BG_TINT_RED = (255, 241, 242)   # Soft crimson highlight panel
    BG_TINT_GREEN = (240, 253, 244) # Soft emerald highlight panel
    BG_TINT_BLUE = (239, 246, 255)  # Soft cobalt highlight panel
    BG_TINT_CYAN = BG_TINT_BLUE
    BG_TINT_GOLD = (255, 250, 235)  # Soft amber highlight panel
else:
    BG_DARK = (5, 8, 15)
    BG_PANEL = (11, 17, 28)
    CYAN = (48, 209, 235)
    GOLD = (255, 204, 0)
    DANGER_RED = (255, 59, 48)
    GREEN = (52, 199, 89)
    TEXT_WHITE = (242, 246, 252)
    TEXT_MUTED = (120, 138, 160)
    GRID_LINE = (18, 28, 44)
    BORDER_CYAN = (30, 80, 120)
    BG_TINT_RED = (40, 12, 16)
    BG_TINT_GREEN = (12, 38, 20)
    BG_TINT_BLUE = (15, 30, 50)
    BG_TINT_CYAN = BG_TINT_BLUE
    BG_TINT_GOLD = (45, 35, 15)

FONT_REG_PATH = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"
FONT_MONO_PATH = "C:/Windows/Fonts/consolab.ttf"


def get_font(size=24, bold=False, mono=False):
    path = FONT_MONO_PATH if mono else (FONT_BOLD_PATH if bold else FONT_REG_PATH)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            return ImageFont.load_default()


def smoothstep(edge0, edge1, x):
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)


def ease_in_out(t):
    return t * t * (3.0 - 2.0 * t)


def create_base_canvas():
    return Image.new("RGB", (W, H), BG_DARK)


def draw_cyber_grid(d, spacing=60, alpha=35):
    col = GRID_LINE if THEME == "LIGHT" else (18, 28, 44, alpha)
    for x in range(0, W, spacing):
        d.line([(x, 0), (x, H)], fill=col, width=1)
    for y in range(0, H, spacing):
        d.line([(0, y), (W, y)], fill=col, width=1)


def draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT // 4D-MGRFF"):
    # Outer bounding brackets
    m = 35
    sz = 24
    c = CYAN
    # Top-Left
    d.line([(m, m), (m + sz, m)], fill=c, width=2)
    d.line([(m, m), (m, m + sz)], fill=c, width=2)
    # Top-Right
    d.line([(W - m, m), (W - m - sz, m)], fill=c, width=2)
    d.line([(W - m, m), (W - m, m + sz)], fill=c, width=2)
    # Bottom-Left
    d.line([(m, H - m), (m + sz, H - m)], fill=c, width=2)
    d.line([(m, H - m), (m, H - m - sz)], fill=c, width=2)
    # Bottom-Right
    d.line([(W - m, H - m), (W - m - sz, H - m)], fill=c, width=2)
    d.line([(W - m, H - m), (W - m, H - m - sz)], fill=c, width=2)

    # Header tech metadata
    f_mono = get_font(15, mono=True)
    d.ellipse([(m + 32, m + 2), (m + 40, m + 10)], fill=GREEN)
    d.text((m + 48, m - 3), title, font=f_mono, fill=TEXT_MUTED)
    d.text((W - m - 220, m - 3), act_str, font=f_mono, fill=CYAN)


def apply_watermark(im, t, dur):
    fade = max(0.0, min(1.0, t / 0.5))
    im = im.convert("RGBA")
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    font = get_font(18, bold=True, mono=True)
    label = "IZHAAN INTELLECT"
    bbox = d.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    mx, my = 48, 42
    x = W - mx - tw
    y = H - my - th
    pad = 9
    if THEME == "LIGHT":
        d.rounded_rectangle(
            [x - pad - 16, y - pad, x + tw + pad, y + th + pad],
            radius=6, fill=(240, 244, 252, int(220 * fade)), outline=(210, 222, 238, int(200 * fade))
        )
        d.ellipse([x - 22, y + th // 2 - 4, x - 14, y + th // 2 + 4], fill=(14, 116, 220, int(230 * fade)))
        d.text((x, y - 1), label, font=font, fill=(15, 23, 42, int(220 * fade)))
    else:
        d.rounded_rectangle(
            [x - pad - 16, y - pad, x + tw + pad, y + th + pad],
            radius=6, fill=(4, 9, 14, int(120 * fade))
        )
        d.ellipse([x - 22, y + th // 2 - 4, x - 14, y + th // 2 + 4], fill=(48, 209, 235, int(220 * fade)))
        d.text((x, y - 1), label, font=font, fill=(235, 242, 248, int(180 * fade)))

    out = Image.alpha_composite(im, overlay).convert("RGB")
    return out


# ------------------------------------------------------------- 4D TESSERACT ENGINE ---
def generate_tesseract_vertices():
    # 16 vertices of a 4D hypercube in {-1, 1}^4
    verts = []
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (-1, 1):
                for w in (-1, 1):
                    verts.append(np.array([x, y, z, w], dtype=np.float32))
    return np.array(verts)


def generate_tesseract_edges():
    # Edges connect vertices that differ by exactly 1 coordinate
    edges = []
    for i in range(16):
        for j in range(i + 1, 16):
            diff = (i ^ j)
            if diff in (1, 2, 4, 8):
                edges.append((i, j))
    return edges


TESS_VERTS = generate_tesseract_vertices()
TESS_EDGES = generate_tesseract_edges()


def rotate_4d(v, theta_xw, theta_zw, theta_yw=0.0, theta_xy=0.0):
    """Compound 4D rotation across 4 orthogonal planes: XW, YW, ZW, and XY."""
    x, y, z, w = v[0], v[1], v[2], v[3]
    # XW plane
    cxw, sxw = math.cos(theta_xw), math.sin(theta_xw)
    x1 = x * cxw - w * sxw
    w1 = x * sxw + w * cxw
    # YW plane
    cyw, syw = math.cos(theta_yw), math.sin(theta_yw)
    y1 = y * cyw - w1 * syw
    w2 = y * syw + w1 * cyw
    # ZW plane
    czw, szw = math.cos(theta_zw), math.sin(theta_zw)
    z1 = z * czw - w2 * szw
    w3 = z * szw + w2 * czw
    # XY plane
    cxy, sxy = math.cos(theta_xy), math.sin(theta_xy)
    x2 = x1 * cxy - y1 * sxy
    y2 = x1 * sxy + y1 * cxy

    return np.array([x2, y2, z1, w3])


def project_4d_to_2d(v, scale=220, cx=W//2, cy=H//2):
    # Perspective projection from 4D -> 3D (camera at distance d4)
    d4 = 2.8
    p4 = 1.0 / max(0.2, (d4 - v[3]))
    x3 = v[0] * p4
    y3 = v[1] * p4
    z3 = v[2] * p4

    # Perspective projection from 3D -> 2D (camera at distance d3)
    d3 = 3.5
    p3 = 1.0 / max(0.2, (d3 - z3))
    x2 = cx + x3 * p3 * scale * 2.8
    y2 = cy + y3 * p3 * scale * 2.8

    return int(round(x2)), int(round(y2)), p4


def render_tesseract_frame(im, d, t, cx=W//2, cy=H//2, scale=240, alpha_edge=200):
    """Renders high-definition compound rotating 4D tesseract with true w-depth fog."""
    theta_xw = t * 0.7
    theta_zw = t * 0.5
    theta_yw = t * 0.35
    theta_xy = t * 0.4

    # Ambient radial bloom
    for r in range(260, 40, -40):
        alpha_tint = (242 + int((260 - r) * 0.04), 246 + int((260 - r) * 0.03), 254) if THEME == "LIGHT" else (10, 20, 35)
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=alpha_tint)

    # Concentric orbital rings
    for r in (180, 300, 420):
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=GRID_LINE, width=1)

    proj_pts = []
    w_coords = []
    p4_depths = []
    for v in TESS_VERTS:
        vr = rotate_4d(v, theta_xw, theta_zw, theta_yw, theta_xy)
        px, py, p4 = project_4d_to_2d(vr, scale, cx, cy)
        proj_pts.append((px, py))
        w_coords.append(vr[3])
        p4_depths.append(p4)

    # Edges sorted by average w coordinate (back to front)
    edge_draw_list = []
    for i, j in TESS_EDGES:
        avg_w = (w_coords[i] + w_coords[j]) * 0.5
        avg_p4 = (p4_depths[i] + p4_depths[j]) * 0.5
        edge_draw_list.append((avg_w, avg_p4, i, j))
    edge_draw_list.sort(key=lambda x: x[0])

    for avg_w, avg_p4, i, j in edge_draw_list:
        p1 = proj_pts[i]
        p2 = proj_pts[j]
        # w-depth fog attenuation
        w_norm = max(0.0, min(1.0, (avg_w + 1.5) / 3.0))
        if THEME == "LIGHT":
            r_col = int(140 - w_norm * 126)
            g_col = int(150 - w_norm * 34)
            b_col = int(170 + w_norm * 50)
            line_w = 3 if w_norm > 0.5 else 1
        else:
            r_col = int(20 + w_norm * 40)
            g_col = int(60 + w_norm * 140)
            b_col = int(100 + w_norm * 155)
            line_w = 2 if w_norm > 0.5 else 1
        d.line([p1, p2], fill=(r_col, g_col, b_col), width=line_w)

    # Glowing vertex nodes
    for idx, (px, py) in enumerate(proj_pts):
        w_val = w_coords[idx]
        w_norm = max(0.0, min(1.0, (w_val + 1.5) / 3.0))
        node_r = int(3 + w_norm * 5)
        node_col = CYAN if w_norm > 0.5 else TEXT_MUTED
        d.ellipse([(px - node_r, py - node_r), (px + node_r, py + node_r)], fill=node_col, outline=(255, 255, 255), width=1)


def apply_cinematic_camera(im, t, dur, max_zoom=1.030, drift_dir=(0.5, 0.5)):
    """
    Subtle 2.5D cinematic Ken Burns camera drift and micro-zoom (1.0 -> 1.030).
    Adds organic film movement to procedural static motion graphic frames.
    Idempotent: guarantees camera is applied at most once per frame.
    """
    if dur <= 0 or getattr(im, "_camera_applied", False):
        return im
    prog = smoothstep(0.0, 1.0, t / dur)
    scale = 1.0 + (max_zoom - 1.0) * prog
    w_crop = int(W / scale)
    h_crop = int(H / scale)
    dx, dy = drift_dir
    cx = int(W * 0.5 + (dx - 0.5) * (W - w_crop))
    cy = int(H * 0.5 + (dy - 0.5) * (H - h_crop))
    x0 = max(0, min(W - w_crop, cx - w_crop // 2))
    y0 = max(0, min(H - h_crop, cy - h_crop // 2))
    cropped = im.crop((x0, y0, x0 + w_crop, y0 + h_crop))
    out = cropped.resize((W, H), Image.Resampling.BILINEAR)
    out._camera_applied = True
    return out


def draw_archival_paper(d, journal_str, title_str, authors_str, quote_str, highlight_frac=1.0, box=(140, 230, W - 140, H - 210)):
    """Renders a prestigious academic paper document card with real-time text highlighter wipe."""
    x0, y0, x1, y1 = box
    paper_bg = (255, 255, 255) if THEME == "LIGHT" else (14, 20, 30)
    paper_border = (205, 218, 235) if THEME == "LIGHT" else (35, 60, 95)
    shadow_col = (222, 230, 242) if THEME == "LIGHT" else (5, 8, 14)

    # Subtle drop shadow
    d.rounded_rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], radius=10, fill=shadow_col)
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=paper_bg, outline=paper_border, width=2)

    # Top archival stamp
    f_stamp = get_font(15, bold=True, mono=True)
    d.text((x0 + 40, y0 + 26), f"ARCHIVAL REPOSITORY // {journal_str}", font=f_stamp, fill=CYAN)
    d.line([(x0 + 40, y0 + 54), (x1 - 40, y0 + 54)], fill=BORDER_CYAN, width=1)

    # Paper title
    f_title = get_font(32, bold=True)
    d.text((x0 + 40, y0 + 72), title_str, font=f_title, fill=TEXT_WHITE)

    # Authors
    f_auth = get_font(19, mono=True)
    d.text((x0 + 42, y0 + 125), f"AUTHORS: {authors_str}", font=f_auth, fill=TEXT_MUTED)

    # Key Thesis Box
    bx0, by0, bx1, by1 = x0 + 40, y0 + 175, x1 - 40, y1 - 35
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=6, fill=BG_PANEL, outline=BORDER_CYAN, width=1)
    d.text((bx0 + 25, by0 + 18), "CORE QUANTITATIVE THEOREM / FINDING:", font=get_font(17, bold=True, mono=True), fill=GOLD)

    # Quote text
    f_quote = get_font(24, bold=True)
    # Highlight wipe effect
    if highlight_frac > 0:
        hl_w = int((bx1 - bx0 - 50) * min(1.0, highlight_frac))
        hl_fill = (255, 238, 130) if THEME == "LIGHT" else (40, 75, 45)
        d.rectangle([bx0 + 22, by0 + 58, bx0 + 22 + hl_w, by0 + 115], fill=hl_fill)

    d.text((bx0 + 25, by0 + 68), f'"{quote_str}"', font=f_quote, fill=TEXT_WHITE)


def draw_news_ticker(d, headline, source="BLOOMBERG WIRE", t=0.0):
    """Renders a breaking news ticker flash lower-third across the screen."""
    ty0, ty1 = H - 105, H - 65
    d.rectangle([0, ty0, W, ty1], fill=(15, 23, 42) if THEME == "LIGHT" else (8, 12, 20))
    # Red live badge
    d.rectangle([0, ty0, 160, ty1], fill=DANGER_RED)
    d.text((22, ty0 + 10), "LIVE WIRE", font=get_font(16, bold=True, mono=True), fill=(255, 255, 255))
    # Source tag
    d.text((180, ty0 + 10), f"[{source}]", font=get_font(16, bold=True, mono=True), fill=CYAN)
    # Marquee headline text
    offset = int((t * 90) % 240)
    d.text((360 - offset, ty0 + 10), headline, font=get_font(19, bold=True), fill=(245, 248, 255))


# ==============================================================================
# CINEMATIC PROCEDURAL MOTION-GRAPHIC WIDGETS
# ==============================================================================

def spring_step(t, dur=1.0, omega=10.0, zeta=0.65):
    """Calculates underdamped harmonic spring response with organic settling overshoot."""
    if t <= 0:
        return 0.0
    if t >= dur:
        return 1.0
    p = t / dur
    wd = omega * math.sqrt(max(0.01, 1.0 - zeta * zeta))
    decay = math.exp(-zeta * omega * p)
    osc = math.cos(wd * p) + (zeta / math.sqrt(max(0.01, 1.0 - zeta * zeta))) * math.sin(wd * p)
    return 1.0 - decay * osc


def draw_glass_panel(d, x, y, w, h, radius=10, fill=None, outline=None, shadow=True):
    """Renders a high-end glassmorphic panel with dual-pass soft drop shadows."""
    if fill is None:
        fill = BG_PANEL
    if outline is None:
        outline = BORDER_CYAN
    if shadow:
        sh_col_1 = (228, 234, 244) if THEME == "LIGHT" else (3, 5, 10)
        sh_col_2 = (215, 224, 236) if THEME == "LIGHT" else (2, 4, 8)
        d.rounded_rectangle([x - 4, y + 4, x + w + 4, y + h + 8], radius=radius + 2, fill=sh_col_1)
        d.rounded_rectangle([x - 2, y + 2, x + w + 2, y + h + 4], radius=radius + 1, fill=sh_col_2)
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=1)


def draw_macro_ticker_tape(d, t, narrative_date="HISTORICAL PIT FEED", x0=480, y0=24, w_tape=1080):
    """Renders a continuous Bloomberg-grade scrolling ticker tape in the top header."""
    h_pill = 24
    d.rounded_rectangle([x0, y0, x0 + w_tape, y0 + h_pill], radius=4, fill=(242, 246, 252) if THEME == "LIGHT" else (10, 16, 26), outline=BORDER_CYAN, width=1)
    d.rectangle([x0, y0, x0 + 115, y0 + h_pill], fill=(14, 116, 220) if THEME == "LIGHT" else (30, 80, 140))
    d.text((x0 + 8, y0 + 4), "LIVE TELEMETRY", font=get_font(11, bold=True, mono=True), fill=(255, 255, 255))

    items = [
        ("BTC/USDT", "$61,420", "-3.15%", False),
        ("ETH/BTC", "0.0468", "-4.82%", False),
        ("DERIBIT DVOL", "64.20", "+18.5%", True),
        ("CBOE VIX", "24.85", "+22.1%", True),
        ("US10Y YIELD", "4.12%", "-0.06%", False),
        ("BINANCE PERP FUND", "-0.012%/8h", "SHORT PAY", False)
    ]
    f_tick = get_font(11, mono=True)
    item_widths = []
    for sym, val, chg, is_spike in items:
        s = f"{sym} {val} [{chg}]   •   "
        bbox = d.textbbox((0, 0), s, font=f_tick)
        item_widths.append((bbox[2] - bbox[0], sym, val, chg, is_spike))
    total_w = sum(w for w, _, _, _, _ in item_widths)
    if total_w <= 0:
        return
    scroll_speed = 60
    offset = int(t * scroll_speed) % total_w
    view_x = x0 + 125
    view_w = w_tape - 135
    cur_x = view_x - offset
    for rep in range(3):
        for w_i, sym, val, chg, is_spike in item_widths:
            if cur_x + w_i >= view_x and cur_x <= view_x + view_w:
                d.text((cur_x, y0 + 5), sym, font=f_tick, fill=TEXT_MUTED)
                sym_bbox = d.textbbox((0, 0), sym + " ", font=f_tick)
                val_x = cur_x + (sym_bbox[2] - sym_bbox[0])
                d.text((val_x, y0 + 5), val, font=f_tick, fill=TEXT_WHITE)
                val_bbox = d.textbbox((0, 0), sym + " " + val + " ", font=f_tick)
                chg_x = cur_x + (val_bbox[2] - val_bbox[0])
                col_chg = DANGER_RED if ("-" in chg or is_spike) else (GREEN if "+" in chg else GOLD)
                d.text((chg_x, y0 + 5), f"[{chg}]", font=f_tick, fill=col_chg)
                sep_x = cur_x + w_i - 20
                if sep_x < view_x + view_w:
                    d.text((sep_x, y0 + 5), "•", font=f_tick, fill=BORDER_CYAN)
            cur_x += w_i


def draw_evidence_badge(d, exhibit_num, title_str, status_str="FORENSIC PROOF: CONFIRMED", x=60, y=H - 140):
    """Renders a prestigious Forensic Case File Evidence Badge in the corner."""
    w_badge = 460
    h_badge = 62
    draw_glass_panel(d, x, y, w_badge, h_badge, radius=6)
    d.rounded_rectangle([x + 4, y + 4, x + 10, y + h_badge - 4], radius=3, fill=GOLD)
    f_tag = get_font(12, bold=True, mono=True)
    f_tit = get_font(14, bold=True)
    f_stat = get_font(11, mono=True)
    d.text((x + 22, y + 8), f"EXHIBIT 0{exhibit_num} // FORENSIC CASE EVIDENCE", font=f_tag, fill=GOLD)
    d.text((x + 22, y + 25), title_str, font=f_tit, fill=TEXT_WHITE)
    d.text((x + 22, y + 43), status_str, font=f_stat, fill=GREEN)


def draw_formula_dissection_card(d, title_str, formula_str, terms_list, x=180, y=240, w=W - 360, h=480):
    """Renders an interactive math explainer card with labeled bracket callouts."""
    draw_glass_panel(d, x, y, w, h, radius=10)
    d.text((x + 30, y + 25), title_str, font=get_font(20, bold=True, mono=True), fill=CYAN)
    d.line([(x + 30, y + 55), (x + w - 30, y + 55)], fill=BORDER_CYAN, width=1)
    box_h = 100
    d.rounded_rectangle([x + 30, y + 75, x + w - 30, y + 75 + box_h], radius=8, fill=BG_TINT_BLUE, outline=BORDER_CYAN, width=1)
    f_math = get_font(34, bold=True, mono=True)
    bbox_m = d.textbbox((0, 0), formula_str, font=f_math)
    mw = bbox_m[2] - bbox_m[0]
    d.text((x + (w - mw) // 2, y + 75 + (box_h - 40) // 2), formula_str, font=f_math, fill=TEXT_WHITE)
    n_terms = len(terms_list)
    col_w = (w - 60) // max(1, n_terms)
    y_terms = y + 200
    for idx, (sym, label_str, desc_str, col_tag) in enumerate(terms_list):
        tx = x + 30 + idx * col_w
        ty = y_terms
        d.rounded_rectangle([tx + 5, ty, tx + col_w - 15, ty + 240], radius=6, fill=(255, 255, 255) if THEME == "LIGHT" else (16, 24, 38), outline=BORDER_CYAN, width=1)
        f_sym = get_font(18, bold=True, mono=True)
        sym_bbox = d.textbbox((0, 0), sym, font=f_sym)
        badge_w = max(45, (sym_bbox[2] - sym_bbox[0]) + 20)
        d.rounded_rectangle([tx + 15, ty + 15, tx + 15 + badge_w, ty + 50], radius=4, fill=col_tag if col_tag else CYAN)
        d.text((tx + 22, ty + 19), sym, font=f_sym, fill=(255, 255, 255))
        d.text((tx + 15, ty + 65), label_str, font=get_font(16, bold=True), fill=TEXT_WHITE)
        words = desc_str.split(" ")
        line = ""
        y_line = ty + 95
        for word in words:
            test_line = line + word + " "
            if len(test_line) > 28:
                d.text((tx + 15, y_line), line.strip(), font=get_font(13), fill=TEXT_MUTED)
                line = word + " "
                y_line += 22
            else:
                line = test_line
        if line:
            d.text((tx + 15, y_line), line.strip(), font=get_font(13), fill=TEXT_MUTED)


def draw_ambient_hud_elements(d, t, f_idx):
    """Draws cinematic corner telemetry, animated spectrum, ticker tape, and timecode."""
    f_mono = get_font(13, mono=True)
    # Timecode
    sec = int(t)
    ms = int((t - sec) * 100)
    tc_str = f"TC: 00:{sec//60:02d}:{sec%60:02d}:{ms:02d} // FRM: {f_idx:05d}"
    d.text((W - 340, H - 32), tc_str, font=f_mono, fill=TEXT_MUTED)

    # Micro spectrum analyzer in bottom left
    sx, sy = 40, H - 36
    for i in range(16):
        h = int(abs(math.sin(t * 5.0 + i * 0.45)) * 14) + 3
        d.rectangle([sx + i * 6, sy - h, sx + i * 6 + 4, sy], fill=CYAN)

    # Top live macro ticker tape
    draw_macro_ticker_tape(d, t)


def draw_speedometer_gauge(d, val, min_val, max_val, title, unit="", cx=W//2, cy=H//2 + 30, radius=150, col=CYAN):
    """Renders a curved analog/digital telemetry dial with swept needle."""
    # Background circular plate
    plate_col = BG_PANEL
    d.ellipse([(cx - radius - 20, cy - radius - 20), (cx + radius + 20, cy + radius + 20)], fill=plate_col, outline=BORDER_CYAN, width=1)

    start_ang = math.pi * 0.75
    end_ang = math.pi * 2.25
    total_ang = end_ang - start_ang

    # Tick marks
    n_ticks = 24
    for i in range(n_ticks + 1):
        frac = i / n_ticks
        ang = start_ang + frac * total_ang
        t_col = GREEN if frac < 0.4 else (GOLD if frac < 0.7 else DANGER_RED)
        r_inner = radius - (14 if i % 4 == 0 else 8)
        x1 = cx + int(math.cos(ang) * r_inner)
        y1 = cy + int(math.sin(ang) * r_inner)
        x2 = cx + int(math.cos(ang) * radius)
        y2 = cy + int(math.sin(ang) * radius)
        d.line([(x1, y1), (x2, y2)], fill=t_col, width=2 if i % 4 == 0 else 1)

    # Value fraction
    clamped_val = max(min_val, min(max_val, val))
    val_frac = (clamped_val - min_val) / max(0.001, max_val - min_val)
    needle_ang = start_ang + val_frac * total_ang

    # Swept arc trail
    arc_steps = max(2, int(val_frac * 40))
    for s in range(arc_steps):
        a0 = start_ang + (s / 40.0) * total_ang
        a1 = start_ang + ((s + 1) / 40.0) * total_ang
        ax0 = cx + int(math.cos(a0) * (radius - 4))
        ay0 = cy + int(math.sin(a0) * (radius - 4))
        ax1 = cx + int(math.cos(a1) * (radius - 4))
        ay1 = cy + int(math.sin(a1) * (radius - 4))
        d.line([(ax0, ay0), (ax1, ay1)], fill=col, width=4)

    # Needle
    nx = cx + int(math.cos(needle_ang) * (radius - 18))
    ny = cy + int(math.sin(needle_ang) * (radius - 18))
    d.line([(cx, cy), (nx, ny)], fill=DANGER_RED if val_frac > 0.75 else col, width=3)
    d.ellipse([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=TEXT_WHITE, outline=col, width=2)

    # Value readout & Title
    f_val = get_font(36, bold=True, mono=True)
    val_str = f"{val:.2f}{unit}"
    bbox_v = d.textbbox((0, 0), val_str, font=f_val)
    vw = bbox_v[2] - bbox_v[0]
    d.text((cx - vw//2, cy + radius - 45), val_str, font=f_val, fill=TEXT_WHITE)

    f_lbl = get_font(18, bold=True, mono=True)
    bbox_l = d.textbbox((0, 0), title, font=f_lbl)
    lw = bbox_l[2] - bbox_l[0]
    d.text((cx - lw//2, cy + radius + 5), title, font=f_lbl, fill=TEXT_MUTED)


def draw_waveform_oscilloscope(d, t, x, y, w, h, freq=1.0, amp=0.8, col=CYAN, title="SIGNAL TRACE", deadband=None):
    """Renders a CRT-style oscilloscope screen with sweeping phosphor beam."""
    # Frame
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(8, 14, 22) if THEME == "DARK" else (245, 248, 254), outline=BORDER_CYAN, width=2)
    # Grid lines inside scope
    grid_c = (20, 32, 48) if THEME == "DARK" else (228, 235, 245)
    for gx in range(x + 40, x + w, 60):
        d.line([(gx, y), (gx, y + h)], fill=grid_c, width=1)
    for gy in range(y + 30, y + h, 40):
        d.line([(x, gy), (x + w, gy)], fill=grid_c, width=1)

    # Title
    d.text((x + 20, y + 15), title, font=get_font(15, bold=True, mono=True), fill=TEXT_MUTED)

    # Deadband limits if requested
    cy = y + h // 2
    if deadband:
        lower_b, upper_b = deadband
        # deadband could be given as (-0.4, 0.4) or (0.20, 0.20)
        y_low = max(y + 25, min(y + h - 10, int(cy - lower_b * (h * 0.38))))
        y_upp = max(y + 25, min(y + h - 10, int(cy - upper_b * (h * 0.38))))
        d.rectangle([x + 2, min(y_low, y_upp), x + w - 2, max(y_low, y_upp)], fill=BG_TINT_GOLD)
        d.line([(x + 2, y_upp), (x + w - 2, y_upp)], fill=DANGER_RED, width=2)
        d.line([(x + 2, y_low), (x + w - 2, y_low)], fill=GREEN, width=2)

    # Dynamic sweeping wave
    pts = []
    n_pts = 100
    sweep_head = int(((t * 1.2) % 1.0) * n_pts)
    norm_amp = min(0.85, amp / max(1.0, h * 0.38)) if amp > 1.0 else min(0.88, max(0.05, amp))
    for i in range(n_pts):
        px = x + int(i * w / n_pts)
        frac = i / n_pts
        val = math.sin(frac * math.pi * 4.0 * freq + t * 4.0) * norm_amp + math.sin(frac * 12.0) * (0.10 * norm_amp)
        py = max(y + 25, min(y + h - 10, cy - int(val * (h * 0.38))))
        pts.append((px, py))

    if len(pts) > 1:
        d.line(pts, fill=col, width=3)
        # Leading phosphor head
        if 0 <= sweep_head < len(pts):
            hx, hy = pts[sweep_head]
            d.ellipse([(hx - 6, hy - 6), (hx + 6, hy + 6)], fill=(255, 255, 255), outline=col, width=2)


def draw_animated_bar_chart(d, categories, values, max_val, x, y, w, h, t, dur, colors=None):
    """Renders progressive racing horizontal bars comparing model metrics with spring physics."""
    draw_glass_panel(d, x, y, w, h, radius=8)
    n = len(categories)
    row_h = (h - 60) // n
    anim_prog = spring_step(t, max(0.1, dur * 0.65), omega=9.0, zeta=0.72)

    for i in range(n):
        ry = y + 40 + i * row_h
        cat = categories[i]
        val = values[i]
        cur_val = val * max(0.0, anim_prog)
        bar_len = int((cur_val / max(0.001, max_val)) * (w - 320))
        bar_col = colors[i] if colors and i < len(colors) else CYAN

        # Label
        d.text((x + 25, ry + 6), cat, font=get_font(18, bold=True, mono=True), fill=TEXT_WHITE)
        # Background bar track
        d.rounded_rectangle([x + 180, ry + 6, x + w - 120, ry + row_h - 12], radius=4, fill=GRID_LINE)
        # Animated active bar
        if bar_len > 4:
            d.rounded_rectangle([x + 180, ry + 6, x + 180 + bar_len, ry + row_h - 12], radius=4, fill=bar_col)
        # Value text
        d.text((x + w - 100, ry + 6), f"{cur_val:.2f}", font=get_font(18, bold=True, mono=True), fill=bar_col)


def draw_flow_diagram(d, steps, active_step, x, y, w, h, t):
    """Renders connected process architecture cards with glowing data pulses."""
    n = len(steps)
    step_w = (w - (n - 1) * 40) // n
    card_h = h - 60

    for i in range(n):
        bx = x + i * (step_w + 40)
        by = y + 30
        is_active = (i == active_step)
        border_col = CYAN if is_active else BORDER_CYAN
        card_fill = BG_TINT_BLUE if is_active else BG_PANEL

        # Step card
        d.rounded_rectangle([bx, by, bx + step_w, by + card_h], radius=8, fill=card_fill, outline=border_col, width=2 if is_active else 1)
        # Step header
        d.text((bx + 16, by + 18), f"STEP {i+1:02d}", font=get_font(14, bold=True, mono=True), fill=GOLD if is_active else TEXT_MUTED)
        title, desc = steps[i]
        d.text((bx + 16, by + 45), title, font=get_font(20, bold=True), fill=TEXT_WHITE)
        d.text((bx + 16, by + 85), desc, font=get_font(14, mono=True), fill=TEXT_MUTED)

        # Connector arrow to next
        if i < n - 1:
            ax0 = bx + step_w + 5
            ax1 = bx + step_w + 35
            ay = by + card_h // 2
            d.line([(ax0, ay), (ax1, ay)], fill=BORDER_CYAN, width=2)
            # Animated moving data pulse
            pulse_x = ax0 + int(((t * 3.0 + i) % 1.0) * (ax1 - ax0))
            d.ellipse([(pulse_x - 3, ay - 3), (pulse_x + 3, ay + 3)], fill=CYAN)


def draw_matrix_heatmap(d, matrix_data, row_labels, col_labels, x, y, w, h, t, highlight_cell=None):
    """Renders a 7x7 contagion propagation matrix heatmap with cell animations."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=BG_PANEL, outline=BORDER_CYAN, width=1)
    n_rows = len(row_labels)
    n_cols = len(col_labels)

    cell_w = (w - 180) // n_cols
    cell_h = (h - 70) // n_rows

    f_lbl = get_font(14, bold=True, mono=True)
    f_num = get_font(13, mono=True)

    # Column headers
    for j, col_name in enumerate(col_labels):
        cx = x + 160 + j * cell_w
        d.text((cx + 6, y + 15), col_name[:5], font=f_lbl, fill=CYAN)

    for i, row_name in enumerate(row_labels):
        ry = y + 45 + i * cell_h
        # Row header
        d.text((x + 20, ry + cell_h//4), row_name[:7], font=f_lbl, fill=TEXT_WHITE)

        for j in range(n_cols):
            cx = x + 160 + j * cell_w
            val = matrix_data[i][j] if i < len(matrix_data) and j < len(matrix_data[i]) else 0.0
            # Color by intensity
            intensity = min(1.0, abs(val) * 1.5)
            if val > 0:
                cell_col = (int(240 - intensity * 50), int(250 - intensity * 30), 255) if THEME == "LIGHT" else (15, int(40 + intensity * 120), int(80 + intensity * 150))
            else:
                cell_col = (255, int(245 - intensity * 45), int(245 - intensity * 45)) if THEME == "LIGHT" else (int(50 + intensity * 150), 20, 30)

            is_hl = (highlight_cell == (i, j))
            d.rounded_rectangle([cx + 2, ry + 2, cx + cell_w - 2, ry + cell_h - 2], radius=4, fill=cell_col, outline=GOLD if is_hl else GRID_LINE, width=2 if is_hl else 1)
            d.text((cx + 8, ry + cell_h//4), f"{val:+.2f}", font=f_num, fill=TEXT_WHITE if not is_hl else GOLD)


def draw_circular_feedback_loop(d, stages, t, cx=W//2, cy=H//2 + 30, radius=190):
    """Renders circular reflexivity loop with revolving orbital particles."""
    n = len(stages)
    # Circle track
    d.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)], outline=BORDER_CYAN, width=2)

    # Rotating orbital particles
    for p in range(4):
        ang_p = t * 1.5 + p * (math.pi / 2)
        px = cx + int(math.cos(ang_p) * radius)
        py = cy + int(math.sin(ang_p) * radius)
        d.ellipse([(px - 6, py - 6), (px + 6, py + 6)], fill=CYAN)

    # Stage nodes
    for i in range(n):
        ang = i * (2 * math.pi / n) - math.pi / 2
        nx = cx + int(math.cos(ang) * radius)
        ny = cy + int(math.sin(ang) * radius)

        node_w, node_h = 170, 75
        d.rounded_rectangle([nx - node_w//2, ny - node_h//2, nx + node_w//2, ny + node_h//2], radius=8, fill=BG_PANEL, outline=CYAN, width=2)
        if isinstance(stages[i], (tuple, list)):
            title, sub = stages[i][0], (stages[i][1] if len(stages[i]) > 1 else "")
        else:
            title, sub = str(stages[i]), ""
        d.text((nx - node_w//2 + 15, ny - node_h//2 + 14), title, font=get_font(15, bold=True), fill=TEXT_WHITE)
        if sub:
            d.text((nx - node_w//2 + 15, ny - node_h//2 + 42), sub, font=get_font(12, mono=True), fill=TEXT_MUTED)

    # Center label
    d.ellipse([(cx - 70, cy - 70), (cx + 70, cy + 70)], fill=BG_TINT_RED, outline=DANGER_RED, width=2)
    d.text((cx - 52, cy - 20), "CIRCULAR", font=get_font(18, bold=True, mono=True), fill=DANGER_RED)
    d.text((cx - 45, cy + 6), "FEEDBACK", font=get_font(16, bold=True, mono=True), fill=TEXT_WHITE)


def draw_candlestick_chart(d, x, y, w, h, t, dur, trend="crash"):
    """Renders authentic Level-1 exchange candlestick chart with volume bars."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=BG_PANEL, outline=BORDER_CYAN, width=1)
    n_candles = 28
    candle_w = (w - 60) // n_candles
    revealed = min(n_candles, int((t / max(0.1, dur * 0.85)) * n_candles) + 2)

    base_p = 68000.0
    for i in range(revealed):
        cx = x + 30 + i * candle_w
        if trend == "crash":
            drift = -i * 1100 if i < 16 else -16000 + (i - 16) * 400
        else:
            drift = i * 850 + math.sin(i * 0.8) * 600

        noise = math.sin(i * 1.5) * 450
        o = base_p + drift + noise
        c = o + math.cos(i * 2.1) * 600 - (300 if trend == "crash" else -300)
        hi = max(o, c) + abs(math.sin(i * 3.3)) * 400
        lo = min(o, c) - abs(math.cos(i * 2.7)) * 400

        is_green = (c >= o)
        col = GREEN if is_green else DANGER_RED

        # Map price to Y
        p_min, p_max = 48000.0, 72000.0
        scale = (h - 120) / (p_max - p_min)
        y_hi = y + h - 70 - int((hi - p_min) * scale)
        y_lo = y + h - 70 - int((lo - p_min) * scale)
        y_top = y + h - 70 - int((max(o, c) - p_min) * scale)
        y_bot = y + h - 70 - int((min(o, c) - p_min) * scale)

        # Wick
        d.line([(cx + candle_w//2, y_hi), (cx + candle_w//2, y_lo)], fill=col, width=1)
        # Body
        d.rectangle([cx + 2, y_top, cx + candle_w - 2, max(y_top + 2, y_bot)], fill=col)
        # Volume bar at bottom
        vol_h = int(abs(math.sin(i * 0.9)) * 40) + 10
        d.rectangle([cx + 2, y + h - 15 - vol_h, cx + candle_w - 2, y + h - 15], fill=GRID_LINE)


def draw_radar_spider_chart(d, categories, values, x, y, radius, t, col=CYAN, label="MODEL PROFILE"):
    """Renders a multi-dimensional quant radar comparison polygon."""
    n = len(categories)
    # Concentric rings
    for ring in (0.33, 0.66, 1.0):
        r_pts = []
        for i in range(n):
            ang = i * (2 * math.pi / n) - math.pi / 2
            rx = x + int(math.cos(ang) * radius * ring)
            ry = y + int(math.sin(ang) * radius * ring)
            r_pts.append((rx, ry))
        d.polygon(r_pts, outline=GRID_LINE, width=1)

    # Spokes and labels
    for i in range(n):
        ang = i * (2 * math.pi / n) - math.pi / 2
        sx = x + int(math.cos(ang) * radius)
        sy = y + int(math.sin(ang) * radius)
        d.line([(x, y), (sx, sy)], fill=GRID_LINE, width=1)
        lx = x + int(math.cos(ang) * (radius + 25))
        ly = y + int(math.sin(ang) * (radius + 25))
        d.text((lx - 25, ly - 8), categories[i], font=get_font(13, bold=True, mono=True), fill=TEXT_MUTED)

    # Data polygon
    d_pts = []
    for i in range(n):
        ang = i * (2 * math.pi / n) - math.pi / 2
        v = min(1.0, max(0.0, values[i])) * min(1.0, t * 1.5)
        dx = x + int(math.cos(ang) * radius * v)
        dy = y + int(math.sin(ang) * radius * v)
        d_pts.append((dx, dy))

    if len(d_pts) > 2:
        d.polygon(d_pts, fill=BG_TINT_BLUE, outline=col, width=2)
        for px, py in d_pts:
            d.ellipse([(px - 4, py - 4), (px + 4, py + 4)], fill=col)

    d.text((x - 55, y - radius - 35), label, font=get_font(15, bold=True, mono=True), fill=col)


def draw_pvalue_fdr_plot(d, pvals, q_val, x, y, w, h, t):
    """Renders Benjamini-Hochberg rank plot with animated critical slope boundary."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=BG_PANEL, outline=BORDER_CYAN, width=1)
    m = len(pvals)
    sorted_p = sorted(pvals)

    # Axes
    ox, oy = x + 80, y + h - 60
    d.line([(ox, oy), (x + w - 40, oy)], fill=BORDER_CYAN, width=2)
    d.line([(ox, oy), (ox, y + 40)], fill=BORDER_CYAN, width=2)
    d.text((x + w - 160, oy + 15), "RANK k (1..m)", font=get_font(14, mono=True), fill=TEXT_MUTED)
    d.text((ox - 70, y + 25), "p-value", font=get_font(14, mono=True), fill=TEXT_MUTED)

    # FDR Critical line: y = (k/m) * q
    x_end = x + w - 40
    y_end = oy - int(((m / m) * q_val) * (h - 120))
    d.line([(ox, oy), (x_end, y_end)], fill=GOLD, width=2)
    d.text((x_end - 140, y_end - 24), f"FDR THRESHOLD (Q={q_val})", font=get_font(13, bold=True, mono=True), fill=GOLD)

    # Animated scatter points
    revealed = min(m, int((t * 2.0) * m) + 1)
    for k in range(revealed):
        p = sorted_p[k]
        px = ox + int(((k + 1) / m) * (w - 140))
        py = oy - int(p * (h - 120))
        crit = ((k + 1) / m) * q_val
        is_sig = (p <= crit)
        dot_col = GREEN if is_sig else DANGER_RED
        d.ellipse([(px - 4, py - 4), (px + 4, py + 4)], fill=dot_col, outline=TEXT_WHITE, width=1)


def draw_orderbook_depth(d, x, y, w, h, t):
    """Renders Level-2 bid/ask cumulative depth volume curves."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=BG_PANEL, outline=BORDER_CYAN, width=1)
    cx = x + w // 2
    cy = y + h - 40

    # Center spread gap
    d.line([(cx, y + 40), (cx, cy)], fill=BORDER_CYAN, width=1)
    d.text((cx - 30, y + 15), "SPREAD", font=get_font(14, bold=True, mono=True), fill=GOLD)

    # Bid curve (green on left, cumulative)
    b_pts = [(x + 30, cy)]
    for i in range(25):
        bx = x + 30 + int(i * (cx - x - 50) / 25)
        frac = (25 - i) / 25.0
        depth_vol = (frac ** 1.8) * (h - 100) + math.sin(i * 0.8 + t * 3.0) * 12
        by = cy - int(depth_vol)
        b_pts.append((bx, by))
    b_pts.append((cx - 20, cy))
    d.polygon(b_pts, fill=BG_TINT_GREEN, outline=GREEN, width=2)

    # Ask curve (red on right, cumulative)
    a_pts = [(cx + 20, cy)]
    for i in range(25):
        ax = cx + 20 + int(i * (x + w - cx - 50) / 25)
        frac = (i + 1) / 25.0
        depth_vol = (frac ** 1.8) * (h - 100) + math.cos(i * 0.8 + t * 3.2) * 12
        ay = cy - int(depth_vol)
        a_pts.append((ax, ay))
    a_pts.append((x + w - 30, cy))
    d.polygon(a_pts, fill=BG_TINT_RED, outline=DANGER_RED, width=2)

    d.text((x + 50, y + 40), "CUMULATIVE BIDS (USDT)", font=get_font(15, bold=True, mono=True), fill=GREEN)
    d.text((x + w - 240, y + 40), "CUMULATIVE ASKS (BTC)", font=get_font(15, bold=True, mono=True), fill=DANGER_RED)


