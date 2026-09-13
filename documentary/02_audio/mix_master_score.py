# -*- coding: utf-8 -*-
"""
Master Audio Suite & Orchestral Mixing Engine
Concatenates Gemini narration beats, cross-fades 8 cinematic cues from 05_BGM,
applies voice-over sidechain ducking, and renders 48kHz stereo master_soundtrack.wav.
"""
import json
import os
import subprocess
import wave
import numpy as np
import scipy.signal

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR = os.path.dirname(DOC_DIR)

BGM_DIR = os.path.join(PROJECT_DIR, "05_BGM")
WAV_DIR = os.path.join(DOC_DIR, "01_narration", "wav")
TIMELINE_PATH = os.path.join(DOC_DIR, "00_script", "timeline.json")
OUT_VOICE = os.path.join(SCRIPT_DIR, "voiceover_master.wav")
OUT_SCORE = os.path.join(SCRIPT_DIR, "orchestral_bed.wav")
OUT_FINAL = os.path.join(SCRIPT_DIR, "master_soundtrack.wav")

SR = 48000

# BGM Track paths
TRACKS = {
    "MAIN_TITLE": os.path.join(BGM_DIR, "Main Title (Take 1).wav"),
    "THE_TRAP": os.path.join(BGM_DIR, "The Trap (Take 1).wav"),
    "THE_MECHANISM": os.path.join(BGM_DIR, "The Mechanism (Take 1).wav"),
    "HIGH_STAKES": os.path.join(BGM_DIR, "High-Stakes Cyber Score.wav"),
    "FALSE_WARMTH": os.path.join(BGM_DIR, "False Warmth (Take 2).wav"),
    "THE_WOUND": os.path.join(BGM_DIR, "The Wound (Take 1).wav"),
    "GRITTY_STRINGS": os.path.join(BGM_DIR, "Gritty Industrial Remix with Cinematic String Stabs.wav"),
    "CYBER_TENSION": os.path.join(BGM_DIR, "Cyber Thriller Tension.wav"),
    "THE_ROOM": os.path.join(BGM_DIR, "The Room (Take 2).wav"),
}


def read_wav_as_float(path):
    w = wave.open(path, "rb")
    n_frames = w.getnframes()
    ch = w.getnchannels()
    frames = w.readframes(n_frames)
    w.close()
    data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    data = data.reshape(-1, ch)
    if ch == 1:
        data = np.repeat(data, 2, axis=1)
    return data


