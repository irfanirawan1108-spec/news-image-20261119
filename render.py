#!/usr/bin/env python3
"""news-image-20261119 round 3 — front page renderer (Pillow).

Draws a 1024x1024 newspaper front page summing up Thursday
19 November 2026: fourteen stories, every one checked against
same-day reporting (ICJ verdict, Shenzhen summit, Anthropic IPO,
Gaza, the Gulf, Bangladesh, GTA VI, the Van Gogh record, plus six
briefs). Run: python3 render.py  ->  writes entry.png next to it.
Deterministic: no network, no clock, no randomness.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
GUT = 12

PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (178, 34, 27)
NAVY = (22, 50, 79)
GRAY = (96, 92, 82)
RULE = (26, 26, 26)
FAINT = (196, 190, 174)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, w, text, fnt, fill=INK, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    leading = leading if leading is not None else int(fnt.size * 1.22)
    for line in wrap(d, text, fnt, w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kick(d, x, y, text, size=15):
    d.text((x, y), text, font=font(SANS_B, size), fill=RED)
    return y + size + 4


def head(d, x, y, w, text, size=30):
    return block(d, x, y, w, text, font(SERIF, size), INK,
                 leading=int(size * 1.08))


def deck(d, x, y, w, text, size=17):
    return block(d, x, y, w, text, font(SERIF_R, size), (52, 48, 42),
                 leading=int(size * 1.28))


def frame(d, box, fill, outline=INK, width=2):
    d.rectangle(box, fill=fill, outline=outline, width=width)


def star(d, cx, cy, r, fill):
    """Five-point star centred at (cx, cy)."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def clipped(img, d, func, box):
    """Render an art panel onto a throwaway layer, then paste it.

    Keeps every stroke inside the panel: a palm frond or a branch
    that runs past the panel edge is cut there, never over the text.
    """
    x0, y0, x1, y1 = box
    tmp = Image.new("RGB", (x1 - x0, y1 - y0), PAPER)
    td = ImageDraw.Draw(tmp)
    func(td, (0, 0, x1 - x0, y1 - y0))
    img.paste(tmp, (x0, y0))
    d.rectangle(box, outline=INK, width=2)


# ---------------------------------------------------------------- art panels

def art_scales(d, box):
    """Scales of justice on deep blue."""
    x0, y0, x1, y1 = box
    frame(d, box, (24, 62, 110))
    gold = (212, 175, 55)
    cx = (x0 + x1) // 2
    top = y0 + 26
    base = y1 - 26
    d.rectangle([cx - 5, top, cx + 5, base], fill=gold)
    d.rectangle([cx - 52, base, cx + 52, base + 10], fill=gold)
    d.rectangle([cx - 118, top + 8, cx + 118, top + 16], fill=gold)
    d.ellipse([cx - 12, y0 + 12, cx + 12, y0 + 36], fill=gold)
    for sgn in (-1, 1):
        px = cx + sgn * 96
        d.line([cx + sgn * 118, top + 12, px - 34, base - 34], fill=gold, width=3)
        d.line([cx + sgn * 118, top + 12, px + 34, base - 34], fill=gold, width=3)
        d.line([cx + sgn * 118, top + 12, px, base - 34], fill=gold, width=3)
        d.pieslice([px - 36, base - 40, px + 36, base + 4], 0, 180, fill=gold)
        d.rectangle([px - 36, base - 40, px + 36, base - 34], fill=gold)


