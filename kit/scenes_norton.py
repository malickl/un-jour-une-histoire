"""Storyboard « L'empereur Norton »."""
import math

import papercut as pc
import scenes as S
from papercut import (PAL, W, H, Builder, put, bput, pop, slam, slide, cue, ease_out, back, clamp,
                      ell_pts, rrect_pts, rect_pts, bar_pts, burst_pts)
from scenes import sweep_sprites, B, memo, calendar_sprite, waves_sprite, person_sprite, doc_sprite, coin_stack, plate_sprite, cuffs_sprite
from scenes_alcatraz import cut_text, moon_sprite

P = PAL


def crown_sprite():
    b = Builder(420, 320, seed=201)
    b.poly([(40, 270), (20, 90), (120, 170), (210, 40), (300, 170), (400, 90), (380, 270)], P["mustard"], rough=1.8)
    b.rect(40, 230, 380, 290, P["orange"], rough=1.2)
    for x, c in [(20, "brick"), (210, "teal"), (400, "brick")]:
        b.ell(x, 90 if x != 210 else 40, 22, 22, P[c], rough=0.8)
    for x in (110, 210, 310):
        b.ell(x, 260, 14, 14, P["cream"], rough=0.5, shadow=False)
    return b.done()


def emperor_sprite():
    def mk():
        b = Builder(420, 560, seed=202)
        b.poly(rrect_pts(120, 200, 300, 450, 40), P["navy_l"], rough=1.4)
        b.rect(120, 330, 300, 350, P["mustard"], rough=0.8, shadow=False)
        for y in (250, 290):
            b.ell(180, y, 9, 9, P["mustard"], rough=0.4, shadow=False)
            b.ell(240, y, 9, 9, P["mustard"], rough=0.4, shadow=False)
        b.ell(108, 220, 40, 22, P["mustard"], rough=1)
        b.ell(312, 220, 40, 22, P["mustard"], rough=1)
        b.rect(150, 440, 190, 540, P["navy_d"], rough=1)
        b.rect(230, 440, 270, 540, P["navy_d"], rough=1)
        b.bar(130, 240, 90, 400, 28, P["navy_l"], rough=1)
        b.bar(290, 240, 330, 400, 28, P["navy_l"], rough=1)
        b.bar(350, 280, 350, 520, 12, P["grey"], rough=0.8)
        b.rect(332, 380, 368, 396, P["mustard"], rough=0.8, shadow=False)
        b.ell(210, 150, 56, 60, P["cream_d"])
        b.poly([(160, 170), (210, 232), (260, 170), (250, 200), (210, 260), (170, 200)], P["cream"], rough=1, shadow=False)
        b.poly([(98, 112), (322, 112), (300, 70), (120, 70)], P["navy_l"], rough=1.2)
        b.poly([(100, 112), (320, 112), (330, 132), (90, 132)], P["mustard"], rough=1)
        b.poly([(250, 70), (330, 10), (390, 40), (310, 90)], P["brick"], rough=1.2, shadow=False)
        return b.done()
    return memo("emperor", mk)


def note_sprite():
    b = Builder(560, 300, seed=203)
    b.rrect(14, 14, 546, 286, 14, P["cream"], rough=2)
    b.rrect(36, 36, 524, 264, 8, P["teal_l"], rough=1.2, shadow=False)
    b.ell(280, 150, 62, 62, P["cream"], rough=1.2, shadow=False)
    b.text(280, 152, "N", "Anton", 80, P["teal"])
    b.text(88, 74, "50", "Anton", 40, P["cream"])
    b.text(472, 226, "50", "Anton", 40, P["cream"])
    return b.done()


def paper_sprite():
    b = Builder(520, 380, seed=204)
    b.rect(20, 20, 500, 360, P["cream"], rough=2)
    b.rect(50, 40, 470, 100, P["ink"], rough=1)
    b.text(260, 72, "JOURNAL", "Anton", 50, P["cream"])
    for i in range(6):
        b.bar(60, 130 + i * 34, 300, 130 + i * 34, 8, P["cream_d"], rough=0.5, shadow=False)
    b.rect(330, 130, 470, 250, P["navy_l"], rough=1, shadow=False)
    return b.done()


def rice_sack():
    b = Builder(360, 420, seed=205)
    b.poly(ell_pts(180, 270, 150, 130), P["cream"], rough=2)
    b.poly([(120, 160), (240, 160), (270, 110), (90, 110)], P["cream"], rough=1.5)
    b.bar(100, 150, 260, 150, 18, P["brick"], rough=1)
    b.text(180, 274, "RIZ", "Anton", 90, P["brick"])
    return b.done()


