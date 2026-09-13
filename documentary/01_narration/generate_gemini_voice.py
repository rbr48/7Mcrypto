# -*- coding: utf-8 -*-
"""
Studio Voice Generation Engine via Google Gemini TTS ('Charon')
With parallel key rotation across provided AIzaSy keys and fallback.
Normalizes to 48kHz broadcast-grade WAV using FFmpeg DSP filters.
Generates master timeline.json with millisecond precision.
"""
import concurrent.futures
import json
import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(DOC_DIR, "00_script"))

from script_beats import BEATS

# Load API keys from environment variables
_env_keys = os.getenv("GEMINI_API_KEYS", os.getenv("GEMINI_API_KEY", ""))
GEMINI_KEYS = [k.strip() for k in _env_keys.split(",") if k.strip()]

RAW_PCM_DIR = os.path.join(SCRIPT_DIR, "raw_pcm")
WAV_DIR = os.path.join(SCRIPT_DIR, "wav")
os.makedirs(RAW_PCM_DIR, exist_ok=True)
os.makedirs(WAV_DIR, exist_ok=True)

VOICE_NAME = "Charon"  # Authoritative, journalistic documentary tone
MODEL_NAME = "gemini-3.1-flash-tts-preview"


def get_audio_duration(file_path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file_path],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())


def synthesize_gemini(text, pcm_path, key_idx=0):
    from google import genai
    from google.genai import types

    for attempt in range(len(GEMINI_KEYS)):
        current_idx = (key_idx + attempt) % len(GEMINI_KEYS)
        api_key = GEMINI_KEYS[current_idx]
        try:
            client = genai.Client(api_key=api_key)
            config = types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE_NAME)
                    )
                )
            )
            resp = client.models.generate_content(
                model=MODEL_NAME,
                contents=text,
                config=config
            )
            pcm_bytes = b""
            for part in resp.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    pcm_bytes += part.inline_data.data

            if len(pcm_bytes) > 1000:
                with open(pcm_path, "wb") as f:
                    f.write(pcm_bytes)
                return True, current_idx
        except Exception:
            time.sleep(0.3)

    return False, key_idx


def synthesize_edge_fallback(text, wav_path):
    import edge_tts
    import asyncio
    
    async def _edge():
        c = edge_tts.Communicate(text, "en-US-ChristopherNeural", rate="+6%", pitch="+0Hz")
        mp3 = wav_path.replace(".wav", ".mp3")
        await c.save(mp3)
        subprocess.run([
            "ffmpeg", "-y", "-i", mp3, "-ar", "48000", "-ac", "1",
            "-af", "highpass=f=70,dynaudnorm=f=180:g=9:p=0.62",
            wav_path
        ], check=True, capture_output=True)
        if os.path.exists(mp3):
            os.remove(mp3)

    asyncio.run(_edge())


def process_one_beat(job):
    idx, (bid, act, text, pause) = job
    pcm_file = os.path.join(RAW_PCM_DIR, f"{bid}.pcm")
    wav_file = os.path.join(WAV_DIR, f"{bid}.wav")

    if os.path.exists(wav_file) and os.path.getsize(wav_file) > 20000:
        return bid, act, text, pause, get_audio_duration(wav_file), "CACHED"

    success = False
    if not (os.path.exists(pcm_file) and os.path.getsize(pcm_file) > 1000):
        success, key_used = synthesize_gemini(text, pcm_file, idx % len(GEMINI_KEYS))
    else:
        success = True
        key_used = idx % len(GEMINI_KEYS)

    if success and os.path.exists(pcm_file) and os.path.getsize(pcm_file) > 1000:
        subprocess.run([
            "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
            "-i", pcm_file, "-ar", "48000",
            "-af", "highpass=f=70,dynaudnorm=f=180:g=9:p=0.62",
            wav_file
        ], check=True, capture_output=True)
        dur = get_audio_duration(wav_file)
        status = f"GEMINI (Key {key_used})"
    else:
        synthesize_edge_fallback(text, wav_file)
        dur = get_audio_duration(wav_file)
        status = "EDGE-FALLBACK"

    return bid, act, text, pause, dur, status


def main():
    print("=" * 70)
    print(f"PARALLEL SYNTHESIS OF {len(BEATS)} BEATS VIA GOOGLE GEMINI TTS ('{VOICE_NAME}')")
    print(f"Rotating across {len(GEMINI_KEYS)} API keys with 6 concurrent threads...")
    print("=" * 70)

    jobs = list(enumerate(BEATS))
    results_map = {}
    done_count = 0
    t0 = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(process_one_beat, job): job[1][0] for job in jobs}
        for future in concurrent.futures.as_completed(futures):
            bid, act, text, pause, dur, status = future.result()
            results_map[bid] = (bid, act, text, pause, dur, status)
            done_count += 1
            if done_count % 10 == 0 or done_count == len(BEATS):
                print(f"  Progress: {done_count:02d}/{len(BEATS):02d} beats completed ({time.time()-t0:4.1f}s)", flush=True)

    # Reassemble chronological timeline
    timeline = []
    current_time = 0.0

    for bid, act, text, pause in BEATS:
        _, _, _, _, dur, status = results_map[bid]
        timeline.append({
            "id": bid,
            "act": act,
            "start": round(current_time, 3),
            "dur": round(dur, 3),
            "end": round(current_time + dur, 3),
            "pause": pause,
            "text": text,
            "status": status
        })
        current_time += dur + pause

    timeline_path = os.path.join(SCRIPT_DIR, "timeline.json")
    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_runtime_sec": round(current_time, 3),
            "total_runtime_min": round(current_time / 60, 2),
            "beats_count": len(timeline),
            "beats": timeline
        }, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(f"ALL BEATS SYNTHESIZED in {time.time()-t0:.1f}s!")
    print(f"MASTER TIMELINE: {current_time:.1f}s = {current_time/60:.2f} MINUTES ({len(timeline)} BEATS)")
    print(f"Saved to: {timeline_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
