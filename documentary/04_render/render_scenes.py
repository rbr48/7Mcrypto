# -*- coding: utf-8 -*-
"""
High-Performance Parallel Scene Renderer for Izhaan Intellect
Renders all 165 motion graphics scenes at 1080p 30 FPS across multi-core CPU workers.
Each scene is encoded into an individual MP4 clip via FFmpeg rawvideo pipe,
and indexed in concat_list.txt for lossless instantaneous assembly.
"""
import os
import sys
import json
import time
import subprocess
import multiprocessing

# Add graphics directory to path
GRAPHICS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_graphics"))
if GRAPHICS_DIR not in sys.path:
    sys.path.insert(0, GRAPHICS_DIR)

import style_engine as SE

THEME_TAG = SE.THEME.lower()
CLIPS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), f"clips_{THEME_TAG}"))
TIMELINE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "00_script", "scene_timeline.json"))
CONCAT_LIST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), f"concat_list_{THEME_TAG}.txt"))

os.makedirs(CLIPS_DIR, exist_ok=True)


def get_scene_function_map():
    """Builds a mapping from scene_id (1..165) to (module_name, func_name)."""
    import scenes_act0_prologue as a0
    import scenes_act1_centralbank as a1
    import scenes_act2_contagion as a2
    import scenes_act3_circularity as a3
    import scenes_act4_walkforward as a4
    import scenes_act5_hysteresis as a5
    import scenes_act6_coda as a6

    mapping = {}

    def register(mod_name, mod, start_id):
        funcs = sorted([f for f in dir(mod) if f.startswith("s_")])
        for idx, f in enumerate(funcs):
            mapping[start_id + idx] = (mod_name, f)

    register("scenes_act0_prologue", a0, 1)
    register("scenes_act1_centralbank", a1, 26)
    register("scenes_act2_contagion", a2, 56)
    register("scenes_act3_circularity", a3, 86)
    register("scenes_act4_walkforward", a4, 111)
    register("scenes_act5_hysteresis", a5, 136)
    register("scenes_act6_coda", a6, 156)

    return mapping


def render_single_scene_worker(task):
    """Worker process: renders a single scene clip via FFmpeg rawvideo pipe."""
    scene_id, mod_name, func_name, duration, frames, fps, out_path = task

    # Import modules within worker process
    if GRAPHICS_DIR not in sys.path:
        sys.path.insert(0, GRAPHICS_DIR)
    import style_engine as SE
    mod = __import__(mod_name)
    func = getattr(mod, func_name)

    # FFmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1920x1080",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        out_path
    ]

    t0 = time.time()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        for f_idx in range(frames):
            t = f_idx / fps
            im = func(t, duration, f_idx)
            im = SE.apply_cinematic_camera(im, t, duration)
            im = SE.apply_watermark(im, t, duration)
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        print(f"Error in scene {scene_id} ({func_name}): {e}", file=sys.stderr)
        raise e

    t1 = time.time()
    fps_rate = frames / max(0.001, (t1 - t0))

    return scene_id, frames, t1 - t0, fps_rate


def main():
    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        timeline_data = json.load(f)

    scene_map = get_scene_function_map()
    tasks = []

    for sc in timeline_data["scenes"]:
        sc_id = sc["scene_id"]
        mod_name, func_name = scene_map[sc_id]
        out_path = os.path.join(CLIPS_DIR, f"scene_{sc_id:03d}.mp4")
        tasks.append((
            sc_id,
            mod_name,
            func_name,
            sc["duration"],
            sc["frames"],
            sc["fps"],
            out_path
        ))

    num_workers = min(10, max(2, (os.cpu_count() or 4) - 2))
    print(f"================================================================")
    print(f"IZHAAN INTELLECT // PARALLEL SCENE RENDER ENGINE")
    print(f"Total Scenes: {len(tasks)} (1080p @ 30 FPS)")
    print(f"Active CPU Workers: {num_workers}")
    print(f"Output Directory: {CLIPS_DIR}")
    print(f"================================================================")

    t_start = time.time()
    completed = 0
    total_frames = sum(t[4] for t in tasks)

    with multiprocessing.Pool(processes=num_workers) as pool:
        for res in pool.imap_unordered(render_single_scene_worker, tasks):
            sc_id, frames, elapsed, fps_rate = res
            completed += 1
            print(f"[{completed:03d}/{len(tasks):03d}] Scene {sc_id:03d} completed: {frames} frames in {elapsed:.2f}s ({fps_rate:.1f} FPS)")

    total_time = time.time() - t_start
    overall_fps = total_frames / max(0.001, total_time)
    print(f"================================================================")
    print(f"ALL {len(tasks)} SCENES RENDERED SUCCESSFULLY IN {total_time:.2f}s!")
    print(f"Average Throughput: {overall_fps:.1f} FPS across {total_frames} frames")
    print(f"================================================================")

    # Generate concat list
    with open(CONCAT_LIST_PATH, "w", encoding="utf-8") as f_out:
        for sc in sorted(timeline_data["scenes"], key=lambda x: x["scene_id"]):
            sc_id = sc["scene_id"]
            clip_name = f"scene_{sc_id:03d}.mp4"
            f_out.write(f"file 'clips_{THEME_TAG}/{clip_name}'\n")

    print(f"Generated concat demuxer manifest: {CONCAT_LIST_PATH}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
