"""Storyboard « L'évasion d'Alcatraz » (réutilise les pièces de scenes.py)."""
import math

from PIL import Image, ImageChops, ImageDraw, ImageFilter

import papercut as pc
import scenes as S
from papercut import (PAL, W, H, Builder, put, bput, pop, slam, slide, cue, ease_out, back, clamp, shake,
                      ell_pts, rrect_pts, rect_pts, bar_pts, burst_pts, font)
from scenes import B, memo, calendar_sprite, waves_sprite, person_sprite, puff_sprite, doc_sprite, sweep_sprites

P = PAL


# ------------------------------------------------------------------ pièces nouvelles
def cut_text(txt, fname, size, color, seed=1):
    """Lettre découpée dans le papier (avec ombre)."""
    f = font(fname, size)
    l, t, r, b = f.getbbox(txt)
    w, h = r - l + 60, b - t + 60
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).text((30 - l, 30 - t), txt, font=f, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh = ImageChops.offset(m, 4, 7).filter(ImageFilter.GaussianBlur(3.5)).point(lambda v: int(v * 0.45))
    blk = Image.new("RGBA", (w, h), (8, 12, 26, 255))
    blk.putalpha(sh)
    out = Image.alpha_composite(out, blk)
    fill = Image.new("RGBA", (w, h), color + (255,))
    fill.putalpha(m)
    out = Image.alpha_composite(out, fill)
    rim = ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(3)))
    hl = Image.new("RGBA", (w, h), (255, 250, 235, 255))
    hl.putalpha(rim.point(lambda v: int(v * 0.35)))
    return Image.alpha_composite(out, hl)


def prison_sprite():
    b = Builder(900, 640, seed=101)
    b.poly([(40, 600), (130, 430), (330, 400), (560, 410), (780, 420), (870, 600)], P["grey"], rough=3)
    b.poly([(130, 430), (330, 400), (200, 470), (120, 520)], (150, 158, 180), rough=2, shadow=False)
    b.rect(170, 215, 700, 440, P["cream_d"], rough=1.6)
    b.rect(150, 190, 720, 225, P["cream"], rough=1.4)
    for r in range(3):
        for c in range(10):
            x = 195 + c * 50
            y = 245 + r * 62
            b.rect(x, y, x + 26, y + 44, P["navy_d"], rough=0.6, shadow=False)
            b.bar(x + 9, y, x + 9, y + 44, 3, P["grey"], rough=0.3, shadow=False)
            b.bar(x + 18, y, x + 18, y + 44, 3, P["grey"], rough=0.3, shadow=False)
    b.rect(735, 110, 810, 440, P["cream"], rough=1.4)
    b.poly([(722, 112), (772, 56), (824, 112)], P["brick"], rough=1.2)
    b.rect(752, 140, 794, 186, P["mustard"], rough=0.8, shadow=False)
    b.rect(90, 190, 165, 440, P["cream"], rough=1.4)
    b.poly([(80, 192), (127, 140), (176, 192)], P["brick"], rough=1.2)
    return b.done()


def bed_sprite(head="human", seed=102):
    def mk():
        b = Builder(720, 400, seed=seed)
        b.rect(30, 290, 70, 390, P["brick"], rough=1)
        b.rect(650, 290, 690, 390, P["brick"], rough=1)
        b.rrect(20, 250, 700, 310, 14, P["brick_l"], rough=1.4)
        b.rrect(40, 190, 680, 270, 20, P["cream"], rough=1.4)
        b.rrect(40, 150, 210, 250, 26, P["white"], rough=1.2)
        if head == "human":
            b.ell(130, 170, 54, 58, P["cream_d"], rough=1)
            b.poly([(80, 135), (130, 105), (180, 135), (170, 150), (90, 150)], P["brick"], rough=1)
        elif head == "dummy":
            b.ell(130, 170, 54, 58, (236, 232, 222), rough=1)
            b.bar(104, 168, 122, 168, 6, P["ink"], rough=0.3, shadow=False)
            b.bar(138, 168, 156, 168, 6, P["ink"], rough=0.3, shadow=False)
            b.bar(116, 198, 146, 198, 6, P["brick"], rough=0.3, shadow=False)
            b.poly([(78, 140), (130, 100), (184, 140), (170, 148), (90, 148)], P["ink"], rough=1)
        b.rrect(150, 150, 690, 275, 40, P["teal"], rough=1.4)
        b.bar(300, 156, 300, 270, 8, P["teal_l"], rough=0.8, shadow=False)
        b.bar(460, 156, 460, 270, 8, P["teal_l"], rough=0.8, shadow=False)
        return b.done()
    return memo(("bed", head), mk)


