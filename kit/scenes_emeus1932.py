"""Storyboard « La guerre des émeus, 1932 »."""
import math
from PIL import Image
import papercut as pc
import scenes as S
import scenes_alcatraz as A
from papercut import (PAL, Builder, put, bput, pop, slam, slide, cue, ease_out, clamp, rrect_pts, burst_pts)
from scenes import B, memo, calendar_sprite, person_sprite

P = PAL


def emu_sprite(seed=301, col="brick_l"):
    b = Builder(300, 420, seed=seed)
    b.bar(120, 300, 110, 405, 12, P["cream_d"], rough=0.6, shadow=False)
    b.bar(170, 300, 185, 405, 12, P["cream_d"], rough=0.6, shadow=False)
    b.bar(105, 408, 140, 408, 10, P["cream_d"], rough=0.4, shadow=False)
    b.bar(180, 408, 215, 408, 10, P["cream_d"], rough=0.4, shadow=False)
    b.ell(140, 250, 100, 72, P[col], rough=2)
    b.poly([(60, 220), (20, 270), (70, 285)], P[col], rough=1.5)
    b.bar(205, 215, 232, 90, 20, P[col], rough=1)
    b.ell(240, 70, 30, 24, P[col], rough=1)
    b.poly([(262, 66), (298, 74), (262, 84)], P["mustard"], rough=0.6, shadow=False)
    b.ell(246, 62, 5, 5, P["ink"], rough=0.2, shadow=False)
    return b.done()


def flip(im):
    return im.transpose(Image.FLIP_LEFT_RIGHT)


def emu(flipped=False, col="brick_l", seed=301):
    k = ("emu", flipped, col, seed)
    return memo(k, lambda: flip(emu_sprite(seed, col)) if flipped else emu_sprite(seed, col))


def wheat_sprite():
    b = Builder(1000, 300, seed=310)
    b.rect(0, 220, 1000, 300, P["mustard"], rough=2)
    for i in range(26):
        x = 20 + i * 38
        b.bar(x, 250, x + (i % 3 - 1) * 6, 80 + (i % 4) * 14, 8, P["mustard"], rough=0.8, shadow=False)
        b.ell(x + (i % 3 - 1) * 6, 70 + (i % 4) * 14, 10, 26, P["orange"], rough=0.8, shadow=False)
    return b.done()


def gun_sprite():
    b = Builder(520, 340, seed=311)
    b.bar(210, 190, 90, 330, 14, P["grey"], rough=0.8)
    b.bar(250, 190, 330, 330, 14, P["grey"], rough=0.8)
    b.bar(230, 190, 230, 300, 14, P["grey"], rough=0.8)
    b.rect(180, 120, 340, 210, P["ink"], rough=1.4)
    b.bar(330, 150, 500, 150, 22, P["grey"], rough=0.8)
    b.ell(240, 100, 50, 28, P["brick"], rough=1)
    b.rect(120, 140, 180, 190, P["mustard"], rough=1)
    return b.done()


def bullets_sprite():
    b = Builder(420, 260, seed=312)
    for r in range(3):
        for i in range(5):
            x, y = 50 + i * 76, 60 + r * 70
            b.rect(x, y + 20, x + 38, y + 80 - 10, P["mustard"], rough=0.5, shadow=False)
            b.poly([(x, y + 20), (x + 19, y - 10), (x + 38, y + 20)], P["brick"], rough=0.5, shadow=False)
    return b.done()


def soldier(seed, col="teal"):
    return person_sprite(col, seed, hat=True)


def e1(C, T, t):
    pop(C, soldier(401), 300, 800, T, 0.25, s=1.9)
    pop(C, emu(True, seed=302), 760, 760, T, 1.9, s=1.5)
    pop(C, B("SOLDATS", 100, "teal_l", "ink", seed=1), 330, 330, T, 0.25, rot=-3)
    pop(C, B("OISEAUX", 100, "orange", "cream", seed=2), 760, 1130, T, 2.45, rot=3)
    pop(C, A.cut_text("VS", "Anton", 150, P["cream"]), 540, 560, T, 1.7, s=0.9, rot=-6)


