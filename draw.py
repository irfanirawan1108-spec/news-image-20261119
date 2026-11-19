"""news-image-20261119 — front page of Thursday 19 November 2026.

Draws a newspaper front page summarising the day's world news, using only
the Python standard library plus Pillow. Fully deterministic: no random
numbers, no clock, no network, no external files besides the DejaVu fonts
shipped with the system.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (24, 24, 22)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GOLD = (176, 132, 24)
GREY = (96, 94, 88)
SKY = (196, 216, 232)
SAND = (226, 205, 158)
GREEN = (46, 110, 62)
DARK = (52, 58, 64)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, f, max_w):
    """Greedy word wrap; every returned line is guaranteed to fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, f, max_w):
    """Draw-or-die check used by every text helper in this file."""
    assert d.textlength(text, font=f) <= max_w, (text, d.textlength(text, font=f), max_w)


def para(d, lines, f, x, y, lh, color=INK):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=color)
        y += lh
    return y


def rule(d, x0, y, x1, width=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def box(d, rect, fill=None, outline=INK, width=1):
    d.rectangle(rect, fill=fill, outline=outline, width=width)


def kicker_headline(d, x, y, w, tag, head, head_size, body, body_size,
                    tag_color=RED, head_color=INK, body_color=(52, 52, 48)):
    """One news panel: coloured tag, headline, wrapped body. Returns bottom y."""
    tf = SANS_B(15)
    fit(d, tag, tf, w)
    d.text((x, y), tag, font=tf, fill=tag_color)
    y += 22
    hf = SERIF_B(head_size)
    for ln in wrap(d, head, hf, w):
        fit(d, ln, hf, w)
        d.text((x, y), ln, font=hf, fill=head_color)
        y += head_size + 6
    y += 2
    bf = SANS(body_size)
    for ln in wrap(d, body, bf, w):
        fit(d, ln, bf, w)
        d.text((x, y), ln, font=bf, fill=body_color)
        y += body_size + 5
    return y


# ------------------------------------------------------------------ icons

def tank_scene(d, x, y, w, h):
    """Lead illustration: a tank rolling across a dashed yellow ceasefire line."""
    box(d, (x, y, x + w, y + h), fill=SKY, outline=INK, width=2)
    d.rectangle((x, y + h - 46, x + w, y + h), fill=SAND)
    d.rectangle((x, y + h - 46, x + w, y + h - 42), fill=(150, 120, 70))
    # dashed yellow line (the ceasefire line) running diagonally down-left
    for i in range(9):
        sx = x + 14 + i * (w - 28) // 9
        sy = y + h - 96 + i * 4
        d.line([(sx, sy), (sx + 26, sy + 12)], fill=(232, 196, 32), width=5)
    # tank body
    bx, by = x + w // 2 - 130, y + h - 108
    d.rectangle((bx, by, bx + 230, by + 52), fill=DARK)
    d.rectangle((bx + 46, by - 26, bx + 150, by + 2), fill=DARK)
    d.line([(bx + 150, by - 12), (bx + 252, by - 22)], fill=DARK, width=10)
    d.rectangle((bx - 12, by + 52, bx + 242, by + 66), fill=(30, 30, 28))
    for i in range(6):
        cx = bx + 8 + i * 40
        d.ellipse((cx, by + 54, cx + 26, by + 80), fill=(120, 118, 110),
                  outline=(30, 30, 28))
    # fleeing family silhouettes on the left
    for fx, fy, s in ((x + 46, y + h - 92, 1.0), (x + 78, y + h - 84, 0.8),
                      (x + 104, y + h - 96, 0.62)):
        d.ellipse((fx, fy - 26 * s, fx + 12 * s, fy - 14 * s), fill=(70, 60, 52))
        d.line([(fx + 6 * s, fy - 14 * s), (fx + 6 * s, fy)], fill=(70, 60, 52),
               width=4)
        d.line([(fx + 6 * s, fy), (fx - 6 * s, fy + 18 * s)],
               fill=(70, 60, 52), width=4)
        d.line([(fx + 6 * s, fy), (fx + 16 * s, fy + 16 * s)],
               fill=(70, 60, 52), width=4)
    d.text((x + 10, y + 8), "RARE GROUND OPERATION", font=SANS_B(13),
           fill=(120, 30, 30))


def flag_trio(d, x, y, w, h):
    """Three small flags — US, China, Russia — for the Shenzhen summit."""
    box(d, (x, y, x + w, y + h), fill=(238, 238, 234), outline=INK, width=2)
    fw, fh = 84, 52
    gap = (w - 3 * fw) // 4
    # United States: stripes + blue canton
    fx = x + gap
    for i in range(7):
        d.rectangle((fx, y + 14 + i * (fh // 7), fx + fw, y + 14 + (i + 1) * (fh // 7)),
                    fill=(178, 34, 34) if i % 2 == 0 else (245, 245, 245))
    d.rectangle((fx, y + 14, fx + 34, y + 14 + 3 * (fh // 7)), fill=(28, 48, 110))
    # China: red field, one big yellow star
    fx = x + 2 * gap + fw
    d.rectangle((fx, y + 14, fx + fw, y + 14 + fh), fill=(222, 41, 16))
    d.regular_polygon((fx + 20, y + 32, 9), 5, rotation=90, fill=(255, 222, 0))
    # Russia: white / blue / red tricolour
    fx = x + 3 * gap + 2 * fw
    for i, c in enumerate(((245, 245, 245), (0, 57, 166), (213, 0, 50))):
        d.rectangle((fx, y + 14 + i * (fh // 3), fx + fw, y + 14 + (i + 1) * (fh // 3)),
                    fill=c)
    d.text((x + 10, y + h - 24), "TRUMP  ·  XI  ·  PUTIN", font=SANS_B(13), fill=INK)


def ipo_chart(d, x, y, w, h):
    """Rising bars ending at the record $81.3bn Anthropic IPO."""
    box(d, (x, y, x + w, y + h), fill=(238, 238, 234), outline=INK, width=2)
    d.text((x + 10, y + 8), "$81.3bn  ·  $83 / share", font=SANS_B(15), fill=RED)
    d.text((x + 10, y + 28), "largest IPO in history", font=SANS(12), fill=GREY)
    bars = [("2021", 0.20, (150, 150, 148)), ("2023", 0.40, (120, 130, 170)),
            ("2025", 0.62, (70, 100, 160)), ("ANT", 0.95, RED)]
    bw = 34
    gap = (w - 4 * bw) // 5
    base = y + h - 22
    avail = base - (y + 48)
    for i, (lab, frac, col) in enumerate(bars):
        bx = x + gap + i * (bw + gap)
        bh = int(avail * frac)
        d.rectangle((bx, base - bh, bx + bw, base), fill=col)
        lt = SANS_B(11)
        d.text((bx + bw / 2 - d.textlength(lab, font=lt) / 2, base + 5), lab,
               font=lt, fill=INK)


def scales_icon(d, cx, cy, s):
    """Stylised scales of justice for the ICJ panel."""
    d.line([(cx, cy - s), (cx, cy + s)], fill=INK, width=4)
    d.line([(cx - s, cy - s + 6), (cx + s, cy - s + 6)], fill=INK, width=4)
    for sgn in (-1, 1):
        d.line([(cx + sgn * s, cy - s + 6), (cx + sgn * (s - 8), cy + 4)],
               fill=INK, width=3)
        d.arc((cx + sgn * (s - 8) - 14, cy - 4, cx + sgn * (s - 8) + 14, cy + 24),
              0, 180, fill=INK, width=3)
        d.line([(cx + sgn * (s - 8) - 14, cy + 10), (cx + sgn * (s - 8) + 14, cy + 10)],
               fill=INK, width=3)
    d.rectangle((cx - 20, cy + s - 4, cx + 20, cy + s + 2), fill=INK)


def bridge_scene(d, x, y, w, h):
    """Crimea bridge: a deck arc, a support tower and a burst of smoke."""
    box(d, (x, y, x + w, y + h), fill=SKY, outline=INK, width=2)
    d.rectangle((x, y + h - 34, x + w, y + h), fill=(120, 150, 170))
    d.line([(x + 8, y + h - 44), (x + w // 2, y + 26), (x + w - 8, y + h - 44)],
           fill=(210, 210, 205), width=8)
    d.line([(x + w // 2, y + 26), (x + w // 2, y + h - 44)], fill=(210, 210, 205),
           width=8)
    for i in range(5):
        px = x + 20 + i * (w - 40) // 4
        d.line([(px, y + h - 44), (x + w // 2, y + 26)], fill=(210, 210, 205),
               width=2)
    cx, cy = x + w - 62, y + 44
    for r, c in ((34, (200, 120, 60)), (22, (240, 170, 40)), (12, (255, 230, 120))):
        d.regular_polygon((cx, cy, r), 10, fill=c)


def blossom_tree(d, x, y, w, h):
    """Van Gogh's chestnut in blossom: trunk, branches, white flower clusters."""
    box(d, (x, y, x + w, y + h), fill=(214, 232, 196), outline=INK, width=2)
    cx = x + w // 2
    d.polygon([(cx - 10, y + h - 8), (cx + 10, y + h - 8), (cx + 4, y + 52),
               (cx - 4, y + 52)], fill=(96, 66, 30))
    for dx, dy, ln in ((-52, -6, 62), (46, -14, 58), (-26, -26, 48), (24, -34, 44)):
        d.line([(cx, y + 56), (cx + dx, y + 56 + dy - ln)], fill=(96, 66, 30),
               width=5)
    for bx, by in ((cx - 52, y + 6), (cx + 46, y + 2), (cx - 26, y - 6),
                   (cx + 24, y - 14), (cx, y - 18)):
        for k in range(7):
            ox = (k % 3 - 1) * 16
            oy = (k // 3 - 1) * 12
            d.ellipse((bx + ox - 8, by + oy - 8, bx + ox + 8, by + oy + 8),
                      fill=(250, 248, 240), outline=(200, 190, 170))
        d.ellipse((bx - 5, by - 5, bx + 5, by + 5), fill=(240, 200, 60))


def vice_city(d, x, y, w, h):
    """GTA VI: neon sunset, palm silhouettes, ocean strip."""
    box(d, (x, y, x + w, y + h), fill=(255, 158, 110), outline=INK, width=2)
    d.ellipse((x + w // 2 - 44, y + 8, x + w // 2 + 44, y + 96),
              fill=(255, 214, 90))
    d.rectangle((x, y + h - 30, x + w, y + h), fill=(30, 120, 160))
    for px, lean in ((x + 34, -14), (x + w - 52, 12)):
        d.line([(px, y + h - 30), (px + lean, y + 34)], fill=(40, 40, 36), width=6)
        for a in range(-4, 5):
            d.arc((px + lean - 26, y + 18 + a * 4, px + lean + 26, y + 46 + a * 4),
                  200 + a * 8, 340 + a * 8, fill=(40, 40, 36), width=3)
    d.text((x + 10, y + h - 26), "VICE CITY", font=SANS_B(13), fill=(255, 255, 255))


def tunnel_section(d, x, y, w, h):
    """Onkalo: a cross-section of the world's first nuclear-waste repository."""
    box(d, (x, y, x + w, y + h), fill=(196, 188, 172), outline=INK, width=2)
    d.rectangle((x, y + 16, x + w, y + 52), fill=(120, 160, 90))
    d.rectangle((x, y + 52, x + w, y + h), fill=(110, 100, 86))
    d.polygon([(x + 16, y + 56), (x + w - 16, y + 56), (x + w - 60, y + h - 12),
               (x + 60, y + h - 12)], fill=(70, 64, 56))
    for i in range(4):
        cx = x + 60 + i * 48
        d.rectangle((cx, y + 66, cx + 30, y + 96), fill=(230, 210, 60),
                    outline=INK)
    d.text((x + 10, y + 104), "500 m BELOW FINLAND", font=SANS_B(12),
           fill=(245, 245, 240))


def strike_burst(d, x, y, w, h):
    """Yemen: a strike burst over a darkened camp silhouette."""
    box(d, (x, y, x + w, y + h), fill=(44, 44, 48), outline=INK, width=2)
    cx, cy = x + w // 2, y + 46
    for r, c in ((40, (255, 140, 40)), (26, (255, 200, 60)), (14, (255, 240, 160))):
        d.regular_polygon((cx, cy, r), 12, fill=c)
    d.rectangle((x, y + h - 26, x + w, y + h), fill=(20, 20, 22))
    for i in range(5):
        tx = x + 16 + i * 52
        d.polygon([(tx, y + h - 26), (tx + 18, y + h - 58), (tx + 36, y + h - 26)],
                  fill=(90, 88, 84))
    d.text((x + 10, y + 10), "53 KILLED", font=SANS_B(13), fill=(255, 200, 60))


# ------------------------------------------------------------------ page

def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer double border
    box(d, (10, 10, W - 11, H - 11), outline=INK, width=3)
    box(d, (18, 18, W - 19, H - 19), outline=INK, width=1)

    # ---- masthead
    mf = SERIF_B(60)
    title = "THE WORLD IN ONE DAY"
    fit(d, title, mf, W - 120)
    d.text(((W - d.textlength(title, font=mf)) / 2, 26), title, font=mf, fill=INK)
    rule(d, 60, 100, W - 60, 3)
    df = SANS_B(19)
    date_line = "Thursday 19 November 2026"
    fit(d, date_line, df, W - 120)
    d.text(((W - d.textlength(date_line, font=df)) / 2, 110), date_line,
           font=df, fill=RED)
    sub = SANS(15)
    tagline = "Nine stories from one day on Earth — Gaza · Shenzhen · Crimea · New York · The Hague · Paris · Vice City · Finland · Yemen"
    fit(d, tagline, sub, W - 90)
    d.text(((W - d.textlength(tagline, font=sub)) / 2, 136), tagline,
           font=sub, fill=GREY)

    # ---- row A: lead Gaza (left, wide) + Shenzhen summit (right)
    lx, ly, lw = 28, 160, 600
    tank_scene(d, lx, ly, lw, 140)
    y = kicker_headline(
        d, lx, ly + 150, lw, "GAZA  ·  LEAD STORY",
        "Israeli tanks cross the ceasefire line",
        28,
        "In a rare ground operation, Israeli armour pushed past the Yellow "
        "Line as displaced families fled the area.",
        17)
    assert y <= 500, y

    rx, rw = 648, 348
    flag_trio(d, rx, ly, rw, 96)
    y = kicker_headline(
        d, rx, ly + 106, rw, "SHENZHEN  ·  SUMMIT",
        "Trump, Xi and Putin meet in rare trilateral summit",
        19,
        "The three leaders sat down together in Shenzhen for a summit "
        "unseen in years.",
        13)
    assert y <= 500, y

    # ---- row B: four panels — Crimea, Van Gogh, GTA VI, Anthropic IPO
    my = 512
    bw4 = 230
    col4 = (28, 270, 512, 754)
    bridge_scene(d, col4[0], my, bw4, 96)
    y = kicker_headline(
        d, col4[0], my + 102, bw4, "CRIMEA  ·  ATTACK",
        "Kerch Bridge hit again; traffic halted",
        18,
        "The bridge linking Crimea to Russia was attacked once more, "
        "stopping traffic across it.",
        13)
    assert y <= 748, y

    blossom_tree(d, col4[1], my, bw4, 96)
    y = kicker_headline(
        d, col4[1], my + 102, bw4, "PARIS  ·  ART",
        "Van Gogh sells for a record $190.4m",
        18,
        "“Châtaigniers en fleurs” fetched the record price at Sotheby’s, "
        "the highest ever paid for a Van Gogh.",
        13)
    assert y <= 748, y

    vice_city(d, col4[2], my, bw4, 96)
    y = kicker_headline(
        d, col4[2], my + 102, bw4, "VICE CITY  ·  GAMES",
        "GTA VI rolls out worldwide",
        18,
        "The long-awaited game begins its global rollout, and players are "
        "pouring back into Vice City.",
        13)
    assert y <= 748, y

    ipo_chart(d, col4[3], my, bw4, 96)
    y = kicker_headline(
        d, col4[3], my + 102, bw4, "NEW YORK  ·  MARKETS",
        "Anthropic IPO is the biggest ever",
        18,
        "$81.3bn at $83 a share; trading starts Thursday on the Nasdaq as "
        "ANT, near a $1.5 trillion value.",
        13)
    assert y <= 748, y

    # ---- row C: three compact panels with a small icon gutter
    by = 752
    mw = 316
    col_x = (28, 360, 692)
    scales_icon(d, col_x[0] + 28, by + 30, 22)
    y = kicker_headline(
        d, col_x[0] + 62, by, mw - 62, "THE HAGUE  ·  JUSTICE",
        "ICJ delivers its Myanmar genocide verdict",
        18,
        "The court at The Hague delivers its verdict today in the "
        "Rohingya genocide case against Myanmar.",
        13)
    assert y <= 880, y

    d.rectangle((col_x[1], by + 6, col_x[1] + 48, by + 54), fill=(110, 100, 86),
                outline=INK)
    d.rectangle((col_x[1] + 10, by + 16, col_x[1] + 38, by + 44),
                fill=(230, 210, 60), outline=INK)
    y = kicker_headline(
        d, col_x[1] + 62, by, mw - 62, "FINLAND  ·  ENERGY",
        "First nuclear-waste repository approved",
        18,
        "Onkalo, the first permanent deep store for spent nuclear fuel, "
        "is cleared to open.",
        13)
    assert y <= 880, y

    d.regular_polygon((col_x[2] + 28, by + 30, 24), 12, fill=(255, 140, 40))
    d.regular_polygon((col_x[2] + 28, by + 30, 14), 12, fill=(255, 220, 90))
    y = kicker_headline(
        d, col_x[2] + 62, by, mw - 62, "YEMEN  ·  WAR",
        "Houthi rocket kills 53 soldiers at army camp",
        18,
        "A rocket strike on a government military camp killed 53 "
        "soldiers, the deadliest such attack in months.",
        13)
    assert y <= 880, y

    # ---- Also Today strip
    ay = 884
    rule(d, 28, ay, W - 28, 3)
    af = SANS_B(15)
    d.text((28, ay + 10), "ALSO TODAY", font=af, fill=RED)
    items = [
        "Australia sanctions Israeli settlers",
        "EU proposes a €45bn loan for Ukraine",
        "Cyclone Akvan nears India’s coast",
        "Russian held over Palantir spying",
    ]
    bf = SANS(15)
    iy2 = ay + 34
    for i, it in enumerate(items):
        cx = 28 + (i % 2) * 500
        cy = iy2 + (i // 2) * 26
        d.text((cx, cy), "▪", font=bf, fill=RED)
        fit(d, it, bf, 470)
        d.text((cx + 18, cy), it, font=bf, fill=INK)
    rule(d, 28, ay + 96, W - 28, 1, GREY)
    ff = SANS(12)
    foot = "All nine stories as reported on Thursday 19 November 2026."
    d.text(((W - d.textlength(foot, font=ff)) / 2, ay + 104), foot,
           font=ff, fill=GREY)
    return img


def main():
    img = draw_page()
    os.makedirs("output", exist_ok=True)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
