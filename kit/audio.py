"""Bruitages très discrets (numpy/scipy) + mixage avec la voix.
Niveaux (pic max) : whoosh -30 dBFS, impact -24 dBFS, pop -26 dBFS. Passe-bas ~6 kHz. Aucune musique."""
import subprocess
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

import importlib
import os

sc = importlib.import_module(os.environ.get("VID_SCENES", "scenes"))

SR = 48000
DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", sys.argv[1]],
                           capture_output=True, text=True).stdout.strip()) if len(sys.argv) > 1 else 52.128


def lp(x, hz=6000, order=4):
    b, a = butter(order, hz / (SR / 2), "low")
    return lfilter(b, a, x)


def db(x):
    return 10 ** (x / 20)


def peak_to(x, dbfs):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * db(dbfs)


def whoosh(rng, length=0.42):
    n = int(SR * length)
    noise = rng.normal(0, 1, n)
    b, a = butter(2, [350 / (SR / 2), 3200 / (SR / 2)], "band")
    x = lfilter(b, a, noise)
    t = np.linspace(0, 1, n)
    env = np.sin(np.pi * t) ** 2.2
    return lp(x * env, 5500)


def impact(length=0.55):
    n = int(SR * length)
    t = np.arange(n) / SR
    f = 42 + 70 * np.exp(-t * 18)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t * 7.5)
    rng = np.random.default_rng(3)
    nz = lp(rng.normal(0, 1, n), 900, 2) * np.exp(-t * 40) * 0.5
    return lp(x + nz, 1500)


def pop(length=0.16):
    n = int(SR * length)
    t = np.arange(n) / SR
    f = 640 - 380 * np.clip(t / 0.06, 0, 1)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return lp(np.sin(ph) * np.exp(-t * 32), 3500)


def place(buf, x, at):
    i = int(at * SR)
    j = min(len(buf), i + len(x))
    if i < 0 or i >= len(buf):
        return
    buf[i:j] += x[: j - i]


def build_sfx(out="sfx.wav"):
    out = os.environ.get("VID_SFX", out)
    buf = np.zeros(int(SR * (DUR + 0.5)), np.float64)
    rng = np.random.default_rng(11)
    # plus de whoosh de transition (demande de Malick) : seulement impacts et pops
    for t in sc.IMPACTS:
        place(buf, peak_to(impact(), -24), t)
    for t in sc.POPS:
        place(buf, peak_to(pop(), -26), t)
    buf = lp(buf, 6000)
    pk = np.max(np.abs(buf))
    if pk > db(-24):  # des évènements proches s'additionnent : on replafonne à -24 dBFS
        buf *= db(-24) / pk
        pk = np.max(np.abs(buf))
    print("pic bruitages : %.1f dBFS" % (20 * np.log10(pk)))
    wavfile.write(out, SR, (np.clip(buf, -1, 1) * 32767).astype(np.int16))


def mix(voice, sfx, out):
    # loudnorm en 2 passes (mesure puis application linéaire) pour tenir I=-14 / TP=-1.5
    import json
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", voice, "-af",
                        "acompressor=threshold=0.125:ratio=2.5:attack=5:release=90:makeup=1.6,loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", voice, "-i", sfx, "-filter_complex",
        f"[0:a]acompressor=threshold=0.125:ratio=2.5:attack=5:release=90:makeup=1.6,{ln},aresample=48000[v];"
        "[1:a]aresample=48000[s];"
        "[v][s]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.82:level=disabled[m]",
        "-map", "[m]", "-c:a", "pcm_s16le", out], check=True)


if __name__ == "__main__":
    build_sfx()
    mix(sys.argv[1], os.environ.get("VID_SFX", "sfx.wav"), sys.argv[2])
    print("mix ok")
