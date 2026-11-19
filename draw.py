#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed palette, fixed fonts, fixed layout, no randomness,
no network, no timestamps in the image. Run: python3 draw.py
Writes entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (20, 33, 61)
GOLD = (212, 160, 60)
RED = (178, 34, 34)
TEAL = (13, 110, 110)
BLUE = (31, 90, 160)
GREEN = (34, 120, 60)
ORANGE = (214, 110, 30)
GREY = (90, 96, 104)
LIGHT = (255, 255, 255)
CARD = (255, 255, 255)
SAND = (226, 205, 160)
DESERT = (196, 164, 110)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, max_w, leading):
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(d, x, y, w, h, kicker, kcolor, headline, body, hsize=27,
          bsize=19, max_text_y=None):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=(200, 196, 184), width=2)
    ix, iy = x + 14, y + 12
    d.text((ix, iy), kicker, font=font(SANS_B, 16), fill=kcolor)
    iy += 26
    iy = text_block(d, ix, iy, headline, font(SANS_B, hsize), INK, w - 28,
                    hsize + 4)
    iy += 4
    iy = text_block(d, ix, iy, body, font(SANS, bsize), (48, 52, 62), w - 28,
                    bsize + 5)
    if max_text_y is not None and iy > max_text_y:
        raise SystemExit(
            "TEXT OVERFLOW in panel %r: text ends y=%d, limit %d"
            % (headline, iy, max_text_y))
    return ix, iy


def starburst(d, cx, cy, r1, r2, n, fill):
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def icon_gaza(d, x, y, w, h):
    # sky / sand, Yellow Line dashed across the middle
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=SAND)
    # tents on the far side
    for tx in (0.10, 0.24, 0.36):
        bx = x + w * tx
        by = y + h * 0.42
        d.polygon([(bx, by - 14), (bx + 18, by), (bx - 18, by)],
                  fill=(150, 120, 80))
    # dashed Yellow Line
    ly = y + h * 0.58
    for i in range(14):
        sx = x + 6 + i * (w - 12) / 14
        d.line([sx, ly, sx + (w - 12) / 28, ly], fill=(232, 190, 0),
               width=4)
    # two tanks below the line
    for tx in (0.55, 0.80):
        cx = x + w * tx
        cy = y + h * 0.76
        d.rectangle([cx - 26, cy - 8, cx + 26, cy + 6], fill=(74, 78, 66))
        d.rectangle([cx - 12, cy - 16, cx + 12, cy - 8], fill=(60, 64, 54))
        d.line([cx + 12, cy - 12, cx + 34, cy - 16], fill=(60, 64, 54),
               width=4)
        for wx in range(-24, 26, 12):
            d.ellipse([cx + wx - 3, cy + 2, cx + wx + 3, cy + 8],
                      fill=(40, 42, 36))
    d.text((x + 8, y + 6), "GAZA  ·  YELLOW LINE",
           font=font(SANS_B, 14), fill=(90, 70, 40))


def icon_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 242))
    # globe
    cx, cy, r = x + w * 0.28, y + h * 0.52, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(31, 90, 160))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255),
              width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    # three flags
    for i, c in enumerate([(178, 34, 34), (20, 33, 61), (31, 90, 160)]):
        fx = x + w * (0.62 + i * 0.12)
        d.line([fx, y + 14, fx, y + h - 14], fill=(80, 80, 80), width=3)
        d.polygon([(fx, y + 14), (fx + 26, y + 22), (fx, y + 30)], fill=c)
    d.text((x + w - 92, y + h - 22), "SHENZHEN", font=font(SANS_B, 14),
           fill=(60, 60, 70))