def art_flags(d, box):
    """US, Chinese and Russian flags in a row."""
    x0, y0, x1, y1 = box
    frame(d, box, (228, 234, 240))
    fw, fh = 118, 64
    gap = 14
    total = 3 * fw + 2 * gap
    sx = x0 + (x1 - x0 - total) // 2
    sy = y0 + 4
    # United States: stripes + canton
    ux = sx
    for i in range(7):
        d.rectangle([ux, sy + i * (fh // 7), ux + fw, sy + (i + 1) * (fh // 7)],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([ux, sy, ux + 46, sy + 36], fill=(30, 50, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([ux + 6 + c * 8, sy + 5 + r * 8, ux + 9 + c * 8, sy + 8 + r * 8],
                      fill=(255, 255, 255))
    # China: red field, one big star + four small
    cx = sx + fw + gap
    d.rectangle([cx, sy, cx + fw, sy + fh], fill=(222, 41, 16))
    star(d, cx + 24, sy + 20, 13, (255, 222, 0))
    for sx2, sy2 in [(54, 10), (65, 20), (65, 32), (54, 40)]:
        star(d, cx + sx2, sy + sy2, 5, (255, 222, 0))
    # Russia: white / blue / red tricolour
    rx = sx + 2 * (fw + gap)
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([rx, sy + i * (fh // 3), rx + fw, sy + (i + 1) * (fh // 3)],
                    fill=col)
    d.text((x0 + (x1 - x0) // 2, y1 - 18), "TRUMP  ·  XI  ·  PUTIN",
           font=font(SANS_B, 13), fill=INK, anchor="ma")


def art_ipo(d, box):
    """Three bars: offer $83, open $111.50, close $97.17."""
    x0, y0, x1, y1 = box
    frame(d, box, (255, 255, 255))
    vals = [("OFFER", 83.0, (150, 150, 150)), ("OPEN", 111.50, (22, 50, 79)),
            ("CLOSE", 97.17, (178, 34, 27))]
    base = y1 - 22
    top = y0 + 16
    bw = 74
    span = (x1 - x0 - 2 * 26 - 3 * bw) // 2
    for i, (lab, val, col) in enumerate(vals):
        bx = x0 + 26 + i * (bw + span)
        bh = int((val / 115.0) * (base - top))
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
        d.text((bx + bw // 2, base - bh - 16), "$%.2f" % val,
               font=font(SANS_B, 13), fill=INK, anchor="ma")
        d.text((bx + bw // 2, base + 5), lab, font=font(SANS_B, 12),
               fill=GRAY, anchor="ma")


def art_gaza(d, box):
    """Tank crossing a dashed ceasefire line; figures fleeing."""
    x0, y0, x1, y1 = box
    frame(d, box, (203, 224, 238))
    horizon = y0 + int((y1 - y0) * 0.62)
    d.rectangle([x0, horizon, x1, y1], fill=(232, 214, 170))
    d.line([x0, horizon, x1, horizon], fill=(150, 120, 70), width=2)
    # dashed yellow line, vertical, near the middle
    lx = x0 + int((x1 - x0) * 0.58)
    for yy in range(y0 + 6, horizon, 13):
        d.line([lx, yy, lx, yy + 7], fill=(222, 178, 0), width=4)
    # tank straddling the line
    tx, ty = x0 + int((x1 - x0) * 0.26), horizon - 30
    d.rectangle([tx, ty, tx + 108, ty + 18], fill=(38, 44, 50))
    d.rectangle([tx + 68, ty - 7, tx + 138, ty - 1], fill=(38, 44, 50))
    d.rectangle([tx + 14, ty + 18, tx + 94, ty + 24], fill=(24, 28, 34))
    for i in range(4):
        d.ellipse([tx + 6 + i * 22, ty + 25, tx + 20 + i * 22, ty + 39],
                  fill=(90, 92, 96), outline=(24, 28, 34))
    # fleeing figures, left of the line
    for fx, fh in [(x0 + 26, 24), (x0 + 52, 20), (x0 + 76, 17)]:
        fy = horizon - fh
        d.ellipse([fx, fy, fx + 8, fy + 8], fill=(26, 26, 26))
        d.line([fx + 4, fy + 8, fx + 4, fy + 18], fill=(26, 26, 26), width=2)
        d.line([fx + 4, fy + 11, fx - 4, fy + 17], fill=(26, 26, 26), width=2)
        d.line([fx + 4, fy + 11, fx + 11, fy + 8], fill=(26, 26, 26), width=2)
        d.line([fx + 4, fy + 18, fx - 3, fy + 28], fill=(26, 26, 26), width=2)
        d.line([fx + 4, fy + 18, fx + 10, fy + 28], fill=(26, 26, 26), width=2)
    d.text((x0 + 8, y0 + 5), "YELLOW LINE", font=font(SANS_B, 11),
           fill=(150, 110, 0))


def art_gulf(d, box):
    """Oil tanker on a blue strait with a warning mark."""
    x0, y0, x1, y1 = box
    frame(d, box, (24, 90, 130))
    # land masses top and bottom
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + 18), (x0 + 120, y0 + 30),
               (x0, y0 + 20)], fill=(210, 190, 150))
    d.polygon([(x0, y1), (x1, y1), (x1, y1 - 16), (x0 + 200, y1 - 32),
               (x0, y1 - 20)], fill=(210, 190, 150))
    d.text((x0 + 10, y0 + 5), "STRAIT OF HORMUZ", font=font(SANS_B, 11),
           fill=(24, 50, 80))
    # tanker
    tx, ty = x0 + 40, y0 + int((y1 - y0) * 0.40)
    d.rectangle([tx, ty, tx + 150, ty + 18], fill=(150, 40, 32))
    d.rectangle([tx + 104, ty - 14, tx + 132, ty], fill=(240, 238, 230))
    d.rectangle([tx + 18, ty - 8, tx + 84, ty], fill=(240, 238, 230))
    d.line([tx - 6, ty + 18, tx + 156, ty + 18], fill=(255, 255, 255), width=2)
    # warning triangle
    wx, wy = x1 - 52, y0 + 40
    d.polygon([(wx, wy - 18), (wx - 18, wy + 12), (wx + 18, wy + 12)],
              fill=(255, 196, 0), outline=(150, 90, 0))
    d.text((wx, wy - 2), "!", font=font(SANS_B, 16), fill=(150, 40, 32),
           anchor="ma")


def art_dhaka(d, box):
    """Building silhouette with flames against a dusk sky."""
    x0, y0, x1, y1 = box
    frame(d, box, (58, 44, 66))
    # dusk band
    d.rectangle([x0, y0, x1, y0 + 18], fill=(120, 62, 62))
    # buildings
    for bx, bw, bh in [(22, 66, 42), (100, 52, 56), (164, 74, 36)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(30, 26, 34))
        for wy in range(y1 - bh + 9, y1 - 9, 16):
            for wx in range(x0 + bx + 8, x0 + bx + bw - 7, 15):
                d.rectangle([wx, wy, wx + 6, wy + 7], fill=(240, 200, 90))
    # flame over the middle building
    fx, fy = x0 + 126, y1 - 56
    d.polygon([(fx - 20, fy + 20), (fx - 6, fy - 2), (fx, fy - 16),
               (fx + 8, fy - 2), (fx + 20, fy + 20)], fill=(255, 122, 26))
    d.polygon([(fx - 10, fy + 20), (fx - 3, fy + 6), (fx, fy - 6),
               (fx + 4, fy + 6), (fx + 10, fy + 20)], fill=(255, 214, 64))


def art_vice(d, box):
    """Vice City sunset: sun, palms, skyline."""
    x0, y0, x1, y1 = box
    frame(d, box, (255, 255, 255))
    # sunset bands
    bands = [(255, 122, 56), (255, 96, 110), (196, 84, 150), (90, 60, 130)]
    bh = (y1 - y0) // 4
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh], fill=col)
    # sun
    cx, cy = (x0 + x1) // 2, y0 + int((y1 - y0) * 0.42)
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(255, 214, 110))
    # skyline
    for bx, bw, bh2 in [(0, 52, 52), (60, 40, 78), (108, 62, 44), (180, 44, 66),
                        (232, 56, 40)]:
        d.rectangle([x0 + bx, y1 - bh2, x0 + bx + bw, y1], fill=(34, 24, 52))
    # palms
    for px, lean in [(x0 + 250, -18), (x1 - 30, 14)]:
        py = y1
        d.line([px, py, px + lean, py - 74], fill=(24, 18, 40), width=6)
        for k in range(5):
            ang = -0.4 - k * 0.45
            import math
            ex = px + lean + int(34 * math.cos(ang))
            ey = py - 74 + int(30 * math.sin(ang)) - k * 2
            d.line([px + lean, py - 74, ex, ey], fill=(24, 18, 40), width=4)
    d.text((x0 + 12, y0 + 8), "VICE CITY", font=font(SANS_B, 13),
           fill=(255, 255, 255))


def art_vangogh(d, box):
    """Flowering chestnut branch in a gold frame."""
    x0, y0, x1, y1 = box
    frame(d, box, (214, 230, 196), outline=(176, 138, 44), width=6)
    # branch
    d.line([x0 + 16, y1 - 18, x0 + 150, y0 + 52], fill=(96, 62, 30), width=7)
    d.line([x0 + 90, y1 - 60, x0 + 210, y0 + 30], fill=(96, 62, 30), width=5)
    d.line([x0 + 60, y1 - 90, x0 + 250, y0 + 96], fill=(96, 62, 30), width=4)
    # blossom clusters: white puffs with yellow centres
    import random
    rnd = random.Random(19111926)
    for _ in range(46):
        bx = rnd.randint(x0 + 40, x1 - 30)
        by = rnd.randint(y0 + 26, y1 - 40)
        r = rnd.randint(9, 15)
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(250, 246, 232),
                  outline=(214, 200, 160))
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(232, 178, 40))
    d.text((x0 + 12, y1 - 26), "1890", font=font(SERIF, 16), fill=(96, 62, 30))


