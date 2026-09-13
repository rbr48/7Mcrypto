# -*- coding: utf-8 -*-
"""
Master Film Assembly Engine for Izhaan Intellect
Multiplexes all 165 motion graphic scenes with the calibrated master soundtrack
(voiceover + ducked BGM score) and integrates Netflix/YouTube subtitles.
Exports the final broadcast-ready 1080p 30 FPS documentary master.
"""
import os
import sys
import json
import subprocess
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GRAPHICS_DIR = os.path.join(BASE_DIR, "03_graphics")
if GRAPHICS_DIR not in sys.path:
    sys.path.insert(0, GRAPHICS_DIR)
import style_engine as SE

MASTER_DIR = os.path.join(BASE_DIR, "05_master")
os.makedirs(MASTER_DIR, exist_ok=True)

AUDIO_PATH = os.path.join(BASE_DIR, "02_audio", "master_soundtrack.wav")
SUBTITLES_ASS = os.path.join(BASE_DIR, "04_subtitles", "documentary_subtitles.ass")
SUBTITLES_SRT = os.path.join(BASE_DIR, "04_subtitles", "documentary_subtitles.srt")

THEME = SE.THEME
THEME_TAG = THEME.lower()

if THEME == "LIGHT":
    CLIPS_DIR = os.path.join(BASE_DIR, "04_render", "clips_light")
    CONCAT_LIST_PATH = os.path.join(BASE_DIR, "04_render", "concat_list_light.txt")
    OUTPUT_CLEAN_MASTER = os.path.join(MASTER_DIR, "IZHAAN_INTELLECT_4D_CRYPTO_RISK_MASTER_WHITE_1080P.mp4")
    OUTPUT_SUBTITLED_MASTER = os.path.join(MASTER_DIR, "IZHAAN_INTELLECT_4D_CRYPTO_RISK_MASTER_WHITE_HARDCODED_SUBTITLES.mp4")
    SUBTITLES_ASS = os.path.join(BASE_DIR, "04_subtitles", "documentary_subtitles_light.ass")
else:
    CLIPS_DIR = os.path.join(BASE_DIR, "04_render", "clips")
    CONCAT_LIST_PATH = os.path.join(BASE_DIR, "04_render", "concat_list.txt")
    OUTPUT_CLEAN_MASTER = os.path.join(MASTER_DIR, "IZHAAN_INTELLECT_4D_CRYPTO_RISK_MASTER_1080P.mp4")
    OUTPUT_SUBTITLED_MASTER = os.path.join(MASTER_DIR, "IZHAAN_INTELLECT_4D_CRYPTO_RISK_MASTER_HARDCODED_SUBTITLES.mp4")


def verify_clips():
    """Verifies that all 165 scene clips exist and are valid non-empty files."""
    missing = []
    empty = []
    for sc_id in range(1, 166):
        fn = os.path.join(CLIPS_DIR, f"scene_{sc_id:03d}.mp4")
        if not os.path.exists(fn):
            missing.append(sc_id)
        elif os.path.getsize(fn) < 1000:
            empty.append(sc_id)

    if missing or empty:
        raise RuntimeError(f"Clips validation failed! Missing: {missing}, Empty: {empty}")
    print(f"Validated all 165 scene clips in {CLIPS_DIR} (100% complete and healthy).")


def assemble_clean_master():
    """Assembles all 165 scene clips with the master soundtrack."""
    temp_visuals = os.path.join(MASTER_DIR, "temp_visuals.mp4")

    print("\n--- STEP 1: Lossless Concat of 165 Video Clips ---")
    t0 = time.time()
    # Concat demuxer
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", CONCAT_LIST_PATH,
        "-c", "copy",
        temp_visuals
    ]
    subprocess.run(cmd_concat, check=True)
    print(f"Concatenated 165 video clips in {time.time() - t0:.2f}s -> {temp_visuals}")

    print("\n--- STEP 2: Multiplexing Video with Master Soundtrack ---")
    t1 = time.time()
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", temp_visuals,
        "-i", AUDIO_PATH,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "320k",
        "-metadata", "title=IZHAAN INTELLECT // THE 4D CRYPTO RISK ILLUSION",
        "-metadata", "artist=Izhaan Intellect (@izhaanintellect)",
        "-metadata", "comment=Cinematic quant documentary: 4D DLM, Walk-Forward Hedging, and Schmitt-Trigger Hysteresis.",
        "-shortest",
        OUTPUT_CLEAN_MASTER
    ]
    subprocess.run(cmd_mux, check=True)
    print(f"Muxed clean master in {time.time() - t1:.2f}s -> {OUTPUT_CLEAN_MASTER}")

    # Remove temp visuals
    if os.path.exists(temp_visuals):
        os.remove(temp_visuals)


def assemble_subtitled_master():
    """Renders broadcast version with hardcoded stylized Netflix-grade ASS subtitles."""
    print("\n--- STEP 3: Rendering Hardcoded Subtitle Master ---")
    t2 = time.time()
    # Need forward slashes and escaped colons for FFmpeg subtitles filter on Windows
    ass_filter_path = SUBTITLES_ASS.replace("\\", "/").replace(":", "\\:")
    cmd_burn = [
        "ffmpeg", "-y",
        "-i", OUTPUT_CLEAN_MASTER,
        "-vf", f"ass='{ass_filter_path}'",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-c:a", "copy",
        OUTPUT_SUBTITLED_MASTER
    ]
    subprocess.run(cmd_burn, check=True)
    print(f"Rendered hardcoded subtitle master in {time.time() - t2:.2f}s -> {OUTPUT_SUBTITLED_MASTER}")


def verify_master(master_path):
    """Runs ffprobe on the master file to confirm specs and duration."""
    print(f"\n--- PROBING MASTER FILE: {os.path.basename(master_path)} ---")
    cmd_probe = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of", "json",
        master_path
    ]
    res = subprocess.run(cmd_probe, capture_output=True, text=True, check=True)
    info = json.loads(res.stdout)

    fmt = info.get("format", {})
    streams = info.get("streams", [])

    dur_sec = float(fmt.get("duration", 0))
    dur_min = dur_sec / 60.0
    size_mb = float(fmt.get("size", 0)) / (1024 * 1024)

    print(f"Duration:   {dur_sec:.2f} seconds ({dur_min:.2f} minutes)")
    print(f"File Size:  {size_mb:.1f} MB")
    for s in streams:
        c_type = s.get("codec_type", "unknown")
        c_name = s.get("codec_name", "unknown")
        if c_type == "video":
            w = s.get("width")
            h = s.get("height")
            fps = s.get("r_frame_rate")
            print(f"Video:      {c_name.upper()} {w}x{h} @ {fps} FPS")
        elif c_type == "audio":
            sr = s.get("sample_rate")
            ch = s.get("channels")
            print(f"Audio:      {c_name.upper()} {sr}Hz ({ch} channels / stereo)")

    return dur_sec


def main():
    print("================================================================")
    print("IZHAAN INTELLECT // MASTER FILM ASSEMBLY ENGINE")
    print("================================================================")
    verify_clips()
    assemble_clean_master()
    verify_master(OUTPUT_CLEAN_MASTER)
    assemble_subtitled_master()
    verify_master(OUTPUT_SUBTITLED_MASTER)
    print("================================================================")
    print("MASTER FILM ASSEMBLY COMPLETE!")
    print(f"Primary Master:           {OUTPUT_CLEAN_MASTER}")
    print(f"Hardcoded Subtitle Master:{OUTPUT_SUBTITLED_MASTER}")
    print("================================================================")


if __name__ == "__main__":
    main()