def dummy_head(hair=False):
    def mk():
        b = Builder(320, 400, seed=103)
        b.ell(160, 210, 104, 134, (236, 232, 222))
        b.ell(56, 216, 17, 30, (222, 216, 204), rough=1)
        b.ell(264, 216, 17, 30, (222, 216, 204), rough=1)
        b.bar(104, 196, 140, 196, 9, P["ink"], rough=0.4, shadow=False)
        b.bar(180, 196, 216, 196, 9, P["ink"], rough=0.4, shadow=False)
        b.poly([(160, 206), (146, 252), (174, 252)], (214, 206, 192), rough=0.6, shadow=False)
        b.bar(124, 290, 196, 290, 10, P["brick"], rough=0.5, shadow=False)
        for x, y in [(80, 120), (230, 150), (170, 70)]:
            b.bar(x, y, x + 24, y + 30, 3, (200, 194, 180), rough=0.4, shadow=False)
        if hair:
            b.poly([(60, 170), (74, 90), (160, 52), (246, 90), (262, 170), (232, 128), (160, 108), (90, 128)], P["ink"], rough=2.4)
        return b.done()
    return memo(("dhead", hair), mk)


def soap_sprite():
    b = Builder(300, 200, seed=104)
    b.poly(rrect_pts(20, 50, 280, 170, 30), P["teal_l"], rough=1.4)
    b.text(150, 112, "SAVON", "Anton", 52, P["cream"])
    for x, y, r in [(250, 40, 20), (216, 24, 13), (270, 80, 11)]:
        b.ell(x, y, r, r, P["white"], rough=0.6, shadow=False)
    return b.done()


def plaster_sprite():
    b = Builder(300, 340, seed=105)
    b.poly(ell_pts(150, 210, 120, 118), P["cream"], rough=2)
    b.poly([(80, 110), (220, 110), (240, 70), (60, 70)], P["cream"], rough=1.6)
    b.bar(70, 100, 230, 100, 14, P["brick"], rough=1)
    b.text(150, 222, "PLÂTRE", "Anton", 58, P["ink"])
    return b.done()


def spoon_sprite():
    b = Builder(240, 460, seed=106)
    b.bar(120, 440, 120, 200, 22, P["grey"], rough=1)
    b.ell(120, 120, 78, 104, P["grey"], rough=1.4)
    b.ell(120, 120, 56, 82, (168, 176, 198), rough=1, shadow=False)
    return b.done()


def drill_sprite():
    b = Builder(560, 300, seed=107)
    b.poly(rrect_pts(120, 70, 470, 170, 36), P["mustard"], rough=1.4)
    b.poly(rrect_pts(250, 150, 330, 290, 20), P["brick"], rough=1.2)
    b.bar(120, 120, 20, 120, 24, P["grey"], rough=0.8)
    b.rect(470, 90, 520, 150, P["grey"], rough=1)
    b.bar(190, 90, 190, 150, 12, P["orange"], rough=0.6, shadow=False)
    return b.done()


def vacuum_sprite():
    b = Builder(560, 360, seed=108)
    b.poly(rrect_pts(150, 90, 520, 280, 80), P["teal"], rough=1.6)
    b.poly(rrect_pts(150, 90, 520, 170, 50), P["teal_l"], rough=1.2, shadow=False)
    b.ell(210, 300, 44, 44, P["ink"])
    b.ell(450, 300, 44, 44, P["ink"])
    b.ell(210, 300, 18, 18, P["cream_d"], rough=0.5, shadow=False)
    b.ell(450, 300, 18, 18, P["cream_d"], rough=0.5, shadow=False)
    b.poly(bar_pts(150, 180, 50, 120, 36), P["grey"], rough=1)
    b.bar(50, 120, 30, 40, 36, P["grey"], rough=1)
    b.text(335, 200, "MOTEUR", "Anton", 46, P["cream"])
    return b.done()


