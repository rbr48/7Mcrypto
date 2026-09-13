# -*- coding: utf-8 -*-
"""
Netflix/YouTube-Grade Subtitle Generator for Izhaan Intellect
Parses timeline.json to generate both:
1. documentary_subtitles.srt (Standard SRT format for YouTube upload)
2. documentary_subtitles.ass (Stylized ASS format for Netflix-grade hardcoding)
Features intelligent keyword color emphasis (Gold & Cyan tags for numbers/equations).
"""
import json
import os
import re

TIMELINE_PATH = "documentary/00_script/timeline.json"
OUT_DIR = "documentary/04_subtitles"
SRT_PATH = os.path.join(OUT_DIR, "documentary_subtitles.srt")
ASS_PATH = os.path.join(OUT_DIR, "documentary_subtitles.ass")

os.makedirs(OUT_DIR, exist_ok=True)

with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
    tl = json.load(f)

beats = tl["beats"]


def format_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def format_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"


# Keywords to highlight in gold/cyan in ASS subtitles
HIGHLIGHT_TERMS = [
    (r"\b51\.32%\b", r"{\\c&H00D7FF&}51.32%{\\c&HFFFFFF&}"),
    (r"\b4D-MGRFF\b", r"{\\c&H00EB961F&}4D-MGRFF{\\c&HFFFFFF&}"),
    (r"\bLightGBM\b", r"{\\c&H00EB961F&}LightGBM{\\c&HFFFFFF&}"),
    (r"\bKalman\b", r"{\\c&H00EB961F&}Kalman{\\c&HFFFFFF&}"),
    (r"\bSchmitt-trigger\b", r"{\\c&H00D7FF&}Schmitt-trigger{\\c&HFFFFFF&}"),
    (r"\bhysteresis\b", r"{\\c&H00D7FF&}hysteresis{\\c&HFFFFFF&}"),
    (r"\bM5\b", r"{\\c&H00D7FF&}M5{\\c&HFFFFFF&}"),
    (r"\bM7\b", r"{\\c&H00EB961F&}M7{\\c&HFFFFFF&}"),
    (r"\bM4\b", r"{\\c&H00EB961F&}M4{\\c&HFFFFFF&}"),
    (r"\bM0\b", r"{\\c&H00D7FF&}M0{\\c&HFFFFFF&}"),
    (r"\bBenjamini-Hochberg\b", r"{\\c&H00D7FF&}Benjamini-Hochberg{\\c&HFFFFFF&}"),
    (r"\bFDR\b", r"{\\c&H00D7FF&}FDR{\\c&HFFFFFF&}"),
    (r"\bBinance\b", r"{\\c&H00EB961F&}Binance{\\c&HFFFFFF&}"),
    (r"\bDeribit\b", r"{\\c&H00EB961F&}Deribit{\\c&HFFFFFF&}"),
    (r"\bDVOL\b", r"{\\c&H00D7FF&}DVOL{\\c&HFFFFFF&}"),
    (r"\bFRED\b", r"{\\c&H00EB961F&}FRED{\\c&HFFFFFF&}"),
    (r"\b12\.95%\b", r"{\\c&H0059C734&}12.95%{\\c&HFFFFFF&}"),
    (r"\b420\.69%\b", r"{\\c&H0059C734&}+420.69%{\\c&HFFFFFF&}"),
    (r"\b477\.79%\b", r"{\\c&H0059C734&}+477.79%{\\c&HFFFFFF&}"),
    (r"\bIzhaan Intellect\b", r"{\\c&H00D7FF&}Izhaan Intellect{\\c&HFFFFFF&}"),
]


def style_ass_text(text):
    styled = text
    for pattern, repl in HIGHLIGHT_TERMS:
        styled = re.sub(pattern, repl, styled, flags=re.IGNORECASE)
    return styled


# 1. Generate SRT
with open(SRT_PATH, "w", encoding="utf-8") as f_srt:
    for idx, b in enumerate(beats, start=1):
        s_str = format_srt_time(b["start"])
        e_str = format_srt_time(b["end"])
        text = b["text"].strip()
        f_srt.write(f"{idx}\n{s_str} --> {e_str}\n{text}\n\n")

print(f"Generated SRT: {SRT_PATH} ({len(beats)} cues)")

# 2. Generate ASS
ASS_HEADER = """[Script Info]
Title: Izhaan Intellect - 4D Crypto Risk Master Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Segoe UI,44,&H00FFFFFF,&H00EB961F,&H00090C12,&H80000000,-1,0,0,0,100,100,0,0,1,2.8,1.2,2,120,120,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

with open(ASS_PATH, "w", encoding="utf-8") as f_ass:
    f_ass.write(ASS_HEADER)
    for b in beats:
        s_str = format_ass_time(b["start"])
        e_str = format_ass_time(b["end"])
        raw_text = b["text"].strip()
        styled_text = style_ass_text(raw_text)
        f_ass.write(f"Dialogue: 0,{s_str},{e_str},Default,,0,0,0,,{styled_text}\n")

print(f"Generated ASS: {ASS_PATH} ({len(beats)} cues)")
