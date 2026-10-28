"""Moteur « papier découpé » : fond papier, pièces découpées (bords irréguliers, ombre, texture),
animations (pop, slam, glissé), effet stop-motion (boil)."""
import math
import os
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

PAL = dict(
    navy=(27, 42, 74), navy_l=(44, 64, 108), navy_d=(16, 26, 50),
    cream=(243, 230, 203), cream_d=(222, 205, 170),
    orange=(238, 122, 40), mustard=(229, 180, 66),
    brick=(172, 66, 48), brick_l=(196, 94, 66), teal=(32, 124, 124), teal_l=(60, 160, 150),
    ink=(20, 28, 52), white=(252, 247, 236), grey=(120, 128, 150),
)
SS = 2  # sur-échantillonnage pour des bords lisses


@lru_cache(maxsize=64)
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, f"{name}.ttf"), int(size))


# ------------------------------------------------------------------ fond papier
def make_bg():
    rng = np.random.default_rng(7)
    base = np.zeros((H, W, 3), np.float32)
    base[:] = PAL["navy"]
    n = rng.random((H // 40 + 2, W // 40 + 2)).astype(np.float32)
    n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    base *= (0.88 + 0.24 * n)[..., None]
    base += rng.normal(0, 4.5, (H, W)).astype(np.float32)[..., None]
    yy, xx = np.mgrid[0:H, 0:W]
    d = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    base *= (1 - 0.20 * np.clip(d, 0, 1.5))[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    dr = ImageDraw.Draw(img, "RGBA")
    for _ in range(450):
        x, y = int(rng.integers(0, W)), int(rng.integers(0, H))
        l, a = int(rng.integers(4, 11)), float(rng.uniform(0, math.pi))
        dr.line((x, y, x + l * math.cos(a), y + l * math.sin(a)), fill=(255, 255, 255, 13), width=1)
    return img


# ------------------------------------------------------------------ formes (listes de points)
def _jit(rnd, j):
    return rnd.uniform(-j, j)


def rpoly(pts, j=1.4, sub=18, seed=0):
    """Polygone aux bords « coupés aux ciseaux » : arêtes subdivisées + léger tremblement."""
    rnd = random.Random(seed)
    out = []
    for i, (x0, y0) in enumerate(pts):
        x1, y1 = pts[(i + 1) % len(pts)]
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / sub))
        for k in range(n):
            t = k / n
            out.append((x0 + (x1 - x0) * t + _jit(rnd, j), y0 + (y1 - y0) * t + _jit(rnd, j)))
    return out


def rect_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rrect_pts(x0, y0, x1, y1, r, n=8):
    pts = []
    for cx, cy, a0 in [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]:
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ell_pts(cx, cy, rx, ry, n=44, a0=0, a1=360):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def burst_pts(cx, cy, r_out, r_in, n=14, rot=0):
    pts = []
    for k in range(n * 2):
        r = r_out if k % 2 == 0 else r_in
        a = math.radians(rot + 180 * k / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def bar_pts(x0, y0, x1, y1, wd):
    a = math.atan2(y1 - y0, x1 - x0)
    dx, dy = math.sin(a) * wd / 2, -math.cos(a) * wd / 2
    return [(x0 + dx, y0 + dy), (x1 + dx, y1 + dy), (x1 - dx, y1 - dy), (x0 - dx, y0 - dy)]


# ------------------------------------------------------------------ constructeur de sprite
class Builder:
    """Compose une image RGBA à partir de pièces de papier superposées."""

    def __init__(self, w, h, seed=0, shadow=True):
        self.w, self.h, self.seed, self.shadow = int(w), int(h), seed, shadow
        self.img = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        self.k = 0

    def poly(self, pts, color, holes=None, rough=1.3, shadow=None, tex=0.05):
        self.k += 1
        rnd_seed = self.seed * 131 + self.k
        pts = rpoly(pts, j=rough, seed=rnd_seed) if rough else pts
        all_pts = list(pts)
        x0 = int(max(0, min(p[0] for p in all_pts) - 14)); y0 = int(max(0, min(p[1] for p in all_pts) - 14))
        x1 = int(min(self.w, max(p[0] for p in all_pts) + 14)); y1 = int(min(self.h, max(p[1] for p in all_pts) + 14))
        if x1 <= x0 or y1 <= y0:
            return self
        cw, ch = x1 - x0, y1 - y0
        m = Image.new("L", (cw * SS, ch * SS), 0)
        d = ImageDraw.Draw(m)
        d.polygon([((x - x0) * SS, (y - y0) * SS) for x, y in pts], fill=255)
        for hp in holes or []:
            d.polygon([((x - x0) * SS, (y - y0) * SS) for x, y in hp], fill=0)
        m = m.resize((cw, ch), Image.LANCZOS)
        region = self.img.crop((x0, y0, x1, y1))
        if (self.shadow if shadow is None else shadow):
            sh = ImageChops.offset(m, 3, 5).filter(ImageFilter.GaussianBlur(3.2)).point(lambda v: int(v * 0.42))
            blk = Image.new("RGBA", (cw, ch), (8, 12, 26, 255))
            blk.putalpha(sh)
            region = Image.alpha_composite(region, blk)
        rng = np.random.default_rng(rnd_seed)
        arr = np.empty((ch, cw, 3), np.float32)
        arr[:] = color
        arr *= (1 + rng.normal(0, tex, (ch, cw)).astype(np.float32))[..., None]
        arr += (rng.random((ch, cw)).astype(np.float32) * 6 - 3)[..., None]
        fill = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
        fill.putalpha(m)
        region = Image.alpha_composite(region, fill)
        rim = ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(3)))
        hl = Image.new("RGBA", (cw, ch), (255, 250, 235, 255))
        hl.putalpha(rim.point(lambda v: int(v * 0.30)))
        region = Image.alpha_composite(region, hl)
        self.img.paste(region, (x0, y0))
        return self

    def rect(self, x0, y0, x1, y1, color, **kw):
        return self.poly(rect_pts(x0, y0, x1, y1), color, **kw)

    def rrect(self, x0, y0, x1, y1, r, color, **kw):
        return self.poly(rrect_pts(x0, y0, x1, y1, r), color, **kw)

    def ell(self, cx, cy, rx, ry, color, **kw):
        return self.poly(ell_pts(cx, cy, rx, ry), color, **kw)

    def ring(self, cx, cy, ro, ri, color, **kw):
        return self.poly(ell_pts(cx, cy, ro, ro), color, holes=[ell_pts(cx, cy, ri, ri)], **kw)

    def bar(self, x0, y0, x1, y1, wd, color, **kw):
        return self.poly(bar_pts(x0, y0, x1, y1, wd), color, **kw)

    def text(self, x, y, txt, fname, size, color, anchor="mm", spacing=0):
        d = ImageDraw.Draw(self.img)
        d.text((x, y), txt, font=font(fname, size), fill=color + (255,), anchor=anchor)
        return self

    def done(self):
        return self.img


