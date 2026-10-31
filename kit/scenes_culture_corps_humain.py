"""Storyboard Culture G « Le corps humain »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
import scenes_culture_fonds_marins as F
from papercut import (PAL, Builder, put, bput, pop, slam, slide, cue, ease_out, clamp)
from scenes import B, memo

P = PAL
num = F.num


def brain_sprite():
    def mk():
        b = Builder(620, 520, seed=601)
        for cx, cy, rx, ry in [(210, 230, 150, 140), (400, 230, 150, 140), (310, 160, 170, 110), (310, 300, 180, 120)]:
            b.ell(cx, cy, rx, ry, P["brick_l"], rough=2)
        for pts in [[(300, 80), (290, 200), (310, 300), (300, 400)], [(150, 200), (220, 240), (180, 320)], [(470, 200), (400, 240), (440, 330)]]:
            for a, c in zip(pts, pts[1:]):
                b.bar(a[0], a[1], c[0], c[1], 10, P["brick"], rough=1.2, shadow=False)
        b.rect(270, 380, 350, 480, P["brick_l"], rough=1.5)
        return b.done()
    return memo("brain", mk)


def bone_sprite(seed=602):
    def mk():
        b = Builder(560, 200, seed=seed)
        b.bar(110, 100, 450, 100, 60, P["cream"], rough=1.2)
        for x in (90, 470):
            b.ell(x, 70, 48, 44, P["cream"], rough=1.2, shadow=False)
            b.ell(x, 130, 48, 44, P["cream"], rough=1.2, shadow=False)
        return b.done()
    return memo(("bone", seed), mk)


def cell_sprite(seed=603):
    def mk():
        b = Builder(200, 200, seed=seed)
        b.ell(100, 100, 80, 80, P["brick"], rough=1.4)
        b.ell(100, 100, 34, 34, P["brick_l"], rough=1, shadow=False)
        return b.done()
    return memo(("cell", seed), mk)


def c1(C, T, t):
    slam(C, num("86 MILLIARDS", 170), 540, 380, T, 0.05)
    pop(C, brain_sprite(), 540, 800, T, 1.2, s=1.15, rot=-3)
    pop(C, B("DE NEURONES", 100, "cream", "ink", seed=2), 540, 1170, T, 2.43, rot=2)


def c2(C, T, t):
    pop(C, B("TON CERVEAU", 84, "cream", "ink", seed=3), 540, 310, T, 4.0, rot=-2)
    pop(C, F.pie_sprite(0.02, 610), 270, 760, T, 5.1, s=0.62)
    pop(C, F.pie_sprite(0.20, 611), 810, 760, T, 7.4, s=0.62)
    slam(C, num("2 %", 200), 270, 1020, T, 5.24)
    pop(C, B("DU POIDS", 56, "mustard", "ink", seed=4), 270, 1180, T, 5.6, rot=-2)
    if T >= 7.4:
        slam(C, num("20 %", 200), 810, 1020, T, 7.49)
        pop(C, B("D'ÉNERGIE", 56, "mustard", "ink", seed=5), 810, 1180, T, 8.0, rot=2)


def c3(C, T, t):
    if T < 12.0:
        pop(C, B("À LA NAISSANCE", 80, "cream", "ink", seed=6), 540, 310, T, 9.2, rot=-2)
        for i, (x, y, r) in enumerate([(330, 720, -12), (700, 800, 10), (430, 920, 4), (760, 1020, -8), (320, 1130, 14)]):
            pop(C, bone_sprite(610 + i), x, y, T, 10.0 + 0.1 * i, s=0.7, rot=r)
        slam(C, num("300 OS", 200), 540, 520, T, 10.83)
    else:
        pop(C, B("ADULTE", 90, "mustard", "ink", seed=7), 540, 330, T, 12.05, rot=2)
        pop(C, bone_sprite(), 540, 820, T, 12.5, s=1.3, rot=-4)
        slam(C, num("206 OS", 230), 540, 560, T, 13.6)
        if T >= 14.65:
            pop(C, B("ILS SE SOUDENT", 80, "brick", "cream", seed=8), 540, 1120, T, 14.84, rot=2)


def c4(C, T, t):
    pop(C, B("CHAQUE SECONDE", 90, "cream", "ink", seed=9), 540, 310, T, 16.2, rot=-2)
    for i in range(9):
        x = 200 + (i % 3) * 340 + (30 if (i // 3) % 2 else 0)
        y = 700 + (i // 3) * 170
        pop(C, cell_sprite(620 + i), x, y, T, 17.6 + 0.08 * i, s=0.75, rot=i * 17 % 40 - 20)
    slam(C, num("2 MILLIONS", 190), 540, 480, T, 18.65)
    pop(C, B("DE GLOBULES ROUGES", 62, "mustard", "ink", seed=10), 540, 1230, T, 19.2, rot=2)


def c5(C, T, t):
    beat = 1 + 0.10 * max(0, math.sin((T - 20.3) * 9))
    pop(C, memo("heart", lambda: S.heart_sprite("brick")), 540, 800, T, 20.4, s=1.5 * beat, rot=-4)
    slam(C, num("100 000", 230), 540, 400, T, 21.24)
    pop(C, B("BATTEMENTS PAR JOUR", 70, "cream", "ink", seed=11), 540, 1160, T, 21.9, rot=2)


def c6(C, T, t):
    A.cta(C, T, 23.89, 25.06, 28.0, 28.46, 29.4)


SCENES = [(0.0, 3.9, c1), (3.9, 9.0, c2), (9.0, 16.1, c3), (16.1, 20.2, c4), (20.2, 23.8, c5), (23.8, 99.0, c6)]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [0.05, 5.24, 7.49, 10.83, 13.6, 18.65, 21.24]
POPS = [25.06, 28.0, 28.46]
