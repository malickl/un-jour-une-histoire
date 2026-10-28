"""Storyboard « Le casse de Nice » : scènes en papier découpé calées sur le timing des mots."""
import math
import random

from PIL import Image

import papercut as pc
from papercut import (PAL, W, H, Builder, banner, bput, put, pop, slam, slide, cue, ease_out, back,
                      clamp, shake, ell_pts, rrect_pts, rect_pts, burst_pts, bar_pts)

P = PAL
_S = {}


def memo(key, fn):
    if key not in _S:
        _S[key] = fn()
    return _S[key]


def B(txt, size=110, fill="cream", ink="navy", lines=None, seed=1):
    return memo(("B", txt, size, fill, ink, tuple(lines or ()), seed),
                lambda: banner(txt, size, fill, ink, lines=lines, seed=seed))


# ====================================================================== sprites
def bank_sprite():
    b = Builder(760, 640, seed=3)
    b.poly([(40, 175), (380, 18), (720, 175)], P["cream"], rough=2)
    b.rect(60, 175, 700, 222, P["cream_d"])
    b.text(380, 199, "BANQUE", "ArchivoBlack", 34, P["ink"])
    for x0 in (95, 205, 465, 575):
        b.rect(x0 - 8, 222, x0 + 78, 246, P["cream_d"])
        b.rect(x0, 246, x0 + 70, 480, P["cream"])
        b.rect(x0 - 8, 480, x0 + 78, 500, P["cream_d"])
    b.rect(310, 232, 450, 500, P["navy_d"])
    b.rect(322, 244, 438, 500, P["orange"], rough=1)
    b.rect(334, 256, 426, 500, P["navy_d"], rough=1)
    for i, (x0, x1) in enumerate([(50, 710), (28, 732), (6, 754)]):
        b.rect(x0, 500 + i * 46, x1, 546 + i * 46, [P["mustard"], P["cream_d"], P["mustard"]][i])
    b.ell(380, 100, 34, 34, P["mustard"])
    b.text(380, 102, "F", "ArchivoBlack", 40, P["ink"])
    return b.done()


def manhole_hole():
    b = Builder(330, 150, seed=4)
    b.ell(165, 78, 150, 56, P["navy_d"], shadow=False)
    b.ell(165, 84, 120, 36, (6, 10, 24), shadow=False)
    return b.done()


def manhole_lid():
    b = Builder(330, 150, seed=5)
    b.ell(165, 82, 150, 58, P["brick"])
    b.ell(165, 74, 150, 58, P["mustard"])
    b.ell(165, 74, 118, 42, P["orange"], rough=1)
    for k in range(-3, 4):
        b.bar(165 + k * 26 - 30, 74 - 30, 165 + k * 26 + 30, 74 + 30, 8, P["mustard"], rough=0.8, shadow=False)
    return b.done()


def palm_sprite():
    b = Builder(420, 620, seed=6)
    b.poly([(170, 600), (215, 600), (232, 200), (205, 120), (190, 130), (175, 330)], P["brick"], rough=1.6)
    for k in range(5):
        y = 520 - k * 70
        b.bar(176 + k * 3, y, 214 + k * 2, y - 8, 12, P["brick_l"], rough=0.6, shadow=False)
    cx, cy = 215, 130
    for ang, ln, col in [(-165, 190, P["teal"]), (-130, 200, P["teal_l"]), (-95, 175, P["teal"]),
                         (-55, 200, P["teal_l"]), (-20, 195, P["teal"]), (-195, 150, P["teal_l"]), (15, 150, P["teal_l"])]:
        a = math.radians(ang)
        ex, ey = cx + ln * math.cos(a), cy + ln * math.sin(a) + 40
        mx, my = (cx + ex) / 2, (cy + ey) / 2 - 36
        nx, ny = -math.sin(a) * 26, math.cos(a) * 26
        b.poly([(cx, cy), (mx + nx, my + ny), (ex, ey), (mx - nx, my - ny)], col, rough=1.8)
    b.ell(cx, cy + 6, 22, 20, P["brick"])
    return b.done()


def sun_sprite():
    b = Builder(420, 420, seed=7)
    b.poly(burst_pts(210, 210, 200, 150, n=16), P["mustard"], rough=1.5)
    b.ell(210, 210, 122, 122, P["orange"])
    return b.done()


def waves_sprite(color, seed, amp=18, wl=170):
    b = Builder(1180, 170, seed=seed)
    top = [(x, 60 + amp * math.sin(x / wl * 2 * math.pi)) for x in range(0, 1181, 30)]
    b.poly(top + [(1180, 170), (0, 170)], color, rough=1.2)
    return b.done()