def text_size(txt, fname, size):
    b = font(fname, size).getbbox(txt)
    return b[2] - b[0], b[3] - b[1]


def banner(txt, size=110, fill="cream", ink="navy", fname="Anton", padx=46, pady=26, seed=1, lines=None):
    """Bandeau de papier déchiré avec un titre."""
    parts = lines or [txt]
    tw = max(text_size(p, fname, size)[0] for p in parts)
    lh = int(size * 1.08)
    w = tw + padx * 2 + 30
    h = lh * len(parts) + pady * 2 + 14
    b = Builder(w, h, seed=seed)
    pts = [(14, 20), (w - 12, 10), (w - 16, h - 12), (10, h - 20)]
    b.poly(pts, PAL[fill], rough=2.6, tex=0.045)
    cy = 14 + pady + lh / 2 + 4
    for i, p in enumerate(parts):
        b.text(w / 2, cy + i * lh, p, fname, size, PAL[ink])
    return b.done()


# ------------------------------------------------------------------ animation
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease_out(p):
    return 1 - (1 - clamp(p)) ** 3


def back(p, s=1.9):
    p = clamp(p)
    return 1 + (s + 1) * (p - 1) ** 3 + s * (p - 1) ** 2


def cue(T, t0, d=0.35):
    return clamp((T - t0) / d)


