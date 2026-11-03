"""Moteur « horreur » : rendu pseudo-3D (couloirs en perspective, éclairage ponctuel, brouillard, grain).
Tout est calculé en numpy à 540x960 puis agrandi à 1080x1920."""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
RW, RH = 540, 960
LIGHT = 0.42
HERE = os.path.dirname(os.path.abspath(__file__))


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def _noise(h, w, cell, seed):
    rng = np.random.default_rng(seed)
    n = rng.random((h // cell + 3, w // cell + 3)).astype(np.float32)
    im = Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im, np.float32) / 255


_FOG = {}


def fog_tex(w, h):
    k = (w, h)
    if k not in _FOG:
        a = _noise(h, w * 2, 90, 1) * 0.6 + _noise(h, w * 2, 40, 2) * 0.4
        _FOG[k] = a
    return _FOG[k]


class Corridor:
    """Couloir en perspective à un point de fuite. Coordonnées monde : x droite, y bas, z profondeur."""

    def __init__(self, w, h, a=1.5, b=1.5, zmax=18.0, vx=0.5, vy=0.46, f=0.95, tile=0.9, seed=0):
        self.w, self.h, self.a, self.b, self.zmax, self.tile = w, h, a, b, zmax, tile
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        self.vpx, self.vpy = w * vx, h * vy
        self.fpx = w * f
        dx = (xx - self.vpx) / self.fpx
        dy = (yy - self.vpy) / self.fpx
        adx, ady = np.abs(dx) + 1e-6, np.abs(dy) + 1e-6
        zw = a / adx
        zfc = b / ady
        z = np.minimum(zw, zfc)
        surf = np.where(zw < zfc, np.where(dx < 0, 2, 3), np.where(dy > 0, 0, 1))
        far = z > zmax
        z = np.where(far, zmax, z)
        surf = np.where(far, 4, surf)
        self.dx, self.dy, self.z, self.surf = dx, dy, z.astype(np.float32), surf
        self.X = dx * z
        self.Y = dy * z
        self.rng = np.random.default_rng(seed)
        self.dirt = _noise(h, w, 14, 5 + seed) * 0.5 + _noise(h, w, 5, 9 + seed) * 0.5

    def albedo(self, camz, doors=()):
        s, z, X, Y = self.surf, self.z + camz, self.X, self.Y
        T = self.tile
        gz = np.abs(((z / T) % 1.0) - 0.5) * 2  # 1 au milieu des dalles, 0 aux joints
        line_z = smooth(gz, 0.0, 0.07)
        alb = np.zeros(z.shape + (3,), np.float32)
        # sol
        gx = np.abs(((X / T + 0.5) % 1.0) - 0.5) * 2
        floor = (0.22 + 0.10 * self.dirt) * (0.55 + 0.45 * line_z * smooth(gx, 0, 0.06))
        ceil = (0.16 + 0.08 * self.dirt) * (0.6 + 0.4 * line_z)
        gy = np.abs(((Y / T * 0.8) % 1.0) - 0.5) * 2
        height = (self.b - Y) / (2 * self.b)  # 0 sol ... 1 plafond ? (Y>0 = bas)
        wall = (0.30 + 0.12 * self.dirt) * (0.5 + 0.5 * line_z * smooth(gy, 0, 0.05))
        wall = wall * (0.55 + 0.45 * smooth(1 - height, 0.0, 0.7))
        val = np.where(s == 0, floor, np.where(s == 1, ceil, np.where(s >= 4, 0.05, wall)))
        alb[..., 0] = val * 0.95
        alb[..., 1] = val * 1.0
        alb[..., 2] = val * 1.03
        for d in doors:  # (côté, z, largeur, couleur, éclat)
            side, dz, dw, col = d[0], d[1], d[2], d[3]
            sid = 2 if side == "L" else 3
            m = (s == sid) & (np.abs(z - dz) < dw / 2) & (Y > self.b - 2.3) & (Y < self.b + 0.01)
            panel = 0.85 + 0.15 * smooth(np.abs(((z - dz) / dw * 2) % 1.0 - 0.5) * 2, 0.0, 0.2)
            for c in range(3):
                alb[..., c] = np.where(m, col[c] * panel * (0.6 + 0.5 * self.dirt), alb[..., c])
            hm = (s == sid) & (np.abs(z - (dz + dw * 0.38)) < 0.05) & (np.abs(Y - (self.b - 1.0)) < 0.06)
            alb[hm] = (0.9, 0.8, 0.5)
        return alb

    def render(self, t, camz, lights, fog=(0.02, 0.03, 0.04), fog_d=0.10, ambient=0.02, doors=(), end_emit=None,
               fog_amp=0.5, gloss=0.55):
        alb = self.albedo(camz, doors)
        zw = self.z + camz
        light = np.full(self.z.shape + (3,), ambient, np.float32)
        spec = np.zeros_like(light)
        floor_m = (self.surf == 0)[..., None]
        for (L, col, inten, sz) in lights:
            if inten <= 0.001:
                continue
            lx, ly, lz = L
            d2 = (self.X - lx) ** 2 + (self.Y - ly) ** 2 + (zw - lz) ** 2
            i = inten * LIGHT / (1 + d2 / (sz * sz))
            light += i[..., None] * np.array(col, np.float32)
            g = inten * LIGHT * np.exp(-((self.X - lx) ** 2) / 0.22) / (1 + ((zw - lz) / 1.1) ** 2)
            spec += (g * gloss)[..., None] * np.array(col, np.float32)
        img = alb * light + spec * floor_m
        # émission du fond (porte lumineuse, train...)
        if end_emit is not None:
            col, (cx, cy, rw, rh) = end_emit
            ex = (self.dx * self.zmax)
            ey = (self.dy * self.zmax)
            m = (self.surf == 4) & (np.abs(ex - cx) < rw) & (np.abs(ey - cy) < rh)
            img = np.where(m[..., None], np.array(col, np.float32), img)
        # brouillard
        ft = fog_tex(self.w, self.h)
        off = int(t * 14) % (self.w)
        fn = ft[:, off:off + self.w]
        dens = fog_d * (1 + fog_amp * (fn - 0.5) * 2)
        fa = 1 - np.exp(-self.z * dens)
        img = img * (1 - fa[..., None]) + np.array(fog, np.float32) * fa[..., None] * (0.5 + 0.5 * fn[..., None]) * 0.8
        # halo volumétrique autour des lampes
        yy, xx = np.mgrid[0:self.h, 0:self.w].astype(np.float32)
        for (L, col, inten, sz) in lights:
            lx, ly, lz = L
            zc = lz - camz
            if zc < 0.4 or inten <= 0.001:
                continue
            sx = self.vpx + self.fpx * lx / zc
            sy = self.vpy + self.fpx * ly / zc
            r = self.fpx * 0.55 / zc + 6
            g = np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (r * r))) * inten * 0.30 / (1 + zc * 0.08)
            img += g[..., None] * np.array(col, np.float32)
        return img

    def proj(self, X, Y, Z, camz):
        zc = Z - camz
        return self.vpx + self.fpx * X / zc, self.vpy + self.fpx * Y / zc