def calendar_sprite(month, big, seed=8):
    def mk():
        b = Builder(560, 380, seed=seed)
        b.rrect(20, 28, 540, 360, 26, P["cream"], rough=1.6)
        b.rrect(20, 28, 540, 128, 26, P["orange"], rough=1.4)
        b.rect(20, 90, 540, 128, P["orange"], rough=1.0, shadow=False)
        for x in (130, 430):
            b.ring(x, 28, 24, 11, P["navy_l"], rough=0.8)
        b.text(280, 82, month, "Anton", 64, P["cream"])
        b.text(280, 246, big, "Anton", 150 if len(big) <= 4 else 110, P["navy"])
        return b.done()
    return memo(("cal", month, big), mk)


def vault_door():
    b = Builder(640, 640, seed=9)
    b.ell(320, 320, 300, 300, (118, 130, 156))
    b.ell(320, 320, 262, 262, (150, 162, 186))
    b.ring(320, 320, 224, 196, (118, 130, 156), rough=1)
    for k in range(12):
        a = math.radians(k * 30)
        b.ell(320 + 244 * math.cos(a), 320 + 244 * math.sin(a), 11, 11, P["mustard"], rough=0.6)
    for k in range(3):
        a = math.radians(k * 120 + 30)
        b.bar(320, 320, 320 + 190 * math.cos(a), 320 + 190 * math.sin(a), 26, P["mustard"], rough=1)
        b.ell(320 + 190 * math.cos(a), 320 + 190 * math.sin(a), 22, 22, P["orange"], rough=0.8)
    b.ell(320, 320, 62, 62, P["orange"])
    b.ell(320, 320, 30, 30, P["mustard"])
    return b.done()


def vault_hole():
    b = Builder(640, 640, seed=10)
    b.ell(320, 320, 300, 300, P["navy_d"], shadow=False)
    b.ell(320, 320, 262, 262, (8, 12, 30), rough=2, shadow=False)
    for k, (x, y, r) in enumerate([(220, 470, 60), (340, 500, 66), (450, 450, 56), (290, 400, 50), (400, 380, 46)]):
        b.ell(x, y, r, r * 0.5, P["mustard"], rough=1.4, shadow=False)
        b.ell(x, y - 8, r, r * 0.5, P["orange"], rough=1.4, shadow=False)
    return b.done()


def person_sprite(body, seed=11, hat=False, arms_up=False):
    def mk():
        b = Builder(160, 330, seed=seed)
        b.poly(rrect_pts(36, 110, 124, 250, 30), P[body], rough=1.2)
        b.rect(48, 236, 74, 316, P["navy_d"], rough=1)
        b.rect(86, 236, 112, 316, P["navy_d"], rough=1)
        if arms_up:
            b.bar(46, 130, 12, 40, 20, P[body], rough=0.8)
            b.bar(114, 130, 148, 40, 20, P[body], rough=0.8)
        else:
            b.bar(44, 128, 24, 220, 20, P[body], rough=0.8)
            b.bar(116, 128, 136, 220, 20, P[body], rough=0.8)
        b.ell(80, 74, 34, 36, P["cream_d"])
        if hat:
            b.rect(34, 52, 126, 64, P["ink"], rough=0.8)
            b.poly(rrect_pts(48, 22, 112, 60, 10), P["ink"], rough=0.8)
        return b.done()
    return memo(("person", body, hat, arms_up), mk)


def boxes_sprite(opened):
    def mk():
        b = Builder(780, 640, seed=12)
        b.rect(10, 10, 770, 630, P["navy_l"], rough=1.6)
        rnd = random.Random(5)
        for r in range(5):
            for c in range(6):
                x0, y0 = 28 + c * 123, 28 + r * 122
                if opened and rnd.random() < 0.72:
                    b.rect(x0, y0, x0 + 108, y0 + 108, P["navy_d"], rough=0.8, shadow=False)
                    b.rect(x0 + 10, y0 + 10, x0 + 98, y0 + 98, (6, 10, 24), rough=0.6, shadow=False)
                    b.poly([(x0 + 108, y0 + 4), (x0 + 150, y0 - 6), (x0 + 150, y0 + 100), (x0 + 108, y0 + 108)],
                           P["grey"], rough=0.8)
                else:
                    b.rect(x0, y0, x0 + 108, y0 + 108, (160, 170, 190), rough=0.8)
                    b.ell(x0 + 54, y0 + 54, 12, 12, P["mustard"], rough=0.5, shadow=False)
                    b.rect(x0 + 20, y0 + 20, x0 + 88, y0 + 28, (190, 198, 214), rough=0.5, shadow=False)
        return b.done()
    return memo(("boxes", opened), mk)