CAM = [0.0, 0.0]  # tremblement d'écran
_TCACHE = {}


def boil(T, key, amp=1.8):
    """Micro-tremblement image par image (10 i/s), valeurs quantifiées pour réutiliser le cache."""
    r = random.Random(int(T * 10) * 7919 + key * 104729)
    return r.choice((-1, 0, 1)) * amp, r.choice((-1, 0, 1)) * amp, r.choice((-0.5, 0, 0.5))


def _xform(spr, s, rot):
    k = (id(spr), round(s, 3), round(rot, 1))
    im = _TCACHE.get(k)
    if im is None:
        im = spr
        if abs(s - 1) > 1e-3:
            im = im.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.BILINEAR)
        if abs(rot) > 1e-3:
            im = im.rotate(rot, resample=Image.BILINEAR, expand=True)
        if len(_TCACHE) > 1500:
            _TCACHE.clear()
        _TCACHE[k] = im
    return im


def squash(spr, sx, sy):
    k = ("sq", id(spr), round(sx, 2), round(sy, 2))
    im = _TCACHE.get(k)
    if im is None:
        im = spr.resize((max(2, int(spr.width * sx)), max(2, int(spr.height * sy))), Image.BILINEAR)
        _TCACHE[k] = im
    return im


def put(C, spr, x, y, s=1.0, rot=0.0, a=1.0, cam=True):
    if s <= 0.01 or a <= 0.01:
        return
    im = _xform(spr, s, rot)
    if a < 0.995:
        al = im.getchannel("A").point(lambda v: int(v * a))
        im = im.copy()
        im.putalpha(al)
    if cam:
        x, y = x + CAM[0], y + CAM[1]
    C.paste(im, (int(x - im.width / 2), int(y - im.height / 2)), im)


def bput(C, spr, x, y, T, s=1.0, rot=0.0, a=1.0, amp=1.8):
    dx, dy, dr = boil(T, id(spr) % 997, amp)
    put(C, spr, x + dx, y + dy, s, rot + dr, a)


def pop(C, spr, x, y, T, t0, s=1.0, rot=0.0, a=1.0, d=0.34):
    p = cue(T, t0, d)
    if p <= 0:
        return
    bput(C, spr, x, y, T, s * back(p), rot, a * clamp(p * 3))


def slam(C, spr, x, y, T, t0, s=1.0, rot=0.0, a=1.0):
    p = cue(T, t0, 0.2)
    if p <= 0:
        return
    bput(C, spr, x, y, T, s * (2.3 - 1.3 * ease_out(p)), rot, a * clamp(p * 3))


def slide(C, spr, p0, p1, T, t0, d=0.4, s=1.0, rot=0.0, a=1.0, boil_amp=1.6):
    p = cue(T, t0, d)
    if p <= 0:
        return
    e = ease_out(p)
    bput(C, spr, p0[0] + (p1[0] - p0[0]) * e, p0[1] + (p1[1] - p0[1]) * e, T, s, rot, a, boil_amp)


def shake(T, t0, d=0.35, amp=16):
    """Retourne le décalage d'écran pour un impact à t0."""
    p = (T - t0) / d
    if p < 0 or p > 1:
        return 0.0, 0.0
    k = (1 - p) * amp
    return math.sin(T * 90) * k, math.cos(T * 71) * k * 0.7