def stone_sprite():
    b = Builder(360, 520, seed=206)
    b.poly([(40, 500), (40, 160), (110, 50), (250, 50), (320, 160), (320, 500)], P["grey"], rough=2)
    b.poly([(70, 480), (70, 170), (125, 80), (235, 80), (290, 170), (290, 480)], (150, 158, 180), rough=1.4, shadow=False)
    b.text(180, 190, "RIP", "Anton", 90, P["navy_d"])
    b.text(180, 290, "1880", "Anton", 70, P["navy_d"])
    return b.done()


def curtain_sprite():
    b = Builder(900, 520, seed=207)
    b.rect(20, 20, 880, 80, P["mustard"], rough=1.2)
    b.poly([(30, 70), (330, 70), (240, 500), (30, 500)], P["brick"], rough=1.6)
    b.poly([(870, 70), (570, 70), (660, 500), (870, 500)], P["brick"], rough=1.6)
    b.poly([(120, 80), (200, 80), (150, 490), (100, 490)], P["brick_l"], rough=1, shadow=False)
    b.poly([(780, 80), (700, 80), (750, 490), (800, 490)], P["brick_l"], rough=1, shadow=False)
    b.rect(330, 400, 570, 500, P["mustard"], rough=1.2, shadow=False)
    return b.done()


def seat_sprite():
    b = Builder(300, 360, seed=208)
    b.poly(rrect_pts(40, 30, 260, 230, 40), P["brick"], rough=1.6)
    b.rect(30, 210, 270, 290, P["brick_l"], rough=1.4)
    b.rect(60, 290, 90, 340, P["navy_d"], rough=0.8)
    b.rect(210, 290, 240, 340, P["navy_d"], rough=0.8)
    b.text(150, 130, "RÉSERVÉ", "Anton", 40, P["mustard"])
    return b.done()


def cop_sprite():
    return memo("cop", lambda: person_sprite("navy_l", 210, hat=True))


def P_(col, seed, hat=False, up=False):
    return person_sprite(col, seed, hat=hat, arms_up=up)


def crowd(C, T, t0, rows, s=0.5, seed=300, hats=False):
    cols = ["orange", "teal", "brick", "mustard", "navy_l", "teal_l"]
    i = 0
    for y, xs in rows:
        for x in xs:
            c = cols[i % 6]
            pop(C, memo(("cr", c, i % 4, hats), lambda c=c, i=i: P_(c, seed + i % 4, hat=hats and i % 2 == 0)), x, y, T, t0 + 0.08 * i, s=s)
            i += 1


# ------------------------------------------------------------------ scènes
def n1(C, T, t):
    pop(C, memo("crown", crown_sprite), 540, 700, T, 1.55, s=1.25, rot=-4)
    pop(C, B("UN HOMME RUINÉ", 92, "cream", "ink", seed=1), 540, 310, T, 0.08, rot=-2)
    slam(C, B("", 96, "mustard", "ink", lines=["EMPEREUR DES", "ÉTATS-UNIS"], seed=2), 540, 1090, T, 1.7, rot=2)


def n2(C, T, t):
    pop(C, B("TOUTE UNE VILLE", 96, "cream", "ink", seed=3), 540, 310, T, 3.2, rot=-2)
    crowd(C, T, 3.5, [(820, [200, 420, 640, 860]), (1030, [310, 540, 770])], s=0.78)
    slam(C, B("LE PREND AU SÉRIEUX", 66, "orange", "cream", seed=4), 540, 1180, T, 4.2, rot=2)


def n3(C, T, t):
    for i, (col, y, sd) in enumerate([(P["teal"], 1050, 61), (P["teal_l"], 1120, 62)]):
        w = memo(("wave2", i), lambda c=col, s=sd: waves_sprite(c, s))
        bput(C, w, 540 + 10 * math.sin(T * 1.5 + i), y + 8 * math.sin(T * 2 + i), T, s=1.0)
    pop(C, memo("sun", S.sun_sprite), 800, 620, T, 5.3, s=0.8)
    pop(C, memo("fac", S.facade_sprite), 330, 800, T, 5.4, s=0.7)
    pop(C, B("SAN FRANCISCO", 96, "mustard", "ink", seed=5), 540, 310, T, 5.46, rot=-2)
    pop(C, calendar_sprite("", "1859"), 780, 1000, T, 6.4, s=0.8, rot=4)


