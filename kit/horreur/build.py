"""Assemble « La gare » : timeline, rendu vidéo (chunks parallèles), musique/sons synthétisés, mixage.
Usage : python3 build.py plan | sheet out.png t1 t2.. | video | audio | all"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

import hscenes as S
import timing
from horror import (W, H, RW, RH, add_grain, font, glitch, smooth, text_c, to_full)

HERE = os.path.dirname(os.path.abspath(__file__))
VOIX = os.environ.get("VOIX_DIR", os.path.join(HERE, "voix"))
FPS = 30
PREFIX = "horreur_gare_"


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p],
                                capture_output=True, text=True).stdout.strip())


def load_seg(k):
    mp3 = os.path.join(VOIX, f"{PREFIX}{k}.mp3")
    txt = open(os.path.join(HERE, "scripts", f"{PREFIX}{k}.txt"), encoding="utf-8").read().split("\n", 1)[1].strip()
    d = dur(mp3)
    words = timing.build_words(os.path.join(VOIX, f"{PREFIX}{k}.json"), txt, d)
    return dict(k=k, mp3=mp3, d=d, words=words, blocks=timing.build_blocks(words))


def wt_un(seg):
    for w in seg["words"]:
        if w["w"].lower() == "un" and ":" in w["punct"]:
            return w["start"]
    return seg["d"] * 0.5


def wt(seg, word, nth=0):
    hits = [w["start"] for w in seg["words"] if w["w"].lower() == word.lower()]
    return hits[nth] if len(hits) > nth else seg["d"] * 0.5


# ---------------------------------------------------------------- timeline
CD, DEATH, REW, TAIL = 3.6, 1.7, 0.9, 0.35


def plan():
    segs = {k: load_seg(k) for k in "1234567" if False} if False else {str(i): load_seg(f"h{i}") for i in range(1, 8)}
    ev = []  # (kind, start, dur, data)
    t = 0.0

    def add(kind, d, **kw):
        nonlocal t
        ev.append(dict(kind=kind, start=t, dur=d, **kw))
        t += d

    s = segs["1"]
    add("speech", s["d"], seg=s, scene="h1")
    add("countdown", CD, scene="h1", seg=s, cards=("LE TUNNEL", "L'ESCALIER"), n=1)
    s = segs["2"]
    add("speech", s["d"] + TAIL, seg=s, scene="bad1")
    add("death", DEATH, label="CHOIX 1 : LE TUNNEL", prev="h1")
    add("rewind", REW, prev="h1", n=1)
    s = segs["3"]
    add("speech", s["d"], seg=s, scene="h3")
    add("countdown", CD, scene="h3", seg=s, cards=("PORTE GRISE", "PORTE ROUGE"), n=2)
    s = segs["4"]
    add("speech", s["d"] + TAIL, seg=s, scene="bad2")
    add("death", DEATH, label="CHOIX 2 : LA PORTE ROUGE", prev="h3")
    add("rewind", REW, prev="h3", n=2)
    s = segs["5"]
    add("speech", s["d"], seg=s, scene="h5")
    add("countdown", CD, scene="h5", seg=s, cards=("PRENDRE LA CLÉ", "DÉCROCHER"), n=3)
    s = segs["6"]
    add("speech", s["d"] + TAIL, seg=s, scene="bad3")
    add("death", DEATH, label="CHOIX 2 : DÉCROCHER", prev="h5")
    add("rewind", REW, prev="h5", n=3)
    s = segs["7"]
    add("speech", s["d"] + 1.2, seg=s, scene="h7")
    return ev, t


# ---------------------------------------------------------------- scènes de segment
def seg_scene(name, t, d, seg):
    """Image float pour la scène `name` au temps local t (le segment dure d)."""
    if name == "h1":
        tc = wt(seg, "Devant")
        if t < tc - 0.3:
            return S.station(t, d)
        if t < tc:
            k = (t - (tc - 0.3)) / 0.3
            return S.station(t, d) * (1 - k) + S.split_choice(t, d) * k
        return S.split_choice(t, d)
    if name == "bad1":
        dead = {}
        for i in range(9):
            tk = d * (0.12 + 0.07 * i)
            dead[i] = 0.0 if t > tk else (flick_out(t, tk))
        k = smooth(t / d, 0.45, 1.0)
        fig = (14.0 - 11.5 * k, smooth(t / d, 0.4, 0.6), 0.0)
        img = S.tunnel(t, d, dead=dead, figure=fig)
        return img
    if name == "h3":
        tc = wt(seg, "En")
        if t < tc - 0.2:
            return S.stairs(t, d, climb=True)
        if t < tc + 0.2:
            k = (t - (tc - 0.2)) / 0.4
            return S.stairs(t, d, climb=True) * (1 - k) + S.doors(t, d) * k
        return S.doors(t, d)
    if name == "bad2":
        return S.red_room(t, d)
    if name == "h5":
        return S.office(t, d, True)
    if name == "bad3":
        return S.bad3(t, d)
    if name == "h7":
        return S.dawn(t, d)
    raise KeyError(name)


def flick_out(t, tk):
    r = tk - t
    return 1.0 if r > 1.0 else (0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 40)))


# ---------------------------------------------------------------- overlays
_CARD = {}


def card(label, num, side):
    k = (label, num, side)
    if k in _CARD:
        return _CARD[k]
    w, h = 470, 170
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=(0, 0, 0, 175), outline=(235, 235, 235, 235), width=4)
    d.ellipse((22, h // 2 - 52, 126, h // 2 + 52), fill=(235, 235, 235, 255))
    d.text((74, h // 2 + 2), str(num), font=font(92), fill=(10, 10, 10, 255), anchor="mm")
    d.text((146 + (w - 146) // 2 - 10, h // 2 + 2), label, font=font(48 if len(label) < 12 else 40), fill=(255, 255, 255, 255), anchor="mm")
    _CARD[k] = im
    return im


def overlay_cards(im, labels, t_on, T):
    k = np.clip((T - t_on) / 0.3, 0, 1)
    if k <= 0:
        return im
    for i, lab in enumerate(labels):
        c = card(lab, i + 1, i)
        x = 40 + i * 530
        y = int(250 - 40 * (1 - k))
        if k < 1:
            c = c.copy()
            c.putalpha(c.getchannel("A").point(lambda v: int(v * k)))
        im.paste(c, (x, y), c)
    return im


def overlay_countdown(im, tl, d):
    n = 3 - int(tl / (d / 3.0))
    n = max(1, min(3, n))
    ph = (tl % (d / 3.0)) / (d / 3.0)
    a = 0.92 - 0.45 * ph
    sz = int(430 + 120 * (1 - ph) ** 2)
    text_c(im, str(n), 540, 1000, sz, (255, 255, 255), 6, (150, 0, 0), a)
    text_c(im, "CHOISIS", 540, 760, 70, (255, 60, 50), 5, (0, 0, 0), 0.95)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    bw = int(760 * (1 - tl / d))
    dd.rounded_rectangle((540 - bw // 2, 1240, 540 + bw // 2, 1256), 8, fill=(220, 30, 30, 230))
    im.paste(ov, (0, 0), ov)
    return im


def subs(im, blocks, T, base=0.0):
    for bi, blk in enumerate(blocks):
        nxt = blocks[bi + 1][0]["start"] if bi + 1 < len(blocks) else 1e9
        t0 = blk[0]["start"]
        t1 = min(blk[-1]["end"] + 0.3, nxt)
        if t0 - 0.02 <= T < t1:
            ai = 0
            for i, w in enumerate(blk):
                if T >= w["start"]:
                    ai = i
            words = [w["w"].upper() for w in blk]
            f = font(88)
            gap = 24
            widths = [f.getlength(x) for x in words]
            tw = sum(widths) + gap * (len(words) - 1)
            x = 540 - tw / 2
            ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            for i, (wd, wi) in enumerate(zip(words, widths)):
                col = (255, 52, 42) if i == ai else (255, 255, 255)
                d.text((x, 1335), wd, font=f, fill=col + (255,), anchor="lm", stroke_width=8, stroke_fill=(0, 0, 0, 255))
                x += wi + gap
            im.paste(ov, (0, 0), ov)
            return im
    return im


# ---------------------------------------------------------------- image finale
def pipeline_cache():
    return {}


def render_frame(T, EV, DTOT):
    rng = np.random.default_rng(int(T * FPS) + 11)
    e = None
    for x in EV:
        if x["start"] <= T < x["start"] + x["dur"]:
            e = x
            break
    if e is None:
        e = EV[-1]
    tl = T - e["start"]
    kind = e["kind"]
    glit = 0.0
    if kind == "speech":
        seg = e["seg"]
        img = seg_scene(e["scene"], tl, e["dur"], seg)
        base = to_full(img)
        if e["scene"] in ("h1", "h3", "h5"):
            lab = None
            tcards = None
            if e["scene"] == "h1":
                lab, tcards = ("LE TUNNEL", "L'ESCALIER"), wt_un(seg)
            elif e["scene"] == "h3":
                lab, tcards = ("PORTE GRISE", "PORTE ROUGE"), wt_un(seg)
            else:
                lab, tcards = ("PRENDRE LA CLÉ", "DÉCROCHER"), wt_un(seg)
            base = overlay_cards(base, lab, tcards, tl)
        if e["scene"] == "h1" and tl < 2.0:  # accroche : texte immédiat
            a = 1.0 if tl < 1.4 else max(0.0, 1 - (tl - 1.4) / 0.4)
            text_c(base, "1 CHEMIN SUR 2", 540, 470, 120, (255, 255, 255), 8, (0, 0, 0), a)
            text_c(base, "TE LAISSE EN VIE", 540, 600, 96, (255, 52, 42), 8, (0, 0, 0), a)
        if e["scene"] == "bad1" and tl > e["dur"] - 0.5:
            glit = 1.0
        if e["scene"] == "bad3" and tl > e["dur"] * 0.55 and tl < e["dur"] * 0.62:
            glit = 1.0
        if e["scene"] == "h7":
            a = smooth(tl, seg["words"][-1]["start"] - 9.0, seg["words"][-1]["start"] - 8.5) if False else 1.0
            ta = wt(seg, "Alors")
            if tl > ta:
                k = min(1.0, (tl - ta) / 0.4)
                text_c(base, "TU AURAIS SURVÉCU ?", 540, 480, 100, (255, 255, 255), 8, (0, 0, 0), k)
        base = subs(base, seg["blocks"], tl)
    elif kind == "countdown":
        seg = e["seg"]
        d_prev = seg["d"]
        img = seg_scene(e["scene"], d_prev + tl, d_prev, seg)
        base = to_full(img)
        base = overlay_cards(base, e["cards"], 0.0, 1.0)
        base = overlay_countdown(base, tl, e["dur"])
    elif kind == "death":
        base = Image.new("RGB", (W, H), (0, 0, 0))
        k = tl / e["dur"]
        a = np.asarray(base).astype(np.float32)
        a[..., 0] = 40 * max(0, 1 - k * 2)
        base = Image.fromarray(a.astype(np.uint8))
        j = int(rng.integers(-8, 9)) if tl < 0.9 else 0
        text_c(base, "MORT", 540 + j, 860 + j // 2, 430, (220, 20, 20), 0)
        text_c(base, e["label"], 540, 1130, 60, (255, 255, 255), 5, (0, 0, 0), min(1, tl / 0.4))
        if tl < 0.12:
            base = Image.blend(base, Image.new("RGB", (W, H), (255, 255, 255)), 1 - tl / 0.12)
        glit = 1.0 if tl < 0.5 else 0.25
    else:  # rewind
        prev = e["prev"]
        evp = [x for x in EV if x["kind"] == "countdown" and x["scene"] == prev][0]
        seg = evp["seg"]
        tend = seg["d"] + evp["dur"]
        tr = tend - (tl / e["dur"]) * min(tend, 6.0)
        img = seg_scene(prev, max(0.0, tr), seg["d"], seg)
        base = to_full(img)
        a = np.asarray(base).astype(np.float32)
        a = a * 0.8 + 25
        a[::6] *= 0.55
        base = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        glit = 1.4
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(ov)
        for i in range(2):
            x0 = 90 + i * 70
            dd.polygon([(x0 + 55, 210), (x0 + 55, 290), (x0, 250)], fill=(255, 255, 255, 235))
        dd.text((300, 250), "REBOBINAGE", font=font(70), fill=(255, 255, 255, 235), anchor="lm")
        base.paste(ov, (0, 0), ov)
    if glit > 0:
        base = glitch(base, rng, glit)
    # flicker global + grain
    fl = 1.0 + 0.04 * math.sin(T * 47) * (1 if rng.random() < 0.3 else 0)
    if fl != 1.0:
        base = Image.fromarray(np.clip(np.asarray(base, np.float32) * fl, 0, 255).astype(np.uint8))
    base = add_grain(base, rng, 11)
    return base


# ---------------------------------------------------------------- rendu vidéo
def render_chunk(args):
    idx, f0, f1, out, EVd, DT = args
    EV = pickle_load(EVd)
    tmp = out + ".part.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(render_frame(f / FPS, EV, DT).tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.rename(tmp, out)
    return idx


def pickle_load(x):
    return x


def video():
    from multiprocessing import Pool
    EV, DT = plan()
    n = int(DT * FPS)
    step = 120
    ch = [(i, s, min(n, s + step), os.path.join(HERE, f"hseg_{i:03d}.mp4"), EV, DT) for i, s in enumerate(range(0, n, step))]
    ch = [c for c in ch if not os.path.exists(c[3])]
    with Pool(2) as pool:
        for i in pool.imap_unordered(render_chunk, ch):
            print("chunk", i, flush=True)
    allc = [os.path.join(HERE, f"hseg_{i:03d}.mp4") for i in range(len(range(0, n, step)))]
    with open(os.path.join(HERE, "hsegs.txt"), "w") as f:
        for c in allc:
            f.write(f"file '{c}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(HERE, "hsegs.txt"),
                    "-c", "copy", os.path.join(HERE, "gare_silent.mp4")], check=True)
    print("silent ok", DT)


# ---------------------------------------------------------------- audio
SR = 48000


def lp(x, hz, order=2):
    from scipy.signal import butter, lfilter
    b, a = butter(order, hz / (SR / 2), "low")
    return lfilter(b, a, x)


def bp(x, lo, hi, order=2):
    from scipy.signal import butter, lfilter
    b, a = butter(order, [lo / (SR / 2), hi / (SR / 2)], "band")
    return lfilter(b, a, x)


def db(x):
    return 10 ** (x / 20)


def place(buf, x, at):
    i = int(at * SR)
    if i >= len(buf) or i < 0:
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i]


def audio():
    EV, DT = plan()
    N = int((DT + 0.5) * SR)
    rng = np.random.default_rng(5)
    tt = np.arange(N) / SR
    # --- nappe angoissante : drones désaccordés + vent + sifflement lent
    drone = (np.sin(2 * np.pi * 55 * tt) + 0.8 * np.sin(2 * np.pi * 55.9 * tt) + 0.5 * np.sin(2 * np.pi * 82.7 * tt + 1.0)
             + 0.35 * np.sin(2 * np.pi * 110.6 * tt))
    drone *= 0.55 + 0.45 * np.sin(2 * np.pi * 0.07 * tt + 0.7) ** 2
    wind = lp(rng.normal(0, 1, N), 380, 2) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * tt + 2.0))
    hiss = np.sin(2 * np.pi * (1480 + 55 * np.sin(2 * np.pi * 0.05 * tt)) * tt) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.09 * tt)) ** 4 * 0.16
    mus = drone * 0.22 + wind * 0.9 + hiss
    # relief final : accord qui s'ouvre sur l'aube
    last = [e for e in EV if e["kind"] == "speech"][-1]
    ts = last["start"]
    env = np.clip((tt - ts) / 4.0, 0, 1) * np.clip((DT - tt) / 3.0 + 0.2, 0, 1)
    pad = sum(np.sin(2 * np.pi * f * tt + p) for f, p in ((220, 0), (277.2, 1), (329.6, 2), (440, 3))) * 0.05 * env
    mus = mus * (1 - 0.55 * np.clip((tt - ts) / 4.0, 0, 1)) + pad
    mus = mus / (np.max(np.abs(mus)) + 1e-9) * db(-17)  # niveau de base (-17 dBFS crête) sous la voix
    sfx = np.zeros(N)
    for e in EV:
        s0, d = e["start"], e["dur"]
        if e["kind"] == "countdown":  # battements de coeur qui s'accélèrent
            t = 0.0
            per = 0.95
            while t < d:
                for off, amp in ((0.0, 1.0), (0.17, 0.7)):
                    n = int(0.18 * SR)
                    x = np.sin(2 * np.pi * (58 - 12 * np.arange(n) / n) * np.arange(n) / SR) * np.exp(-np.arange(n) / SR * 22)
                    place(sfx, x * amp * db(-12), s0 + t + off)
                t += per
                per = max(0.5, per - 0.12)
            # tic de compte à rebours
            for k in range(3):
                n = int(0.06 * SR)
                x = np.sin(2 * np.pi * 1500 * np.arange(n) / SR) * np.exp(-np.arange(n) / SR * 90)
                place(sfx, x * db(-20), s0 + k * d / 3)
        if e["kind"] == "speech" and e["scene"].startswith("bad"):
            # montée de tension avant la mort
            n = int(d * SR)
            tr = np.arange(n) / SR
            f = 120 + 900 * (tr / d) ** 2.2
            ph = 2 * np.pi * np.cumsum(f) / SR
            ris = np.sin(ph) * (tr / d) ** 2.0 * 0.5 + bp(rng.normal(0, 1, n), 800, 5000) * (tr / d) ** 3 * 0.35
            place(sfx, ris * db(-18), s0)
            if e["scene"] == "bad1":  # pas qui se rapprochent
                tpos = d * 0.4
                gap = 1.1
                while tpos < d - 0.2:
                    n2 = int(0.22 * SR)
                    x = lp(rng.normal(0, 1, n2), 300) * np.exp(-np.arange(n2) / SR * 18)
                    place(sfx, x / (np.max(np.abs(x)) + 1e-9) * db(-14) * (0.4 + 0.6 * tpos / d), s0 + tpos)
                    tpos += gap
                    gap = max(0.45, gap - 0.08)
            if e["scene"] == "bad2":  # murmures
                for k in range(26):
                    at = d * 0.45 + k * (d * 0.55 / 26)
                    n2 = int(rng.uniform(0.12, 0.3) * SR)
                    x = bp(rng.normal(0, 1, n2), 900, 3500) * np.hanning(n2)
                    place(sfx, x / (np.max(np.abs(x)) + 1e-9) * db(-20 + 8 * (at - s0 - d * 0.45) / d), s0 + at)
                n2 = int(0.35 * SR)  # claquement de la porte
                x = lp(rng.normal(0, 1, n2), 900) * np.exp(-np.arange(n2) / SR * 14)
                place(sfx, x / (np.max(np.abs(x)) + 1e-9) * db(-8), s0 + d * 0.45)
        if e["kind"] == "speech" and e["scene"] == "h5":
            t = 0.0
            ring_start = wt(e["seg"], "téléphone", 0)
            for rep in range(int((e["dur"] + CD - ring_start) / 2.4) + 1):
                for off in (0.0, 0.5):
                    n = int(0.4 * SR)
                    arr = np.arange(n) / SR
                    x = (np.sin(2 * np.pi * 1400 * arr) + np.sin(2 * np.pi * 2060 * arr)) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 22 * arr)))
                    place(sfx, x * np.hanning(n) * db(-24), s0 + ring_start + rep * 2.4 + off)
        if e["kind"] == "death":
            n = int(1.6 * SR)
            tr = np.arange(n) / SR
            boom = np.sin(2 * np.pi * (46 + 90 * np.exp(-tr * 9)) * tr) * np.exp(-tr * 2.8)
            noise = bp(rng.normal(0, 1, n), 200, 6000) * np.exp(-tr * 4.0)
            clus = sum(np.sin(2 * np.pi * f * tr) for f in (698, 1103, 1517, 2111, 2859)) * np.exp(-tr * 3.2) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tr))
            x = boom * 1.0 + noise * 0.55 + clus * 0.10
            place(sfx, x / np.max(np.abs(x)) * db(-5), s0)
        if e["kind"] == "rewind":
            n = int(e["dur"] * SR)
            tr = np.arange(n) / SR
            f = 2400 * np.exp(-tr * 3.0) + 120
            ph = 2 * np.pi * np.cumsum(f) / SR
            x = np.sin(ph) * 0.4 + bp(rng.normal(0, 1, n), 1500, 7000) * 0.5 * (1 - tr / e["dur"])
            place(sfx, x * np.hanning(n) ** 0.4 * db(-14), s0)
    # voix : segments posés à leurs positions
    voice = np.zeros(N)
    for e in EV:
        if e["kind"] == "speech":
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", e["seg"]["mp3"], "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                 capture_output=True).stdout
            x = np.frombuffer(raw, np.float32).astype(np.float64)
            place(voice, x, e["start"])
    import scipy.io.wavfile as wf
    wf.write(os.path.join(HERE, "voice_raw.wav"), SR, voice.astype(np.float32))
    wf.write(os.path.join(HERE, "music.wav"), SR, (mus + 0).astype(np.float32))
    wf.write(os.path.join(HERE, "sfx.wav"), SR, (sfx * 0.9).astype(np.float32))
    # chaîne voix : compresseur + écho de salle discret, loudnorm 2 passes
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", "voice_raw.wav", "-af",
                        "highpass=f=70,acompressor=threshold=0.1:ratio=3:attack=5:release=120:makeup=2,aecho=0.8:0.55:70|140:0.22|0.12,loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True, cwd=HERE)
    j = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
          f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice_raw.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                    f"[0:a]highpass=f=70,acompressor=threshold=0.1:ratio=3:attack=5:release=120:makeup=2,aecho=0.8:0.55:70|140:0.22|0.12,{ln},aresample=48000[v];"
                    "[1:a]aresample=48000[m];[2:a]aresample=48000[s];"
                    "[v][m][s]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.84:level=disabled[o]",
                    "-map", "[o]", "-c:a", "pcm_s16le", "gare_mix.wav"], check=True, cwd=HERE)
    print("audio ok")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "plan":
        EV, DT = plan()
        for e in EV:
            print(f"{e['start']:7.2f} {e['dur']:6.2f} {e['kind']:10s} {e.get('scene', e.get('prev', ''))}")
        print("total", round(DT, 2))
    elif mode == "sheet":
        EV, DT = plan()
        ts = [float(x) for x in sys.argv[3:]]
        ims = [render_frame(t, EV, DT).resize((270, 480)) for t in ts]
        sh = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims):
            sh.paste(im, (i * 270, 0))
        sh.save(sys.argv[2])
    elif mode == "video":
        video()
    elif mode == "audio":
        audio()