def e2(C, T, t):
    pop(C, B("C'EST VRAI", 120, "cream", "ink", seed=3), 540, 330, T, 3.5, rot=-2)
    pop(C, calendar_sprite("ARRIVÉ EN", "1932"), 540, 800, T, 4.97, s=1.2, rot=3)
    pop(C, emu(False, seed=303), 540, 1030, T, 5.3, s=0.9)


def e3(C, T, t):
    pop(C, memo("wheat", wheat_sprite), 540, 1060, T, 6.2, s=1.0)
    pop(C, B("", 90, "mustard", "ink", lines=["AUSTRALIE", "OCCIDENTALE"], seed=4), 540, 330, T, 6.2, rot=-2)
    xs = [(150, 840), (340, 800), (540, 850), (740, 800), (930, 840)]
    for i, (x, y) in enumerate(xs):
        pop(C, emu(i % 2 == 0, seed=304 + i), x, y, T, 8.43 + 0.12 * i, s=0.8)
    slam(C, B("", 100, "brick", "cream", lines=["20 000", "ÉMEUS"], seed=5), 540, 610, T, 8.43, rot=2)


def e4(C, T, t):
    for i, (c, x) in enumerate([("orange", 250), ("mustard", 540), ("teal_l", 830)]):
        pop(C, person_sprite(c, 410 + i), x, 900, T, 10.43 + 0.3 * i, s=1.2)
    pop(C, B("FERMIERS", 110, "cream", "ink", seed=6), 540, 320, T, 10.43, rot=-2)
    pop(C, B("ANCIENS COMBATTANTS", 62, "mustard", "ink", seed=7), 540, 1160, T, 11.54, rot=2)
    if T >= 12.67:
        slam(C, B("L'ARMÉE !", 100, "brick", "cream", seed=8), 540, 560, T, 12.67, rot=-4)


def e5(C, T, t):
    pop(C, soldier(420, "brick"), 540, 800, T, 14.4, s=2.2)
    pop(C, B("LE GOUVERNEMENT", 80, "cream", "ink", seed=9), 540, 320, T, 13.97, rot=-2)
    pop(C, B("UN MAJOR", 100, "orange", "cream", seed=10), 540, 1160, T, 14.92, rot=2)


def e6(C, T, t):
    g = memo("gun", gun_sprite)
    pop(C, g, 330, 640, T, 15.9, s=1.1, rot=-4)
    pop(C, flip(g) if False else memo("gun2", lambda: flip(gun_sprite())), 740, 800, T, 16.1, s=1.0, rot=4)
    pop(C, B("2 MITRAILLEUSES", 80, "cream", "ink", seed=11), 540, 310, T, 15.9, rot=-2)
    if T >= 17.0:
        pop(C, memo("bul", bullets_sprite), 540, 990, T, 17.0, s=0.8)
        slam(C, B("", 76, "brick", "cream", lines=["10 000 CARTOUCHES"], seed=12), 540, 1180, T, 17.12, rot=2)


def e7(C, T, t):
    # 18.2-20.3 : dispersion
    k = ease_out(cue(T, 18.96, 1.2))
    for i, (x0, y0, dx, dy) in enumerate([(540, 740, -380, -100), (540, 740, 0, 130), (540, 740, 380, -80), (540, 740, -200, 150), (540, 740, 220, 130)]):
        pop(C, emu(dx > 0, seed=310 + i), x0 + dx * k, y0 + dy * k, T, 18.3 + 0.05 * i, s=0.75)
    pop(C, B("LES ÉMEUS SE DISPERSENT", 62, "cream", "ink", seed=13), 540, 320, T, 18.5, rot=-2)
    pop(C, B("PETITS GROUPES", 72, "mustard", "ink", seed=14), 540, 1160, T, 19.42, rot=2)


def e8(C, T, t):
    pop(C, B("PLUS VITES", 100, "cream", "ink", seed=15), 540, 320, T, 20.52, rot=-2)
    pop(C, B("QUE LES CAMIONS", 72, "orange", "cream", seed=16), 540, 1180, T, 21.04, rot=2)
    p = ease_out(cue(T, 20.4, 1.4))
    bput(C, memo("car", S.car_sprite), 60 + 330 * p, 880, T, s=1.0)
    bput(C, emu(False, seed=330), 560 + 380 * p, 760, T, s=0.95, rot=6 * math.sin(T * 14))


