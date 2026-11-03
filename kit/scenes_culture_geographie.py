"""Storyboard Culture G « La géographie »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
import scenes_culture_fonds_marins as F
from papercut import (PAL, Builder, put, pop, slam, cue)
from scenes import B, memo

P = PAL
num = F.num


def globe_sprite():
    def mk():
        b = Builder(560, 560, seed=901)
        b.ell(280, 280, 240, 240, P["teal"], rough=2)
        b.ell(210, 220, 90, 60, P["mustard"], rough=2, shadow=False)
        b.ell(350, 340, 70, 80, P["mustard"], rough=2, shadow=False)
        return b.done()
    return memo("globe", mk)


def dome_sprite():
    def mk():
        b = Builder(560, 460, seed=902)
        b.rect(60, 250, 500, 430, P["cream"], rough=1.5)
        b.ell(280, 250, 130, 120, P["orange"], rough=1.5)
        b.rect(60, 250, 500, 280, P["cream"], rough=1, shadow=False)
        b.rect(268, 60, 292, 130, P["ink"], rough=1, shadow=False)
        b.rect(248, 80, 312, 100, P["ink"], rough=1, shadow=False)
        for x in (110, 210, 310, 410):
            b.rect(x, 310, x + 40, 420, P["navy"], rough=1, shadow=False)
        return b.done()
    return memo("dome", mk)


def coast_sprite():
    def mk():
        b = Builder(800, 380, seed=903)
        b.poly([(20, 360), (60, 200), (140, 250), (200, 120), (290, 210), (360, 90), (450, 230),
                (540, 140), (620, 260), (710, 170), (780, 360)], P["brick_l"], rough=2)
        b.poly([(0, 300), (800, 300), (800, 380), (0, 380)], P["teal"], rough=2, shadow=False)
        return b.done()
    return memo("coast", mk)


def mountain_sprite():
    def mk():
        b = Builder(760, 560, seed=904)
        b.poly([(20, 540), (380, 40), (740, 540)], P["teal"], rough=2)
        b.poly([(380, 40), (300, 190), (360, 170), (400, 220), (450, 170), (470, 190)], P["cream"], rough=1.5, shadow=False)
        return b.done()
    return memo("mountain", mk)


def clock(h, seed):
    def mk():
        b = Builder(150, 150, seed=seed)
        b.ell(75, 75, 65, 65, P["cream"], rough=1.2)
        b.bar(75, 75, 75, 28, 8, P["ink"], rough=0.6, shadow=False)
        b.bar(75, 75, 75 + 30 * math.sin(h), 75 - 30 * math.cos(h), 8, P["brick"], rough=0.6, shadow=False)
        return b.done()
    return memo(("clock", seed), mk)


def c1(C, T, t):
    slam(C, num("12", 360), 540, 560, T, 0.05)
    pop(C, B("FUSEAUX HORAIRES", 84, "cream", "ink", seed=2), 540, 830, T, 0.5, rot=-2)
    if T >= 2.0:
        pop(C, B("RECORD DU MONDE", 76, "mustard", "ink", seed=3), 540, 1000, T, 2.0, rot=2)
    if T >= 3.5:
        pop(C, B("LA FRANCE", 100, "brick", "cream", seed=4), 540, 300, T, 3.5, rot=-2)
    if T >= 4.8:
        pop(C, B("OUTRE-MER", 80, "teal", "cream", seed=5), 540, 1130, T, 4.8, rot=2)
    for i, (x, y) in enumerate(((180, 1230), (900, 1230), (150, 440), (930, 440))):
        if T >= 1.0 + 0.3 * i:
            pop(C, clock(i * 1.5, 20 + i), x, y, T, 1.0 + 0.3 * i, s=0.7, rot=i * 6 - 9)


def c2(C, T, t):
    pop(C, B("LE VATICAN", 96, "cream", "ink", seed=6), 540, 310, T, 8.1, rot=-2)
    pop(C, dome_sprite(), 540, 640, T, 8.4, s=1.0, rot=2)
    slam(C, num("< 0,5 KM²", 190), 540, 960, T, 9.5)
    if T >= 11.1:
        pop(C, B("À PIED : QUELQUES MINUTES", 58, "orange", "cream", seed=7), 540, 1130, T, 11.2, rot=-2)


def c3(C, T, t):
    pop(C, B("LE CANADA", 96, "cream", "ink", seed=8), 540, 310, T, 14.5, rot=-2)
    pop(C, coast_sprite(), 540, 640, T, 14.9, s=1.1, rot=2)
    pop(C, B("PLUS LONG LITTORAL", 66, "mustard", "ink", seed=9), 540, 900, T, 15.6, rot=-2)
    slam(C, num("200 000 KM", 190), 540, 1060, T, 17.1)
    if T >= 18.6:
        pop(C, B("5 FOIS LE TOUR DE LA TERRE", 54, "brick", "cream", seed=10), 540, 1210, T, 18.7, rot=2)
    if T >= 18.8:
        pop(C, globe_sprite(), 880, 560, T, 18.9, s=0.4, rot=10)


def c4(C, T, t):
    pop(C, B("MONT EVEREST", 90, "cream", "ink", seed=11), 540, 310, T, 21.9, rot=-2)
    pop(C, mountain_sprite(), 540, 700, T, 22.2, s=0.95, rot=0)
    slam(C, num("8 848,86 M", 190), 540, 1060, T, 23.56)
    if T >= 20.8:
        pop(C, B("DEPUIS 2020", 64, "orange", "cream", seed=12), 300, 440, T, 20.85, rot=-4)
    if T >= 26.0:
        pop(C, B("CHINE + NÉPAL", 70, "teal", "cream", seed=13), 540, 1210, T, 26.1, rot=2)


def c5(C, T, t):
    A.cta(C, T, 28.23, 29.4, 32.2, 32.75, 33.7)


SCENES = [(0.0, 6.5, c1), (6.5, 13.4, c2), (13.4, 20.7, c3), (20.7, 28.1, c4), (28.1, 99.0, c5)]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [0.05, 9.5, 17.1, 23.56]
POPS = [32.2, 32.75]
