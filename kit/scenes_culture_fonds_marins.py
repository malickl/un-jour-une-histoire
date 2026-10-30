"""Storyboard Culture G « Les fonds marins »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
from papercut import (PAL, Builder, put, bput, pop, slam, slide, cue, ease_out, clamp)
from scenes import B, memo, calendar_sprite, waves_sprite

P = PAL


def pie_sprite(frac, seed=501):
    def mk():
        b = Builder(560, 560, seed=seed)
        cx = cy = 280
        r = 240
        b.ell(cx, cy, r, r, P["navy_l"], rough=1.2)
        a0 = -math.pi / 2
        n = max(8, int(60 * frac))
        pts = [(cx, cy)] + [(cx + r * math.cos(a0 + 2 * math.pi * frac * i / n), cy + r * math.sin(a0 + 2 * math.pi * frac * i / n)) for i in range(n + 1)]
        b.poly(pts, P["orange"], rough=1.2, shadow=False)
        return b.done()
    return memo(("pie", frac), mk)


def qmark():
    return memo("q", lambda: A.cut_text("?", "Anton", 300, P["cream"]))


def mountains_sprite():
    def mk():
        b = Builder(1000, 480, seed=510)
        b.poly([(0, 470), (170, 190), (300, 330), (470, 60), (640, 320), (760, 200), (1000, 470)], P["grey"], rough=2.5)
        b.poly([(470, 60), (420, 140), (470, 120), (520, 150)], P["cream"], rough=1.4, shadow=False)
        b.poly([(170, 190), (140, 250), (180, 235), (210, 260)], P["cream"], rough=1.4, shadow=False)
        b.poly([(760, 200), (735, 245), (765, 238), (790, 255)], P["cream"], rough=1.4, shadow=False)
        return b.done()
    return memo("mnt", mk)


def water_sprite(h=420):
    def mk():
        b = Builder(1180, h + 60, seed=511)
        top = [(x, 40 + 14 * math.sin(x / 150 * 2 * math.pi)) for x in range(0, 1181, 30)]
        b.poly(top + [(1180, h + 60), (0, h + 60)], P["teal"], rough=1.2, shadow=False)
        return b.done()
    return memo(("water", h), mk)


def globe_sprite():
    def mk():
        b = Builder(560, 560, seed=512)
        b.ell(280, 280, 200, 200, P["teal"], rough=1.4)
        b.poly([(150, 200), (230, 150), (290, 210), (250, 290), (170, 280)], P["mustard"], rough=1.5, shadow=False)
        b.poly([(330, 300), (410, 270), (430, 350), (360, 400)], P["mustard"], rough=1.5, shadow=False)
        return b.done()
    return memo("globe", mk)


def ring_sprite(r=260):
    def mk():
        b = Builder(2 * r + 80, 2 * r + 80, seed=513)
        b.ring(r + 40, r + 40, r, r - 16, P["orange"], rough=1.2)
        return b.done()
    return memo(("ring", r), mk)


def num(txt, size, col="orange"):
    return memo(("num", txt, size, col), lambda: A.cut_text(txt, "Anton", size, P[col]))


def c1(C, T, t):
    slam(C, num("27,3 %", 270), 540, 620, T, 0.05)
    pop(C, B("DES FONDS MARINS", 76, "cream", "ink", seed=2), 540, 300, T, 2.5, rot=-2)
    pop(C, B("CARTOGRAPHIÉS", 84, "mustard", "ink", seed=3), 540, 960, T, 3.2, rot=2)
    pop(C, pie_sprite(0.273), 540, 1090, T, 4.2, s=0.62)


def c2(C, T, t):
    pop(C, B("LE RESTE ?", 110, "cream", "ink", seed=4), 540, 330, T, 5.73, rot=-2)
    pop(C, pie_sprite(0.273), 540, 800, T, 5.8, s=1.0)
    pop(C, qmark(), 540, 880, T, 6.83, s=1.0, rot=-6)
    slam(C, B("MYSTÈRE", 110, "brick", "cream", seed=5), 540, 1170, T, 7.02, rot=2)


def c3(C, T, t):
    pop(C, calendar_sprite("EN", "2017"), 540, 640, T, 8.19, s=1.15, rot=-3)
    pop(C, B("SEULEMENT", 90, "cream", "ink", seed=6), 540, 330, T, 9.2, rot=2)
    slam(C, num("6 %", 260), 540, 1050, T, 9.93)


def c4(C, T, t):
    slam(C, num("+ DE 70 %", 200), 540, 400, T, 11.98)
    pop(C, pie_sprite(0.273, 502), 540, 860, T, 10.95, s=0.9)
    pop(C, B("INCONNUS", 100, "cream", "ink", seed=7), 540, 1180, T, 13.48, rot=-2)


def c5(C, T, t):
    pop(C, B("LA PLUS LONGUE", 84, "cream", "ink", seed=8), 540, 310, T, 15.94, rot=-2)
    pop(C, B("CHAÎNE DE MONTAGNES", 64, "mustard", "ink", seed=9), 540, 430, T, 16.27, rot=2)
    pop(C, mountains_sprite(), 540, 850, T, 15.3, s=1.0)
    if T >= 17.5:
        k = ease_out(cue(T, 17.5, 0.8))
        put(C, water_sprite(300), 540, 1010 + (1 - k) * 300, 1.0, 0, 1)
    slam(C, B("DORSALE OCÉANIQUE", 70, "brick", "cream", seed=10), 540, 1170, T, 17.94, rot=2)


def c6(C, T, t):
    pop(C, globe_sprite(), 540, 760, T, 19.5, s=1.1)
    pop(C, ring_sprite(), 540, 760, T, 22.65, s=1.1)
    slam(C, num("65 000 KM", 190), 540, 340, T, 20.56)
    pop(C, B("1,5 TOUR DE LA TERRE", 62, "cream", "ink", seed=11), 540, 1180, T, 22.65, rot=2)


def c7(C, T, t):
    slam(C, num("90 %", 260), 540, 360, T, 25.38)
    pop(C, mountains_sprite(), 540, 880, T, 25.0, s=1.0)
    put(C, water_sprite(420), 540, 960, 1.0, 0, 1)
    pop(C, B("SOUS L'EAU", 100, "teal_l", "ink", seed=12), 540, 540, T, 26.7, rot=2)
    if T >= 28.28:
        pop(C, B("2 500 M", 100, "cream", "ink", seed=13), 540, 1040, T, 28.28, rot=-2)
        pop(C, B("DE PROFONDEUR", 64, "mustard", "ink", seed=14), 540, 1170, T, 29.1, rot=2)


def c8(C, T, t):
    A.cta(C, T, 30.62, 31.78, 34.58, 35.14, 35.9)


SCENES = [
    (0.0, 5.5, c1), (5.5, 8.0, c2), (8.0, 10.9, c3), (10.9, 14.7, c4), (14.7, 19.3, c5),
    (19.3, 24.8, c6), (24.8, 30.5, c7), (30.5, 99.0, c8),
]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [0.05, 9.93, 11.98, 17.94, 20.56, 25.38]
POPS = [31.78, 34.58, 35.14]