def wall_sprite():
    b = Builder(900, 620, seed=13)
    b.rect(10, 10, 890, 610, P["cream_d"], rough=2)
    rnd = random.Random(9)
    for r in range(11):
        off = 0 if r % 2 == 0 else -60
        for c in range(9):
            x0 = 16 + off + c * 120
            lo, hi = max(16, x0), min(884, x0 + 112)
            if hi - lo < 18:
                continue
            col = rnd.choice([P["brick"], P["brick_l"], (186, 80, 56), (160, 58, 42)])
            b.rect(lo, 16 + r * 54, hi, 16 + r * 54 + 46, col, rough=0.7, shadow=False, tex=0.08)
    return b.done()


def note_line(txt, seed, fill="cream", ink="ink"):
    return B(txt, 100, fill, ink, seed=seed)


def ground_sprite():
    b = Builder(1000, 700, seed=14)
    b.rect(10, 90, 990, 690, P["brick_l"], rough=2, tex=0.07)
    b.rect(10, 90, 990, 150, P["teal"], rough=2)
    for k in range(9):
        b.ell(80 + k * 105, 300 + (k % 3) * 120, 26 + (k % 2) * 10, 16, P["brick"], rough=1, shadow=False)
    b.rect(10, 90, 990, 150, P["teal"], rough=1.5, shadow=False)
    return b.done()


def tunnel_sprite():
    b = Builder(780, 110, seed=15)
    b.rrect(10, 14, 770, 96, 40, P["navy_d"], rough=1.6, shadow=False)
    b.rrect(24, 28, 756, 82, 28, (8, 12, 28), rough=1.2, shadow=False)
    return b.done()


def pipe_sprite():
    b = Builder(1000, 70, seed=16)
    b.rrect(8, 8, 992, 62, 24, P["teal"], rough=1.4)
    b.rrect(20, 20, 980, 50, 14, P["navy_d"], rough=1, shadow=False)
    return b.done()


def pick_sprite():
    b = Builder(220, 220, seed=17)
    b.bar(60, 190, 160, 50, 20, P["cream_d"], rough=1)
    b.poly([(20, 70), (110, 14), (200, 70), (170, 56), (110, 40), (50, 56)], P["grey"], rough=1)
    return b.done()


def plate_sprite():
    b = Builder(560, 300, seed=18)
    b.ell(280, 170, 250, 100, P["cream"])
    b.ell(280, 164, 200, 72, P["cream_d"], rough=1, shadow=False)
    b.ell(280, 162, 130, 44, P["brick_l"], rough=1.6)
    b.ell(250, 152, 26, 12, P["mustard"], rough=1, shadow=False)
    b.ell(310, 168, 30, 12, P["teal_l"], rough=1, shadow=False)
    return b.done()


def baguette_sprite():
    b = Builder(560, 160, seed=19)
    b.poly(rrect_pts(14, 40, 546, 120, 40), P["mustard"], rough=1.4)
    for k in range(5):
        x = 90 + k * 100
        b.bar(x, 52, x + 40, 108, 14, P["orange"], rough=0.8, shadow=False)
    return b.done()


def bottle_sprite():
    b = Builder(190, 460, seed=20)
    b.rrect(34, 150, 156, 440, 30, P["teal"], rough=1.2)
    b.rect(76, 36, 114, 170, P["teal"], rough=1)
    b.rect(80, 14, 110, 52, P["brick"], rough=1)
    b.rect(44, 270, 146, 370, P["cream"], rough=1, shadow=False)
    b.text(95, 320, "CRU", "Anton", 44, P["ink"])
    return b.done()


def fork_sprite():
    b = Builder(80, 360, seed=21)
    b.bar(40, 130, 40, 340, 18, P["grey"], rough=0.7)
    for x in (16, 32, 48, 64):
        b.bar(x, 20, x, 140, 9, P["grey"], rough=0.6, shadow=False)
    b.rect(14, 118, 68, 144, P["grey"], rough=0.7, shadow=False)
    return b.done()


def sack_sprite(seed=22):
    b = Builder(360, 420, seed=seed)
    b.poly(ell_pts(180, 270, 150, 130) , P["mustard"], rough=2)
    b.poly([(120, 160), (240, 160), (270, 110), (90, 110)], P["mustard"], rough=1.5)
    b.bar(100, 150, 260, 150, 18, P["brick"], rough=1)
    b.ell(180, 270, 78, 78, P["cream"], rough=1.4, shadow=False)
    b.text(180, 274, "F", "Anton", 120, P["brick"])
    return b.done()