def figure_mask(w, h, cx, foot_y, height, t=0.0, face=0.0, sway=1.0):
    """Silhouette humaine (masque 0..1, flou léger). face>0 : visage pâle aux orbites noires."""
    S = 2
    m = Image.new("L", (w * S, h * S), 0)
    d = ImageDraw.Draw(m)
    H0 = height * S
    x0, y0 = cx * S, foot_y * S
    sw = math.sin(t * 5.0) * 0.03 * H0 * sway
    head_r = H0 * 0.065
    neck_y = y0 - H0 * 0.86
    d.ellipse((x0 - head_r + sw * 0.3, neck_y - head_r * 1.7, x0 + head_r + sw * 0.3, neck_y + head_r * 0.3), fill=255)
    d.polygon([(x0 - H0 * 0.17 + sw, neck_y + H0 * 0.02), (x0 + H0 * 0.17 + sw, neck_y + H0 * 0.02),
               (x0 + H0 * 0.12 + sw * 0.5, y0 - H0 * 0.45), (x0 - H0 * 0.12 + sw * 0.5, y0 - H0 * 0.45)], fill=255)
    d.polygon([(x0 - H0 * 0.12, y0 - H0 * 0.46), (x0 + H0 * 0.12, y0 - H0 * 0.46),
               (x0 + H0 * 0.10 + sw, y0), (x0 + H0 * 0.01 + sw, y0), (x0, y0 - H0 * 0.3), (x0 - H0 * 0.01 - sw, y0),
               (x0 - H0 * 0.10 - sw, y0)], fill=255)
    d.polygon([(x0 - H0 * 0.17 + sw, neck_y), (x0 - H0 * 0.23 + sw * 1.4, y0 - H0 * 0.42),
               (x0 - H0 * 0.19 + sw * 1.4, y0 - H0 * 0.42), (x0 - H0 * 0.13 + sw, neck_y + H0 * 0.04)], fill=255)
    d.polygon([(x0 + H0 * 0.17 + sw, neck_y), (x0 + H0 * 0.23 + sw * 1.4, y0 - H0 * 0.42),
               (x0 + H0 * 0.19 + sw * 1.4, y0 - H0 * 0.42), (x0 + H0 * 0.13 + sw, neck_y + H0 * 0.04)], fill=255)
    m = m.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(float(max(0.6, height / 150))))
    pale = None
    if face > 0:
        fm = Image.new("L", (w * S, h * S), 0)
        fd = ImageDraw.Draw(fm)
        fd.ellipse((x0 - head_r + sw * 0.3, neck_y - head_r * 1.7, x0 + head_r + sw * 0.3, neck_y + head_r * 0.3), fill=255)
        pale = fm.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(float(max(1.0, height / 90))))
        eyes = Image.new("L", (w * S, h * S), 0)
        ed = ImageDraw.Draw(eyes)
        ey = neck_y - head_r * 0.7
        for sx in (-0.42, 0.42):
            ed.ellipse((x0 + sw * 0.3 + sx * head_r - head_r * 0.28, ey - head_r * 0.45, x0 + sw * 0.3 + sx * head_r + head_r * 0.28,
                        ey + head_r * 0.55), fill=255)
        ed.rectangle((x0 + sw * 0.3 - head_r * 0.28, neck_y - head_r * 0.05, x0 + sw * 0.3 + head_r * 0.28, neck_y + head_r * 0.12), fill=255)
        eyes = eyes.resize((w, h), Image.LANCZOS)
        return np.asarray(m, np.float32) / 255, np.asarray(pale, np.float32) / 255 * face, np.asarray(eyes, np.float32) / 255
    return np.asarray(m, np.float32) / 255, None, None