# ---------------------------------------------------------------- stories

LEAD = ("THE HAGUE · JUSTICE",
        "World court finds Myanmar guilty of genocide",
        "The ICJ rules 9–6 that Myanmar's army committed genocide "
        "against the Rohingya in 2017 — the first time any state has "
        "been held responsible — and orders reparations.")

HALVES = [
    ("SHENZHEN · SUMMIT",
     "Trump, Xi and Putin meet in first three-way summit",
     "The three leaders issue a four-point 'Declaration toward Peace' "
     "and agree to talk on nuclear risks.",
     art_flags),
    ("NEW YORK · MARKETS",
     "Anthropic IPO is the biggest ever",
     "$81.3bn raised at $83 a share; ANT opens at $111.50 and closes "
     "at $97.17 on its first Nasdaq day.",
     art_ipo),
]

THIRDS = [
    ("GAZA · WAR",
     "Israeli troops cross the ceasefire line",
     "Rare ground operation beyond the Yellow Line; Hamas cries "
     "ceasefire breach.",
     art_gaza),
    ("THE GULF · ENERGY",
     "Iran widens its Gulf attacks",
     "Kuwait and Bahrain hit; IEA calls it the greatest threat ever "
     "to energy security.",
     art_gulf),
    ("DHAKA · UNREST",
     "Yunus home torched as violence spreads",
     "Arson and bomb blasts hit 28 districts as Hasina supporters "
     "protest; troops deploy.",
     art_dhaka),
]

