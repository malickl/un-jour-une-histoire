"""Storyboard Culture G « L'espace »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
import scenes_culture_fonds_marins as F
from papercut import (PAL, Builder, put, bput, pop, slam, slide, cue, ease_out, clamp)
from scenes import B, memo

P = PAL
num = F.num


def sun():
    return memo("sun", S.sun_sprite)


def moon():
    return memo("moon", A.moon_sprite)


def earth_sprite():
    def mk():
        b = Builder(300, 300, seed=701)
        b.ell(150, 150, 110, 110, P["teal"], rough=1.6)
        b.poly([(90, 110), (150, 80), (190, 130), (150, 180), (100, 170)], P["mustard"], rough=1.5, shadow=False)
        return b.done()
    return memo("earth", mk)


def venus_sprite():
    def mk():
        b = Builder(300, 300, seed=702)
        b.ell(150, 150, 115, 115, P["mustard"], rough=1.6)
        b.ell(120, 130, 40, 24, P["orange"], rough=1, shadow=False)
        b.ell(190, 190, 34, 20, P["orange"], rough=1, shadow=False)
        return b.done()
    return memo("venus", mk)


def dot(seed, col="cream"):
    def mk():
        b = Builder(80, 80, seed=seed)
        b.ell(40, 40, 22, 22, P[col], rough=1.2)
        return b.done()
    return memo(("dot", seed, col), mk)


def c1(C, T, t):
    slam(C, num("8 MIN 20 S", 215), 540, 380, T, 0.08)
    pop(C, sun(), 190, 800, T, 1.9, s=0.9, rot=-4)
    pop(C, earth_sprite(), 850, 800, T, 2.9, s=0.8)
    k = ease_out(cue(T, 3.1, 1.4))
    pop(C, dot(1, "mustard"), 330 + k * 400, 800, T, 3.1, s=0.5)
    pop(C, B("LA LUMIÈRE DU SOLEIL", 62, "cream", "ink", seed=2), 540, 1100, T, 2.7, rot=-2)


def c2(C, T, t):
    slam(C, num("300 000", 230), 540, 380, T, 5.49)
    pop(C, B("KILOMÈTRES PAR SECONDE", 62, "mustard", "ink", seed=3), 540, 1130, T, 6.0, rot=2)
    for i in range(4):
        x = (T * 900 + i * 300) % 1300 - 100
        put(C, dot(10 + i, "cream"), x, 700 + i * 70, 1.4, 0, 1)


def c3(C, T, t):
    pop(C, sun(), 540, 800, T, 7.5, s=1.6, rot=-3)
    slam(C, num("99,86 %", 250), 540, 380, T, 8.95)
    if T < 13.1:
        pop(C, B("DE LA MASSE DU SYSTÈME SOLAIRE", 56, "cream", "ink", seed=4), 540, 1190, T, 11.0, rot=2)
    else:
        pop(C, B("LES PLANÈTES ? DU DÉTAIL", 64, "brick", "cream", seed=5), 540, 1190, T, 13.2, rot=-2)


def c4(C, T, t):
    pop(C, B("SUR VÉNUS", 100, "cream", "ink", seed=6), 540, 310, T, 15.4, rot=-2)
    pop(C, venus_sprite(), 540, 800, T, 15.6, s=1.5, rot=-4)
    slam(C, num("1 JOUR = 243 J", 125), 540, 560, T, 17.05)
    if T >= 20.3:
        slam(C, num("1 AN = 225 J", 125), 540, 1130, T, 20.95)


def c5(C, T, t):
    pop(C, earth_sprite(), 300, 820, T, 22.2, s=1.1)
    a = clamp((T - 23.4) / 3.0, 0, 1)
    pop(C, moon(), 560 + 120 * a, 820, T, 23.3, s=0.7, rot=-5)
    slam(C, num("+ 3,8 CM", 230), 540, 400, T, 24.55)
    pop(C, B("CHAQUE ANNÉE", 80, "mustard", "ink", seed=7), 540, 1150, T, 22.3, rot=2)


def c6(C, T, t):
    A.cta(C, T, 26.2, 27.9, 30.2, 30.74, 31.6)


SCENES = [(0.0, 5.3, c1), (5.3, 7.3, c2), (7.3, 15.0, c3), (15.0, 22.0, c4), (22.0, 26.0, c5), (26.0, 99.0, c6)]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [0.08, 5.49, 8.95, 17.05, 20.95, 24.55]
POPS = [27.9, 30.2, 30.74]