def n4(C, T, t):
    pop(C, memo("emp0", lambda: person_sprite("teal", 220, hat=True)), 300, 860, T, 7.96, s=1.3)
    pop(C, B("JOSHUA NORTON", 96, "cream", "ink", seed=6), 540, 310, T, 7.96, rot=-2)
    pop(C, B("TOUT PERDU", 80, "brick", "cream", seed=7), 540, 1170, T, 9.1, rot=2)
    for i in range(4):
        k = cue(T, 9.2 + 0.1 * i, 1.0)
        if k > 0:
            put(C, memo("coin1", lambda: coin_stack(1)), 560 + 90 * i, 640 + 380 * k * k, 0.5, 0, 1 - clamp((k - 0.8) * 5))
    pop(C, memo("rice", rice_sack), 760, 820, T, 10.3, s=0.8, rot=6)
    pop(C, B("SPÉCULATION", 56, "mustard", "ink", seed=8), 760, 560, T, 9.86, rot=-3)


def n5(C, T, t):
    pop(C, B("UNE LETTRE", 100, "cream", "ink", seed=9), 540, 310, T, 11.35, rot=-2)
    slide(C, memo("doc", doc_sprite), (-300, 800), (300, 800), T, 12.2, 0.5, s=0.8)
    pop(C, memo("paper", paper_sprite), 700, 860, T, 12.87, s=0.95, rot=4)
    pop(C, B("AUX JOURNAUX", 74, "orange", "cream", seed=10), 540, 1170, T, 12.87, rot=-2)


def n6(C, T, t):
    pop(C, B("NORTON Ier", 130, "mustard", "ink", seed=11), 540, 300, T, 14.14, rot=-2)
    pop(C, memo("crown", crown_sprite), 540, 760, T, 14.4, s=1.0, rot=4)
    slam(C, B("", 92, "cream", "ink", lines=["EMPEREUR DES", "ÉTATS-UNIS"], seed=12), 540, 1090, T, 15.25, rot=-2)


def n7(C, T, t):
    pop(C, memo("emperor", emperor_sprite), 480, 800, T, 16.64, s=1.45)
    pop(C, B("UNIFORME BLEU", 78, "cream", "ink", seed=13), 540, 290, T, 17.34, rot=-2)
    pop(C, B("SABRE", 66, "orange", "cream", seed=14), 880, 700, T, 18.78, rot=4)
    pop(C, B("CHAPEAU À PLUME", 64, "mustard", "ink", seed=15), 520, 1180, T, 19.51, rot=-2)


def n8(C, T, t):
    pop(C, B("SA PROPRE MONNAIE", 80, "cream", "ink", seed=16), 540, 300, T, 20.88, rot=-2)
    pop(C, memo("note", note_sprite), 540, 700, T, 21.2, s=1.0, rot=-5)
    pop(C, memo("cs", lambda: coin_stack(4)), 250, 1020, T, 21.7, s=0.85)
    pop(C, memo("cs2", lambda: coin_stack(3)), 830, 1050, T, 21.95, s=0.85)
    slam(C, B("ACCEPTÉE !", 100, "teal", "cream", seed=17), 540, 1170, T, 22.94, rot=2)


def n9(C, T, t):
    pop(C, B("RESTAURANTS", 100, "cream", "ink", seed=18), 540, 300, T, 24.0, rot=-2)
    pop(C, memo("plate", plate_sprite), 540, 760, T, 24.5, s=1.1)
    slam(C, B("REPAS OFFERTS", 90, "orange", "cream", seed=19), 540, 1100, T, 24.97, rot=2)


def n10(C, T, t):
    pop(C, memo("curt", curtain_sprite), 540, 640, T, 25.8, s=1.1)
    pop(C, B("THÉÂTRES", 100, "cream", "ink", seed=20), 540, 300, T, 25.9, rot=-2)
    pop(C, memo("seat", seat_sprite), 540, 1030, T, 26.4, s=0.95)
    pop(C, B("UNE PLACE", 70, "mustard", "ink", seed=21), 790, 960, T, 26.76, rot=3)


def n11(C, T, t):
    pop(C, B("UN JOUR…", 100, "cream", "ink", seed=22), 540, 300, T, 27.62, rot=-2)
    pop(C, memo("cop", cop_sprite), 300, 880, T, 28.58, s=1.5)
    pop(C, memo("pn", lambda: person_sprite("teal", 230, hat=True)), 700, 900, T, 28.0, s=1.3)
    pop(C, memo("cuf", cuffs_sprite), 560, 1130, T, 29.08, s=0.6, rot=-4)
    slam(C, B("ARRESTÉ", 100, "brick", "cream", seed=23), 540, 560, T, 29.08, rot=-3)


def n12(C, T, t):
    crowd(C, T, 29.97, [(800, [180, 400, 620, 840]), (1010, [280, 500, 720])], s=0.8)
    slam(C, B("TOLLÉ", 150, "orange", "cream", seed=24), 540, 330, T, 29.97, rot=-3)
    pop(C, B("GÉNÉRAL", 100, "cream", "ink", seed=25), 540, 520, T, 30.27, rot=2)