def coin_stack(n=5, seed=23):
    b = Builder(240, 90 + 34 * n, seed=seed)
    for i in range(n):
        y = 40 + (n - 1 - i) * 34
        b.ell(120, y + 30, 100, 32, P["orange"], rough=1)
        b.ell(120, y + 20, 100, 32, P["mustard"], rough=1)
    b.ell(120, 28 + 20, 60, 16, P["orange"], rough=0.8, shadow=False)
    return b.done()


def silhouette_card():
    b = Builder(520, 720, seed=24)
    b.rrect(14, 14, 506, 706, 22, P["cream"], rough=2)
    b.rect(36, 36, 484, 110, P["brick"], rough=1.4)
    b.text(260, 74, "LE CERVEAU", "Anton", 58, P["cream"])
    b.rect(60, 140, 460, 640, P["navy_l"], rough=1.2)
    b.ell(260, 340, 82, 92, P["ink"])
    b.poly([(70, 640), (110, 520), (200, 462), (320, 462), (410, 520), (450, 640)], P["ink"], rough=1.2)
    b.rect(160, 268, 360, 292, P["ink"], rough=0.8)
    b.poly(rrect_pts(184, 196, 336, 276, 14), P["ink"], rough=0.8)
    return b.done()


def cuffs_sprite(opened=False):
    def mk():
        b = Builder(560, 300, seed=26)
        b.ring(130, 160, 100, 56, P["grey"], rough=1)
        b.rect(94, 40, 166, 70, (170, 178, 198), rough=0.8, shadow=False)
        for k in range(6):
            x = 235 + k * 18
            b.ring(x, 160 + (6 if k % 2 else -6), 15, 7, (170, 178, 198), rough=0.5, shadow=False)
        if opened:
            b.poly(ell_pts(430, 160, 100, 100, a0=40, a1=330), (150, 160, 184), holes=None, rough=1)
            b.poly(ell_pts(430, 160, 56, 56, a0=40, a1=330), P["navy"], rough=0.5, shadow=False)
        else:
            b.ring(430, 160, 100, 56, P["grey"], rough=1)
        return b.done()
    return memo(("cuffs", opened), mk)


def gavel_sprite():
    b = Builder(420, 420, seed=27)
    b.bar(130, 380, 280, 170, 30, P["brick"], rough=1)
    b.poly(rrect_pts(150, 40, 340, 170, 18), P["mustard"], rough=1.4)
    b.rect(150, 40, 175, 170, P["orange"], rough=1, shadow=False)
    b.rect(315, 40, 340, 170, P["orange"], rough=1, shadow=False)
    return b.done()


def facade_sprite():
    b = Builder(900, 760, seed=28)
    b.rect(20, 20, 880, 740, P["cream_d"], rough=2)
    b.rect(20, 20, 880, 80, P["cream"], rough=1.4)
    b.rect(310, 140, 590, 470, P["navy_d"], rough=1.2)
    b.rect(330, 160, 570, 450, (28, 44, 80), rough=1, shadow=False)
    b.rect(446, 160, 454, 450, P["cream_d"], rough=0.8, shadow=False)
    b.rect(330, 300, 570, 308, P["cream_d"], rough=0.8, shadow=False)
    b.rect(290, 470, 610, 500, P["cream"], rough=1.2)
    for x in (80, 700):
        b.rect(x, 140, x + 120, 470, P["cream"], rough=1.2)
    b.rect(20, 620, 880, 740, P["brick_l"], rough=1.6)
    return b.done()


def car_sprite():
    b = Builder(520, 260, seed=29)
    b.poly(rrect_pts(20, 110, 500, 210, 30), P["brick"], rough=1.4)
    b.poly([(120, 112), (190, 30), (350, 30), (420, 112)], P["brick_l"], rough=1.4)
    b.poly([(142, 108), (198, 48), (260, 48), (260, 108)], P["teal_l"], rough=1, shadow=False)
    b.poly([(276, 108), (276, 48), (344, 48), (400, 108)], P["teal_l"], rough=1, shadow=False)
    for x in (120, 400):
        b.ell(x, 214, 46, 46, P["ink"])
        b.ell(x, 214, 20, 20, P["cream_d"], rough=0.6, shadow=False)
    b.ell(484, 150, 12, 12, P["mustard"], rough=0.5, shadow=False)
    return b.done()


def puff_sprite(seed=30):
    b = Builder(300, 240, seed=seed)
    for cx, cy, r in [(90, 130, 70), (160, 90, 80), (220, 140, 66), (150, 160, 70)]:
        b.ell(cx, cy, r, r, P["cream"], rough=2)
    return b.done()