def moon_sprite():
    b = Builder(300, 300, seed=109)
    b.ell(150, 150, 120, 120, P["cream"], rough=2)
    for x, y, r in [(110, 120, 22), (190, 180, 28), (140, 200, 14)]:
        b.ell(x, y, r, r, P["cream_d"], rough=1, shadow=False)
    return b.done()


def raft_sprite():
    b = Builder(640, 240, seed=110)
    b.poly(rrect_pts(20, 80, 620, 210, 60), P["mustard"], rough=2)
    cols = [P["orange"], P["teal"], P["brick_l"], P["teal_l"], P["cream"], P["orange"]]
    for i in range(6):
        b.rect(60 + i * 90, 100, 130 + i * 90, 190, cols[i], rough=1.2, shadow=False)
    b.poly(ell_pts(320, 90, 300, 34), P["mustard"], rough=1.6, shadow=False)
    return b.done()


def badge_sprite():
    b = Builder(380, 440, seed=111)
    b.poly([(40, 40), (340, 40), (340, 250), (190, 410), (40, 250)], P["mustard"], rough=2)
    b.poly([(66, 66), (314, 66), (314, 240), (190, 370), (66, 240)], P["navy_l"], rough=1.6, shadow=False)
    b.text(190, 190, "FBI", "Anton", 130, P["cream"])
    return b.done()


def magnifier_sprite():
    b = Builder(380, 380, seed=112)
    b.bar(250, 250, 340, 340, 40, P["brick"], rough=1)
    b.ring(150, 150, 120, 86, P["grey"], rough=1.2)
    b.ell(150, 150, 86, 86, (190, 205, 235), rough=1, shadow=False)
    return b.done()


def bubbles_sprite():
    b = Builder(200, 240, seed=113)
    for x, y, r in [(100, 190, 26), (60, 120, 18), (130, 70, 14), (80, 30, 9)]:
        b.ring(x, y, r, r - 5, P["cream"], rough=0.6, shadow=False)
    return b.done()


# ------------------------------------------------------------------ scènes
def vanish(C, spr, x, y, T, t0, t1, s=0.8):
    """Silhouette visible jusqu'à t1, puis disparaît dans un nuage."""
    if T < t0:
        return
    fade = 1 - cue(T, t1, 0.3)
    pop(C, spr, x, y, T, t0, s=s, a=fade)
    if T >= t1:
        k = cue(T, t1, 0.5)
        put(C, memo("puff", puff_sprite), x, y - 40 - 40 * k, 0.55 + 0.7 * k, 0, 1 - k * 0.85)


def a1(C, T, t):
    pop(C, memo("prison", prison_sprite), 540, 780, T, 0.05, s=0.98)
    for i, (col, x) in enumerate([("orange", 330), ("teal", 540), ("mustard", 750)]):
        vanish(C, memo(("pp", col), lambda c=col, i=i: person_sprite(c, 120 + i, hat=False)), x, 880, T, 0.3 + 0.08 * i, 0.9 + 0.12 * i)
    slam(C, B("", 112, lines=["3 DÉTENUS", "DISPARUS"], seed=1), 540, 330, T, 0.08, rot=-2)
    pop(C, B("PRISON IMPRENABLE", 80, "orange", "cream", seed=2), 540, 1160, T, 1.52, rot=-2)