def n13(C, T, t):
    pop(C, B("LE CHEF DE POLICE", 74, "cream", "ink", seed=26), 540, 300, T, 31.34, rot=-2)
    pop(C, memo("cop", cop_sprite), 330, 860, T, 31.5, s=1.5)
    op = T >= 32.26
    pop(C, memo(("cf", op), lambda: cuffs_sprite(op)), 740, 880, T, 31.7, s=0.7, rot=-6)
    if op:
        pop(C, B("LIBÉRÉ", 100, "teal", "cream", seed=27), 540, 1130, T, 32.26, rot=2)
    if T >= 33.09:
        pop(C, B("S'EXCUSE", 74, "mustard", "ink", seed=28), 540, 1250 - 780, T, 33.09, rot=-3)


def n14(C, T, t):
    for i, x in enumerate([230, 450, 670, 890]):
        pop(C, memo(("ag", i), lambda i=i: person_sprite(["navy_l", "navy_l", "teal", "navy_l"][i], 240 + i, hat=True, arms_up=(i % 2 == 0))), x, 860, T, 34.2 + 0.1 * i, s=0.95)
    pop(C, B("TOUS LES AGENTS", 80, "cream", "ink", seed=29), 540, 300, T, 34.25, rot=-2)
    pop(C, B("LE SALUENT", 100, "orange", "cream", seed=30), 540, 1110, T, 34.87, rot=2)


def n15(C, T, t):
    pop(C, memo("moon", moon_sprite), 800, 480, T, 36.3, s=0.6)
    pop(C, memo("stone", stone_sprite), 540, 840, T, 36.5, s=1.2)
    pop(C, calendar_sprite("", "1880"), 250, 1010, T, 36.82, s=0.7, rot=-5)
    pop(C, B("MEURT EN 1880", 90, "cream", "ink", seed=31), 540, 300, T, 36.27, rot=-2)
    pop(C, B("EN PLEINE RUE", 74, "brick", "cream", seed=32), 540, 1180, T, 38.19, rot=2)


def n16(C, T, t):
    crowd(C, T, 39.1, [(640, [150, 330, 510, 690, 870]), (810, [240, 420, 600, 780]), (980, [150, 330, 510, 690, 870])], s=0.62, hats=True)
    pop(C, B("DES MILLIERS", 100, "mustard", "ink", seed=33), 540, 300, T, 39.27, rot=-2)
    pop(C, B("D'OBSÈQUES", 80, "cream", "ink", seed=34), 540, 1160, T, 40.84, rot=2)


def cta(C, T, t_tu, t_com, t_like, t_abo, t_tap):
    pop(C, B("TU CONNAISSAIS ?", 110, "cream", "ink", seed=21), 540, 310, T, t_tu, rot=-2)
    pop(C, memo("bubble", S.bubble_sprite), 540, 640, T, t_tu + 0.75, s=1.0, rot=-2)
    if T >= t_com:
        pop(C, B("DIS-LE EN COMMENTAIRE", 64, "orange", "cream", seed=22), 540, 960, T, t_com, rot=1.5)
    if T >= t_like:
        beat = 1 + 0.12 * max(0, math.sin((T - t_like) * 9))
        pop(C, memo("heart", lambda: S.heart_sprite("brick")), 230, 1110, T, t_like, s=0.8 * beat, rot=-8)
    if T >= t_abo:
        pop(C, memo("btn", S.button_sprite), 690, 1110, T, t_abo, s=0.85)
        tap = cue(T, t_tap, 0.5)
        if tap > 0:
            put(C, memo("finger", S.finger_sprite), 880, 1190 - 20 * math.sin(tap * math.pi), 0.8, -10, 1)


def n17(C, T, t):
    cta(C, T, 41.86, 43.56, 46.40, 46.98, 47.8)


SCENES = [
    (0.00, 3.19, n1), (3.19, 5.07, n2), (5.07, 7.90, n3), (7.90, 11.30, n4), (11.30, 13.60, n5),
    (13.60, 16.60, n6), (16.60, 20.70, n7), (20.70, 23.90, n8), (23.90, 25.75, n9), (25.75, 27.55, n10),
    (27.55, 29.95, n11), (29.95, 31.30, n12), (31.30, 34.15, n13), (34.15, 36.25, n14), (36.25, 39.05, n15),
    (39.05, 41.80, n16), (41.80, 99.0, n17),
]
BOUNDS = [s[0] for s in SCENES[1:]]
SWEEPS = [5.07, 36.25]
IMPACTS = [1.7, 15.25, 22.94, 29.08, 29.97]
POPS = [43.56, 46.40, 46.98]
