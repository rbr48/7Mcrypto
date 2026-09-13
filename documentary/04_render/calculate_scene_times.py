# -*- coding: utf-8 -*-
"""
Calculates exact millisecond-accurate start, duration, and end times
for each of the 165 scenes, precisely matched to the calibrated audio timeline.
"""
import json
import os

TIMELINE_PATH = "documentary/00_script/timeline.json"
OUTPUT_PATH = "documentary/00_script/scene_timeline.json"

with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
    tl = json.load(f)

total_audio_dur = tl["total_runtime_sec"]
beats = tl["beats"]

# Group beats by act
acts = {}
for b in beats:
    acts.setdefault(b["act"], []).append(b)

# Scene allocations per act:
# Act 0: 1 to 25 (25 scenes)
# Act 1: 26 to 55 (30 scenes)
# Act 2: 56 to 85 (30 scenes)
# Act 3: 86 to 110 (25 scenes)
# Act 4: 111 to 135 (25 scenes)
# Act 5: 136 to 155 (20 scenes)
# Act 6: 156 to 165 (10 scenes)

scene_counts = {
    0: (1, 25),
    1: (26, 55),
    2: (56, 85),
    3: (86, 110),
    4: (111, 135),
    5: (136, 155),
    6: (156, 165),
}

# Calculate act start and end times
# To prevent gaps between acts, each act spans from its start to the start of the next act,
# and the final act spans until total_audio_dur.
act_spans = {}
for a in range(7):
    a_start = acts[a][0]["start"]
    if a < 6:
        a_end = acts[a + 1][0]["start"]
    else:
        a_end = total_audio_dur
    act_spans[a] = (a_start, a_end, a_end - a_start)

print("ACT TIME SPANS:")
for a in range(7):
    s, e, d = act_spans[a]
    cnt = scene_counts[a][1] - scene_counts[a][0] + 1
    avg_d = d / cnt
    print(f"Act {a}: {s:.2f}s -> {e:.2f}s (dur={d:.2f}s, scenes={cnt}, avg={avg_d:.2f}s/scene)")

# Distribute time evenly among scenes in each act
scenes = []
for a in range(7):
    s_start, s_end, a_dur = act_spans[a]
    start_id, end_id = scene_counts[a]
    cnt = end_id - start_id + 1
    scene_dur = a_dur / cnt

    for idx in range(cnt):
        sc_id = start_id + idx
        sc_s = s_start + idx * scene_dur
        sc_e = s_start + (idx + 1) * scene_dur
        if sc_id == 165:
            sc_e = total_audio_dur
            scene_dur = sc_e - sc_s

        scenes.append({
            "scene_id": sc_id,
            "act": a,
            "start": round(sc_s, 3),
            "end": round(sc_e, 3),
            "duration": round(sc_e - sc_s, 3),
            "fps": 30,
            "frames": int(round((sc_e - sc_s) * 30))
        })

data = {
    "total_runtime_sec": total_audio_dur,
    "total_runtime_min": tl["total_runtime_min"],
    "scene_count": len(scenes),
    "scenes": scenes
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Successfully generated {OUTPUT_PATH} with {len(scenes)} scenes!")
