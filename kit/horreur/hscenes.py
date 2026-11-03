"""Scènes de « La gare » : chacune renvoie une image float (RH,RW,3) déjà étalonnée."""
import math

import numpy as np

from horror import RW, RH, Corridor, grade, paste_figure, smooth

COLD = (0.70, 0.95, 0.88)
RED = (1.0, 0.18, 0.10)
WARM = (1.0, 0.72, 0.42)

_C = {}


def cor(key, w=RW, h=RH, **kw):
    k = (key, w, h)
    if k not in _C:
        _C[k] = Corridor(w, h, **kw)
    return _C[k]


def flick(t, seed, rate=9.0, depth=0.35):
    r = math.sin(t * rate + seed * 3.1) * math.sin(t * rate * 2.7 + seed) + math.sin(t * 31 + seed * 7) * 0.5
    return 1.0 - depth * max(0.0, r) ** 2


def lamps(zs, y, col, inten, sz, t, seed=0, flk=0.3, dead=None):
    out = []
    for i, z in enumerate(zs):
        k = inten * flick(t, i + seed, depth=flk)
        if dead and i in dead:
            k *= dead[i]
        out.append(((0.0, y, z), col, k, sz))
    return out


# ------------------------------------------------------------------ 1. hall de gare
def station(t, d, w=RW, h=RH):
    c = cor("station", w, h, a=3.2, b=1.8, zmax=26, vy=0.47, tile=1.1, seed=1)
    camz = 0.5 * t
    zs = [4 + 6 * i for i in range(7)]
    L = lamps(zs, -1.6, COLD, 5.5, 3.2, t, 0, 0.5)
    # train qui repart : feux rouges qui s'éloignent
    k = max(0.0, 1 - t / 6.0)
    em = ((1.0, 0.1, 0.06), (0.0, 0.2, 0.55 * k + 0.05, 0.12 * k + 0.02)) if k > 0 else None
    img = c.render(t, camz, L, fog=(0.04, 0.07, 0.08), fog_d=0.085, ambient=0.03, end_emit=em)
    return grade(img, (0.88, 1.0, 1.0), 0.95, 0.6)


# ------------------------------------------------------------------ 2. tunnel éclairé / escalier
def tunnel(t, d, w=RW, h=RH, dead=None, camspeed=0.6, figure=None):
    c = cor("tunnel", w, h, a=1.7, b=1.5, zmax=30, vy=0.47, tile=1.0, seed=2)
    camz = camspeed * t
    zs = [3.5 * i + 1.5 for i in range(9)]
    L = lamps(zs, -1.35, (0.75, 1.0, 0.85), 6.5, 2.6, t, 3, 0.4, dead)
    img = c.render(t, camz, L, fog=(0.05, 0.09, 0.08), fog_d=0.07, ambient=0.025)
    if figure:
        zf, alpha, face = figure
        px, py = c.proj(0.0, c.b, zf + camz, camz)
        hp = c.fpx * 1.75 / zf
        paste_figure(img, px + math.sin(t * 2) * 1.5, py, hp, t, alpha, face)
    return grade(img, (0.85, 1.0, 0.95), 0.92, 0.6)


def stairs(t, d, w=RW, h=RH, climb=False):
    c = cor("stairs", w, h, a=1.15, b=1.35, zmax=22, vy=0.40 if not climb else 0.34, tile=0.45, seed=3)
    camz = 0.55 * t
    zs = [6.0, 13.0, 20.0]
    L = lamps(zs, -1.1, (1.0, 0.25, 0.15), 3.0, 2.4, t, 5, 0.7)
    img = c.render(t, camz, L, fog=(0.05, 0.015, 0.015), fog_d=0.10, ambient=0.012)
    # marches : bandes lumineuses
    zz = c.z + camz
    steps = (np.abs(((zz / 0.45) % 1.0) - 0.5) * 2)
    img *= (0.55 + 0.6 * smooth(steps, 0.1, 0.5) * (c.surf == 0) + 0.45 * (c.surf != 0))[..., None]
    return grade(img, (1.0, 0.9, 0.9), 0.9, 0.7)


def split_choice(t, d):
    """Écran partagé : tunnel (gauche) / escalier (droite)."""
    hw = RW // 2
    a = tunnel(t, d, hw, RH)
    b = stairs(t, d, hw, RH)
    img = np.concatenate([a, b], axis=1)
    img[:, hw - 1:hw + 1] = 0.02
    return img