def a2(C, T, t):
    for i, (x, y, r, col) in enumerate([(250, 760, -12, "cream"), (540, 700, 4, "orange"), (830, 780, 14, "mustard")]):
        pop(C, memo(("q", col), lambda c=col: cut_text("?", "Anton", 520, P[c])), x, y, T, 3.4 + 0.5 * i, s=1.0, rot=r)
    pop(C, B("PERSONNE NE SAIT", 100, "cream", "ink", seed=3), 540, 320, T, 3.43, rot=-2)
    slam(C, B("ET ILS SONT ?", 86, "brick", "cream", seed=4), 540, 1150, T, 4.63, rot=2)


def a3(C, T, t):
    for i, (col, y, sd) in enumerate([(P["teal"], 1060, 61), (P["teal_l"], 1120, 62)]):
        w = memo(("wave2", i), lambda c=col, s=sd: waves_sprite(c, s))
        slide(C, w, (-400, y), (540 + (20 if i else -10), y), T, 5.4 + 0.05 * i, 0.5)
    pop(C, memo("prison", prison_sprite), 540, 760, T, 5.45, s=0.9)
    slam(C, B("ALCATRAZ", 140, "mustard", "ink", seed=5), 540, 290, T, 5.51, rot=-2)
    pop(C, calendar_sprite("JUIN", "1962"), 780, 1010, T, 6.61, s=0.78, rot=4)


def a4(C, T, t):
    pop(C, memo("sun", S.sun_sprite), 800, 560, T, 8.2, s=0.8)
    pop(C, memo("pg", lambda: person_sprite("teal", 131, hat=True)), 330, 880, T, 9.2, s=1.45)
    pop(C, memo("doc", doc_sprite), 560, 880, T, 9.9, s=0.7, rot=8)
    pop(C, B("L'APPEL DU MATIN", 100, "cream", "ink", seed=6), 540, 310, T, 8.45, rot=-2)
    pop(C, B("LES GARDIENS", 66, "orange", "cream", seed=7), 540, 1170, T, 9.35, rot=1.5)


def a5(C, T, t):
    for i, y in enumerate([620, 820, 1020]):
        pop(C, memo(("bed1", i), lambda: bed_sprite("human")), 540, y, T, 10.82 + 0.22 * i, s=0.85)
    pop(C, cut_text("ZZZ", "Anton", 130, P["cream"]), 840, 540, T, 11.9, s=0.9, rot=8)
    pop(C, B("TROIS HOMMES", 90, "mustard", "ink", seed=8), 540, 300, T, 11.03, rot=-2)


def a6(C, T, t):
    flip = T >= 13.95
    pop(C, memo(("bed2", flip), lambda: bed_sprite("dummy" if flip else "human")), 540, 780, T, 12.5, s=1.2)
    pop(C, B("SAUF QUE…", 110, "brick", "cream", seed=9), 540, 310, T, 12.53, rot=-3)
    if flip:
        slam(C, B("PAS DES HOMMES !", 90, "orange", "cream", seed=10), 540, 1150, T, 14.14, rot=2)


def a7(C, T, t):
    slam(C, B("FAUSSES TÊTES", 100, "cream", "ink", seed=11), 540, 300, T, 15.35, rot=-2)
    hair = T >= 18.21
    bput(C, memo(("dh", hair), lambda: dummy_head(hair)), 540, 780, T, s=1.28 if True else 1)
    pop(C, memo("plaster", plaster_sprite), 220, 1090, T, 16.53, s=0.62, rot=-8)
    pop(C, memo("soap", soap_sprite), 540, 1110, T, 17.33, s=0.75, rot=4)
    if hair:
        pop(C, B("VRAIS CHEVEUX", 68, "orange", "cream", seed=12), 800, 1070, T, 18.21, rot=-3)


def a8(C, T, t):
    pop(C, memo("wall", S.wall_sprite), 540, 840, T, 19.1, s=1.0)
    k = ease_out(cue(T, 20.78, 0.6))
    if k > 0:
        hole = memo("whole", lambda: Builder(300, 300, seed=140).ell(150, 150, 130, 130, P["navy_d"], shadow=False).ell(
            150, 160, 100, 100, (6, 10, 24), shadow=False).done())
        put(C, hole, 600, 860, 0.9 * k, 0, 1)
    pop(C, B("FRANK MORRIS", 92, "mustard", "ink", seed=13), 540, 300, T, 19.19, rot=-2)
    pop(C, B("LES FRÈRES ANGLIN", 76, "orange", "cream", seed=14), 540, 1170, T, 19.99, rot=2)
    for i, (c, x) in enumerate([("teal", 160), ("orange", 270), ("brick", 380)]):
        pop(C, memo(("pw", c), lambda c=c, i=i: person_sprite(c, 150 + i)), x, 1030, T, 19.4 + 0.2 * i, s=0.62)