def write_float_as_wav(path, data, sr=48000):
    # Clip and convert float32 [-1.0, 1.0] to int16
    data_clipped = np.clip(data, -0.98, 0.98)
    int_data = (data_clipped * 32767.0).astype(np.int16)
    w = wave.open(path, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(int_data.tobytes())
    w.close()


def generate_sub_bass_braam(dur_sec=2.5, pitch=44.0):
    n = int(dur_sec * SR)
    t = np.linspace(0, dur_sec, n, endpoint=False)
    f_inst = (pitch + 12.0) * np.exp(-t * 0.9) + (pitch - 6.0)
    phase = 2 * np.pi * np.cumsum(f_inst) / SR
    harmonics = (
        np.sin(phase) +
        0.65 * np.sin(2 * phase) * np.exp(-t * 2.2) +
        0.40 * np.sin(3 * phase) * np.exp(-t * 3.5) +
        0.25 * np.sin(4 * phase) * np.exp(-t * 4.8)
    )
    sat = np.tanh(harmonics * 2.2)
    env = np.exp(-t * 1.6)
    sig = sat * env * 0.72
    shift = int(0.003 * SR)
    sig_l = sig
    sig_r = np.roll(sig, shift)
    sig_r[:shift] = 0
    return np.column_stack((sig_l, sig_r)).astype(np.float32)


def generate_keyboard_typing(dur_sec=1.4, num_clicks=16):
    n = int(dur_sec * SR)
    sig = np.zeros((n, 2), dtype=np.float32)
    clicks = np.linspace(0.04, dur_sec - 0.05, num_clicks) + np.random.uniform(-0.018, 0.018, num_clicks)
    for c in clicks:
        idx = int(c * SR)
        k_len = int(0.016 * SR)
        if idx + k_len < n:
            kt = np.linspace(0, 0.016, k_len, endpoint=False)
            freq = np.random.uniform(2800, 4400)
            k_sig = np.sin(2 * np.pi * freq * kt) * np.exp(-kt * 380)
            k_sig[:int(0.002 * SR)] += np.random.uniform(-0.5, 0.5, int(0.002 * SR))
            pan = np.random.uniform(0.3, 0.7)
            sig[idx:idx+k_len, 0] += k_sig * (1.0 - pan) * 0.35
            sig[idx:idx+k_len, 1] += k_sig * pan * 0.35
    return sig


def generate_odometer_ticks(dur_sec=1.2, num_ticks=22):
    n = int(dur_sec * SR)
    sig = np.zeros((n, 2), dtype=np.float32)
    ticks = np.geomspace(0.03, dur_sec - 0.15, num_ticks)
    for t_val in ticks:
        idx = int(t_val * SR)
        t_len = int(0.010 * SR)
        if idx + t_len < n:
            tt = np.linspace(0, 0.010, t_len, endpoint=False)
            t_sig = np.sin(2 * np.pi * 3200 * tt) * np.exp(-tt * 600)
            sig[idx:idx+t_len, 0] += t_sig * 0.28
            sig[idx:idx+t_len, 1] += t_sig * 0.28
    thud_idx = int((dur_sec - 0.12) * SR)
    thud_len = int(0.12 * SR)
    if thud_idx + thud_len <= n:
        tht = np.linspace(0, 0.12, thud_len, endpoint=False)
        thud = (np.sin(2 * np.pi * 110 * tht) + 0.5 * np.sin(2 * np.pi * 55 * tht)) * np.exp(-tht * 35) * 0.65
        sig[thud_idx:thud_idx+thud_len, 0] += thud
        sig[thud_idx:thud_idx+thud_len, 1] += thud
    return sig


def generate_whoosh(dur_sec=1.0):
    n = int(dur_sec * SR)
    t = np.linspace(0, dur_sec, n, endpoint=False)
    noise = np.random.normal(0, 0.45, n)
    f_center = 180.0 + 2200.0 * (np.sin(np.pi * (t / dur_sec)) ** 2)
    carrier = np.sin(2 * np.pi * np.cumsum(f_center) / SR)
    env = np.sin(np.pi * (t / dur_sec)) ** 2
    w_sig = (noise * 0.45 + carrier * 0.55) * env * 0.48
    pan = np.linspace(0.15, 0.85, n)
    stereo = np.column_stack((w_sig * (1.0 - pan), w_sig * pan)).astype(np.float32)
    return stereo


def generate_glitch_crunch(dur_sec=0.45):
    n = int(dur_sec * SR)
    t = np.linspace(0, dur_sec, n, endpoint=False)
    steps = 6
    chunk_len = n // steps
    sig = np.zeros(n, dtype=np.float32)
    freqs = [180.0, 920.0, 310.0, 1450.0, 240.0, 680.0]
    for i in range(steps):
        s0 = i * chunk_len
        s1 = min(n, (i + 1) * chunk_len)
        ct = t[s0:s1] - t[s0]
        f = freqs[i]
        square = np.sign(np.sin(2 * np.pi * f * ct)) * 0.4
        noise = np.random.uniform(-0.3, 0.3, len(ct))
        sig[s0:s1] = square + noise
    env = np.linspace(1.0, 0.05, n)
    sig = sig * env * 0.42
    stereo = np.column_stack((sig, np.roll(sig, int(0.002 * SR)))).astype(np.float32)
    return stereo


def generate_lock_chime(dur_sec=1.5):
    n = int(dur_sec * SR)
    t = np.linspace(0, dur_sec, n, endpoint=False)
    sig = (
        0.50 * np.sin(2 * np.pi * 1046.5 * t) +
        0.35 * np.sin(2 * np.pi * 1318.5 * t) +
        0.25 * np.sin(2 * np.pi * 1567.9 * t) +
        0.20 * np.sin(2 * np.pi * 2093.0 * t)
    ) * np.exp(-t * 2.6) * 0.65
    stereo = np.column_stack((sig, sig)).astype(np.float32)
    return stereo


def generate_mechanical_relay_click(dur_sec=0.10):
    """
    Simulates a heavy physical electrical relay / circuit breaker latch:
    Primary metallic strike (solenoid impact) followed by contact bounce / latch recoil.
    """
    n = int(dur_sec * SR)
    sig = np.zeros(n, dtype=np.float32)
    
    t1_start = int(0.005 * SR)
    t1_len = int(0.025 * SR)
    if t1_start + t1_len < n:
        tt1 = np.linspace(0, 0.025, t1_len, endpoint=False)
        strike1 = (np.sin(2 * np.pi * 1850.0 * tt1) * 0.7 + 
                   np.sin(2 * np.pi * 3400.0 * tt1) * 0.4 +
                   np.random.uniform(-0.6, 0.6, t1_len) * 0.5) * np.exp(-tt1 * 420.0)
        sig[t1_start:t1_start + t1_len] += strike1 * 0.9

    t2_start = int(0.022 * SR)
    t2_len = int(0.035 * SR)
    if t2_start + t2_len < n:
        tt2 = np.linspace(0, 0.035, t2_len, endpoint=False)
        strike2 = (np.sin(2 * np.pi * 2650.0 * tt2) * 0.5 + 
                   np.sin(2 * np.pi * 4800.0 * tt2) * 0.35 +
                   np.random.uniform(-0.4, 0.4, t2_len) * 0.3) * np.exp(-tt2 * 320.0)
        sig[t2_start:t2_start + t2_len] += strike2 * 0.75

    thud_len = int(0.05 * SR)
    tt_thud = np.linspace(0, 0.05, thud_len, endpoint=False)
    thud = np.sin(2 * np.pi * 140.0 * tt_thud) * np.exp(-tt_thud * 90.0) * 0.45
    sig[:thud_len] += thud

    pan = 0.48
    stereo = np.column_stack((sig * (1.0 - pan), sig * pan)).astype(np.float32)
    return stereo


def generate_geiger_burst(dur_sec=0.75, num_pulses=22):
    """
    Simulates a Geiger counter ionizing risk radiation burst:
    High-density stochastic micro-clicks when systemic risk spikes.
    """
    n = int(dur_sec * SR)
    sig = np.zeros((n, 2), dtype=np.float32)
    
    times = np.random.beta(2.0, 3.0, num_pulses) * (dur_sec - 0.04) + 0.01
    times.sort()
    
    click_dur = 0.003
    click_n = int(click_dur * SR)
    ct = np.linspace(0, click_dur, click_n, endpoint=False)
    
    for t_val in times:
        idx = int(t_val * SR)
        if idx + click_n < n:
            cf = np.random.uniform(4200.0, 7800.0)
            c_wave = np.sin(2 * np.pi * cf * ct) * np.exp(-ct * 1800.0)
            c_wave += np.random.uniform(-0.3, 0.3, click_n) * np.exp(-ct * 2200.0)
            pan = np.random.uniform(0.35, 0.65)
            gain = np.random.uniform(0.4, 0.8)
            sig[idx:idx + click_n, 0] += c_wave * (1.0 - pan) * gain
            sig[idx:idx + click_n, 1] += c_wave * pan * gain
            
    return sig


def generate_pneumatic_swoosh(dur_sec=0.65):
    """
    Pressurized pneumatic air-actuator swoosh for sliding glass HUD panels.
    """
    n = int(dur_sec * SR)
    t = np.linspace(0, dur_sec, n, endpoint=False)
    noise = np.random.normal(0, 0.35, n)
    env = (np.sin(np.pi * (t / dur_sec)) ** 1.8) * np.exp(-t * 2.0)
    carrier_f = 900.0 + 1600.0 * (1.0 - t / dur_sec)
    carrier = np.sin(2 * np.pi * np.cumsum(carrier_f) / SR)
    sig = (noise * 0.7 + carrier * 0.3) * env * 0.55
    pan = np.linspace(0.2, 0.8, n)
    stereo = np.column_stack((sig * (1.0 - pan), sig * pan)).astype(np.float32)
    return stereo


def process_vocal_dsp(voice):
    """
    Applies high-pass filter (75Hz) to clear rumble,
    subtle warmth saturation, and mild broadcast conditioning.
    """
    b, a = scipy.signal.butter(2, 75.0 / (SR / 2.0), btype='highpass')
    v_clean = np.zeros_like(voice)
    v_clean[:, 0] = scipy.signal.lfilter(b, a, voice[:, 0])
    v_clean[:, 1] = scipy.signal.lfilter(b, a, voice[:, 1])
    v_warm = np.tanh(v_clean * 1.12) / 1.05
    return v_warm


def inject_cinematic_sfx(score, total_sec, act_starts):
    total_samples = len(score)

    def add_sfx(sfx_sig, t_sec, gain=1.0):
        s_idx = int(t_sec * SR)
        if s_idx >= total_samples:
            return
        end_idx = min(total_samples, s_idx + len(sfx_sig))
        fit_len = end_idx - s_idx
        score[s_idx:end_idx] += sfx_sig[:fit_len] * gain

    print("   Injecting procedural SFX & Foley layer...")
    # Opening Glitch + Sub-Bass Braam at t=2.0s
    add_sfx(generate_glitch_crunch(0.4), 1.8, 0.6)
    add_sfx(generate_sub_bass_braam(2.8, 42.0), 2.2, 0.85)

    # Liquidation cascade wipe at t=7.5s
    add_sfx(generate_whoosh(1.2), 7.2, 0.6)
    add_sfx(generate_glitch_crunch(0.35), 8.0, 0.5)

    # Systemic contagion cascade Geiger alarm at t=18.0s (FTX/Luna unwind)
    add_sfx(generate_geiger_burst(0.85, 24), 18.0, 0.65)

    # Act 1: HUD panel pneumatic deployment and Kalman relay latch
    add_sfx(generate_pneumatic_swoosh(0.7), 45.0, 0.6)
    add_sfx(generate_mechanical_relay_click(0.12), 72.0, 0.85)

    # Act Transitions: Whoosh + Sub-Bass Braams
    for act_num, st in act_starts.items():
        if st > 5.0:
            add_sfx(generate_whoosh(1.2), st - 0.4, 0.7)
            add_sfx(generate_sub_bass_braam(2.5, 45.0), st, 0.8)

    # Act 2: GIRF matrix slide and threshold breach relay
    add_sfx(generate_pneumatic_swoosh(0.65), 140.0, 0.55)
    # Pesaran & Shin paper reveal at t=158.0s
    add_sfx(generate_lock_chime(1.5), 158.0, 0.7)
    add_sfx(generate_whoosh(0.8), 157.6, 0.5)
    add_sfx(generate_mechanical_relay_click(0.10), 184.0, 0.8)

    # Act 3: FDR slaughter Geiger alarm and lookahead bias panel
    add_sfx(generate_geiger_burst(0.9, 28), 236.0, 0.7)
    add_sfx(generate_pneumatic_swoosh(0.6), 275.0, 0.55)

    # Act 4: Tournament arena pneumatic split & M5 Hedge activation relay
    add_sfx(generate_pneumatic_swoosh(0.7), 310.0, 0.6)
    add_sfx(generate_mechanical_relay_click(0.12), 325.0, 0.9)
    # August 5 Yen carry trade crash alarm & split-screen replay latch
    add_sfx(generate_geiger_burst(1.0, 32), 338.0, 0.75)
    add_sfx(generate_mechanical_relay_click(0.12), 342.0, 0.85)
    # M5 LightGBM +420.69% reveal at t=345.0s
    add_sfx(generate_odometer_ticks(1.4, 24), 344.2, 0.8)
    add_sfx(generate_lock_chime(1.5), 345.6, 0.85)

    # M0 Anomaly pause & low drone at t=372.0s
    add_sfx(generate_sub_bass_braam(3.0, 36.0), 371.5, 0.75)

    # Walk-forward execution relay & Code Forensics typing burst at t=420-422s
    add_sfx(generate_mechanical_relay_click(0.10), 420.0, 0.8)
    add_sfx(generate_keyboard_typing(1.6, 20), 421.8, 0.75)

    # Act 5: Whipsaw turbulence alarm & Schmitt Trigger Hysteresis lock chime/relay
    add_sfx(generate_geiger_burst(0.8, 20), 445.0, 0.65)
    add_sfx(generate_mechanical_relay_click(0.12), 451.8, 0.85)
    add_sfx(generate_lock_chime(1.6), 452.0, 0.8)

    # Fee savings odometer roll and pneumatic accounting panel at t=470-480s
    add_sfx(generate_odometer_ticks(1.3, 20), 469.8, 0.75)
    add_sfx(generate_pneumatic_swoosh(0.65), 480.0, 0.55)

    # Git repo terminal clatter at t=518.0s
    add_sfx(generate_keyboard_typing(1.8, 22), 517.5, 0.8)

    # Final 4D Dissolve resonance at t=540.0s
    add_sfx(generate_sub_bass_braam(3.2, 40.0), 540.0, 0.8)
    add_sfx(generate_lock_chime(2.0), 541.0, 0.8)


def assemble_voiceover(timeline_data):
    total_sec = timeline_data["total_runtime_sec"]
    total_samples = int(math_ceil(total_sec * SR))
    voice_track = np.zeros((total_samples, 2), dtype=np.float32)

    for b in timeline_data["beats"]:
        wav_p = os.path.join(WAV_DIR, f"{b['id']}.wav")
        if os.path.exists(wav_p):
            samples = read_wav_as_float(wav_p)
            start_s = int(b["start"] * SR)
            end_s = min(total_samples, start_s + len(samples))
            fit_len = end_s - start_s
            voice_track[start_s:end_s] += samples[:fit_len]

    return voice_track


def math_ceil(x):
    return int(x) + (1 if x > int(x) else 0)


def build_bgm_score(total_sec, act_starts):
    total_samples = int(math_ceil(total_sec * SR))
    score = np.zeros((total_samples, 2), dtype=np.float32)

    # Act Cues: (track_key, t0, t1, gain, fade_in, fade_out)
    cues = [
        ("MAIN_TITLE", 0.0, min(total_sec, act_starts.get(1, 75.0)), 0.75, 1.0, 3.0),
        ("THE_TRAP", 3.0, min(total_sec, act_starts.get(1, 75.0)), 0.68, 2.0, 3.0),
        ("THE_MECHANISM", act_starts.get(1, 75.0), act_starts.get(2, 165.0), 0.65, 3.0, 3.0),
        ("HIGH_STAKES", act_starts.get(2, 165.0), act_starts.get(3, 255.0), 0.68, 3.0, 3.0),
        ("THE_WOUND", act_starts.get(3, 255.0), act_starts.get(4, 345.0), 0.65, 3.0, 3.0),
        ("GRITTY_STRINGS", act_starts.get(4, 345.0), act_starts.get(5, 435.0), 0.72, 2.5, 3.0),
        ("CYBER_TENSION", act_starts.get(5, 435.0), act_starts.get(6, 520.0), 0.70, 2.5, 3.0),
        ("THE_ROOM", act_starts.get(6, 520.0), total_sec, 0.72, 2.0, 3.0),
        ("MAIN_TITLE", max(0.0, total_sec - 15.0), total_sec, 0.78, 1.0, 2.0),
    ]

    for key, t0, t1, gain, fi, fo in cues:
        p = TRACKS[key]
        if not os.path.exists(p):
            continue
        audio = read_wav_as_float(p)
        dur = t1 - t0
        needed_samples = int(dur * SR)

        if len(audio) < needed_samples:
            repeats = int(needed_samples // len(audio)) + 1
            audio = np.tile(audio, (repeats, 1))

        segment = audio[:needed_samples].copy() * gain

        fi_s = int(fi * SR)
        if fi_s > 0 and fi_s < len(segment):
            fade_curve = np.linspace(0.0, 1.0, fi_s).reshape(-1, 1)
            segment[:fi_s] *= fade_curve

        fo_s = int(fo * SR)
        if fo_s > 0 and fo_s < len(segment):
            fade_curve = np.linspace(1.0, 0.0, fo_s).reshape(-1, 1)
            segment[-fo_s:] *= fade_curve

        s0 = int(t0 * SR)
        s1 = s0 + len(segment)
        if s1 > total_samples:
            segment = segment[:total_samples - s0]
            s1 = total_samples
        score[s0:s1] += segment

    # Inject full cinematic SFX suite
    inject_cinematic_sfx(score, total_sec, act_starts)

    return score


def apply_sidechain_ducking(voice, bgm):
    # Envelope follower on voice track
    voice_mono = np.max(np.abs(voice), axis=1)
    block_size = 256
    n_blocks = len(voice_mono) // block_size
    v_blocks = voice_mono[:n_blocks * block_size].reshape(n_blocks, block_size).max(axis=1)

    # Smooth ducking gain
    duck_gain = np.ones(n_blocks, dtype=np.float32)
    threshold = 0.03
    for i in range(n_blocks):
        if v_blocks[i] > threshold:
            duck_gain[i] = 0.28  # -11 dB attenuation
        else:
            duck_gain[i] = 1.00

    # Smooth transitions (attack/release)
    smoothed_gain = np.copy(duck_gain)
    alpha_atk = 0.15
    alpha_rel = 0.02
    for i in range(1, n_blocks):
        if duck_gain[i] < smoothed_gain[i - 1]:
            smoothed_gain[i] = smoothed_gain[i - 1] * (1 - alpha_atk) + duck_gain[i] * alpha_atk
        else:
            smoothed_gain[i] = smoothed_gain[i - 1] * (1 - alpha_rel) + duck_gain[i] * alpha_rel

    # Interpolate back to sample level
    sample_gain = np.repeat(smoothed_gain, block_size)
    rem = len(bgm) - len(sample_gain)
    if rem > 0:
        sample_gain = np.concatenate([sample_gain, np.full(rem, sample_gain[-1])])
    else:
        sample_gain = sample_gain[:len(bgm)]

    ducked_bgm = bgm * sample_gain.reshape(-1, 1)
    return ducked_bgm


def main():
    if not os.path.exists(TIMELINE_PATH):
        print("Waiting for timeline.json...")
        return

    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        timeline_data = json.load(f)

    total_sec = timeline_data["total_runtime_sec"]
    print("=" * 70)
    print(f"MIXING MASTER SOUNDTRACK FOR RUNTIME: {total_sec:.1f}s ({total_sec/60:.2f} MIN)")
    print("=" * 70)

    # Find act start times from beats
    act_starts = {}
    for b in timeline_data["beats"]:
        act = b["act"]
        if act not in act_starts:
            act_starts[act] = b["start"]

    print("Act Start Timestamps:")
    for act, st in sorted(act_starts.items()):
        print(f"  Act {act}: {st:6.1f}s ({st/60:4.2f}m)")

    print("\n1. Assembling 48kHz voiceover master track...")
    voice = assemble_voiceover(timeline_data)
    print("   Applying vocal DSP (75Hz high-pass rumble filter + broadcast warmth)...")
    voice = process_vocal_dsp(voice)
    write_float_as_wav(OUT_VOICE, voice * 1.15)
    print(f"   Saved voiceover to: {OUT_VOICE}")

    print("\n2. Building 8-track cinematic orchestral bed from 05_BGM...")
    bgm = build_bgm_score(total_sec, act_starts)
    write_float_as_wav(OUT_SCORE, bgm)
    print(f"   Saved orchestral bed to: {OUT_SCORE}")

    print("\n3. Applying automated voice-over sidechain ducking (-11dB)...")
    ducked_bgm = apply_sidechain_ducking(voice, bgm)

    print("\n4. Mastering final soundtrack (Voice + Ducked Orchestral Bed)...")
    master = (voice * 1.15) + (ducked_bgm * 0.95)
    write_float_as_wav(OUT_FINAL, master)
    print(f"   MASTER SOUNDTRACK READY: {OUT_FINAL}")
    print(f"   Duration: {len(master)/SR:.2f}s ({len(master)/SR/60:.2f} min)")
    print("=" * 70)


if __name__ == "__main__":
    main()