# ------------------------------------------------------------------ 3. couloir aux deux portes
def doors(t, d, w=RW, h=RH):
    c = cor("doors", w, h, a=1.5, b=1.5, zmax=20, vy=0.47, tile=1.0, seed=4)
    camz = 0.35 * t
    L = lamps([3.0, 9.0, 15.0], -1.35, (0.55, 0.85, 0.7), 3.4, 2.4, t, 8, 0.6)
    pulse = 0.7 + 0.3 * math.sin(t * 2.2)
    L.append(((1.2, 0.5, 8.0), RED, 2.6 * pulse, 1.8))  # lueur sous la porte rouge
    breath = 0.5 + 0.5 * math.sin(t * 1.4)
    L.append(((-1.2, 0.5, 8.0), (0.7, 0.8, 0.9), 1.0 * breath, 1.2))  # la porte grise « respire »
    dr = [("R", 8.0, 1.1, (0.55, 0.06, 0.05)), ("L", 8.0, 1.1, (0.45, 0.47, 0.50))]
    img = c.render(t, camz, L, fog=(0.04, 0.06, 0.06), fog_d=0.08, ambient=0.02, doors=dr)
    return grade(img, (1.0, 0.97, 0.95), 0.92, 0.6)


# ------------------------------------------------------------------ 4. pièce rouge
def red_room(t, d):
    c = cor("redroom", a=1.3, b=1.5, zmax=7.0, vy=0.47, tile=0.8, seed=6)
    slam = 0.45 * d
    camz = 0.25 * t
    f = flick(t, 4, 12, 0.6)
    after = t > slam
    L = [((0.0, -1.3, 3.0), RED, (4.0 if not after else 0.5) * f, 2.2),
         ((0.0, -1.3, 6.0), RED, 2.0 * (0.3 if after else 1.0), 2.0)]
    img = c.render(t, camz, L, fog=(0.08, 0.01, 0.01), fog_d=0.16, ambient=0.01)
    if after:
        k = (t - slam) / (d - slam)
        paste_figure(img, RW / 2 + math.sin(t * 3) * 2, c.proj(0, c.b, 7 + camz - 4.8 * smooth(k, 0.1, 1) , camz)[1],
                     c.fpx * 1.75 / max(1.5, 7 - 4.8 * smooth(k, 0.1, 1)), t, 0.95, 0.0)
    out = grade(img, (1.0, 0.9, 0.9), 0.9, 0.7)
    if abs(t - slam) < 0.12:
        out = np.clip(out * 3.0, 0, 1)
    return out


