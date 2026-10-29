"""Rendu : fond papier + scène + sous-titres + transitions, en parallèle, puis encodage ffmpeg."""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

import papercut as pc
import importlib
import timing
from papercut import PAL, W, H, Builder, put, clamp, ease_out, cue, back

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = os.environ.get("VID_NAME", "casse_nice_v2")
sc = importlib.import_module(os.environ.get("VID_SCENES", "scenes"))
DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1",
                            os.path.join(HERE, NAME + ".mp3")], capture_output=True, text=True).stdout.strip())
TXT = open(os.path.join(HERE, NAME + ".txt"), encoding="utf-8").read()
WORDS = timing.build_words(os.path.join(HERE, NAME + ".json"), TXT, DUR)
BLOCKS = timing.build_blocks(WORDS)

_BG = None
_SUB = {}


def bg():
    global _BG
    if _BG is None:
        p = os.path.join(HERE, "bg.png")
        if os.path.exists(p):
            _BG = Image.open(p).convert("RGB")
        else:
            _BG = pc.make_bg()
            _BG.save(p)
    return _BG


def sub_sprite(bi, ai):
    k = (bi, ai)
    if k in _SUB:
        return _SUB[k]
    words = [w["w"].upper() for w in BLOCKS[bi]]
    size, gap, f = 92, 26, "Anton"
    widths = [pc.text_size(w, f, size)[0] for w in words]
    tw = sum(widths) + gap * (len(words) - 1)
    w, h = tw + 110, 160
    b = Builder(w, h, seed=bi + 3)
    b.poly([(12, 22), (w - 10, 12), (w - 14, h - 14), (10, h - 22)], PAL["cream"], rough=2.4, tex=0.04)
    x = 55
    for i, (wd, wi) in enumerate(zip(words, widths)):
        col = PAL["orange"] if i == ai else PAL["ink"]
        b.text(x, h / 2 + (-6 if i == ai else 0) + 4, wd, f, size, col, anchor="lm")
        x += wi + gap
    _SUB[k] = b.done()
    return _SUB[k]


def draw_subs(C, T):
    for bi, blk in enumerate(BLOCKS):
        nxt = BLOCKS[bi + 1][0]["start"] if bi + 1 < len(BLOCKS) else DUR
        t0 = blk[0]["start"]
        t1 = min(blk[-1]["end"] + 0.35, nxt)
        if t0 - 0.02 <= T < t1:
            ai = 0
            for i, w in enumerate(blk):
                if T >= w["start"]:
                    ai = i
            spr = sub_sprite(bi, ai)
            p = cue(T, t0 - 0.02, 0.12)
            s = 0.86 + 0.14 * back(p, 1.4)
            put(C, spr, 540, 1345, s, -1.4, clamp(p * 4), cam=False)
            return


def draw_transition(C, T):
    sweeps = getattr(sc, "SWEEPS", [])  # balayages : seulement ceux listés (rares)
    if not sweeps:
        return False
    a, c = sc.sweep_sprites()
    for bnd in sweeps:
        d = 0.60
        if bnd - d / 2 <= T <= bnd + d / 2 + 0.06:
            for spr, lag in ((a, 0.0), (c, 0.06)):
                p = clamp((T - (bnd - d / 2) - lag) / d)
                p = p * p * (3 - 2 * p)  # smoothstep : balayage doux
                x = -1100 + 3300 * p
                put(C, spr, x, 960, 1, 0, 1, cam=False)
            return True
    return False


def scene_at(T):
    for i, (t0, t1, fn) in enumerate(sc.SCENES):
        if t0 <= T < t1:
            return fn, t0
    return sc.SCENES[-1][2], sc.SCENES[-1][0]


def frame(T):
    pc.CAM[0] = pc.CAM[1] = 0.0
    C = bg().copy()
    # pendant la transition, la scène bascule au milieu du balayage
    Ts = T
    fn, t0 = scene_at(Ts)
    fn(C, Ts, Ts - t0)
    pc.CAM[0] = pc.CAM[1] = 0.0
    draw_subs(C, T)
    draw_transition(C, T)
    return C


def render_chunk(args):
    idx, f0, f1, out = args
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(frame(f / FPS).tobytes())
    p.stdin.close()
    p.wait()
    return idx


def preview(times, out="sheet.png", cols=4, scale=0.3):
    ims = [frame(t).resize((int(W * scale), int(H * scale))) for t in times]
    rows = (len(ims) + cols - 1) // cols
    sw, sh = ims[0].size
    sheet = Image.new("RGB", (cols * sw, rows * sh), (0, 0, 0))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * sw, (i // cols) * sh))
    sheet.save(out)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "sheet":
        ts = [float(x) for x in sys.argv[3:]]
        preview(ts, sys.argv[2])
    elif mode == "full":
        from multiprocessing import Pool
        nframes = int(DUR * FPS)
        step = 100
        chunks = [(i, s, min(nframes, s + step), os.path.join(HERE, f"seg_{NAME}_{i:03d}.mp4")) for i, s in enumerate(range(0, nframes, step))]
        bg()
        with Pool(2) as pool:
            for i in pool.imap_unordered(render_chunk, chunks):
                print("chunk", i, "ok", flush=True)
        with open(os.path.join(HERE, f"segs_{NAME}.txt"), "w") as f:
            for c in chunks:
                f.write(f"file '{c[3]}'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(HERE, f"segs_{NAME}.txt"),
                        "-c", "copy", os.path.join(HERE, f"{NAME}_silent.mp4")], check=True)
        print(f"{NAME}_silent.mp4 ok")