def paste_figure(img, cx, foot_y, height, t, alpha=1.0, face=0.0, rim=(0.15, 0.2, 0.25)):
    h, w = img.shape[:2]
    m, pale, eyes = figure_mask(w, h, cx, foot_y, height, t, face)
    m = m * alpha
    img[:] = img * (1 - m[..., None] * 0.97) + np.array(rim, np.float32) * (m[..., None] * 0.10)
    if pale is not None:
        p = pale * alpha
        img[:] = img * (1 - p[..., None]) + np.array((0.42, 0.45, 0.43), np.float32) * p[..., None]
        e = eyes * alpha
        img[:] = img * (1 - e[..., None])


def grade(img, tint=(1, 1, 1), gamma=0.9, vign=0.55, lift=(0.0, 0.0, 0.0)):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.48) / (h / 2)) ** 2
    v = 1 - vign * np.clip(d, 0, 1.6)
    img = img * v[..., None] * np.array(tint, np.float32) + np.array(lift, np.float32)
    img = np.clip(img, 0, 1.5)
    img = img / (1 + 0.55 * np.clip(img - 0.7, 0, None))  # compression douce des hautes lumières
    return np.clip(img, 0, 1) ** gamma


def to_full(img):
    u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(u8).resize((W, H), Image.BICUBIC)


def add_grain(im, rng, amt=14):
    a = np.asarray(im, np.int16)
    g = rng.normal(0, amt, (H // 2, W // 2)).astype(np.float32)
    g = np.kron(g, np.ones((2, 2), np.float32))
    a = a + g[..., None].astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def glitch(im, rng, strength=1.0):
    a = np.asarray(im).copy()
    h = a.shape[0]
    for _ in range(int(8 * strength) + 2):
        y = int(rng.integers(0, h - 80))
        hh = int(rng.integers(8, 90))
        sh = int(rng.integers(-60, 60) * strength)
        a[y:y + hh] = np.roll(a[y:y + hh], sh, axis=1)
    r = np.roll(a[..., 0], int(10 * strength), axis=1)
    b = np.roll(a[..., 2], int(-10 * strength), axis=1)
    a[..., 0], a[..., 2] = r, b
    return Image.fromarray(a)


_F = {}


def font(sz):
    if sz not in _F:
        _F[sz] = ImageFont.truetype(os.path.join(HERE, "fonts", "Anton.ttf"), sz)
    return _F[sz]


def text_c(im, txt, cx, cy, size, fill=(255, 255, 255), stroke=0, stroke_fill=(0, 0, 0), alpha=1.0):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.text((cx, cy), txt, font=font(size), fill=fill + (int(255 * alpha),), anchor="mm", stroke_width=stroke,
           stroke_fill=stroke_fill + (int(255 * alpha),))
    im.paste(ov, (0, 0), ov)
    return im
