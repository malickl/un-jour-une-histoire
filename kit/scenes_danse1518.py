"""Storyboard « La danse de 1518 »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
from papercut import (PAL, Builder, put, bput, pop, slam, slide, cue, ease_out, clamp, ell_pts, rrect_pts, burst_pts)
from scenes import B, memo, calendar_sprite, person_sprite, sweep_sprites

P = PAL
COLS = ["orange", "teal", "brick", "mustard", "teal_l", "cream"]


def cathedral():
    b = Builder(700, 900, seed=201)
    b.rect(160, 330, 540, 860, P["cream_d"], rough=1.6)
    b.poly([(300, 330), (350, 40), (400, 330)], P["brick"], rough=1.4)
    b.rect(290, 250, 410, 340, P["cream"], rough=1.2)
    b.rect(120, 420, 200, 860, P["cream"], rough=1.2)
    b.rect(500, 420, 580, 860, P["cream"], rough=1.2)
    b.poly([(110, 420), (160, 330), (210, 420)], P["brick"], rough=1)
    b.poly([(490, 420), (540, 330), (590, 420)], P["brick"], rough=1)
    b.ell(350, 520, 62, 62, P["mustard"], rough=1, shadow=False)
    b.ell(350, 520, 34, 34, P["navy_d"], rough=0.8, shadow=False)
    b.poly([(290, 860), (290, 700), (350, 650), (410, 700), (410, 860)], P["navy_d"], rough=1, shadow=False)
    return b.done()


def chapel():
    b = Builder(600, 520, seed=202)
    b.rect(90, 220, 510, 490, P["cream"], rough=1.6)
    b.poly([(60, 230), (300, 70), (540, 230)], P["brick"], rough=1.6)
    b.rect(270, 20, 330, 120, P["cream"], rough=1)
    b.bar(300, 0, 300, 60, 8, P["mustard"], rough=0.5, shadow=False)
    b.bar(280, 30, 320, 30, 8, P["mustard"], rough=0.5, shadow=False)
    b.poly([(240, 490), (240, 360), (300, 310), (360, 360), (360, 490)], P["navy_d"], rough=1, shadow=False)
    return b.done()


def stage():
    b = Builder(820, 360, seed=203)
    b.rect(30, 120, 790, 330, P["brick_l"], rough=2)
    b.rect(10, 90, 810, 140, P["mustard"], rough=1.6)
    for i in range(6):
        b.rect(70 + i * 120, 150, 100 + i * 120, 330, P["brick"], rough=1, shadow=False)
    return b.done()


def note():
    b = Builder(160, 240, seed=204)
    b.ell(60, 190, 40, 30, P["cream"], rough=0.8)
    b.bar(96, 190, 96, 40, 12, P["cream"], rough=0.6)
    b.poly([(96, 40), (150, 80), (96, 100)], P["cream"], rough=0.8)
    return b.done()


def drum():
    b = Builder(300, 280, seed=205)
    b.rect(40, 90, 260, 250, P["brick"], rough=1.4)
    b.ell(150, 90, 110, 40, P["cream"], rough=1.2)
    for i in range(4):
        b.poly([(40 + i * 55, 90), (95 + i * 55, 250), (70 + i * 55, 250)], P["mustard"], rough=0.6, shadow=False)
    b.bar(60, 20, 140, 80, 10, P["cream_d"], rough=0.5)
    b.bar(240, 20, 170, 80, 10, P["cream_d"], rough=0.5)
    return b.done()


def trumpet():
    b = Builder(420, 240, seed=206)
    b.bar(30, 120, 280, 120, 22, P["mustard"], rough=1)
    b.poly([(270, 120), (400, 40), (400, 200)], P["mustard"], rough=1.2)
    b.bar(90, 120, 90, 180, 14, P["orange"], rough=0.5, shadow=False)
    return b.done()


def fallen(col, seed):
    return memo(("fall", col), lambda: person_sprite(col, seed))


def wob(T, k=0, a=14, f=7):
    return a * math.sin(T * f + k), -18 * abs(math.sin(T * f * 0.5 + k))


def dancer(C, T, x, y, col, k, s=0.9, t0=0.0, arms=True):
    if T < t0:
        return
    dx, dy = wob(T, k)
    pop(C, person_sprite(col, 300 + int(k) % 7, arms_up=arms and int(T * 5 + k) % 2 == 0), x, y + dy, T, t0, s=s, rot=dx)


def d1(C, T, t):
    for i, x in enumerate([200, 880]):
        if T > 1.0:
            put(C, note(), x, 560 + 30 * math.sin(T * 3 + i), 0.8, 12 * (i - .5), clamp(cue(T, 1.0 + .2 * i, .3)) * 0.0)
    dancer(C, T, 540, 800, "orange", 0, s=2.2, t0=0.08)
    pop(C, B("ELLE DANSE", 110, "cream", "ink", seed=1), 540, 310, T, 0.08, rot=-2)
    pop(C, B("SANS S'ARRÊTER", 84, "orange", "cream", seed=2), 540, 1160, T, 2.16, rot=2)


def d2(C, T, t):
    pop(C, memo("cath", cathedral), 540, 760, T, 3.7, s=0.95)
    pop(C, B("STRASBOURG", 124, "mustard", "ink", seed=3), 540, 300, T, 3.74, rot=-2)
    pop(C, calendar_sprite("JUILLET", "1518"), 790, 1010, T, 4.77, s=0.8, rot=4)


def d3(C, T, t):
    dancer(C, T, 540, 800, "teal", 1, s=2.0, t0=6.6)
    pop(C, B("MADAME TROFFEA", 92, "cream", "ink", seed=4), 540, 310, T, 6.6, rot=-2)
    if T >= 8.25:
        pop(C, memo("note", note), 240, 620, T, 8.25, s=1.0, rot=-10)
        pop(C, memo("note", note), 850, 700, T, 8.3, s=0.8, rot=12)
        pop(C, memo("x", lambda: A.cut_text("✕", "Anton", 420, P["brick"]) if False else Builder(300, 300, seed=210).bar(40, 40, 260, 260, 40, P["brick"], rough=1.4).bar(260, 40, 40, 260, 40, P["brick"], rough=1.4).done()),
            240, 650, T, 8.6, s=1.0)
        pop(C, B("SANS MUSIQUE", 70, "orange", "cream", seed=5), 540, 1160, T, 8.25, rot=2)
    if T >= 9.49:
        pop(C, B("DES JOURS", 76, "mustard", "ink", seed=6), 540, 1010, T, 9.49, rot=-2)


def d4(C, T, t):
    n = 1 if T < 11.68 else 1 + int(clamp((T - 11.68) / 1.2) * 29)
    pos = [(i % 6, i // 6) for i in range(30)]
    for i in range(min(n, 30)):
        c, r = pos[i]
        x = 160 + c * 150 + (60 if r % 2 else 0)
        y = 650 + r * 100
        if n == 1:
            x, y = 540, 800
        dancer(C, T, x, y, COLS[i % 6], i, s=0.5 if n > 1 else 1.9, t0=10.3 if i == 0 else 11.68 + 0.04 * i, arms=True)
    pop(C, B("1 SEMAINE", 100, "cream", "ink", seed=7), 540, 310, T, 10.31, rot=-2)
    if T >= 11.68:
        slam(C, B("30 PERSONNES", 84, "orange", "cream", seed=8), 540, 1160, T, 11.68, rot=2)


def d5(C, T, t):
    for i in range(28):
        c, r = i % 7, i // 7
        x = 130 + c * 130 + (50 if r % 2 else 0)
        y = 620 + r * 120
        dancer(C, T, x, y, COLS[(i * 5) % 6], i * 1.3, s=0.46, t0=13.55 + 0.03 * i)
    pop(C, B("1 MOIS", 110, "cream", "ink", seed=9), 540, 300, T, 13.53, rot=-2)
    if T >= 15.17:
        slam(C, memo("400", lambda: A.cut_text("400", "Anton", 330, P["orange"])), 540, 840, T, 15.17, rot=-4)
        pop(C, B("DANSEURS", 80, "mustard", "ink", seed=10), 540, 1160, T, 15.57, rot=2)


def d6(C, T, t):
    pop(C, person_sprite("cream", 330, hat=True), 300, 860, T, 16.6, s=1.7)
    pop(C, memo("mag", A.magnifier_sprite), 700, 780, T, 17.0, s=0.9, rot=-10)
    for i, (x, y, r) in enumerate([(780, 520, 8), (560, 480, -10), (900, 600, 14)]):
        pop(C, memo("q", lambda: A.cut_text("?", "Anton", 220, P["orange"])), x, y, T, 17.5 + 0.2 * i, s=1.0, rot=r)
    pop(C, B("AUCUNE CAUSE", 96, "cream", "ink", seed=11), 540, 300, T, 17.22, rot=-2)


def d7(C, T, t):
    pop(C, B("", 90, "brick", "cream", lines=["DÉCISION", "ÉTONNANTE"], seed=12), 540, 330, T, 18.96, rot=-2)
    pop(C, memo("gav", S.gavel_sprite), 560, 800, T, 19.5, s=1.3, rot=-8)
    pop(C, memo("doc", S.doc_sprite), 250, 960, T, 19.9, s=0.7, rot=-6)


def d8(C, T, t):
    pop(C, memo("stage", stage), 540, 900, T, 21.0, s=1.15)
    pop(C, B("UNE SCÈNE", 100, "cream", "ink", seed=13), 540, 310, T, 21.13, rot=-2)
    pop(C, memo("drum", drum), 330, 740, T, 22.23, s=0.9, rot=-5)
    pop(C, memo("trump", trumpet), 760, 760, T, 22.6, s=0.8, rot=8)
    pop(C, B("DES MUSICIENS", 70, "mustard", "ink", seed=14), 540, 1150, T, 22.62, rot=2)
    for i in range(3):
        if T >= 23.0:
            put(C, memo("note", note), 400 + i * 150, 560 - 50 * ((T * .8 + i * .3) % 1), 0.6, 8 * i - 8, 1 - ((T * .8 + i * .3) % 1))


def d9(C, T, t):
    for i in range(8):
        c, r = i % 4, i // 4
        dancer(C, T, 220 + c * 210, 700 + r * 200, COLS[i % 6], i * 1.7, s=0.8, t0=23.56 + .05 * i)
    pop(C, B("ET ILS DANSENT", 90, "orange", "cream", seed=15), 540, 310, T, 23.95, rot=-2)


def d10(C, T, t):
    slam(C, B("ÇA EMPIRE", 130, "brick", "cream", seed=16), 540, 330, T, 24.88, rot=-3)
    for i in range(6):
        pop(C, person_sprite(COLS[i], 340 + i), 200 + i * 130, 860 + (i % 2) * 60, T, 26.5 + 0.15 * i, s=0.8, rot=(70 if i % 2 else -80))
    pop(C, B("ÉPUISEMENT", 84, "mustard", "ink", seed=17), 540, 1160, T, 27.09, rot=2)


def d11(C, T, t):
    pop(C, memo("chapel", chapel), 540, 800, T, 29.0, s=1.2)
    for i in range(5):
        k = clamp((T - 29.0 - 0.1 * i) / 1.5)
        if T > 29.0:
            bput(C, person_sprite(COLS[i], 350 + i), 120 + 130 * i * (0.6 + 0.4 * k), 1000 - 120 * k, T, s=0.4)
    pop(C, B("", 80, "cream", "ink", lines=["PÈLERINAGE"], seed=18), 540, 300, T, 29.48, rot=-2)
    pop(C, B("SAINT GUY", 90, "mustard", "ink", seed=19), 540, 1160, T, 31.03, rot=2)


def d12(C, T, t):
    slam(C, memo("stamp3", lambda: Builder(560, 200, seed=220).poly(rrect_pts(14, 14, 546, 186, 22), P["teal"], rough=2, holes=[rrect_pts(34, 34, 526, 166, 14)]).text(280, 100, "FINI", "Anton", 120, P["teal"]).done()), 540, 760, T, 31.93, rot=-6, s=1.4)
    pop(C, B("L'ÉPIDÉMIE S'ARRÊTE", 62, "cream", "ink", seed=20), 540, 330, T, 32.0, rot=-2)


def d13(C, T, t):
    pop(C, memo("doc", S.doc_sprite), 540, 760, T, 33.3, s=1.0, rot=-3)
    pop(C, B("LES HISTORIENS", 84, "cream", "ink", seed=21), 540, 300, T, 33.26, rot=-2)
    if T >= 34.71:
        slam(C, B("", 84, "brick", "cream", lines=["HYSTÉRIE", "COLLECTIVE"], seed=22), 540, 1090, T, 34.71, rot=2)


def d14(C, T, t):
    pop(C, memo("q1", lambda: A.cut_text("?", "Anton", 640, P["orange"])), 540, 760, T, 36.4, s=1.0, rot=-6)
    pop(C, B("PERSONNE NE SAIT", 84, "cream", "ink", seed=23), 540, 300, T, 36.26, rot=-2)
    pop(C, B("POURQUOI", 100, "mustard", "ink", seed=24), 540, 1150, T, 37.85, rot=2)


def d15(C, T, t):
    A.cta(C, T, 38.72, 40.42, 43.26, 43.83, 44.7)


SCENES = [
    (0.00, 3.45, d1), (3.45, 6.35, d2), (6.35, 10.15, d3), (10.15, 13.35, d4), (13.35, 16.4, d5),
    (16.4, 18.85, d6), (18.85, 20.9, d7), (20.9, 23.5, d8), (23.5, 24.7, d9), (24.7, 28.95, d10),
    (28.95, 31.8, d11), (31.8, 33.1, d12), (33.1, 36.1, d13), (36.1, 38.6, d14), (38.6, 99.0, d15),
]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [11.68, 15.17, 24.88, 31.93, 34.71]
POPS = [40.42, 43.26, 43.83]
