"""Storyboard Culture G « Les animaux »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
import scenes_culture_fonds_marins as F
from papercut import (PAL, Builder, put, bput, pop, slam, slide, cue, ease_out, clamp)
from scenes import B, memo

P = PAL
num = F.num


def whale_sprite():
    def mk():
        b = Builder(700, 380, seed=801)
        b.ell(320, 210, 280, 130, P["teal"], rough=2)
        b.poly([(560, 190), (690, 90), (670, 200), (690, 300), (560, 230)], P["teal"], rough=2)
        b.ell(150, 250, 110, 50, P["cream"], rough=1.5, shadow=False)
        b.ell(130, 180, 12, 12, P["ink"], rough=0.5, shadow=False)
        return b.done()
    return memo("whale", mk)


def octo_sprite():
    def mk():
        b = Builder(560, 560, seed=802)
        b.ell(280, 190, 170, 150, P["brick_l"], rough=2)
        for i, x in enumerate((110, 190, 270, 350, 430)):
            b.bar(x, 300, x + (i - 2) * 25, 500, 34, P["brick_l"], rough=1.5, shadow=False)
        b.ell(220, 190, 24, 28, P["cream"], rough=0.6, shadow=False)
        b.ell(340, 190, 24, 28, P["cream"], rough=0.6, shadow=False)
        return b.done()
    return memo("octo", mk)


def giraffe_sprite(n=7, seed=803):
    def mk():
        b = Builder(480, 900, seed=seed)
        b.ell(250, 90, 85, 60, P["mustard"], rough=1.5)
        b.rect(190, 20, 215, 70, P["brick"], rough=1)
        b.rect(270, 20, 295, 70, P["brick"], rough=1)
        for i in range(n):
            y = 150 + i * 100
            b.rect(170, y, 310, y + 92, P["mustard"] if i % 2 == 0 else P["orange"], rough=1.4)
        b.ell(240, 880, 190, 40, P["mustard"], rough=1.5, shadow=False)
        return b.done()
    return memo(("giraffe", n, seed), mk)


def c1(C, T, t):
    slam(C, num("1 200", 270), 540, 420, T, 0.09)
    pop(C, B("BATTEMENTS PAR MINUTE", 66, "cream", "ink", seed=2), 540, 640, T, 1.0, rot=-2)
    beat = 1 + 0.10 * max(0, math.sin((T - 1.2) * 14))
    pop(C, memo("bird", S.bird_sprite), 540, 900, T, 2.2, s=1.3, rot=-6)
    pop(C, B("LE COLIBRI", 90, "mustard", "ink", seed=3), 540, 1180, T, 3.1, rot=2)
    if T >= 1.2:
        pop(C, memo("heart", lambda: S.heart_sprite("brick")), 880, 780, T, 1.2, s=0.7 * beat, rot=8)


def c2(C, T, t):
    pop(C, B("TOI", 90, "cream", "ink", seed=4), 540, 320, T, 4.9, rot=-2)
    beat = 1 + 0.10 * max(0, math.sin((T - 5.0) * 6))
    pop(C, memo("heart", lambda: S.heart_sprite("brick")), 540, 800, T, 5.0, s=1.3 * beat, rot=-4)
    slam(C, num("70", 260), 540, 520, T, 5.66)
    pop(C, B("PAR MINUTE", 80, "mustard", "ink", seed=5), 540, 1150, T, 6.0, rot=2)


def c3(C, T, t):
    pop(C, B("BALEINE BLEUE", 88, "cream", "ink", seed=6), 540, 310, T, 7.9, rot=-2)
    pop(C, whale_sprite(), 540, 640, T, 8.3, s=1.25, rot=-3)
    slam(C, num("180 KILOS", 200), 540, 920, T, 9.57)
    if T >= 10.9:
        pop(C, B("UN SEUL CŒUR", 76, "brick", "cream", seed=7), 540, 1090, T, 10.95, rot=2)
    if T >= 12.5:
        pop(C, B("2 ADULTES", 76, "orange", "cream", seed=8), 540, 1090, T, 12.5, rot=-2)


def c4(C, T, t):
    pop(C, B("LA PIEUVRE", 90, "cream", "ink", seed=9), 540, 310, T, 13.62, rot=-2)
    pop(C, octo_sprite(), 540, 830, T, 14.0, s=1.2, rot=2)
    if T >= 15.22:
        slam(C, num("3 CŒURS", 220), 540, 480, T, 15.3)
        for i, x in enumerate((420, 540, 660)):
            pop(C, memo("heart", lambda: S.heart_sprite("brick")), x, 800, T, 15.5 + 0.15 * i, s=0.35, rot=i * 8 - 8)
    if T >= 16.2:
        pop(C, B("SANG BLEU", 90, "teal", "cream", seed=10), 540, 1170, T, 16.3, rot=-2)


def c5(C, T, t):
    pop(C, B("LA GIRAFE", 90, "cream", "ink", seed=11), 540, 300, T, 17.3, rot=-2)
    pop(C, giraffe_sprite(), 330, 800, T, 17.6, s=0.95, rot=0)
    slam(C, num("7", 420), 760, 600, T, 18.3)
    pop(C, B("VERTÈBRES", 70, "mustard", "ink", seed=12), 760, 860, T, 18.9, rot=3)
    if T >= 19.78:
        pop(C, B("COMME TOI", 76, "brick", "cream", seed=13), 760, 1010, T, 19.85, rot=-3)
    if T >= 21.15:
        pop(C, B("25 CM CHACUNE", 62, "orange", "cream", seed=14), 700, 1170, T, 21.3, rot=2)


def c6(C, T, t):
    A.cta(C, T, 23.58, 24.75, 27.55, 28.03, 29.0)


SCENES = [(0.0, 4.6, c1), (4.6, 6.8, c2), (6.8, 13.5, c3), (13.5, 17.1, c4), (17.1, 23.5, c5), (23.5, 99.0, c6)]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [0.09, 5.66, 9.57, 15.3, 18.3]
POPS = [27.55, 28.03]
