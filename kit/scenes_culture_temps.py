"""Storyboard Culture G « Le temps »."""
import math
import papercut as pc
import scenes as S
import scenes_alcatraz as A
import scenes_culture_fonds_marins as F
import scenes_culture_espace as E
from papercut import (PAL, Builder, put, pop, slam, cue, ease_out, clamp)
from scenes import B, memo

P = PAL
num = F.num


def pyramid_sprite():
    def mk():
        b = Builder(360, 280, seed=801)
        b.poly([(20, 260), (180, 30), (340, 260)], P["mustard"], rough=2)
        b.poly([(180, 30), (340, 260), (230, 260)], P["orange"], rough=1.5, shadow=False)
        return b.done()
    return memo("pyr", mk)


def rocket_sprite():
    def mk():
        b = Builder(200, 360, seed=802)
        b.rect(70, 90, 130, 290, P["cream"], rough=1.5)
        b.poly([(70, 90), (100, 20), (130, 90)], P["brick"], rough=1.2, shadow=False)
        b.poly([(70, 230), (30, 310), (70, 290)], P["brick"], rough=1.2, shadow=False)
        b.poly([(130, 230), (170, 310), (130, 290)], P["brick"], rough=1.2, shadow=False)
        b.ell(100, 150, 16, 16, P["teal"], rough=1, shadow=False)
        return b.done()
    return memo("rocket", mk)


def queen_sprite():
    def mk():
        b = Builder(240, 300, seed=803)
        b.poly([(50, 290), (70, 150), (170, 150), (190, 290)], P["teal"], rough=1.5)
        b.ell(120, 100, 44, 48, P["cream"], rough=1.2)
        b.rect(76, 40, 164, 62, P["mustard"], rough=1, shadow=False)
        b.poly([(76, 40), (90, 10), (105, 40), (120, 5), (135, 40), (150, 10), (164, 40)], P["mustard"], rough=1, shadow=False)
        return b.done()
    return memo("queen", mk)


def atom_sprite():
    def mk():
        b = Builder(420, 420, seed=804)
        b.ell(210, 210, 190, 70, P["cream"], rough=1.5, shadow=False)
        b.ell(210, 210, 175, 56, P["navy"], rough=1.2, shadow=False)
        b.ell(210, 210, 70, 190, P["cream"], rough=1.5, shadow=False)
        b.ell(210, 210, 56, 175, P["navy"], rough=1.2, shadow=False)
        b.ell(210, 210, 46, 46, P["orange"], rough=1.5)
        return b.done()
    return memo("atom", mk)


def cal_sprite():
    def mk():
        b = Builder(700, 360, seed=805)
        b.rect(10, 10, 690, 350, P["cream"], rough=2)
        b.rect(10, 10, 690, 80, P["brick"], rough=1.5, shadow=False)
        b.text(350, 48, "OCTOBRE 1582", "Anton", 52, P["cream"], anchor="mm")
        for i in range(15):
            x = 60 + (i % 5) * 120
            y = 150 + (i // 5) * 70
            gone = 4 <= i <= 13
            b.text(x, y, str(i + 1), "Anton", 48, P["brick"] if gone else P["ink"], anchor="mm")
            if gone:
                b.bar(x - 28, y + 4, x + 28, y - 4, 7, P["brick"], rough=0.6, shadow=False)
        return b.done()
    return memo("cal", mk)


def dot(seed, col="cream"):
    return E.dot(seed, col)


def c1(C, T, t):
    slam(C, num("243 JOURS", 230), 540, 400, T, 0.1)
    pop(C, E.venus_sprite(), 540, 800, T, 1.0, s=1.4, rot=-4)
    if T < 6.2:
        pop(C, B("1 JOUR SUR VÉNUS", 70, "cream", "ink", seed=2), 540, 1130, T, 2.4, rot=-2)
    if T >= 6.2:
        slam(C, num("225 JOURS", 150), 540, 1060, T, 6.3)
        pop(C, B("1 AN SUR VÉNUS", 70, "mustard", "ink", seed=3), 540, 1200, T, 6.5, rot=2)
    if T >= 8.4:
        pop(C, B("JOUR > ANNÉE", 100, "brick", "cream", seed=4), 540, 300, T, 8.5, rot=-2)


def c2(C, T, t):
    pop(C, B("LA SECONDE", 100, "cream", "ink", seed=5), 540, 310, T, 10.0, rot=-2)
    pop(C, atom_sprite(), 540, 700, T, 11.0, s=1.0, rot=0)
    a = T * 3
    for i in range(3):
        put(C, dot(30 + i, "mustard"), 540 + 190 * math.cos(a + i * 2.1), 700 + 70 * math.sin(a + i * 2.1), 0.5, 0, 1)
    if T >= 11.2:
        pop(C, B("DEPUIS 1967", 66, "orange", "cream", seed=6), 540, 910, T, 11.3, rot=2)
    if T >= 13.5:
        pop(C, B("ATOME DE CÉSIUM", 62, "teal", "cream", seed=7), 540, 1020, T, 13.6, rot=-2)
    if T >= 15.0:
        slam(C, num("9 192 631 770", 140), 540, 1190, T, 15.05)


def c3(C, T, t):
    pop(C, B("CLÉOPÂTRE", 100, "cream", "ink", seed=8), 540, 310, T, 20.0, rot=-2)
    pop(C, queen_sprite(), 540, 700, T, 20.5, s=1.0, rot=-3)
    if T >= 21.5:
        pop(C, B("MORTE EN -30", 66, "mustard", "ink", seed=9), 300, 940, T, 21.6, rot=2)
    if T >= 23.5:
        pop(C, rocket_sprite(), 870, 700, T, 24.0, s=0.8, rot=8)
        pop(C, B("APOLLO 11", 56, "teal", "cream", seed=10), 800, 940, T, 24.2, rot=-2)
    if T >= 26.4:
        pop(C, pyramid_sprite(), 210, 720, T, 26.5, s=0.62, rot=-6)
    if T >= 25.0:
        slam(C, num("ENV. 2 000 ANS", 110), 540, 1060, T, 25.1)
    if T >= 27.8:
        slam(C, num("ENV. 2 500 ANS", 110, "brick"), 540, 1190, T, 27.9)


def c4(C, T, t):
    pop(C, B("OCTOBRE 1582", 90, "cream", "ink", seed=11), 540, 310, T, 28.9, rot=-2)
    pop(C, cal_sprite(), 540, 680, T, 29.3, s=1.25, rot=-2)
    if T >= 30.8:
        slam(C, num("10 JOURS", 190), 540, 1010, T, 30.9)
    if T >= 31.6:
        pop(C, B("DISPARUS", 80, "brick", "cream", seed=12), 540, 1160, T, 31.7, rot=2)
    if T >= 33.1:
        pop(C, B("DU 4 AU 15", 100, "orange", "cream", seed=13), 540, 1160, T, 33.1, rot=-2)


def c5(C, T, t):
    A.cta(C, T, 35.5, 37.0, 39.6, 40.0, 40.9)


SCENES = [(0.0, 9.9, c1), (9.9, 19.0, c2), (19.0, 28.6, c3), (28.6, 35.3, c4), (35.3, 99.0, c5)]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [0.1, 6.3, 15.05, 25.1, 30.9]
POPS = [39.6, 40.0]