PAIRS = [
    ("VICE CITY · GAMES",
     "GTA VI rolls out worldwide",
     "The decade's most awaited game unlocks at midnight.",
     art_vice),
    ("NEW YORK · ART",
     "Van Gogh sells for a record $190.4m",
     "“Châtaigniers en fleurs” (1890) sets the artist's auction record.",
     art_vangogh),
]

BRIEFS = [
    "Crimea bridge hit again; traffic halted",
    "EU proposes €45bn Ukraine loan; leaders meet in Berlin",
    "Denmark approves Greenland–US security pact",
    "US and Venezuela sign a military cooperation deal",
    "North Korea expands uranium site, watchdog says",
    "COP31 ministers race to unblock climate talks in Antalya",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

    # ---- masthead
    d.text((W // 2, 20), "THE WORLD IN ONE DAY", font=font(SERIF, 52),
           fill=INK, anchor="ma")
    d.line([MARGIN, 84, W - MARGIN, 84], fill=INK, width=3)
    d.text((W // 2, 92), "THURSDAY 19 NOVEMBER 2026",
           font=font(SANS_B, 24), fill=RED, anchor="ma")
    d.line([MARGIN, 124, W - MARGIN, 124], fill=INK, width=2)

    # ---- lead: ICJ
    ly = 136
    lx0, lx1 = MARGIN, W - MARGIN
    ax0 = 636
    k, h, deck_t = LEAD
    ty = ly + 4
    ty = kick(d, lx0, ty, k, size=16)
    ty = head(d, lx0, ty, ax0 - lx0 - 20, h, size=36)
    deck(d, lx0, ty + 6, ax0 - lx0 - 20, deck_t, size=17)
    clipped(img, d, art_scales, (ax0, ly, lx1, ly + 140))
    y = 316
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)

    # ---- halves: Shenzhen + Anthropic
    hy = y + 12
    half_w = (W - 2 * MARGIN - GUT) // 2
    for i, (k, h, deck_t, art) in enumerate(HALVES):
        x0 = MARGIN + i * (half_w + GUT)
        clipped(img, d, art, (x0, hy, x0 + half_w, hy + 84))
        ty = kick(d, x0, hy + 92, k)
        ty = head(d, x0, ty, half_w, h, size=24)
        deck(d, x0, ty + 2, half_w, deck_t, size=15)
    y = 540
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)

    # ---- thirds: Gaza, Gulf, Bangladesh
    ty3 = y + 12
    third_w = (W - 2 * MARGIN - 2 * GUT) // 3
    for i, (k, h, deck_t, art) in enumerate(THIRDS):
        x0 = MARGIN + i * (third_w + GUT)
        clipped(img, d, art, (x0, ty3, x0 + third_w, ty3 + 72))
        yy = kick(d, x0, ty3 + 80, k, size=14)
        yy = head(d, x0, yy, third_w, h, size=21)
        deck(d, x0, yy + 2, third_w, deck_t, size=14)
    y = 752
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)

    # ---- pairs: GTA VI + Van Gogh (art left, text right)
    py = y + 12
    ph = 124
    for i, (k, h, deck_t, art) in enumerate(PAIRS):
        x0 = MARGIN + i * (half_w + GUT)
        clipped(img, d, art, (x0, py, x0 + 168, py + ph))
        tx = x0 + 180
        tw = half_w - 180
        yy = kick(d, tx, py + 2, k, size=14)
        yy = head(d, tx, yy, tw, h, size=22)
        deck(d, tx, yy + 2, tw, deck_t, size=15)
    y = py + ph
    d.line([MARGIN, y + 10, W - MARGIN, y + 10], fill=RULE, width=1)

    # ---- also today
    ay = y + 22
    d.text((MARGIN, ay), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    ay += 25
    col_w = (W - 2 * MARGIN - 24) // 2
    for i, b in enumerate(BRIEFS):
        bx = MARGIN + (i % 2) * (col_w + 24)
        by = ay + (i // 2) * 20
        d.rectangle([bx, by + 4, bx + 8, by + 12], fill=RED)
        d.text((bx + 16, by), b, font=font(SERIF_R, 15), fill=INK)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