def a9(C, T, t):
    pop(C, B("DES MOIS", 110, "cream", "ink", seed=15), 540, 300, T, 22.49, rot=-2)
    pop(C, memo("spoon", spoon_sprite), 220, 760, T, 23.45, s=0.95, rot=-18)
    pop(C, B("CUILLÈRES", 60, "mustard", "ink", seed=16), 220, 1070, T, 23.6, rot=3)
    pop(C, cut_text("+", "Anton", 220, P["cream"]), 470, 760, T, 24.0, s=0.9)
    pop(C, memo("drill", drill_sprite), 760, 700, T, 24.10, s=0.78, rot=-6)
    pop(C, memo("vac", vacuum_sprite), 700, 1010, T, 25.29, s=0.9)
    pop(C, B("PERCEUSE BRICOLÉE", 60, "orange", "cream", seed=17), 650, 540, T, 24.46, rot=2)


def a10(C, T, t):
    moon = memo("moon", moon_sprite)
    pop(C, moon, 860, 470, T, 26.8, s=0.7)
    for k, (x, y) in enumerate([(160, 500), (420, 430), (640, 560), (300, 640), (940, 700)]):
        put(C, memo("star", lambda: Builder(80, 80, seed=160).poly(burst_pts(40, 40, 34, 12, n=4), P["cream"], rough=0.8, shadow=False).done()),
            x, y + 6 * math.sin(T * 3 + k), 0.8, 0, clamp(cue(T, 26.8 + 0.1 * k, 0.4)))
    pop(C, memo("prison", prison_sprite), 540, 860, T, 26.9, s=0.9)
    pop(C, B("CETTE NUIT-LÀ", 100, "mustard", "ink", seed=18), 540, 300, T, 26.97, rot=-2)
    pp = memo(("pp3", "o"), lambda: person_sprite("orange", 170))
    for i in range(3):
        p = cue(T, 27.7 + 0.12 * i, 1.0)
        q = cue(T, 28.8 + 0.1 * i, 1.0)
        if p > 0:
            x = 330 + 90 * i + 160 * ease_out(q)
            y = (940 - 360 * ease_out(p)) + 420 * ease_out(q)
            bput(C, pp, x, y, T, s=0.34, rot=0)
    pop(C, B("LE TOIT", 70, "cream", "ink", seed=19), 380, 400, T, 28.21, rot=-3)
    pop(C, B("LE RIVAGE", 70, "orange", "cream", seed=20), 820, 1150, T, 29.36, rot=3)


def a11(C, T, t):
    for i, (col, y, sd) in enumerate([(P["teal"], 1010, 71), (P["teal_l"], 1090, 72), (P["teal"], 1160, 73)]):
        w = memo(("wave3", i), lambda c=col, s=sd: waves_sprite(c, s))
        bput(C, w, 540 + 10 * math.sin(T * 1.5 + i), y + 8 * math.sin(T * 2 + i), T, s=1.0)
    p = ease_out(cue(T, 30.57, 0.7))
    raft = memo("raft", raft_sprite)
    bob = 12 * math.sin(T * 3)
    if p > 0:
        bput(C, raft, 340 + 200 * p, 760 + 230 * (1 - p) - 20 + bob, T, s=0.95, rot=-6 * (1 - p) + 2 * math.sin(T * 2.4))
        for i, c in enumerate(["orange", "teal", "brick"]):
            bput(C, memo(("pr", c), lambda c=c, i=i: person_sprite(c, 180 + i)), 410 + 200 * p + i * 80, 690 + 230 * (1 - p) - 20 + bob, T, s=0.3)
    pop(C, B("", 88, "cream", "ink", lines=["RADEAU EN", "IMPERMÉABLES"], seed=21), 540, 330, T, 31.31, rot=-2)