def icon_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 238))
    # sky
    d.rectangle([x, y, x + w, y + h * 0.45], fill=(158, 196, 224))
    # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(24, 72, 110))
    for i in range(3):
        wx = x + 14 + i * (w - 28) / 2
        d.arc([wx, y + h * 0.72, wx + 34, y + h * 0.88], 0, 180,
              fill=(255, 255, 255), width=3)
    # bridge deck, broken in the middle
    dy = y + h * 0.52
    d.line([x + 8, dy, x + w * 0.44, dy], fill=(70, 70, 78), width=8)
    d.line([x + w * 0.60, dy, x + w - 8, dy], fill=(70, 70, 78), width=8)
    # fallen span in the water
    d.line([x + w * 0.46, dy + 6, x + w * 0.56, y + h * 0.86],
           fill=(70, 70, 78), width=7)
    # one arch standing, one tilted
    d.arc([x + w * 0.10, dy - 52, x + w * 0.40, dy + 10], 180, 360,
          fill=(150, 40, 40), width=5)
    d.arc([x + w * 0.62, dy - 40, x + w * 0.90, dy + 22], 200, 340,
          fill=(150, 40, 40), width=5)
    # smoke
    d.ellipse([x + w * 0.44, dy - 34, x + w * 0.58, dy - 10],
              fill=(120, 120, 120))


def icon_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    # rising bars
    bars = [0.25, 0.35, 0.30, 0.48, 0.60, 0.78]
    bw = w / len(bars)
    for i, f in enumerate(bars):
        bx = x + i * bw + 6
        bh = h * f
        d.rectangle([bx, y + h - 8 - bh, bx + bw - 12, y + h - 8],
                    fill=(34, 160, 90) if i < 5 else (212, 160, 60))
    # trend arrow (kept below the top label)
    d.line([x + 12, y + h * 0.58, x + w * 0.55, y + h * 0.38,
            x + w - 16, y + h * 0.24], fill=(255, 255, 255), width=3)
    d.polygon([(x + w - 16, y + h * 0.24), (x + w - 32, y + h * 0.24),
               (x + w - 16, y + h * 0.40)], fill=(255, 255, 255))
    d.text((x + 8, y + 6), "ANT  ·  $83  ·  $81.3BN",
           font=font(SANS_B, 14), fill=(255, 255, 255))


def icon_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    # courthouse pediment + columns
    px, py = x + w * 0.5, y + 8
    d.polygon([(px - 52, py + 18), (px + 52, py + 18), (px, py)],
              fill=(150, 40, 40))
    d.rectangle([px - 52, py + 18, px + 52, py + 24], fill=(90, 70, 50))
    for i in range(4):
        cx = x + w * (0.28 + i * 0.15)
        d.rectangle([cx - 5, py + 24, cx + 5, y + h - 10],
                    fill=(120, 100, 80))
    d.rectangle([x + w * 0.18, y + h - 12, x + w * 0.82, y + h - 6],
                fill=(90, 70, 50))
    # scales of justice, small, at right
    sx, sy = x + w * 0.86, y + h * 0.30
    d.line([sx, sy - 10, sx, sy + 12], fill=(60, 60, 60), width=2)
    d.line([sx - 12, sy - 8, sx + 12, sy - 8], fill=(60, 60, 60), width=2)
    d.polygon([(sx - 14, sy + 2), (sx - 8, sy + 2), (sx - 11, sy + 8)],
              fill=(212, 160, 60))
    d.polygon([(sx + 8, sy + 2), (sx + 14, sy + 2), (sx + 11, sy + 8)],
              fill=(212, 160, 60))
    d.text((x + 8, y + 4), "THE HAGUE", font=font(SANS_B, 13),
           fill=(60, 60, 70))


def icon_vangogh(d, x, y, w, h):
    # framed painting: blossom tree under a swirling sky
    d.rectangle([x, y, x + w, y + h], fill=(120, 84, 50))
    ix, iy, iw, ih = x + 5, y + 5, w - 10, h - 10
    d.rectangle([ix, iy, ix + iw, iy + ih], fill=(96, 140, 200))
    # swirl sun
    sx, sy = ix + iw * 0.78, iy + ih * 0.28
    d.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], fill=(255, 214, 90))
    d.arc([sx - 18, sy - 18, sx + 18, sy + 18], 20, 300,
          fill=(255, 214, 90), width=3)
    # blossom tree
    tx = ix + iw * 0.30
    top = iy + ih * 0.42
    d.polygon([(tx - 6, iy + ih), (tx + 6, iy + ih), (tx + 2, top),
               (tx - 2, top)], fill=(90, 60, 30))
    for dx, dy, r in [(-16, -8, 9), (10, -14, 10), (0, -22, 9), (18, -4, 8),
                      (-6, 2, 7)]:
        d.line([tx, top, tx + dx, top + dy], fill=(90, 60, 30), width=3)
        d.ellipse([tx + dx - r, top + dy - r,
                   tx + dx + r, top + dy + r],
                  fill=(255, 220, 230))
    d.rectangle([ix, iy + ih - 8, ix + iw, iy + ih], fill=(110, 160, 90))


