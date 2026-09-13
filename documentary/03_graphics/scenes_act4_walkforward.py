# -*- coding: utf-8 -*-
"""
Procedural Scene Renderers — ACT 4: THE TRUE WALK-FORWARD HEDGE (Scenes 111 - 135)
1080p 30 FPS cinematic motion graphics for @izhaanintellect.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import style_engine as SE

W, H = SE.W, SE.H


def draw_header(d, title, sub):
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT 4 // WALK-FORWARD HEDGE")
    f_t = SE.get_font(42, bold=True)
    f_s = SE.get_font(20, mono=True)
    d.text((80, 85), title, font=f_t, fill=SE.TEXT_WHITE)
    d.text((82, 140), sub, font=f_s, fill=SE.CYAN)
    d.line([(80, 175), (W - 80, 175)], fill=SE.BORDER_CYAN, width=1)


def s_111_the_hedging_mandate(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE INSTITUTIONAL HEDGING MANDATE", "100% LONG SPOT BITCOIN // NO SPOT SALES (NO TAXABLE DISPOSAL)")

    # Dual dials: Spot Core (+1.00) vs Dynamic Derivative (-1.00)
    SE.draw_speedometer_gauge(d, 100.0, 0.0, 100.0, "CORE SPOT BTC", "% ALLOC", W // 4 + 40, H // 2 + 10, 130, SE.GREEN)
    hedge_on = (t / max(0.1, dur * 0.8)) > 0.5
    h_val = -100.0 if hedge_on else 0.0
    SE.draw_speedometer_gauge(d, h_val, -100.0, 0.0, "SHORT PERP OVERLAY", "% DELTA", 3 * W // 4 - 40, H // 2 + 10, 130, SE.DANGER_RED if hedge_on else SE.CYAN)

    d.text((160, H - 200), "ZERO TAX FRICTION: SPOT BITCOIN NEVER SOLD. PORTFOLIO IMMUNIZED EXCLUSIVELY VIA DERIVATIVES.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_112_short_perp_overlay(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "DELTA-NEUTRAL PROTECTION MECHANISM", "SPOT DELTA = +1.0 // PERPETUAL DELTA = -1.0 // NET DELTA = 0.0")

    # Calm Regime card vs Crisis Shield card
    d.rounded_rectangle([160, 240, W // 2 - 40, H - 240], radius=10, fill=SE.BG_TINT_GREEN, outline=SE.GREEN, width=2)
    d.text((200, 280), "CALM REGIME (P < 0.20)", font=SE.get_font(22, bold=True, mono=True), fill=SE.GREEN)
    d.text((200, 360), "NET PORTFOLIO DELTA: +1.00", font=SE.get_font(32, bold=True, mono=True), fill=SE.TEXT_WHITE)
    d.text((200, 430), "100% EXPOSURE TO BTC SECULAR UPSIDE", font=SE.get_font(16, mono=True), fill=SE.CYAN)

    d.rounded_rectangle([W // 2 + 40, 240, W - 160, H - 240], radius=10, fill=SE.BG_TINT_RED, outline=SE.DANGER_RED, width=2)
    d.text((W // 2 + 80, 280), "CRISIS REGIME (P >= 0.20)", font=SE.get_font(22, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W // 2 + 80, 360), "NET PORTFOLIO DELTA: 0.00", font=SE.get_font(32, bold=True, mono=True), fill=SE.CYAN)
    d.text((W // 2 + 80, 430), "DELTA-NEUTRAL SHIELD FREEZES EQUITY VALUE", font=SE.get_font(16, mono=True), fill=SE.GOLD)

    d.text((160, H - 200), "MATHEMATICAL IMMUNIZATION: SHORT DERIVATIVE PROFITS EXACTLY OFFSET SPOT COLLAPSE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_113_exchange_friction_detail(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "REAL-WORLD EXCHANGE FRICTION MODEL", "10 BASIS POINTS ROUND-TRIP TRANSACTION COST PER HEDGE FLIP")

    categories = ["BINANCE VIP 0 TAKER", "MARKET ORDER SLIPPAGE", "TOTAL ROUND-TRIP FRICTION"]
    values = [0.05, 0.05, 0.10]
    colors = [SE.GOLD, SE.GOLD, SE.DANGER_RED]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=0.15,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "DEDUCTED INSTANTLY ON EVERY STATE TRANSITION: 5 BPS ENTRY + 5 BPS EXIT = 10 BPS CHURN DRAG.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_114_funding_cash_flows(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PERPETUAL FUNDING CASH FLOW INTEGRATION", "RECEIVING OR PAYING ACTUAL 8-HOUR FUNDING RATES DAILY")

    # Funding rate oscilloscope with positive cash flow accumulator
    SE.draw_waveform_oscilloscope(
        d, t, 160, 240, W - 320, 220,
        freq=1.8, amp=50, col=SE.GREEN,
        title="BINANCE PERPETUAL FUNDING ACCRUAL (LONG TRADERS PAYING SHORT HEDGE)", deadband=None
    )

    t_prog = min(1.0, t / max(0.1, dur * 0.8))
    cur_cash = 5.91 * t_prog
    d.text((W - 550, 480), f"CASH HARVESTED: +{cur_cash:.2f}%", font=SE.get_font(36, bold=True, mono=True), fill=SE.GREEN)

    d.text((160, H - 200), "ASYMMETRIC REWARD: IN PANIC SELLOFFS, PERP FUNDING DIPS NEGATIVE, PAYING CASH TO THE HEDGE (+5.91%).", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_115_walkforward_simulation_run(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "WALK-FORWARD CONTINUOUS BACKTEST EXECUTION", "292 INDEPENDENT ROLLING TRADING ORIGINS (STEP = 3 DAYS)")

    d.rounded_rectangle([160, 240, W - 160, H - 260], radius=10, fill=SE.BG_PANEL, outline=SE.CYAN, width=2)

    # Animated rolling calendar
    t_prog = min(1.0, t / max(0.1, dur * 0.8))
    cur_origin = int(1 + 291 * t_prog)
    d.text((200, 280), "LIVE WALK-FORWARD SIMULATOR ACTIVE:", font=SE.get_font(22, bold=True, mono=True), fill=SE.CYAN)
    d.text((200, 350), f"SIMULATING ORIGIN {cur_origin:03d} OF 292", font=SE.get_font(56, bold=True, mono=True), fill=SE.GOLD)

    # Progress timeline
    d.rectangle([200, 450, W - 200, 475], fill=SE.BG_PANEL, outline=SE.BORDER_CYAN, width=1)
    d.rectangle([200, 450, 200 + int((W - 400) * t_prog), 475], fill=SE.CYAN)

    d.text((200, 510), "ACCOUNTING LOG: SPOT CAPITAL, HEDGE P&L, 10 BPS CHURN FRICTION, 8H FUNDING CASH FLOWS", font=SE.get_font(16, mono=True), fill=SE.TEXT_WHITE)
    d.text((160, H - 200), "NO RETROSPECTIVE OVERFIT: MODELS WERE TRAINED ONLY ON DATA KNOWN AS OF EACH ORIGIN DAY.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_116_unhedged_baseline_curve(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "UNHEDGED SPOT BITCOIN BASELINE", "TOTAL RETURN: +16.48% // MAX DRAWDOWN: 51.32% // SHARPE: 0.26")

    # Red collapsing equity curve
    pts = []
    n = 80
    revealed = min(n, int((t / max(0.1, dur * 0.85)) * n) + 4)
    for i in range(revealed):
        x = 160 + int(i * (W - 320) / n)
        # Volatile sideways then huge crash
        val = 1.0 + 0.4 * math.sin(i * 0.2) - (0.5132 if i > 45 else 0.1 * math.sin(i * 0.3))
        y = H - 250 - int(val * 180)
        pts.append((x, y))

    if len(pts) > 1:
        d.line(pts, fill=SE.DANGER_RED, width=4)
        d.ellipse([(pts[-1][0] - 6, pts[-1][1] - 6), (pts[-1][0] + 6, pts[-1][1] + 6)], fill=SE.DANGER_RED, outline=SE.TEXT_WHITE)

    d.text((W - 650, 270), "MAX DRAWDOWN: -51.32%", font=SE.get_font(44, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((W - 650, 335), "TOTAL RETURN: +16.48%", font=SE.get_font(24, mono=True), fill=SE.TEXT_WHITE)
    d.text((W - 650, 375), "SHARPE: 0.26 // SORTINO: 0.38", font=SE.get_font(20, mono=True), fill=SE.TEXT_MUTED)

    d.text((160, H - 200), "PASSIVE BUY & HOLD DISASTER: OVER HALF OF PORTFOLIO WEALTH ERASED DURING THE SECULAR DRAWDOWN.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_117_m5_hedged_equity_curve(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "M5 LIGHTGBM HEDGED STRATEGY (THETA = 0.20)", "TOTAL RETURN: +420.69% NET // SHARPE: 2.22 // SORTINO: 3.78")

    pts = []
    n = 80
    revealed = min(n, int((t / max(0.1, dur * 0.85)) * n) + 4)
    for i in range(revealed):
        x = 160 + int(i * (W - 320) / n)
        frac = i / n
        y = H - 250 - int((frac ** 0.85) * 440 + math.sin(i * 0.4) * 15)
        pts.append((x, y))

    if len(pts) > 1:
        poly = [(pts[0][0], H - 250)] + pts + [(pts[-1][0], H - 250)]
        d.polygon(poly, fill=SE.BG_TINT_GREEN)
        d.line(pts, fill=SE.GREEN, width=4)
        hx, hy = pts[-1]
        d.ellipse([(hx - 7, hy - 7), (hx + 7, hy + 7)], fill=SE.GREEN, outline=SE.TEXT_WHITE, width=2)

    ret_prog = min(1.0, t / max(0.1, dur * 0.80))
    cur_ret = 16.48 + (420.69 - 16.48) * (ret_prog ** 1.3)
    d.text((W - 680, 260), f"NET RETURN: +{cur_ret:6.2f}%", font=SE.get_font(42, bold=True, mono=True), fill=SE.GREEN)
    d.text((W - 680, 325), "SHARPE: 2.22 // SORTINO: 3.78", font=SE.get_font(24, mono=True), fill=SE.TEXT_WHITE)
    d.text((W - 680, 370), "MAX DRAWDOWN HALTED AT 12.95%", font=SE.get_font(20, mono=True), fill=SE.CYAN)

    d.text((160, H - 200), "A 25X OUTPERFORMANCE: TURNING A MEAGER +16% HOLD RETURN INTO +420% NET OF ALL FEES AND SLIPPAGE.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_118_drawdown_comparison_split(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE DRAWDOWN HALTING SHIELD", "UNHEDGED: 51.32% -> M5 HEDGED: 12.95% (38.38 PP REDUCTION)")

    categories = ["UNHEDGED BITCOIN", "M5 LIGHTGBM HEDGED"]
    values = [51.32, 12.95]
    colors = [SE.DANGER_RED, SE.GREEN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=60.0,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "38.38 PERCENTAGE POINTS SAVED: 74.8% OF THE SECULAR CRYPTO CRASH WAS SYSTEMATICALLY NEUTRALIZED.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_119_march_2024_alltime_high(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "MARCH 2024 ALL-TIME HIGH CYCLE", "M5 REMAINS FULLY EXPOSED DURING UPTREND (ZERO PREMATURE HEDGE)")

    SE.draw_candlestick_chart(d, x=180, y=240, w=W - 360, h=H - 480, t=t, dur=dur, trend="bullish")

    d.text((W - 550, 270), "BTC ATH: $73,750", font=SE.get_font(38, bold=True, mono=True), fill=SE.GREEN)
    d.text((W - 550, 330), "P(CRASH) < 0.20 (HEDGE OFF)", font=SE.get_font(20, mono=True), fill=SE.CYAN)
    d.text((W - 550, 370), "FULL 100% UPSIDE PARTICIPATION", font=SE.get_font(16, mono=True), fill=SE.TEXT_MUTED)

    d.text((180, H - 200), "SELECTIVE ACTIVATION: M5 AVOIDED PREMATURE HEDGING, CAPTURING THE ENTIRE SECULAR EXPANSION.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_120_august_crash_shield(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "AUGUST 5, 2024 FLASH CRASH DUAL SIMULATION", "SIDE-BY-SIDE REPLAY: UNHEDGED SPOT VS M5 SYSTEMIC HEDGE")

    w_card = (W - 360) // 2
    h_card = H - 460
    y_card = 230
    x_left = 160
    x_right = x_left + w_card + 40

    # Left Panel: UNHEDGED PORTFOLIO
    SE.draw_glass_panel(d, x_left, y_card, w_card, h_card, radius=10, fill=SE.BG_TINT_RED)
    d.text((x_left + 25, y_card + 20), "UNHEDGED SPOT BUY & HOLD", font=SE.get_font(20, bold=True, mono=True), fill=SE.DANGER_RED)
    d.line([(x_left + 25, y_card + 50), (x_left + w_card - 25, y_card + 50)], fill=SE.BORDER_CYAN, width=1)

    # Mini candlestick chart on left
    SE.draw_candlestick_chart(d, x=x_left + 20, y=y_card + 65, w=w_card - 40, h=220, t=t, dur=dur, trend="bearish")
    # Loss metrics
    loss_prog = min(1.0, t / max(0.1, dur * 0.8))
    equity_left = 100000 - int(23300 * loss_prog)
    d.text((x_left + 30, y_card + 300), f"PORTFOLIO: ${equity_left:,}", font=SE.get_font(32, bold=True, mono=True), fill=SE.DANGER_RED)
    d.text((x_left + 30, y_card + 345), f"DRAWDOWN: -{23.3 * loss_prog:.1f}% // STATUS: UNPROTECTED", font=SE.get_font(15, mono=True), fill=SE.TEXT_MUTED)

    # Right Panel: M5 LIGHTGBM HEDGED
    SE.draw_glass_panel(d, x_right, y_card, w_card, h_card, radius=10, fill=SE.BG_TINT_GREEN)
    d.text((x_right + 25, y_card + 20), "M5 LIGHTGBM DYNAMIC HEDGE", font=SE.get_font(20, bold=True, mono=True), fill=SE.GREEN)
    d.line([(x_right + 25, y_card + 50), (x_right + w_card - 25, y_card + 50)], fill=SE.BORDER_CYAN, width=1)

    # Mini candlestick chart on right
    SE.draw_candlestick_chart(d, x=x_right + 20, y=y_card + 65, w=w_card - 40, h=220, t=t, dur=dur, trend="bearish")
    # Hedged metrics
    equity_right = 100000 - int(600 * loss_prog)
    d.text((x_right + 30, y_card + 300), f"PORTFOLIO: ${equity_right:,}", font=SE.get_font(32, bold=True, mono=True), fill=SE.GREEN)
    d.text((x_right + 30, y_card + 345), f"1.0X SHORT PERP OPENED // PERP GAIN: +$22,700", font=SE.get_font(15, bold=True, mono=True), fill=SE.CYAN)

    SE.draw_evidence_badge(d, 3, "AUGUST 5 YEN UNWIND NEUTRALIZED", "PORTFOLIO DRAWDOWN CAPPED AT 12.95%")
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_121_funding_bonus_explained(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE FUNDING CASH FLOW BONUS", "COLLECTING CASH FROM RETAIL TRADERS SHORTING THE BOTTOM")

    SE.draw_speedometer_gauge(d, 5.91, 0.0, 10.0, "FUNDING CASH FLOW", "% NAV", W // 4 + 40, H // 2 + 10, 130, SE.GREEN)

    # Cash counter card
    d.rounded_rectangle([W // 2 + 40, 260, W - 160, H - 240], radius=10, fill=SE.BG_PANEL, outline=SE.GOLD, width=2)
    d.text((W // 2 + 80, 300), "CASH GENERATION DYNAMICS:", font=SE.get_font(22, bold=True, mono=True), fill=SE.GOLD)
    d.text((W // 2 + 80, 370), "+5.91% CASH HARVESTED", font=SE.get_font(48, bold=True, mono=True), fill=SE.GREEN)
    d.text((W // 2 + 80, 460), "Panicked retail traders paid excessive funding to short into the lows,", font=SE.get_font(18), fill=SE.TEXT_WHITE)
    d.text((W // 2 + 80, 500), "which our hedge captured directly into portfolio cash equity.", font=SE.get_font(18), fill=SE.TEXT_WHITE)

    d.text((160, H - 200), "DOUBLE VICTORY: NOT ONLY WAS CAPITAL PROTECTED, BUT CASH WAS ACTIVELY EXTRACTED FROM LIQUIDATING SHORTS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_122_m4_autoregression_result(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "M4 DYNAMIC-AR HEDGED RESULTS", "TOTAL RETURN: +353.29% // MAX DRAWDOWN: 21.68% // SHARPE: 1.78")

    SE.draw_speedometer_gauge(d, 353.29, 0.0, 450.0, "M4 NET RETURN", "%", W // 4 + 40, H // 2 + 10, 130, SE.CYAN)
    SE.draw_speedometer_gauge(d, 21.68, 0.0, 55.0, "MAX DRAWDOWN", "%", 3 * W // 4 - 40, H // 2 + 10, 130, SE.GOLD)

    d.text((160, H - 200), "M4 VALIDATION: ACHIEVED 29.65 PP DRAWDOWN REDUCTION WITH ONLY 28 HEDGE TRANSITIONS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_123_m7_central_bank_flop(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "M7 FULL 4D DLM TRADING EXECUTION", "TOTAL RETURN: +48.69% // MAX DRAWDOWN: 51.32% (0.00% PROTECTION)")

    categories = ["UNHEDGED BASELINE", "M7 CENTRAL BANK DLM", "M5 LIGHTGBM"]
    values = [51.32, 51.32, 12.95]
    colors = [SE.DANGER_RED, SE.DANGER_RED, SE.GREEN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=60.0,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "ZERO DOWNSIDE PROTECTION: M7 DELIVERED THE EXACT SAME 51.32% DRAWDOWN AS NEVER HEDGING AT ALL.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_124_why_m7_failed_hedge(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "WHY M7 FAILED AS A TRADING TRIGGER", "GAUSSIAN KALMAN SMOOTHING NEVER CROSSED 0.20 DURING RAPID INTRADAY DRAINS")

    # Probability time series for M7: peaked at 0.18, just below the 0.20 activation line
    SE.draw_waveform_oscilloscope(
        d, t, 160, 250, W - 320, 240,
        freq=1.2, amp=40, col=SE.GOLD,
        title="M7 POSTERIOR PROBABILITY P(CRASH) — PEAKED AT 0.18 (BELOW 0.20 THRESHOLD)",
        deadband=(0.20, 0.20)
    )

    d.text((160, H - 200), "THRESHOLD PARALYSIS: BECAUSE KALMAN SMOOTHING COMPRESSES EXTREMES, P NEVER EXCEEDED 0.20.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_125_leaderboard_inspection(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "SORTING THE COMPLETE TOURNAMENT LEADERBOARD", "COMPARING TOTAL RETURNS NET OF TRANSACTION FRICTION")

    # Animated table sorting
    categories = ["M0 PERSISTENCE", "M5 LIGHTGBM", "M4 DYNAMIC-AR", "M3 MULTI-LOG", "M6 2D-DLM", "M7 4D-DLM", "UNHEDGED SPOT"]
    values = [477.79, 420.69, 353.29, 142.10, 85.40, 48.69, 16.48]
    colors = [SE.GOLD, SE.GREEN, SE.CYAN, SE.TEXT_MUTED, SE.TEXT_MUTED, SE.DANGER_RED, SE.DANGER_RED]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=520.0,
        x=180, y=240, w=W - 360, h=H - 480,
        t=t, dur=dur, colors=colors
    )
    d.text((180, H - 200), "AN IMPOSSIBLE RESULT: M0 NAIVE PERSISTENCE SITS AT THE VERY TOP (+477.79%), BEATING MACHINE LEARNING.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_126_anomaly_spotted(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "ANOMALY: MODEL ZERO IN FIRST PLACE", "NAIVE PERSISTENCE (+477.79%) OUTPERFORMS MACHINE LEARNING (+420.69%)")

    # Side-by-side shock comparison
    d.rounded_rectangle([160, 240, W // 2 - 40, H - 240], radius=10, fill=SE.BG_TINT_GOLD, outline=SE.GOLD, width=2)
    d.text((200, 280), "M0 NAIVE PERSISTENCE", font=SE.get_font(24, bold=True, mono=True), fill=SE.GOLD)
    d.text((200, 360), "+477.79% NET", font=SE.get_font(56, bold=True, mono=True), fill=SE.GOLD)
    d.text((200, 450), "1-LINE DUMB HEURISTIC: REPEAT YESTERDAY'S STATE", font=SE.get_font(16, mono=True), fill=SE.TEXT_WHITE)

    d.rounded_rectangle([W // 2 + 40, 240, W - 160, H - 240], radius=10, fill=SE.BG_TINT_GREEN, outline=SE.GREEN, width=2)
    d.text((W // 2 + 80, 280), "M5 LIGHTGBM (GRADIENT TREES)", font=SE.get_font(24, bold=True, mono=True), fill=SE.GREEN)
    d.text((W // 2 + 80, 360), "+420.69% NET", font=SE.get_font(56, bold=True, mono=True), fill=SE.GREEN)
    d.text((W // 2 + 80, 450), "100 DECISION TREES + 7 MULTI-DOMAIN FEATURES", font=SE.get_font(16, mono=True), fill=SE.CYAN)

    d.text((160, H - 200), "HOW COULD A ZERO-MATH BASELINE OUTPERFORM ADVANCED GRADIENT-BOOSTED MACHINE LEARNING BY +57%?", font=SE.get_font(18, bold=True, mono=True), fill=SE.GOLD)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_127_m0_persistence_stats(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "M0 PERSISTENCE BENCHMARK STATS", "TOTAL RETURN: +477.79% // MAX DRAWDOWN: 12.89% // SHARPE: 2.11")

    SE.draw_speedometer_gauge(d, 477.79, 0.0, 500.0, "M0 TOTAL RETURN", "%", W // 4 + 40, H // 2 + 10, 130, SE.GOLD)
    SE.draw_speedometer_gauge(d, 12.89, 0.0, 50.0, "MAX DRAWDOWN", "%", 3 * W // 4 - 40, H // 2 + 10, 130, SE.GREEN)

    d.text((160, H - 200), "M0 RULE: IF SPOT DRAWDOWN WAS >= 85TH PERCENTILE YESTERDAY, MAINTAIN SHORT HEDGE TODAY.", font=SE.get_font(18, bold=True, mono=True), fill=SE.CYAN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_128_humiliation_of_ai(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "THE HUMILIATION OF ARTIFICIAL INTELLIGENCE", "ZERO TREES, ZERO KALMAN FILTERS, YET +57% HIGHER NET DOLLARS")

    # Question mark pulsing radar profile
    categories = ["MATH ELEGANCE", "FEATURE DIVERSITY", "COMPUTE BUDGET", "NET DOLLARS"]
    values_ai = [0.95, 0.92, 0.88, 0.70]
    values_m0 = [0.05, 0.05, 0.01, 1.00]

    SE.draw_radar_spider_chart(d, categories, values_ai, W // 4 + 40, H // 2 + 10, 130, t, col=SE.CYAN, label="AI MODELS")
    SE.draw_radar_spider_chart(d, categories, values_m0, 3 * W // 4 - 40, H // 2 + 10, 130, t, col=SE.GOLD, label="M0 DUMB RULE")

    d.text((160, H - 200), "AN APPARENT DEFEAT FOR QUANTITATIVE FINANCE: WAS ADVANCED MACHINE LEARNING OVERKILL ALL ALONG?", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_129_friction_drag_column(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "INSPECTING THE FRICTION DRAG COLUMN", "THE REAL CULPRIT: CHURN AND BOUNDARY FLICKERING")

    categories = ["M0 PERSISTENCE", "M5 LIGHTGBM", "M4 DYNAMIC-AR"]
    values = [38, 56, 28]  # Hedge flip counts
    colors = [SE.GREEN, SE.DANGER_RED, SE.CYAN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=70,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "THE CHURN MYSTERY: M5 FLIPPED POSITIONS 56 TIMES COMPARED TO M0'S 38 FLIPS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_130_fee_bleeding_breakdown(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "M5 LIGHTGBM FEE BLEEDING EXPOSED", "56 HEDGE FLIPS INCURRING 16.37% CAPITAL DRAG IN FEES AND SLIPPAGE")

    categories = ["GROSS ALPHA HARVESTED", "EXCHANGE TAKER FEES", "MARKET SLIPPAGE", "NET REMAINING RETURN"]
    values = [58.4, 8.18, 8.19, 42.06]
    colors = [SE.GREEN, SE.DANGER_RED, SE.DANGER_RED, SE.CYAN]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=70.0,
        x=200, y=260, w=W - 400, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((200, H - 200), "16.37% OF CAPITAL DESTROYED IN FEES: 56 FLIPS ATE MASSIVE CAPITAL AT 10 BPS PER ROUND-TRIP.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_131_persistence_calm(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "PERSISTENCE DISCIPLINE", "M0 FLIPPED ONLY 38 TIMES (10.14% DRAG) // HELD IN SOLID BLOCKS")

    # M0 flip bar vs M5 flip bar
    categories = ["M0 PERSISTENCE (10.14% DRAG)", "M5 LIGHTGBM (16.37% DRAG)"]
    values = [10.14, 16.37]
    colors = [SE.GREEN, SE.DANGER_RED]

    SE.draw_animated_bar_chart(
        d, categories, values, max_val=20.0,
        x=220, y=260, w=W - 440, h=H - 520,
        t=t, dur=dur, colors=colors
    )
    d.text((220, H - 200), "6.23% CAPITAL SAVED PURELY BY NOT OVERTRADING: M0 HELD ITS GROUND IN SOLID BLOCKS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.GREEN)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_132_whipsaw_oscilloscope(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "HAIRLINE PROBABILITY WHIPSAWS", "TODAY: 20.1% (ENTER) // TOMORROW: 19.9% (EXIT) // DAY AFTER: 20.2% (ENTER)")

    # Rapid high frequency wave crossing 0.20 threshold
    SE.draw_waveform_oscilloscope(
        d, t * 2.5, 160, 250, W - 320, 240,
        freq=3.5, amp=45, col=SE.DANGER_RED,
        title="PROBABILITY FLICKERING ON THE 0.20 KNIFE-EDGE (RAPID CHURN TRIGGER)",
        deadband=(0.20, 0.20)
    )

    d.text((160, H - 200), "THE EXCHANGE GETS RICH WHILE YOUR PREDICTIVE ALPHA DIES IN TAKER FEES ON MARGINAL FLICKERS.", font=SE.get_font(18, bold=True, mono=True), fill=SE.DANGER_RED)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_133_mandelbrot_vindication(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "VOLATILITY CLUSTERING IN CRYPTO", "BENOIT MANDELBROT'S STYLIZED FACT EXPLOITED BY PERSISTENCE")

    hl_prog = max(0.0, min(1.0, (t - 0.4) / max(0.1, dur * 0.7)))
    SE.draw_archival_paper(
        d,
        journal_str="JOURNAL OF BUSINESS 36 (1963) 394–419",
        title_str="The Variation of Certain Speculative Prices",
        authors_str="Benoit B. Mandelbrot (IBM Thomas J. Watson Research Center)",
        quote_str="Large changes tend to be followed by large changes, of either sign, and small changes tend to be followed by small changes.",
        highlight_frac=hl_prog,
        box=(140, 230, W - 140, H - 210)
    )
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_134_the_deep_dive_begins(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    draw_header(d, "IS PERSISTENCE TRULY SUPERIOR?", "TESTING PARAMETER SENSITIVITY ACROSS THRESHOLDS THETA IN [0.10, 0.40]")

    # Grid preview of sensitivity sweep
    thresholds = ["theta = 0.10", "theta = 0.15", "theta = 0.20", "theta = 0.25", "theta = 0.30", "theta = 0.35", "theta = 0.40"]
    cw = (W - 280) // len(thresholds)
    for i, th in enumerate(thresholds):
        bx = 140 + i * cw
        d.rounded_rectangle([bx + 4, 280, bx + cw - 4, 480], radius=8, fill=SE.BG_PANEL, outline=SE.CYAN, width=1)
        d.text((bx + 12, 310), th, font=SE.get_font(15, bold=True, mono=True), fill=SE.GOLD)
        d.text((bx + 12, 380), "SWEEPING", font=SE.get_font(14, mono=True), fill=SE.CYAN)

    d.text((140, H - 210), "SCIENTIFIC RIGOR: WE SWEPT THE ACTIVATION THRESHOLD ACROSS 7 LEVELS TO TEST FOR MODEL FRAGILITY.", font=SE.get_font(18, bold=True, mono=True), fill=SE.TEXT_WHITE)
    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)


def s_135_act5_transition(t, dur, f_idx):
    im = SE.create_base_canvas()
    d = ImageDraw.Draw(im)
    SE.draw_cyber_grid(d)
    SE.draw_hud_frame(d, title="IZHAAN INTELLECT // FORENSIC RISK LAB", act_str="ACT V // THE ONE-BIT TRAP")

    cx, cy = W // 2, H // 2
    d.text((cx - 380, cy - 60), "ACT V: THE ONE-BIT TRAP", font=SE.get_font(54, bold=True), fill=SE.TEXT_WHITE)
    d.text((cx - 440, cy + 30), "WHY PERSISTENCE IS AN ILLUSION & HOW HYSTERESIS SAVED AI", font=SE.get_font(24, mono=True), fill=SE.CYAN)
    d.line([(cx - 440, cy + 85), (cx + 440, cy + 85)], fill=SE.BORDER_CYAN, width=2)

    SE.draw_ambient_hud_elements(d, t, f_idx)
    return SE.apply_cinematic_camera(im, t, dur)
