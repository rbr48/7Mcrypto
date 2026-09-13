# -*- coding: utf-8 -*-
"""
Calibrate voiceover audio speed to hit exactly ~9.2 to 9.5 minutes runtime.
Applies atempo=1.28 and rebuilds documentary/00_script/timeline.json.
"""
import json
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.dirname(SCRIPT_DIR)
TIMELINE_SRC = os.path.join(DOC_DIR, "01_narration", "timeline.json")
TIMELINE_DST = os.path.join(DOC_DIR, "00_script", "timeline.json")
WAV_DIR = os.path.join(DOC_DIR, "01_narration", "wav")

with open(TIMELINE_SRC, "r", encoding="utf-8") as f:
    tl = json.load(f)

tempo = 1.28
total_t = 0.0
new_beats = []

print(f"Applying atempo={tempo} to {len(tl['beats'])} voice clips...")

for i, b in enumerate(tl["beats"]):
    bid = b["id"]
    f_in = os.path.join(WAV_DIR, f"{bid}.wav")
    f_tmp = os.path.join(WAV_DIR, f"{bid}_tmp.wav")

    subprocess.run([
        "ffmpeg", "-y", "-i", f_in,
        "-filter:a", f"atempo={tempo}",
        f_tmp
    ], check=True, capture_output=True)
    os.replace(f_tmp, f_in)

    r = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", f_in
    ], capture_output=True, text=True)
    d = float(r.stdout.strip())

    pause = 0.6 if (bid.startswith("c_") or bid.endswith("_14") or bid == "p_10") else 0.25
    new_beats.append({
        "id": bid,
        "act": b["act"],
        "start": round(total_t, 3),
        "dur": round(d, 3),
        "end": round(total_t + d, 3),
        "pause": pause,
        "text": b["text"]
    })
    total_t += d + pause

with open(TIMELINE_DST, "w", encoding="utf-8") as f:
    json.dump({
        "total_runtime_sec": round(total_t, 3),
        "total_runtime_min": round(total_t / 60, 2),
        "beats_count": len(new_beats),
        "beats": new_beats
    }, f, indent=2, ensure_ascii=False)

# Also copy to 01_narration/timeline.json
with open(TIMELINE_SRC, "w", encoding="utf-8") as f:
    json.dump({
        "total_runtime_sec": round(total_t, 3),
        "total_runtime_min": round(total_t / 60, 2),
        "beats_count": len(new_beats),
        "beats": new_beats
    }, f, indent=2, ensure_ascii=False)

print("=" * 70)
print(f"CALIBRATION COMPLETE!")
print(f"TOTAL RUNTIME: {total_t:.1f}s = {total_t/60:.2f} MINUTES (TARGET: 8-10 MIN)")
print("=" * 70)