def icon_gta(d, x, y, w, h):
    # Vice City sunset: orange sky, skyline, palm
    d.rectangle([x, y, x + w, y + h], fill=(232, 120, 80))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(90, 40, 90))
    # sun
    sx, sy = x + w * 0.72, y + h * 0.34
    d.ellipse([sx - 12, sy - 12, sx + 12, sy + 12], fill=(255, 230, 150))
    # skyline
    for bx, bw, bh in [(0.04, 0.16, 0.34), (0.24, 0.12, 0.44),
                       (0.40, 0.18, 0.30), (0.62, 0.14, 0.40)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h],
                    fill=(40, 20, 60))
    # palm tree
    px, py = x + w * 0.52, y + h * 0.62
    d.line([px, py, px + 2, y + h - 4], fill=(30, 60, 30), width=3)
    for ang in (-50, -20, 10, 40):
        ex = px + 14 * math.cos(math.radians(ang - 90))
        ey = py + 12 * math.sin(math.radians(ang - 90))
        d.line([px, py, ex, ey], fill=(30, 120, 50), width=3)
    d.text((x + 8, y + 4), "VICE CITY", font=font(SANS_B, 13),
           fill=(255, 255, 255))


def icon_onkalo(d, x, y, w, h):
    # underground repository: rock layers + lit tunnel
    d.rectangle([x, y, x + w, y + h], fill=(96, 78, 60))
    d.rectangle([x, y, x + w, y + h * 0.30], fill=(120, 100, 78))
    d.line([x, y + h * 0.30, x + w, y + h * 0.30], fill=(70, 56, 44),
           width=2)
    # tunnel arch
    cx, cy = x + w * 0.5, y + h * 0.78
    d.pieslice([cx - 34, cy - 26, cx + 34, cy + 26], 180, 360,
               fill=(20, 16, 12))
    d.rectangle([cx - 34, cy, cx + 34, cy + 10], fill=(20, 16, 12))
    # light at the end
    d.ellipse([cx - 5, cy - 8, cx + 5, cy + 2], fill=(255, 220, 120))
    # radiation trefoil, small, top right
    tx, ty = x + w * 0.86, y + h * 0.16
    d.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill=(255, 220, 0))
    for a in (90, 210, 330):
        ex = tx + 9 * math.cos(math.radians(a))
        ey = ty + 9 * math.sin(math.radians(a))
        d.pieslice([ex - 5, ey - 5, ex + 5, ey + 5], 0, 360,
                   fill=(255, 220, 0))
    d.text((x + 8, y + 4), "ONKALO", font=font(SANS_B, 13),
           fill=(255, 235, 200))


