#!/usr/bin/env python3
"""Render the round-4 front page for Thursday 19 November 2026.

Newspaper front page, 1024x1024, drawn with PIL. Eight main stories.
Copy is kept to what was reported that day: no vote counts, no intraday
prices, no superlatives the reporting did not carry, no dated stories.
Run: python3 render.py  (writes entry.png)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (31, 56, 100)
GOLD = (217, 164, 65)
GRAY = (102, 102, 102)
SKY = (188, 216, 234)
SAND = (217, 196, 154)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def kicker(d, x, y, text, size=16):
    d.text((x, y), text, font=font(SANS_B, size), fill=RED)
    return y + size + 4


def headline(d, x, y, text, size, max_w):
    f = font(SERIF_B, size)
    lh = int(size * 1.22)
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=INK)
        y += lh
    return y


def deck(d, x, y, text, size, max_w):
    f = font(SANS, size)
    lh = int(size * 1.35)
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=INK)
        y += lh
    return y


def rule(d, y, x0=28, x1=996, width=2):
    d.line([(x0, y), (x1, y)], fill=INK, width=width)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    for i in range(0, 7, 2):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill=(178, 34, 52))
    cw, ch = w * 0.4, h * 4 / 7
    d.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 4 + c * cw / 5, y + 3 + r * ch / 4,
                       x + 8 + c * cw / 5, y + 7 + r * ch / 4], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=1)
    star(d, x + w * 0.22, y + h * 0.3, h * 0.22, (255, 222, 0))
    for sx, sy in [(0.55, 0.15), (0.68, 0.28), (0.68, 0.48), (0.55, 0.62)]:
        star(d, x + w * sx, y + h * sy, h * 0.08, (255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx, top, bot = x + w / 2, y + 22, y + h - 26
    d.rectangle([cx - 5, top, cx + 5, bot], fill=GOLD)
    d.rectangle([x + 40, bot, x + w - 40, bot + 10], fill=GOLD)
    d.rectangle([cx - 105, top + 14, cx + 105, top + 22], fill=GOLD)
    d.ellipse([cx - 12, top - 10, cx + 12, top + 14], fill=GOLD)
    for sx in (cx - 105, cx + 105):
        d.line([(sx, top + 18), (sx - 26, bot - 34)], fill=GOLD, width=3)
        d.line([(sx, top + 18), (sx + 26, bot - 34)], fill=GOLD, width=3)
        d.line([(sx - 26, bot - 34), (sx + 26, bot - 34)], fill=GOLD, width=3)
        d.pieslice([sx - 30, bot - 36, sx + 30, bot + 8], 0, 180, fill=GOLD)


def tank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    gy = y + h * 0.62
    d.rectangle([x, gy, x + w, y + h], fill=SAND)
    d.line([(x + 8, gy + 26), (x + w - 8, gy + 26)], fill=(230, 200, 40), width=4)
    bx, by, bw, bh = x + w * 0.30, gy - 34, w * 0.58, 30
    d.polygon([(bx, by + bh), (bx, by + 8), (bx + 18, by),
               (bx + bw, by), (bx + bw, by + bh)], fill=(40, 44, 48))
    d.line([(bx + bw - 6, by + 10), (bx + bw + 34, by + 2)], fill=(40, 44, 48), width=7)
    for i in range(6):
        wx = bx + 8 + i * (bw - 16) / 5
        d.ellipse([wx - 8, by + bh - 4, wx + 8, by + bh + 12], fill=(90, 90, 90),
                  outline=INK, width=2)
    for fx in (x + 26, x + 52):
        d.ellipse([fx - 5, gy - 26, fx + 5, gy - 16], fill=INK)
        d.line([(fx, gy - 16), (fx, gy + 2)], fill=INK, width=3)
        d.line([(fx, gy - 8), (fx - 8, gy + 2)], fill=INK, width=3)
        d.line([(fx, gy - 8), (fx + 8, gy + 2)], fill=INK, width=3)


def bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 222, 238))
    sy = y + h * 0.62
    d.rectangle([x, sy, x + w, y + h], fill=(90, 140, 175))
    ex, ey = x + w * 0.62, y + 26
    d.ellipse([ex - 22, ey - 14, ex + 22, ey + 30], fill=(232, 120, 30))
    d.ellipse([ex - 11, ey - 4, ex + 11, ey + 18], fill=(245, 200, 60))
    d.line([(x + 6, sy - 6), (x + w - 6, sy - 6)], fill=(60, 60, 60), width=5)
    for px in (0.2, 0.5, 0.8):
        d.line([(x + w * px, sy - 6), (x + w * px, sy - 30)], fill=(60, 60, 60), width=4)
        d.line([(x + w * px, sy - 30), (x + w * px - 16, sy - 6)], fill=(60, 60, 60), width=2)
        d.line([(x + w * px, sy - 30), (x + w * px + 16, sy - 6)], fill=(60, 60, 60), width=2)


def sunset(d, x, y, w, h):
    for i, col in enumerate([(244, 130, 60), (238, 90, 90), (150, 70, 130), (60, 50, 110)]):
        d.rectangle([x, y + i * h / 4, x + w, y + (i + 1) * h / 4], fill=col)
    d.ellipse([x + w * 0.36, y + h * 0.10, x + w * 0.72, y + h * 0.62], fill=(250, 210, 90))
    base = y + h * 0.72
    for bx, bw, bh in [(0.02, 0.20, 0.30), (0.24, 0.14, 0.42), (0.40, 0.18, 0.26),
                       (0.60, 0.12, 0.38), (0.74, 0.24, 0.22)]:
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + bw), y + h], fill=(30, 25, 45))
    d.line([(x + w * 0.86, y + h * 0.30), (x + w * 0.88, y + h * 0.72)], fill=(30, 25, 45), width=5)
    for a in (-50, -20, 10, 40):
        rad = math.radians(a - 90)
        d.line([(x + w * 0.86, y + h * 0.32),
                (x + w * 0.86 + 26 * math.cos(rad), y + h * 0.32 + 26 * math.sin(rad))],
               fill=(30, 25, 45), width=4)


def blossom(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 200))
    d.line([(x + 8, y + h - 8), (x + w * 0.55, y + 12)], fill=(110, 70, 40), width=7)
    d.line([(x + w * 0.30, y + h * 0.62), (x + w * 0.85, y + h * 0.30)], fill=(110, 70, 40), width=5)
    spots = [(0.25, 0.62), (0.38, 0.45), (0.52, 0.30), (0.62, 0.18), (0.72, 0.42),
             (0.82, 0.55), (0.45, 0.62), (0.58, 0.52), (0.30, 0.30), (0.68, 0.68),
             (0.15, 0.45), (0.88, 0.30)]
    for sx, sy in spots:
        cx, cy = x + w * sx, y + h * sy
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(250, 246, 235),
                  outline=(200, 190, 170), width=1)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 200, 60))


def ipo_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    d.text((x + 10, y + 6), "$81.3bn  ·  $83 / share", font=font(SANS_B, 14), fill=RED)
    d.text((x + 10, y + 26), "largest IPO in history", font=font(SANS, 13), fill=GRAY)
    base = y + h - 24
    vals = [("2021", 16, (170, 170, 170)), ("2023", 24, (140, 150, 190)),
            ("2025", 34, (70, 90, 160)), ("ANT", 46, (176, 30, 36))]
    bw = (w - 40) / 4
    for i, (lab, bh, col) in enumerate(vals):
        bx = x + 20 + i * bw
        d.rectangle([bx, base - bh, bx + bw - 12, base], fill=col)
        d.text((bx, base + 4), lab, font=font(SANS, 12), fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, 1010, 1010], outline=INK, width=3)
    d.rectangle([20, 20, 1004, 1004], outline=INK, width=1)

    # Masthead
    d.text((W / 2, 32), "THE WORLD IN ONE DAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    rule(d, 106)
    d.text((W / 2, 114), "THURSDAY 19 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=RED, anchor="ma")
    d.text((W / 2, 150), "Eight stories from one day on Earth — The Hague · Gaza · "
           "Shenzhen · New York · Crimea · Vice City · Paris · Brussels",
           font=font(SANS, 15), fill=GRAY, anchor="ma")

    # Lead: ICJ verdict
    kicker(d, 28, 178, "THE HAGUE · JUSTICE")
    y = headline(d, 28, 200, "World court finds Myanmar guilty of genocide", 36, 566)
    deck(d, 28, y + 6, "The court at The Hague rules Myanmar's army committed "
         "genocide against the Rohingya and orders reparations.", 17, 566)
    scales(d, 622, 178, 374, 162)

    rule(d, 364)

    # Row 2: summit + IPO
    flag_us(d, 28, 378, 148, 62)
    flag_cn(d, 184, 378, 148, 62)
    flag_ru(d, 340, 378, 148, 62)
    d.text((28, 446), "TRUMP  ·  XI  ·  PUTIN", font=font(SANS_B, 14), fill=INK)
    kicker(d, 28, 468, "SHENZHEN · SUMMIT")
    y = headline(d, 28, 490, "Trump, Xi and Putin meet in rare trilateral summit", 24, 462)
    deck(d, 28, y + 4, "The three leaders sat down together in Shenzhen.", 15, 462)
    ipo_chart(d, 524, 378, 472, 92)
    kicker(d, 524, 468, "NEW YORK · MARKETS")
    y = headline(d, 524, 490, "Anthropic IPO is the biggest ever", 24, 472)
    deck(d, 524, y + 4, "The $81.3bn listing at $83 a share is the largest ever.", 15, 472)

    rule(d, 586)

    # Row 3: three illustrated stories
    cols = [(28, tank, "GAZA · WAR", "Israeli troops cross the ceasefire line",
             "Israeli armour pushed past the Yellow Line in a rare ground operation."),
            (360, bridge, "CRIMEA · ATTACK", "Kerch Bridge hit again; traffic halted",
             "The bridge linking Crimea to Russia was attacked once more."),
            (692, sunset, "VICE CITY · GAMES", "GTA VI rolls out worldwide",
             "The long-awaited game begins its global rollout.")]
    for x, art, kick, head, dk in cols:
        art(d, x, 598, 304, 70)
        kicker(d, x, 676, kick, 15)
        y = headline(d, x, 698, head, 20, 304)
        deck(d, x, y + 2, dk, 13, 304)

    rule(d, 798)

    # Row 4: Van Gogh + EU loan
    blossom(d, 28, 810, 190, 104)
    kicker(d, 236, 810, "PARIS · ART")
    y = headline(d, 236, 832, "Van Gogh sells for a record $190.4m", 23, 264)
    deck(d, 236, y + 4, "“Châtaigniers en fleurs” (1890) set the record at "
         "Sotheby's.", 14, 264)
    d.ellipse([524, 810, 578, 864], fill=NAVY)
    d.text((551, 820), "€", font=font(SANS_B, 30), fill=(255, 255, 255), anchor="ma")
    kicker(d, 592, 810, "BRUSSELS · EUROPE")
    y = headline(d, 592, 832, "EU proposes a €45bn loan for Ukraine", 23, 404)
    deck(d, 592, y + 4, "Brussels puts forward the loan as Kyiv seeks funds to "
         "keep the war effort going.", 14, 404)

    # Also today
    rule(d, 942)
    kicker(d, 28, 954, "ALSO TODAY")
    items = ["Australia sanctions Israeli settlers",
             "Cyclone Akvan nears India's coast",
             "Russian held over Palantir spying"]
    for i, item in enumerate(items):
        x = 28 + i * 324
        d.rectangle([x, 980, x + 9, 989], fill=RED)
        d.text((x + 16, 976), item, font=font(SANS, 14), fill=INK)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