def a12(C, T, t):
    pop(C, memo("badge", badge_sprite), 330, 760, T, 32.6, s=1.0, rot=-5)
    pop(C, B("FBI", 120, "cream", "ink", seed=22), 330, 330, T, 32.87, rot=-3)
    m = memo("mag", magnifier_sprite)
    if T >= 33.33:
        bput(C, m, 720 + 40 * math.sin(T * 2.2), 700 + 26 * math.cos(T * 1.7), T, s=1.0, rot=-12)
    pop(C, calendar_sprite("ENQUÊTE", "17 ANS"), 600, 1020, T, 34.10, s=0.8, rot=3)


def a13(C, T, t):
    for i, (col, y, sd) in enumerate([(P["teal"], 900, 81), (P["teal_l"], 990, 82), (P["teal"], 1080, 83)]):
        w = memo(("wave4", i), lambda c=col, s=sd: waves_sprite(c, s))
        bput(C, w, 540 + 12 * math.sin(T * 1.4 + i), y + 8 * math.sin(T * 1.9 + i), T, s=1.0)
    bub = memo("bub", bubbles_sprite)
    for i, x in enumerate([300, 540, 780]):
        put(C, bub, x, 760 - 40 * ((T * 0.8 + i * 0.35) % 1.0), 1.0, 0, 1 - ((T * 0.8 + i * 0.35) % 1.0))
    pop(C, B("VERDICT", 120, "cream", "ink", seed=23), 540, 320, T, 35.05, rot=-2)
    pop(C, B("PROBABLEMENT", 80, "mustard", "ink", seed=24), 540, 520, T, 36.03, rot=2)
    slam(C, S.stamp_sprite() if False else memo("stamp2", lambda: Builder(520, 200, seed=190).poly(
        rrect_pts(14, 14, 506, 186, 22), P["brick"], rough=2, holes=[rrect_pts(34, 34, 486, 166, 14)]).text(
        260, 100, "NOYÉS ?", "Anton", 110, P["brick"]).done()), 540, 760, T, 36.56, rot=-8)


def a14(C, T, t):
    for i, (col, y, sd) in enumerate([(P["teal"], 1000, 91), (P["teal_l"], 1090, 92)]):
        w = memo(("wave5", i), lambda c=col, s=sd: waves_sprite(c, s))
        bput(C, w, 540 + 12 * math.sin(T * 1.4 + i), y + 8 * math.sin(T * 1.9 + i), T, s=1.0)
    pop(C, memo("q1", lambda: cut_text("?", "Anton", 560, P["orange"])), 330, 700, T, 37.5, s=1.0, rot=-8)
    raft = memo("raft", raft_sprite)
    pop(C, raft, 760, 930 + 10 * math.sin(T * 2.5), T, 38.48, s=0.55, rot=4 * math.sin(T * 2))
    slam(C, B("", 96, "cream", "ink", lines=["AUCUN CORPS", "RETROUVÉ"], seed=25), 540, 330, T, 38.10, rot=-2)


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


def a15(C, T, t):
    cta(C, T, 40.03, 42.31, 44.70, 45.20, 46.1)


SCENES = [
    (0.00, 3.20, a1), (3.20, 5.35, a2), (5.35, 8.15, a3), (8.15, 10.60, a4), (10.60, 12.40, a5),
    (12.40, 14.80, a6), (14.80, 19.05, a7), (19.05, 22.10, a8), (22.10, 26.60, a9), (26.60, 30.20, a10),
    (30.20, 32.55, a11), (32.55, 34.98, a12), (34.98, 37.25, a13), (37.25, 39.92, a14), (39.92, 99.0, a15),
]
BOUNDS = [s[0] for s in SCENES[1:]]
IMPACTS = [5.51, 14.14, 20.78, 32.87, 36.56]
POPS = [42.31, 44.70, 45.20]