def bird_sprite():
    b = Builder(340, 220, seed=31)
    b.poly([(170, 120), (20, 40), (96, 120), (30, 70)][:3] + [(170, 120)], P["cream"], rough=1.2)
    b.poly([(170, 120), (320, 40), (244, 120)], P["cream"], rough=1.2)
    b.ell(170, 128, 56, 34, P["cream"], rough=1.2)
    b.poly([(214, 118), (262, 128), (214, 138)], P["orange"], rough=0.8, shadow=False)
    b.ell(196, 118, 5, 5, P["ink"], rough=0.3, shadow=False)
    return b.done()


def doc_sprite():
    b = Builder(360, 460, seed=38)
    b.rect(20, 20, 340, 440, P["cream"], rough=2)
    b.rect(60, 60, 240, 80, P["ink"], rough=0.8, shadow=False)
    for k in range(7):
        b.rect(60, 120 + k * 42, 300 - (40 if k % 3 == 2 else 0), 134 + k * 42, P["grey"], rough=0.8, shadow=False)
    b.ell(270, 380, 46, 46, P["brick"], rough=1.4, shadow=False)
    return b.done()


def heart_pts(cx, cy, s):
    pts = []
    for k in range(60):
        t = math.pi * 2 * k / 60
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * s, cy - y * s))
    return pts


def heart_sprite(color="brick", seed=32):
    return memo(("heart", color), lambda: Builder(380, 360, seed=seed).poly(heart_pts(190, 180, 9.4), P[color], rough=1.2).done())


def bubble_sprite():
    b = Builder(620, 420, seed=33)
    b.poly(rrect_pts(20, 20, 600, 320, 60), P["cream"], rough=1.8)
    b.poly([(110, 300), (170, 300), (90, 392)], P["cream"], rough=1.2, shadow=False)
    for k in range(3):
        b.ell(210 + k * 100, 170, 26, 26, P["navy"], rough=0.8, shadow=False)
    return b.done()


def button_sprite():
    b = Builder(640, 200, seed=34)
    b.poly(rrect_pts(20, 20, 620, 180, 80), P["orange"], rough=1.6)
    b.text(320, 104, "S'ABONNER +", "Anton", 92, P["cream"])
    return b.done()


def finger_sprite():
    b = Builder(200, 260, seed=35)
    b.poly(rrect_pts(70, 10, 130, 150, 28), P["cream"], rough=1)
    b.poly(rrect_pts(30, 120, 170, 240, 44), P["cream"], rough=1)
    return b.done()


def burst_sprite(color="orange", r=520, seed=36):
    return memo(("burst", color, r), lambda: Builder(r * 2 + 20, r * 2 + 20, seed=seed).poly(
        burst_pts(r + 10, r + 10, r, r * 0.62, n=18), P[color], rough=2).done())


def stamp_sprite():
    b = Builder(560, 200, seed=37)
    b.poly(rrect_pts(14, 14, 546, 186, 22), P["brick"], rough=2,
           holes=[rrect_pts(34, 34, 526, 166, 14)])
    b.text(280, 100, "ARRÊTÉ", "Anton", 120, P["brick"])
    return b.done()


def sweep_sprites():
    def mk():
        a = Builder(1700, 2500, seed=40, shadow=False)
        a.poly([(60, 40), (1640, 20), (1620, 2480), (80, 2470)], P["orange"], rough=7, tex=0.03, shadow=False)
        c = Builder(1700, 2500, seed=41, shadow=True)
        c.poly([(120, 30), (1580, 50), (1600, 2470), (100, 2480)], P["cream"], rough=7, tex=0.03)
        return (a.done().rotate(11, expand=True, resample=Image.BILINEAR),
                c.done().rotate(11, expand=True, resample=Image.BILINEAR))
    return memo("sweep", mk)


# ====================================================================== scènes
CY = 700   # centre de la zone d'illustration


def sc1(C, T, t):
    bank = memo("bank", bank_sprite)
    pop(C, bank, 540, 660, T, 0.05, s=0.95, d=0.4)
    hole, lid = memo("hole", manhole_hole), memo("lid", manhole_lid)
    pop(C, hole, 540, 1010, T, 0.45, s=1.0)
    p = ease_out(cue(T, 1.0, 0.45))
    pop(C, lid, 540 + 320 * p, 1000 - 40 * p, T, 0.45, s=1.0, rot=-28 * p)
    slam(C, B("UNE BANQUE VIDÉE", 112), 540, 290, T, 0.10)
    pop(C, B("PAR LES ÉGOUTS", 100, "orange", "cream", seed=2), 540, 1170, T, 2.0, rot=-2)