def e9(C, T, t):
    pop(C, emu(True, seed=331), 700, 720, T, 21.88, s=1.5)
    pop(C, B("ENCAISSENT", 100, "brick", "cream", seed=17), 540, 330, T, 21.88, rot=-2)
    pop(C, B("LES BALLES", 100, "cream", "ink", seed=18), 540, 1170, T, 22.28, rot=2)
    for i in range(5):
        c = cue(T, 22.3 + 0.12 * i, 0.4)
        if c > 0:
            put(C, memo("bl", lambda: Builder(60, 20, seed=340).bar(6, 10, 54, 10, 10, P["mustard"], shadow=False).done()),
                160 + 420 * ease_out(c), 700 + 60 * i - 20 * i, 1, 0, 1 - 0.3 * c)


def e10(C, T, t):
    pop(C, B("L'ARMÉE SE RETIRE", 80, "cream", "ink", seed=19), 540, 320, T, 23.1, rot=-2)
    s = ease_out(cue(T, 23.54, 1.2))
    for i, c in enumerate(["teal", "brick", "teal_l"]):
        bput(C, person_sprite(c, 440 + i, hat=True), 700 - 360 * s + 80 * i, 880, T, s=1.0)
    if T >= 24.40:
        slam(C, B("ELLE REVIENT", 100, "mustard", "ink", seed=20), 540, 1160, T, 24.40, rot=2)


def e11(C, T, t):
    pop(C, emu(False, seed=350), 300, 780, T, 25.0, s=1.6)
    pop(C, B("", 84, "cream", "ink", lines=["PUIS", "ABANDONNE"], seed=21), 540, 330, T, 25.67, rot=-2)
    slam(C, memo("stampA", lambda: Builder(560, 200, seed=360).poly(rrect_pts(14, 14, 546, 186, 22), P["brick"], rough=2,
         holes=[rrect_pts(34, 34, 526, 166, 14)]).text(280, 100, "PERDU", "Anton", 120, P["brick"]).done()),
         700, 900, T, 25.86, rot=-8, s=1.2)


def e12(C, T, t):
    pop(C, soldier(460, "brick"), 280, 880, T, 26.95, s=1.6)
    pop(C, memo("bubble", S.bubble_sprite), 700, 760, T, 27.0, s=0.85, rot=2)
    pop(C, B("LE MAJOR", 90, "mustard", "ink", seed=22), 540, 320, T, 27.03, rot=-2)
    pop(C, B("IMPRESSIONNÉ", 80, "orange", "cream", seed=23), 540, 1170, T, 27.69, rot=2)


def e13(C, T, t):
    for i in range(5):
        pop(C, emu(i % 2 == 0, seed=370 + i), 160 + 190 * i, 780 + 50 * (i % 2), T, 29.1 + 0.1 * i, s=0.7)
    pop(C, B("", 80, "cream", "ink", lines=["UNE DIVISION", "D'ÉMEUS"], seed=24), 540, 350, T, 29.03, rot=-2)
    if T >= 30.57:
        slam(C, B("", 80, "brick", "cream", lines=["N'IMPORTE QUELLE", "ARMÉE"], seed=25), 540, 1150, T, 30.57, rot=2)


def e14(C, T, t):
    A.cta(C, T, 32.28, 33.98, 36.82, 37.40, 38.2)


SCENES = [
    (0.00, 3.30, e1), (3.30, 6.10, e2), (6.10, 10.10, e3), (10.10, 13.80, e4), (13.80, 15.70, e5),
    (15.70, 18.20, e6), (18.20, 20.40, e7), (20.40, 21.80, e8), (21.80, 23.00, e9), (23.00, 25.0, e10),
    (25.0, 26.85, e11), (26.85, 29.0, e12), (29.0, 32.2, e13), (32.2, 99.0, e14),
]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [8.43, 12.67, 17.12, 21.88, 24.40, 25.86, 30.57]
POPS = [33.98, 36.82, 37.40]
