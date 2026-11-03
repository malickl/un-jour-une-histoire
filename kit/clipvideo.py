"""Montage « vraies images » : clips verticaux (clips/out/*.mp4) + voix + gros chiffres + sous-titres.
Usage : python3 clipvideo.py <spec.json> <dossier_clips> <dossier_voix> <dossier_scripts> <fonts_dir> <sortie_silencieuse.mp4>
Spec : {"name": "culture_espace", "scenes": [{"start":0,"end":7.3,"clip":"espace_soleil","texts":[{"t":0.08,"big":"8 MIN 20","sub":""}]}]}"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import timing

W, H, FPS = 1080, 1920, 30
spec_p, CLIPS, VOIX, SCRIPTS, FONTS, OUT = sys.argv[1:7]
spec = json.load(open(spec_p, encoding="utf-8"))
NAME = spec["name"]
mp3 = os.path.join(VOIX, NAME + ".mp3")
DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", mp3],
                           capture_output=True, text=True).stdout.strip())
txt = open(os.path.join(SCRIPTS, NAME + ".txt"), encoding="utf-8").read().strip()
words = timing.build_words(os.path.join(VOIX, NAME + ".json"), txt, DUR)
blocks = timing.build_blocks(words)
_f = {}


def font(s):
    if s not in _f:
        _f[s] = ImageFont.truetype(os.path.join(FONTS, "Anton.ttf"), s)
    return _f[s]


YELLOW, RED = (255, 196, 0), (190, 20, 40)
yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
SHADE = (0.55 + 0.45 * np.minimum(1, np.minimum(yy / 0.25, (1 - yy) / 0.3) ** 0.8)).astype(np.float32)  # bords haut/bas assombris
xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :, None]
SHADE = SHADE * (1 - 0.25 * xx ** 2)


def zoom(im, z):
    px, py = W / 2, H * 0.5
    box = (px - px / z, py - py / z, px + (W - px) / z, py + (H - py) / z)
    return im.transform((W, H), Image.EXTENT, box, Image.BICUBIC)


def draw_text(ov, t, big, sub, T):
    k = np.clip((T - t) / 0.2, 0, 1)
    if k <= 0:
        return
    s = 1.0 + 0.35 * (1 - k) ** 2
    size = int(230 * s) if len(big) <= 9 else int(170 * s)
    d = ImageDraw.Draw(ov)
    a = int(255 * k)
    d.text((W / 2, 640), big, font=font(size), fill=(255, 255, 255, a), anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0, a))
    if sub:
        f = font(62)
        w = f.getlength(sub) + 70
        d.rounded_rectangle((W / 2 - w / 2, 800, W / 2 + w / 2, 890), 10, fill=RED + (int(235 * k),))
        d.text((W / 2, 847), sub, font=f, fill=YELLOW + (a,), anchor="mm")


def draw_subs(ov, T):
    for bi, blk in enumerate(blocks):
        nxt = blocks[bi + 1][0]["start"] if bi + 1 < len(blocks) else 1e9
        t0, t1 = blk[0]["start"], min(blk[-1]["end"] + 0.3, nxt)
        if t0 - 0.02 <= T < t1:
            ai = max([i for i, w in enumerate(blk) if T >= w["start"]] or [0])
            ws = [w["w"].upper() for w in blk]
            f = font(88)
            wd = [f.getlength(x) for x in ws]
            x = W / 2 - (sum(wd) + 24 * (len(ws) - 1)) / 2
            d = ImageDraw.Draw(ov)
            for i, (a, b) in enumerate(zip(ws, wd)):
                d.text((x, 1335), a, font=f, fill=(YELLOW if i == ai else (255, 255, 255)) + (255,), anchor="lm", stroke_width=8, stroke_fill=(0, 0, 0, 255))
                x += b + 24
            return


def scene_frames(sc):
    n = int(round((sc["end"] - sc["start"]) * FPS))
    cmd = ["ffmpeg", "-loglevel", "error", "-stream_loop", "-1", "-i", os.path.join(CLIPS, sc["clip"] + ".mp4"), "-frames:v", str(n),
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for i in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        yield i, np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    p.stdout.close()
    p.wait()


def main():
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
    scenes = spec["scenes"]
    scenes[-1]["end"] = max(scenes[-1]["end"], DUR + 0.3)
    for sc in scenes:
        dur = sc["end"] - sc["start"]
        for i, fr in scene_frames(sc):
            T = sc["start"] + i / FPS
            lt = i / FPS
            im = Image.fromarray((fr.astype(np.float32) * SHADE * 0.92).clip(0, 255).astype(np.uint8))
            z = 1.0 + 0.07 * lt / max(dur, 1) + 0.06 * math.exp(-lt / 0.1)
            im = zoom(im, z)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            for tx in sc.get("texts", []):
                draw_text(ov, tx["t"], tx["big"], tx.get("sub", ""), T)
            draw_subs(ov, T)
            im = im.convert("RGBA")
            im.alpha_composite(ov)
            im = im.convert("RGB")
            if lt < 0.1 and sc["start"] > 0:
                im = Image.blend(im, Image.new("RGB", (W, H), (255, 255, 255)), 0.35 * (1 - lt / 0.1))
            enc.stdin.write(im.tobytes())
    enc.stdin.close()
    enc.wait()
    print("ok", DUR)


main()