def sc2(C, T, t):
    pop(C, memo("sun", sun_sprite), 820, 520, T, 3.28, s=0.9)
    for i, (col, y, sd) in enumerate([(P["teal"], 1080, 51), (P["teal_l"], 1130, 52)]):
        w = memo(("wave", i), lambda c=col, s=sd: waves_sprite(c, s))
        slide(C, w, (540 - 500, y), (540 + (20 if i else -10), y), T, 3.25 + 0.06 * i, 0.5)
    pop(C, memo("palm", palm_sprite), 280, 760, T, 3.3, s=1.05, rot=-3)
    slam(C, B("NICE", 140), 540, 300, T, 3.34, rot=-2)
    pop(C, calendar_sprite("JUILLET", "1976"), 760, 920, T, 4.12, s=0.9, rot=4)


def sc3(C, T, t):
    slam(C, B("LUNDI MATIN", 112, "mustard", "ink"), 540, 290, T, 6.25, rot=-2)
    bank = memo("bank", bank_sprite)
    pop(C, bank, 270, 660, T, 6.5, s=0.72)
    pop(C, memo("pers_a", lambda: person_sprite("teal", 41)), 150, 1070, T, 7.5, s=0.85)
    pop(C, memo("pers_b", lambda: person_sprite("orange", 42)), 270, 1090, T, 7.7, s=0.75)
    pop(C, B("SOCIÉTÉ GÉNÉRALE", 70, "cream", "ink", seed=3), 540, 470, T, 8.13, rot=-1.5)
    vh, vd = memo("vh", vault_hole), memo("vd", vault_door)
    pop(C, vh, 770, 860, T, 9.0, s=0.78)
    op = ease_out(cue(T, 9.15, 0.6))
    if T >= 9.0:
        scl = back(cue(T, 9.0, 0.34)) * 0.78
        sq = pc.squash(vd, scl * (1 - 0.78 * op), scl)
        put(C, sq, 770 - 235 * op * scl / 0.78, 860, 1, 0, clamp(cue(T, 9.0, 0.34) * 3))
    pop(C, B("LA SALLE DES COFFRES", 66, "orange", "cream", seed=4), 600, 1170, T, 9.42, rot=2)


def sc4(C, T, t):
    dx, dy = shake(T, 10.58, 0.4, 22)
    pc.CAM[0], pc.CAM[1] = dx, dy
    pop(C, memo(("boxes", False), lambda: boxes_sprite(False)), 540, 800, T, 10.45, s=1.0)
    if T >= 10.58:
        bput(C, memo(("boxes", True), lambda: boxes_sprite(True)), 540, 800, T)
        C.paste(Image.new("RGB", C.size, (255, 246, 224)), (0, 0),
                Image.new("L", C.size, int(255 * max(0, 1 - (T - 10.58) / 0.12) * 0.7)))
    slam(C, B("CHOC !", 190, "brick", "cream", seed=5), 540, 330, T, 10.58, rot=-4)
    pop(C, B("DES CENTAINES DE COFFRES", 60, "cream", "ink", seed=6), 540, 1190, T, 11.54, rot=1.5)


def sc5(C, T, t):
    pop(C, B("SUR UN MUR :", 100, "mustard", "ink", seed=7), 540, 290, T, 13.6, rot=-2)
    pop(C, memo("wall", wall_sprite), 540, 800, T, 13.7, s=1.0)
    L = [("SANS ARMES,", 15.12, 650, -3), ("NI HAINE,", 16.11, 810, 2), ("NI VIOLENCE.", 16.71, 970, -2)]
    for i, (txt, t0, y, r) in enumerate(L):
        slam(C, note_line(txt, 50 + i), 540, y, T, t0, rot=r)


def sc6(C, T, t):
    pop(C, calendar_sprite("WEEK-END", "14 JUILLET"), 230, 470, T, 18.6, s=0.62, rot=-4)
    g = memo("ground", ground_sprite)
    pop(C, g, 540, 880, T, 17.98, s=1.0)
    for k, x in enumerate((180, 420, 760)):
        pop(C, memo(("house", k), lambda k=k: Builder(190, 200, seed=60 + k).rect(14, 70, 176, 190, P["cream"]).poly(
            [(4, 76), (95, 14), (186, 76)], P["brick"]).rect(70, 120, 118, 190, P["navy_d"]).done()), x, 706, T, 18.2 + 0.1 * k, s=0.8)
    pipe = memo("pipe", pipe_sprite)
    pop(C, pipe, 540, 980, T, 19.5, s=1.0)
    tun = memo("tun", tunnel_sprite)
    p = cue(T, 19.86, 2.9)
    if p > 0:
        full = tun
        cw = max(2, int(full.width * ease_out(p)))
        crop = full.crop((0, 0, cw, full.height))
        x_left = 540 - full.width / 2 + 40
        put(C, crop, x_left + cw / 2, 1100, 1.0, 0, 1.0)
        pick = memo("pick", pick_sprite)
        bput(C, pick, x_left + cw + 20, 1100, T, s=0.6, rot=-20 + 14 * math.sin(T * 14))
    pop(C, B("UN TUNNEL", 100, "orange", "cream", seed=8), 700, 330, T, 20.61, rot=1.5)
    pop(C, vault_door_small(), 880, 1100, T, 22.3, s=1.0)
    pop(C, B("SALLE BLINDÉE", 66, "cream", "ink", seed=9), 780, 570, T, 22.51, rot=-2)