# ------------------------------------------------------------------ 5. bureau abandonné
def office(t, d, ring=True, w=RW, h=RH):
    c = cor("office", w, h, a=2.3, b=1.5, zmax=5.0, vy=0.46, tile=0.8, seed=7)
    L = [((0.5, -0.6, 3.2), WARM, 3.2 * flick(t, 2, 10, 0.55), 2.2),
         ((-1.6, -1.35, 1.5), (0.6, 0.8, 0.9), 0.9 * flick(t, 9, 5, 0.8), 2.5)]
    img = c.render(t, 0.1 * t, L, fog=(0.06, 0.05, 0.04), fog_d=0.09, ambient=0.02)
    # accessoires sur le mur du fond : bureau, téléphone, clé
    from PIL import Image, ImageDraw
    S = 2
    ov = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d_ = ImageDraw.Draw(ov)
    cx, cy = c.vpx * S, c.vpy * S
    u = c.fpx * S / c.zmax  # px par unité à la profondeur du mur
    # étagère
    d_.rectangle((cx + 0.6 * u * 1.0, cy - 1.2 * u, cx + 1.9 * u, cy + 0.2 * u), fill=(30, 22, 18, 255))
    for i in range(4):
        d_.line((cx + 0.6 * u, cy - 1.0 * u + i * 0.35 * u, cx + 1.9 * u, cy - 1.0 * u + i * 0.35 * u), fill=(60, 45, 35, 255), width=3)
    # bureau
    d_.rectangle((cx - 1.9 * u, cy + 0.25 * u, cx + 1.9 * u, cy + 0.42 * u), fill=(58, 40, 28, 255))
    d_.rectangle((cx - 1.8 * u, cy + 0.42 * u, cx - 1.65 * u, cy + 1.5 * u), fill=(40, 28, 20, 255))
    d_.rectangle((cx + 1.65 * u, cy + 0.42 * u, cx + 1.8 * u, cy + 1.5 * u), fill=(40, 28, 20, 255))
    # téléphone (gauche), secoué quand il sonne
    ph = (t % 2.4) < 1.0 if ring else False
    sh = math.sin(t * 60) * 0.03 * u if ph else 0
    px = cx + 1.1 * u + sh
    d_.rounded_rectangle((px - 0.38 * u, cy - 0.02 * u, px + 0.38 * u, cy + 0.27 * u), 10, fill=(14, 14, 16, 255))
    d_.rounded_rectangle((px - 0.42 * u, cy - 0.12 * u, px + 0.42 * u, cy - 0.02 * u), 10, fill=(10, 10, 12, 255))
    if ph and int(t * 8) % 2 == 0:
        d_.ellipse((px - 0.06 * u, cy + 0.08 * u, px + 0.06 * u, cy + 0.2 * u), fill=(255, 40, 30, 255))
    # clé (droite) qui brille
    kx = cx - 1.1 * u
    d_.ellipse((kx - 0.14 * u, cy + 0.03 * u, kx + 0.04 * u, cy + 0.21 * u), outline=(210, 180, 80, 255), width=4)
    d_.rectangle((kx + 0.03 * u, cy + 0.11 * u, kx + 0.36 * u, cy + 0.15 * u), fill=(210, 180, 80, 255))
    ov = ov.resize((w, h), Image.LANCZOS)
    a = np.asarray(ov, np.float32) / 255
    lit = 0.55 + 0.45 * flick(t, 2, 10, 0.55)
    img = img * (1 - a[..., 3:4]) + a[..., :3] * a[..., 3:4] * lit * 0.9
    gl = 0.5 + 0.5 * math.sin(t * 6)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    kx_s, ky_s = c.vpx + 1.2 * u / S * S / S * 1.0, c.vpy + 0.12 * u / S * S / S
    g = np.exp(-(((xx - (c.vpx - 1.0 * u / S * 1.0)) ** 2 + (yy - (c.vpy + 0.12 * u / S)) ** 2) / 120)) * 0.9 * gl
    img += g[..., None] * np.array((1.0, 0.9, 0.5), np.float32)
    return grade(img, (1.0, 0.95, 0.9), 0.92, 0.6)


def office_choice(t, d):
    return office(t, d, True)


def bad3(t, d):
    """Tu te retournes : visage pâle, très près."""
    k = t / d
    if k < 0.55:
        return office(t, d, True)
    c = cor("tunnel", RW, RH, a=1.7, b=1.5, zmax=30, vy=0.47, tile=1.0, seed=2)
    zf = 3.2 - 1.9 * smooth(k, 0.55, 1.0)
    L = lamps([2.0, 6.0], -1.35, (0.6, 0.8, 0.9), 1.6, 2.2, t, 1, 0.9)
    img = c.render(t, 0.0, L, fog=(0.05, 0.06, 0.06), fog_d=0.14, ambient=0.01)
    px, py = c.proj(0.0, c.b, zf, 0.0)
    paste_figure(img, px, py, c.fpx * 1.75 / zf, t, 1.0, face=1.0)
    return grade(img, (0.95, 1.0, 1.0), 0.95, 0.7)


# ------------------------------------------------------------------ 6. aube / sortie
def dawn(t, d):
    c = cor("dawn", a=1.5, b=1.5, zmax=16, vy=0.47, tile=1.0, seed=8)
    k = smooth(t, 0.0, 5.0)
    camz = 0.55 * t
    L = [((0.0, -0.4, 15.5 + 0.0), WARM, 8.0 * k, 5.0)]
    em = ((1.0, 0.82, 0.55), (0.0, 0.1, 0.28 + 0.9 * k * 0.5, 0.55 + 0.45 * k))
    img = c.render(t, camz, L, fog=(0.45 * k + 0.04, 0.32 * k + 0.05, 0.2 * k + 0.05), fog_d=0.10, ambient=0.03 + 0.04 * k,
                   end_emit=em)
    return grade(img, (1.0, 0.97, 0.9), 0.9, 0.5)


def black(t, d):
    return np.zeros((RH, RW, 3), np.float32)
