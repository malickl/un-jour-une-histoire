"""Storyboard Culture G « Les volcans »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
import scenes_culture_fonds_marins as F
from papercut import (PAL, Builder, put, pop, slam, cue, ease_out, clamp)
from scenes import B, memo

P = PAL
num = F.num


def volcano_sprite(seed=901, lava=True):
    def mk():
        b = Builder(520, 380, seed=seed)
        b.poly([(10, 370), (190, 90), (330, 90), (510, 370)], P["brick"], rough=2)
        b.poly([(250, 90), (330, 90), (510, 370), (400, 370)], P["orange"], rough=1.5, shadow=False)
        if lava:
            b.poly([(190, 90), (260, 40), (330, 90)], P["mustard"], rough=1.5, shadow=False)
        return b.done()
    return memo(("volc", seed, lava), mk)


def mountain_sprite():
    def mk():
        b = Builder(300, 300, seed=902)
        b.poly([(10, 290), (150, 20), (290, 290)], P["cream"], rough=2)
        b.poly([(150, 20), (290, 290), (210, 290)], P["teal"], rough=1.5, shadow=False)
        return b.done()
    return memo("mtn", mk)


def sea_sprite():
    def mk():
        b = Builder(900, 260, seed=903)
        b.rect(10, 10, 890, 250, P["teal"], rough=2)
        return b.done()
    return memo("sea", mk)


def cloud_sprite(seed):
    def mk():
        b = Builder(300, 180, seed=seed)
        for x, y, r in [(80, 110, 60), (150, 80, 70), (220, 110, 55)]:
            b.ell(x, y, r, r * 0.8, P["cream"], rough=1.5, shadow=False)
        return b.done()
    return memo(("cloud", seed), mk)


def wave_sprite():
    def mk():
        b = Builder(300, 300, seed=905)
        b.ell(150, 150, 140, 140, P["mustard"], rough=1.5, shadow=False)
        b.ell(150, 150, 105, 105, P["navy"], rough=1.5, shadow=False)
        b.ell(150, 150, 65, 65, P["mustard"], rough=1.5, shadow=False)
        b.ell(150, 150, 30, 30, P["brick"], rough=1.2, shadow=False)
        return b.done()
    return memo("wave", mk)


def flake_sprite(seed):
    def mk():
        b = Builder(120, 120, seed=seed)
        b.ell(60, 60, 40, 40, P["cream"], rough=1.2, shadow=False)
        return b.done()
    return memo(("flake", seed), mk)


def c1(C, T, t):
    slam(C, num("10 000 M", 250), 540, 420, T, 0.1)
    pop(C, B("MAUNA KEA", 84, "cream", "ink", seed=2), 540, 640, T, 2.2, rot=-2)
    pop(C, sea_sprite(), 540, 1130, T, 4.3, s=1.0)
    pop(C, volcano_sprite(), 540, 910, T, 3.2, s=1.1, rot=-1)
    if T >= 4.4:
        pop(C, B("DEPUIS LE FOND", 62, "mustard", "ink", seed=3), 540, 1190, T, 4.5, rot=2)
    if T >= 6.7:
        pop(C, mountain_sprite(), 210, 840, T, 6.8, s=0.7, rot=-4)
        pop(C, B("L'EVEREST", 60, "orange", "cream", seed=4), 210, 1010, T, 6.9, rot=-2)


def c2(C, T, t):
    pop(C, B("1883", 100, "cream", "ink", seed=5), 540, 310, T, 8.0, rot=-2)
    pop(C, volcano_sprite(903, True), 540, 640, T, 8.4, s=0.8, rot=2)
    if T >= 10.0:
        pop(C, B("KRAKATOA", 84, "brick", "cream", seed=6), 540, 880, T, 10.0, rot=-2)
    if T >= 11.8:
        slam(C, num("5 000 KM", 190), 540, 1040, T, 11.85)
    if T >= 13.4:
        pop(C, B("LE BRUIT LE PLUS FORT", 56, "mustard", "ink", seed=7), 540, 1200, T, 13.5, rot=2)
    if T >= 11.8:
        for i in range(3):
            s = 0.4 + ((T - 11.8) * 0.8 + i * 0.35) % 1.1
            put(C, wave_sprite(), 800, 520, s, 0, max(0.0, 1 - s / 1.5))


def c3(C, T, t):
    if T < 21.0:
        pop(C, B("1815", 100, "cream", "ink", seed=8), 280, 310, T, 15.4, rot=-2)
    if 17.1 <= T < 21.0:
        pop(C, B("TAMBORA", 84, "brick", "cream", seed=9), 730, 310, T, 17.1, rot=2)
    pop(C, volcano_sprite(904, True), 540, 800, T, 16.0, s=0.8, rot=-2)
    if 19.2 <= T < 21.0:
        pop(C, B("DES MILLIERS DE MORTS", 56, "orange", "cream", seed=10), 540, 1080, T, 19.3, rot=-2)
    if T >= 21.0:
        pop(C, B("1816", 130, "cream", "ink", seed=11), 540, 310, T, 21.8, rot=2)
        pop(C, B("L'ANNÉE SANS ÉTÉ", 66, "teal", "cream", seed=12), 540, 1080, T, 23.2, rot=-2)
    if T >= 21.0:
        for i in range(8):
            x = 160 + 100 * i
            y = 460 + ((T * 90 + i * 130) % 420)
            put(C, flake_sprite(910 + i), x, y, 0.5, 0, 1)
        pop(C, cloud_sprite(920), 300, 560, T, 21.3, s=1.1)
        pop(C, cloud_sprite(921), 760, 620, T, 21.5, s=1.0)
    if 24.4 <= T < 26.3:
        pop(C, B("NEIGE EN JUIN", 70, "cream", "ink", seed=13), 540, 1190, T, 24.5, rot=2)
    if T >= 26.3:
        pop(C, B("FAMINE", 110, "brick", "cream", seed=14), 540, 1190, T, 26.4, rot=-3)


def c4(C, T, t):
    pop(C, B("YELLOWSTONE", 90, "cream", "ink", seed=15), 540, 310, T, 27.6, rot=-2)
    pop(C, volcano_sprite(906, False), 540, 700, T, 28.2, s=0.9, rot=1)
    if 29.8 <= T < 31.1:
        pop(C, B("SUPERVOLCAN", 80, "brick", "cream", seed=16), 540, 960, T, 29.8, rot=-2)
    if T >= 31.1:
        pop(C, B("DERNIÈRE ÉRUPTION", 58, "mustard", "ink", seed=17), 540, 960, T, 31.2, rot=2)
    if T >= 33.3:
        slam(C, num("640 000 ANS", 160), 540, 1120, T, 33.35)


def c5(C, T, t):
    A.cta(C, T, 34.7, 36.3, 38.7, 39.1, 40.0)


SCENES = [(0.0, 7.8, c1), (7.8, 15.3, c2), (15.3, 27.4, c3), (27.4, 34.4, c4), (34.4, 99.0, c5)]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [0.1, 11.85, 33.35]
POPS = [38.7, 39.1]