def vault_door_small():
    return memo("vds", lambda: vault_door().resize((260, 260), Image.LANCZOS))


def sc7(C, T, t):
    pop(C, memo("plate", plate_sprite), 540, 880, T, 23.3, s=1.0)
    pop(C, memo("fork", fork_sprite), 220, 880, T, 23.5, s=1.0, rot=-6)
    pop(C, memo("bag", baguette_sprite), 590, 700, T, 23.7, s=1.0, rot=-12)
    pop(C, memo("bot", bottle_sprite), 880, 760, T, 23.9, s=1.0, rot=6)
    slam(C, B("ILS ONT MÊME MANGÉ !", 86, "mustard", "ink", seed=10), 540, 320, T, 23.63, rot=-2)


def sc8(C, T, t):
    slam(C, B("LE BUTIN", 130, "orange", "cream", seed=11), 540, 310, T, 25.36, rot=-2)
    pop(C, memo("sack1", sack_sprite), 300, 800, T, 25.8, s=1.25, rot=-6)
    pop(C, memo("sack2", lambda: sack_sprite(52)), 790, 830, T, 26.0, s=1.1, rot=7)
    pop(C, memo("coins", coin_stack), 540, 960, T, 26.5, s=1.35)
    pop(C, B("DES DIZAINES DE MILLIONS", 64, "cream", "ink", seed=12), 540, 1170, T, 26.7, rot=1)
    pop(C, B("DE FRANCS", 64, "mustard", "ink", seed=13), 540, 1250, T, 27.06, rot=-1)


def sc9(C, T, t):
    dx, dy = shake(T, 27.79, 0.4, 20)
    pc.CAM[0], pc.CAM[1] = dx, dy
    pop(C, burst_sprite("orange"), 540, 760, T, 27.74, s=0.9 + 0.04 * math.sin(T * 6), d=0.4)
    pop(C, burst_sprite("mustard", 400), 540, 760, T, 27.8, s=1.0, d=0.4)
    slam(C, B("", 150, lines=["LE CASSE", "DU SIÈCLE"], seed=14), 540, 760, T, 27.79, rot=-4)


def sc10(C, T, t):
    pop(C, memo("card", silhouette_card), 540, 760, T, 29.2, s=1.0, rot=-3)
    pop(C, B("ALBERT SPAGGIARI", 84, "cream", "ink", seed=15), 540, 1160, T, 30.23, rot=1.5)
    slam(C, memo("stamp", stamp_sprite), 700, 900, T, 31.68, rot=-14)
    pop(C, memo("cuffs", lambda: cuffs_sprite(False)), 330, 1010, T, 31.68, s=0.62, rot=8)
    pop(C, B("QUELQUES MOIS PLUS TARD", 52, "mustard", "ink", seed=16), 540, 340, T, 32.06, rot=-1)


def sc11a(C, T, t):
    m = ease_out(cue(T, 35.2, 0.45))
    cal = calendar_sprite("MARS", "1977")
    if T < 35.2:
        slam(C, cal, 540, 520, T, 33.55, s=0.95, rot=-3)
    else:
        bput(C, cal, 540 + (230 - 540) * m, 520 + (470 - 520) * m, T, s=0.95 + (0.62 - 0.95) * m, rot=-3)
    hit = cue(T, 36.08, 0.12)
    gav = memo("gavel", gavel_sprite)
    ang = -40 + 40 * ease_out(hit) if T >= 33.9 else -40
    pop(C, gav, 640, 1000, T, 35.3, s=0.9, rot=ang)
    pop(C, Builder(420, 90, seed=70).rrect(10, 10, 410, 80, 18, P["brick"]).done(), 470, 1130, T, 35.3)
    pop(C, memo("doc", doc_sprite), 330, 900, T, 34.1, s=0.9, rot=-6)
    pop(C, B("CHEZ LE JUGE", 90, "cream", "ink", seed=17), 700, 330, T, 35.46, rot=2)
    if T >= 36.08:
        for k in range(6):
            a = math.radians(-160 + k * 28)
            r0, r1 = 70, 70 + 90 * ease_out(cue(T, 36.08, 0.25))
            if r1 > 72:
                put(C, Builder(40, 40, seed=80).ell(20, 20, 10, 10, P["mustard"]).done(), 470 + r1 * math.cos(a), 1120 + r1 * math.sin(a),
                    1, 0, 1 - cue(T, 36.08, 0.4))