def icon_yemen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    # camp tents
    for tx in (0.14, 0.30):
        bx = x + w * tx
        by = y + h * 0.80
        d.polygon([(bx, by - 12), (bx + 14, by), (bx - 14, by)],
                  fill=(150, 120, 80))
    # incoming rocket + explosion
    rx, ry = x + w * 0.72, y + h * 0.30
    d.line([rx - 34, ry + 12, rx - 6, ry + 2], fill=(120, 120, 120),
           width=2)
    d.polygon([(rx - 12, ry - 4), (rx + 12, ry + 2), (rx - 12, ry + 8)],
              fill=(70, 70, 78))
    starburst(d, rx + 16, ry + 14, 16, 7, 8, (255, 196, 0))
    starburst(d, rx + 16, ry + 14, 9, 4, 8, (232, 90, 20))
    d.text((x + 8, y + 4), "YEMEN", font=font(SANS_B, 13),
           fill=(90, 70, 40))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 14), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 52), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 76), "THURSDAY  ·  19 NOVEMBER 2026",
           font=font(SANS_B, 26), fill=GOLD, anchor="ma")
    d.line([24, 118, W - 24, 118], fill=GOLD, width=3)

    # ---- Lead row: Gaza (left) + Shenzhen summit (right) ----
    y0, lh = 132, 300
    panel(d, 24, y0, 576, lh, "LEAD  ·  GAZA", RED,
          "Israeli tanks cross Gaza ceasefire line",
          "A rare ground incursion beyond the Yellow Line sent "
          "displaced families fleeing their tents in central Gaza.",
          hsize=30, bsize=20, max_text_y=y0 + 190)
    icon_gaza(d, 40, y0 + 196, 544, 88)
    panel(d, 616, y0, 384, lh, "CHINA  ·  SUMMIT", TEAL,
          "Trump, Xi and Putin meet in Shenzhen",
          "Xi embraced Trump on the tarmac. The three leaders hold "
          "a rare trilateral summit on Thursday.",
          hsize=26, bsize=19, max_text_y=y0 + 190)
    icon_summit(d, 632, y0 + 196, 352, 88)

    # ---- Row 2: Kerch, Anthropic, ICJ ----
    y1, h2 = 446, 244
    panel(d, 24, y1, 312, h2, "UKRAINE  ·  WAR", BLUE,
          "Crimean Bridge attacked again",
          "Traffic halted after a fresh strike on the bridge.",
          hsize=24, bsize=17, max_text_y=y1 + 166)
    icon_bridge(d, 38, y1 + 172, 284, 58)
    panel(d, 352, y1, 312, h2, "BUSINESS  ·  ANTHROPIC", GREEN,
          "Biggest IPO ever: $81.3bn",
          "Claude's maker priced shares at $83. Trading starts "
          "Thursday on Nasdaq as ANT.",
          hsize=24, bsize=17, max_text_y=y1 + 166)
    icon_ipo(d, 366, y1 + 172, 284, 58)
    panel(d, 680, y1, 320, h2, "JUSTICE  ·  THE HAGUE", RED,
          "ICJ rules on Myanmar genocide case",
          "The Hague delivers its verdict today in The Gambia's case "
          "over the 2017 Rohingya crackdown.",
          hsize=24, bsize=17, max_text_y=y1 + 166)
    icon_icj(d, 694, y1 + 172, 292, 58)

    # ---- Row 3: four small stories ----
    y2, h3 = 704, 216
    small = [
        ("ART  ·  NEW YORK", ORANGE, "Van Gogh sells for $190.4m",
         "Record price; Nazi-era dispute settled.",
         icon_vangogh),
        ("CULTURE  ·  GAMING", TEAL, "GTA VI rolls out worldwide",
         "Gamers enter Vice City at last.",
         icon_gta),
        ("ENERGY  ·  FINLAND", GREEN, "Nuclear waste store opens",
         "World's first spent-fuel store, at Onkalo.",
         icon_onkalo),
        ("WAR  ·  YEMEN", RED, "Houthi rocket kills 53 soldiers",
         "Strike on a government army camp in Yemen.",
         icon_yemen),
    ]
    x = 24
    for kicker, kc, head, body, icon in small:
        w = 238 if x < 700 else 240
        panel(d, x, y2, w, h3, kicker, kc, head, body, hsize=21, bsize=17,
              max_text_y=y2 + 148)
        icon(d, x + 14, y2 + 154, w - 28, 48)
        x += w + 8

    # ---- Footer strip ----
    fy = 936
    d.rectangle([24, fy, W - 24, 1000], fill=NAVY)
    d.text((W // 2, fy + 10),
           "ALSO: Australia sanctions Israeli settlers  ·  EU proposes €45bn Ukraine loan",
           font=font(SANS_B, 17), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, fy + 36),
           "Cyclone Akvan nears India's coast  ·  Russian held over Palantir spying",
           font=font(SANS, 16), fill=(200, 210, 225), anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
