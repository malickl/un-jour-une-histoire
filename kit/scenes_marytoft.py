"""Storyboard « Mary Toft, la femme qui accouchait de lapins, 1726 »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
from papercut import (PAL, Builder, put, bput, pop, slam, slide, cue, ease_out, clamp, rrect_pts, ell_pts, burst_pts)
from scenes import B, memo, calendar_sprite, person_sprite, doc_sprite

P = PAL


def rabbit_sprite(col="cream", seed=401):
    def mk():
        b = Builder(300, 400, seed=seed)
        b.poly(ell_pts(120, 80, 22, 70), P[col], rough=1)
        b.poly(ell_pts(176, 84, 22, 70), P[col], rough=1)
        b.poly(ell_pts(124, 90, 9, 50), P["brick_l"], rough=0.5, shadow=False)
        b.poly(ell_pts(172, 94, 9, 50), P["brick_l"], rough=0.5, shadow=False)
        b.ell(150, 250, 98, 110, P[col], rough=1.6)
        b.ell(150, 170, 62, 56, P[col], rough=1.2)
        b.ell(128, 160, 7, 7, P["ink"], rough=0.2, shadow=False)
        b.ell(172, 160, 7, 7, P["ink"], rough=0.2, shadow=False)
        b.ell(150, 182, 9, 7, P["brick_l"], rough=0.3, shadow=False)
        b.ell(235, 300, 28, 28, P["white"], rough=1)
        b.ell(100, 350, 36, 20, P[col], rough=0.8)
        b.ell(200, 350, 36, 20, P[col], rough=0.8)
        return b.done()
    return memo(("rabbit", col), mk)


def crown_sprite():
    b = Builder(420, 320, seed=402)
    b.poly([(40, 250), (30, 90), (130, 170), (210, 50), (290, 170), (390, 90), (380, 250)], P["mustard"], rough=1.6)
    b.rect(36, 240, 384, 290, P["orange"], rough=1.2)
    for x, c in [(120, "brick"), (210, "teal"), (300, "brick")]:
        b.ell(x, 265, 14, 14, P[c], rough=0.4, shadow=False)
    for x, y in [(30, 90), (210, 50), (390, 90)]:
        b.ell(x, y, 16, 16, P["cream"], rough=0.5)
    return b.done()


def cottage_sprite():
    b = Builder(800, 560, seed=403)
    b.poly([(80, 540), (140, 400), (700, 400), (740, 540)], P["teal"], rough=2.5)
    b.rect(160, 250, 640, 520, P["cream_d"], rough=1.8)
    b.poly([(110, 270), (400, 90), (690, 270)], P["brick"], rough=1.8)
    b.rect(540, 110, 590, 220, P["brick_l"], rough=1)
    b.rect(350, 360, 450, 520, P["navy_d"], rough=1)
    b.rect(210, 320, 300, 400, P["mustard"], rough=1, shadow=False)
    b.rect(500, 320, 590, 400, P["mustard"], rough=1, shadow=False)
    b.bar(255, 320, 255, 400, 6, P["brick"], rough=0.3, shadow=False)
    b.bar(545, 320, 545, 400, 6, P["brick"], rough=0.3, shadow=False)
    return b.done()


def cell_sprite():
    b = Builder(560, 640, seed=404)
    b.rect(40, 40, 520, 600, P["navy_d"], rough=1.6)
    for i in range(6):
        b.bar(95 + i * 74, 40, 95 + i * 74, 600, 24, P["grey"], rough=0.8, shadow=False)
    b.bar(40, 120, 520, 120, 22, P["grey"], rough=0.8)
    b.bar(40, 520, 520, 520, 22, P["grey"], rough=0.8)
    return b.done()


def hat_surgeon(col):
    return person_sprite(col, 410, hat=True)


def laugh_sprite():
    b = Builder(260, 200, seed=405)
    b.poly(rrect_pts(10, 10, 250, 140, 40), P["cream"], rough=1.4)
    b.poly([(60, 130), (100, 130), (50, 190)], P["cream"], rough=0.8, shadow=False)
    b.text(130, 76, "HA HA", "Anton", 62, P["ink"])
    return b.done()


def gloss(C, T, x0=0):
    pass


# ------------------------------------------------------------------ scènes
def m1(C, T, t):
    pop(C, calendar_sprite("ANGLETERRE", "1726"), 540, 560, T, 0.1, s=0.9, rot=-3)
    pop(C, B("ELLE ACCOUCHE", 90, "cream", "ink", seed=1), 540, 320, T, 1.7, rot=-2)
    pop(C, memo("rab", rabbit_sprite), 540, 880, T, 2.65, s=1.2, rot=4)
    slam(C, B("DE LAPINS ?!", 96, "orange", "cream", seed=2), 540, 1170, T, 2.7, rot=2)


def m2(C, T, t):
    pop(C, memo("crown", crown_sprite), 540, 640, T, 3.5, s=1.25, rot=-4)
    slam(C, B("LE ROI Y A CRU", 92, "mustard", "ink", seed=3), 540, 330, T, 3.82, rot=-2)
    pop(C, memo("rab", rabbit_sprite), 800, 1050, T, 4.3, s=0.6, rot=8)


def m3(C, T, t):
    pop(C, memo("cottage", cottage_sprite), 540, 780, T, 5.0, s=1.05)
    pop(C, B("GODALMING", 120, "cream", "ink", seed=4), 540, 320, T, 5.02, rot=-2)
    pop(C, B("ANGLETERRE", 70, "orange", "cream", seed=5), 540, 1130, T, 6.09, rot=2)


def m4(C, T, t):
    pop(C, memo("mary", lambda: person_sprite("orange", 420)), 330, 800, T, 7.25, s=1.9)
    pop(C, B("MARY TOFT", 110, "cream", "ink", seed=6), 540, 320, T, 7.23, rot=-2)
    pop(C, calendar_sprite("ÂGE", "25 ANS"), 780, 760, T, 8.75, s=0.7, rot=5)
    for i, (x, y, r) in enumerate([(720, 1060, 10), (880, 980, -10)]):
        pop(C, memo("rab", rabbit_sprite), x, y, T, 10.83 + 0.2 * i, s=0.55, rot=r)
    pop(C, B("MORCEAUX DE LAPIN", 60, "brick", "cream", seed=7), 540, 1180, T, 10.83, rot=2)


def m5(C, T, t):
    pop(C, memo("chir", lambda: hat_surgeon("teal")), 300, 820, T, 12.1, s=1.9)
    pop(C, B("LE CHIRURGIEN", 88, "mustard", "ink", seed=8), 540, 320, T, 12.13, rot=-2)
    n = sum(1 for tt in (14.85, 15.18, 15.49, 15.84) if T >= tt)
    for i in range(n):
        pop(C, memo("rab", rabbit_sprite), 560 + (i % 2) * 220, 650 + (i // 2) * 330, T, (14.85, 15.18, 15.49, 15.84)[i], s=0.5, rot=(-8, 8)[i % 2])
    if T >= 14.4:
        slam(C, B("IL LE JURE !", 80, "brick", "cream", seed=9), 540, 1170, T, 14.4, rot=2)


def m6(C, T, t):
    pop(C, B("LA NOUVELLE", 100, "cream", "ink", seed=10), 540, 320, T, 17.0, rot=-2)
    for i, (x, y, r) in enumerate([(280, 760, -10), (560, 700, 4), (820, 800, 12)]):
        pop(C, memo("doc", doc_sprite), x, y + 20 * math.sin(T * 3 + i), T, 17.2 + 0.2 * i, s=0.8, rot=r)
    pop(C, B("FAIT LE TOUR DU PAYS", 66, "orange", "cream", seed=11), 540, 1150, T, 17.7, rot=2)


def m7(C, T, t):
    pop(C, memo("crown", crown_sprite), 540, 560, T, 18.8, s=1.0, rot=3)
    pop(C, B("GEORGE Ier", 110, "mustard", "ink", seed=12), 540, 320, T, 19.05, rot=-2)
    slide(C, memo("chir2", lambda: hat_surgeon("brick")), (1250, 900), (540, 900), T, 20.4, d=0.8, s=1.5)
    pop(C, B("SON PROPRE CHIRURGIEN", 56, "cream", "ink", seed=13), 540, 1170, T, 20.66, rot=2)


def m8(C, T, t):
    pop(C, memo("mary", lambda: person_sprite("orange", 420)), 300, 820, T, 22.3, s=1.7)
    m = memo("mag", A.magnifier_sprite)
    if T >= 22.33:
        bput(C, m, 640 + 30 * math.sin(T * 2.2), 700 + 20 * math.cos(T * 1.7), T, s=1.0, rot=-12)
    pop(C, B("IL EXAMINE", 100, "cream", "ink", seed=14), 540, 320, T, 22.33, rot=-2)
    if T >= 23.69:
        slam(C, B("CONVAINCU !", 100, "orange", "cream", seed=15), 540, 1150, T, 23.69, rot=2)


def m9(C, T, t):
    pop(C, memo("facade", S.facade_sprite), 540, 780, T, 24.9, s=1.0)
    pop(C, B("LONDRES", 130, "cream", "ink", seed=16), 540, 320, T, 25.5, rot=-2)
    m = memo("mag", A.magnifier_sprite)
    if T >= 26.45:
        pop(C, B("SURVEILLÉE", 76, "orange", "cream", seed=17), 540, 1150, T, 26.45, rot=2)
        bput(C, m, 700 + 40 * math.sin(T * 2.2), 780 + 24 * math.cos(T * 1.7), T, s=1.2, rot=-12)
    pop(C, memo("mary", lambda: person_sprite("orange", 420)), 330, 920, T, 25.2, s=1.0)


def m10(C, T, t):
    pop(C, B("MAIS…", 130, "brick", "cream", seed=18), 540, 320, T, 27.91, rot=-3)
    pop(C, memo("porter", lambda: person_sprite("mustard", 430)), 330, 820, T, 28.2, s=1.8)
    pop(C, memo("rab", rabbit_sprite), 640, 780, T, 30.27, s=0.8, rot=10)
    pop(C, B("UN PORTEUR", 76, "cream", "ink", seed=19), 540, 1120, T, 28.19, rot=2)
    if T >= 30.61:
        slam(C, B("SURPRIS !", 100, "orange", "cream", seed=20), 540, 540, T, 30.61, rot=-3)


def m11(C, T, t):
    pop(C, B("ELLE AVOUE", 110, "cream", "ink", seed=21), 540, 320, T, 31.91, rot=-2)
    pop(C, memo("mary", lambda: person_sprite("orange", 420)), 300, 820, T, 32.31, s=1.8)
    pop(C, memo("bubble", S.bubble_sprite), 700, 700, T, 33.03, s=0.6, rot=3)
    for i, tt in enumerate((34.10, 34.48, 34.94)):
        pop(C, memo("rab", rabbit_sprite), 600 + 150 * i, 1020 - 30 * (i % 2), T, tt, s=0.42, rot=-8 + 8 * i)
    pop(C, B("ELLE LES GLISSAIT", 60, "brick", "cream", seed=22), 540, 1180, T, 33.28, rot=2)


def m12(C, T, t):
    pop(C, memo("cell", cell_sprite), 330, 800, T, 36.0, s=1.0)
    pop(C, memo("mary", lambda: person_sprite("orange", 420)), 330, 840, T, 36.1, s=0.9, a=0.9)
    slam(C, B("PRISON", 120, "cream", "ink", seed=23), 540, 320, T, 36.03, rot=-2)
    if T >= 36.99:
        pop(C, memo("chir2", lambda: hat_surgeon("brick")), 790, 860, T, 36.99, s=1.3)
        pop(C, memo("laugh", laugh_sprite), 780, 600, T, 38.0, s=0.9, rot=-6)
        pop(C, memo("laugh", laugh_sprite), 930, 700, T, 38.4, s=0.7, rot=8)
        pop(C, B("LA RISÉE DU PAYS", 66, "orange", "cream", seed=24), 540, 1170, T, 38.21, rot=2)


def m13(C, T, t):
    A.cta(C, T, 39.84, 41.54, 44.38, 45.00, 45.9)


SCENES = [
    (0.00, 3.40, m1), (3.40, 4.95, m2), (4.95, 7.20, m3), (7.20, 11.90, m4), (11.90, 16.85, m5),
    (16.85, 18.70, m6), (18.70, 22.15, m7), (22.15, 24.65, m8), (24.65, 27.85, m9), (27.85, 31.55, m10),
    (31.55, 35.70, m11), (35.70, 39.80, m12), (39.80, 99.0, m13),
]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [2.7, 3.82, 14.4, 23.69, 30.61, 36.03]
POPS = [41.54, 44.38, 45.00]