def sc11b(C, T, t):
    fac = memo("facade", facade_sprite)
    pop(C, fac, 400, 760, T, 36.75, s=0.95)
    car = memo("car", car_sprite)
    carx = 800 + (0 if T < 39.9 else 900 * ease_out(cue(T, 39.9, 0.5)) )
    slide(C, car, (1400, 1030), (carx if T >= 39.9 else 770, 1030), T, 37.6, 0.7)
    # saut
    pers = memo("pers_j", lambda: person_sprite("orange", 43, hat=True, arms_up=True))
    p = cue(T, 36.96, 1.7)
    if 0 < p < 1:
        x = 400 + (770 - 400) * p
        y = 690 + (830 - 690) * p - 190 * math.sin(math.pi * p)
        bput(C, pers, x, y, T, s=0.9, rot=-30 + 60 * p)
    elif p >= 1:
        fade = 1 - cue(T, 39.65, 0.35)
        sq = 1 - 0.18 * math.sin(math.pi * clamp((T - 38.65) / 0.25)) if T < 38.9 else 1
        put(C, pers, 770, 830, 0.9 * sq, 0, fade)
    if T >= 39.65:
        k = cue(T, 39.65, 0.5)
        for dx, dy, ss in [(-70, 0, 0.7), (40, -50, 0.9), (110, 20, 0.6)]:
            put(C, memo("puff", puff_sprite), 770 + dx, 800 + dy - 60 * k, ss * (0.5 + 0.9 * k), 0, 1 - k * 0.8)
    slam(C, B("IL SAUTE !", 120, "orange", "cream", seed=18), 540, 300, T, 36.96, rot=-3)
    if T >= 39.65:
        slam(C, B("DISPARU !", 120, "cream", "ink", seed=19), 540, 1160, T, 39.65, rot=2)


def sc12(C, T, t):
    pop(C, memo("cuffs_o", lambda: cuffs_sprite(True)), 540, 1000, T, 40.55, s=0.95, rot=-6)
    slam(C, B("JAMAIS RATTRAPÉ", 100, "mustard", "ink", seed=20), 540, 300, T, 41.11, rot=-2)
    pop(C, calendar_sprite("MEURT LIBRE", "1989"), 400, 640, T, 43.0, s=0.85, rot=-3)
    p = ease_out(cue(T, 43.56, 1.2))
    if p > 0:
        bput(C, memo("bird", bird_sprite), 600 + 380 * p, 900 - 380 * p, T, s=0.9 + 0.1 * math.sin(T * 12), rot=-18)


def sc13(C, T, t):
    pop(C, B("TU CONNAISSAIS ?", 110, "cream", "ink", seed=21), 540, 310, T, 45.15, rot=-2)
    pop(C, memo("bubble", bubble_sprite), 540, 640, T, 45.9, s=1.0, rot=-2)
    if T >= 47.43:
        pop(C, B("DIS-LE EN COMMENTAIRE", 64, "orange", "cream", seed=22), 540, 960, T, 47.43, rot=1.5)
    if T >= 49.69:
        h = memo("heart", lambda: heart_sprite("brick"))
        beat = 1 + 0.12 * max(0, math.sin((T - 49.82) * 9))
        pop(C, h, 230, 1110, T, 49.82, s=0.8 * beat, rot=-8)
    if T >= 50.27:
        btn = memo("btn", button_sprite)
        pop(C, btn, 690, 1110, T, 50.27, s=0.85)
        tap = cue(T, 51.2, 0.5)
        if tap > 0:
            put(C, memo("finger", finger_sprite), 880, 1190 - 20 * math.sin(tap * math.pi), 0.8, -10, 1)


SCENES = [
    (0.00, 3.20, sc1), (3.20, 5.95, sc2), (5.95, 10.45, sc3), (10.45, 13.30, sc4),
    (13.30, 17.85, sc5), (17.85, 23.25, sc6), (23.25, 25.15, sc7), (25.15, 27.72, sc8),
    (27.72, 29.15, sc9), (29.15, 33.35, sc10), (33.35, 36.75, sc11a), (36.75, 40.50, sc11b),
    (40.50, 45.00, sc12), (45.00, 99.0, sc13),
]
BOUNDS = [s[0] for s in SCENES[1:]]
# évènements sonores : (temps, type)
IMPACTS = [10.58, 15.12, 27.79, 31.68, 38.65]
POPS = [47.43, 49.82, 50.27]
