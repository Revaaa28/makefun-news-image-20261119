#!/usr/bin/env python3
"""Render entry.png: the world news of Thursday 19 November 2026 in one image.

Newspaper-poster style, drawn entirely with PIL shapes and DejaVu type so
every word stays crisp. Layout: masthead naming the day, a hero story (the
first-ever Trump-Xi-Putin trilateral in Shenzhen), three pictured panels
(GTA VI launch, the ICJ Rohingya judgment, Cyclone Akvan), a dotted world
map with numbered pins for all 13 stories, and nine one-line briefs.

Every story was verified against reporting first published on 19 November
2026 (Reuters, AP, People, NASA, the ICJ, India's IMD); where an event was
scheduled for later in the day, the wording says so ("meets today",
"delivers its verdict today") and states no outcome in advance.

Run:  python3 tools/render.py   ->  writes entry.png at the repo root
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 241, 227)      # cream newsprint
NAVY = (20, 33, 61)          # ink navy
RED = (193, 39, 45)          # accent red
PANEL_BG = (255, 253, 246)   # panel paper
MAP_BG = (233, 238, 243)     # pale sea grey-blue
CREAM = (247, 241, 227)
WHITE = (255, 255, 255)
SKY = (38, 64, 110)          # hero sky
GOLD = (212, 175, 55)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(d, text, path, max_w, start, minimum=10):
    """Largest size <= start whose text still fits max_w."""
    size = start
    while size > minimum:
        f = font(path, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, minimum)


def wrap_text(d, text, f, max_w):
    """Greedy word wrap measured with textlength; nothing overflows."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def headline_lines(d, text, max_w, max_lines=3, start=33, minimum=18,
                   max_h=None):
    """Shrink the headline font until the wrap fits max_lines lines
    (and, when max_h is given, fits that pixel height too)."""
    size = start
    while size >= minimum:
        f = font(SANS_B, size)
        lines = wrap_text(d, text, f, max_w)
        lh = int(size * 1.18)
        if len(lines) <= max_lines and (max_h is None
                                        or len(lines) * lh <= max_h):
            return f, lines
        size -= 1
    f = font(SANS_B, minimum)
    return f, wrap_text(d, text, f, max_w)


# ---------------------------------------------------------------- masthead

def draw_masthead(d):
    d.rectangle([0, 0, W, 100], fill=NAVY)
    d.rectangle([0, 100, W, 104], fill=RED)
    title = "THE WORLD IN ONE DAY"
    f = fit_font(d, title, SERIF_B, 940, 56)
    d.text((512, 40), title, font=f, fill=WHITE, anchor="mm")
    d.text((28, 78), "ONE DAY  ·  13 STORIES  ·  EVERY REGION",
           font=font(SANS_B, 15), fill=CREAM, anchor="lm")
    date = "THURSDAY, 19 NOVEMBER 2026"
    f = fit_font(d, date, SANS_B, 420, 24)
    d.text((996, 78), date, font=f, fill=(255, 120, 110), anchor="rm")


# ------------------------------------------------------------------ icons

def star_points(cx, cy, r_out, r_in, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_flag_us(d, x, y, w, h):
    """Stylised Stars and Stripes on a pole."""
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=NAVY, width=2)
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                        fill=RED)
    d.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill=NAVY)
    for r in range(3):
        for c in range(4):
            sx = x + 6 + c * (w * 0.42 - 10) / 3
            sy = y + 5 + r * (h * 4 / 7 - 8) / 2
            d.polygon(star_points(sx, sy, 3.2, 1.3), fill=WHITE)


def draw_flag_cn(d, x, y, w, h):
    """Stylised Chinese flag: red field, one large gold star."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=NAVY,
                width=2)
    d.polygon(star_points(x + w * 0.28, y + h * 0.42, 11, 4.5), fill=GOLD)
    for sx, sy in [(0.62, 0.2), (0.74, 0.32), (0.74, 0.52), (0.62, 0.64)]:
        d.polygon(star_points(x + w * sx, y + h * sy, 4.5, 1.8), fill=GOLD)


def draw_flag_ru(d, x, y, w, h):
    """Stylised Russian tricolour."""
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=NAVY, width=2)
    d.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def draw_hero_art(d, x, y, w, h):
    """Shenzhen at dusk: tower skyline and three flags."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # stars in the dusk sky
    for sx, sy in ((18, 16), (120, 10), (300, 12), (52, 34), (210, 26)):
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                  fill=(255, 230, 150))
    # skyline silhouettes
    towers = [(0, 78, 26, 118), (30, 58, 26, 138), (60, 88, 22, 108),
              (86, 48, 24, 148), (114, 70, 26, 126), (144, 90, 22, 106),
              (170, 60, 26, 136), (200, 84, 24, 112), (226, 66, 26, 130),
              (256, 92, 24, 104), (284, 74, 26, 122)]
    for tx, ty, tw, th in towers:
        d.rectangle([x + tx, y + h - th, x + tx + tw, y + h], fill=(13, 24, 48))
        for wy in range(y + h - th + 8, y + h - 8, 12):
            d.rectangle([x + tx + 6, wy, x + tx + 10, wy + 5],
                        fill=(255, 214, 120))
    # ground band
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(13, 24, 48))
    d.line([x, y + h - 26, x + w, y + h - 26], fill=GOLD, width=3)
    # three flags on poles above the skyline
    for i, fn in enumerate((draw_flag_us, draw_flag_cn, draw_flag_ru)):
        fx = x + 30 + i * 100
        d.line([fx + 16, y + 10, fx + 16, y + 82], fill=WHITE, width=3)
        fn(d, fx + 16, y + 12, 72, 46)


def draw_gta_art(d, x, y, w, h):
    """Vice City sunset: neon bands, palm silhouettes, glowing sign."""
    bands = [(255, 94, 98), (255, 149, 81), (255, 183, 77),
             (255, 214, 120), (138, 43, 226)]
    bh = h / len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=col)
    sr = h * 0.26
    d.ellipse([x + w // 2 - sr, y + h * 0.10 - sr, x + w // 2 + sr,
               y + h * 0.10 + sr], fill=(255, 244, 190))
    # sea strip
    sea = y + h * 0.82
    d.rectangle([x, sea, x + w, y + h], fill=(24, 44, 84))
    d.line([x, sea, x + w, sea], fill=(255, 120, 180), width=2)
    # palms
    for px, lean in ((x + 22, 1), (x + w - 26, -1)):
        top_y = y + h * 0.30
        d.line([px, sea, px + lean * 10, top_y], fill=(20, 20, 40), width=4)
        for a in range(-50, 61, 25):
            ang = math.radians(a - 90 + (20 if lean > 0 else -20))
            ex = px + lean * 10 + 26 * math.cos(ang)
            ey = top_y + 26 * math.sin(ang) * 0.55
            d.line([px + lean * 10, top_y, ex, ey], fill=(20, 20, 40),
                   width=3)
    f = fit_font(d, "VICE CITY", SANS_B, w - 16, 22)
    d.text((x + w // 2, y + h * 0.68), "VICE CITY", font=f,
           fill=(255, 255, 255), anchor="mm",
           stroke_width=2, stroke_fill=(255, 0, 128))


def draw_icj_art(d, x, y, w, h):
    """The Peace Palace: columns and pediment."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 222, 232))
    cx = x + w // 2
    # pediment + columns
    d.polygon([(x + 8, y + h * 0.52), (cx, y + h * 0.10),
               (x + w - 8, y + h * 0.52)], fill=NAVY)
    d.ellipse([cx - 11, y + h * 0.20, cx + 11, y + h * 0.20 + 22],
              fill=GOLD, outline=WHITE, width=2)
    for i in range(4):
        ccx = x + 26 + i * (w - 52) // 3
        d.rectangle([ccx - 8, y + h * 0.56, ccx + 8, y + h - 12], fill=WHITE,
                    outline=NAVY, width=2)
    d.rectangle([x + 8, y + h * 0.52, x + w - 8, y + h * 0.60], fill=NAVY)
    d.rectangle([x + 8, y + h - 12, x + w - 8, y + h - 6], fill=NAVY)


def draw_akvan_art(d, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal, rain over the coast."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 92))
    cx, cy = x + w // 2, y + h // 2 - 4
    r_max = int(h * 0.44)
    for r in range(r_max, 6, -7):
        a0 = (r_max - r) * 0.09
        d.arc([cx - r, cy - r, cx + r, cy + r], math.degrees(a0),
              math.degrees(a0 + 4.4), fill=WHITE, width=5)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    # rain
    for i in range(12):
        rx = x + 10 + (i * 31) % (w - 20)
        ry = y + 6 + (i * 19) % (h - 30)
        d.line([rx, ry, rx - 4, ry + 9], fill=(140, 190, 255), width=2)
    # coast + waves at the bottom
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(16, 90, 70))
    for i in range(4):
        wx = x + 8 + i * 70
        d.arc([wx, y + h - 11, wx + 40, y + h - 1], 200, 340,
              fill=WHITE, width=2)

# -------------------------------------------------------------------- map

# Equirectangular landmask, 104 columns (lon -180..180) by 24 rows
# (lat +80..-58). '#' is land, '.' is sea. Pins below are (column, row)
# cells in the same grid.

LANDMASK = [
    "....................########...........#####...........##..###....#############.......#########.....###.",
    "...########....####################...########.......##################################################.",
    "...#########...##########.....########..#####..#....##################################################..",
    "....########....###########...########...##.......###################################################...",
    "...............############..########.............###############################################.###...",
    "................#####################.............############################################...##.....",
    "................###################..............##########...####################################......",
    "...............##################................###..#######.##############################...##.......",
    "...............################.................###########################################.............",
    "................###########.##.................######################...#################...............",
    "..................##########.###...............#################.........#####..######.##...............",
    "........................###########............#######################....###....#####.##...............",
    "..........................###########...........####################........#.....###########...........",
    "...........................##############........################..................########...#######...",
    "...........................###############............##########.....................#########.######...",
    "............................###############............#########.........................###.#####......",
    ".............................############..............#########.......................###########......",
    "..............................#########................########.###....................###########......",
    "..............................########..................######..##......................#########.......",
    "...............................######....................#####...........................#######......##",
    "...............................#####........................................................#####....###",
    "...............................####..................................................................##.",
    "...............................###......................................................................",
    "...............................##.......................................................................",
]

# (label, column, row) for all 13 stories.
MAP_PINS = [
    ("1", 85, 10),    # Shenzhen
    ("2", 27, 10),    # Vice City / Miami
    ("3", 54, 4),     # The Hague
    ("4", 77, 11),    # Andhra coast
    ("5", 18, 8),     # Pasadena (NASA JPL)
    ("6", 29, 5),     # Ottawa
    ("7", 52, 6),     # Paris
    ("8", 92, 8),     # Tokyo
    ("9", 31, 8),     # Washington DC
    ("10", 58, 8),    # East Libya
    ("11", 65, 14),   # Mogadishu
    ("12", 61, 7),    # Antalya
    ("13", 96, 20),   # Australia
]

MAP_X0, MAP_Y0 = 32.7, 531.2   # centre of the (0, 0) cell
MAP_PX, MAP_PY = 9.31, 6.33    # cell pitch in pixels


def map_cell(col, row):
    return (MAP_X0 + col * MAP_PX, MAP_Y0 + row * MAP_PY)


def draw_map(d):
    d.rectangle([28, 500, 996, 684], fill=MAP_BG, outline=NAVY, width=3)
    d.rectangle([28, 500, 996, 528], fill=NAVY)
    d.text((44, 514), "THE DAY ON THE MAP", font=font(SANS_B, 19),
           fill=WHITE, anchor="lm")
    note = "numbered pins: all 13 stories"
    f = fit_font(d, note, SANS, 400, 15, minimum=11)
    d.text((980, 514), note, font=f, fill=CREAM, anchor="rm")
    for row, line in enumerate(LANDMASK):
        for col, ch in enumerate(line):
            if ch == "#":
                cx, cy = map_cell(col, row)
                d.ellipse([cx - 2.7, cy - 2.7, cx + 2.7, cy + 2.7], fill=NAVY)
    for label, col, row in MAP_PINS:
        cx, cy = map_cell(col, row)
        if len(label) > 1:
            r, fs = 11, 10
        else:
            r, fs = 10, 13
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=WHITE,
                  width=2)
        d.text((cx, cy), label, font=font(SANS_B, fs), fill=WHITE, anchor="mm")


# ------------------------------------------------------------------- hero

def draw_hero(d):
    d.rectangle([28, 112, 996, 300], fill=PANEL_BG, outline=NAVY, width=3)
    draw_hero_art(d, 36, 120, 330, 172)
    d.text((382, 132), "1  ·  SHENZHEN  ·  APEC SUMMIT  ·  FIRST-EVER TRILATERAL",
           font=font(SANS_B, 15), fill=RED, anchor="la")
    f, lines = headline_lines(d, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                              596, max_lines=2, start=36, minimum=28)
    ty = 156
    for line in lines:
        d.text((382, ty), line, font=f, fill=NAVY, anchor="la")
        ty += int(f.size * 1.16)
    body = ("The leaders of the US, China and Russia sit down together for "
            "the first time — with Ukraine, Iran and nuclear arms on the "
            "agenda.")
    bf = font(SANS, 16)
    for i, line in enumerate(wrap_text(d, body, bf, 596)):
        d.text((382, ty + 4 + i * 19), line, font=bf, fill=(40, 40, 40),
               anchor="la")


# ----------------------------------------------------------------- panels

PANELS = [
    ("2  ·  VICE CITY", "GTA VI LAUNCHES WORLDWIDE",
     "Rockstar's Vice City epic arrives after 13 years, to a 99 "
     "Metacritic score.", draw_gta_art),
    ("3  ·  THE HAGUE", "WORLD COURT RULES ON ROHINGYA CASE",
     "The Hague delivers its verdict today in The Gambia's genocide case "
     "against Myanmar.", draw_icj_art),
    ("4  ·  BAY OF BENGAL", "CYCLONE AKVAN NEARS INDIA'S COAST",
     "Red alerts and school closures in Odisha and Andhra Pradesh; "
     "landfall due Friday.", draw_akvan_art),
]


def draw_panels(d):
    pw, ph = 314, 184
    for i, (place, headline, body, art) in enumerate(PANELS):
        px = 28 + i * (pw + 13)
        py = 308
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL_BG, outline=NAVY,
                    width=3)
        d.rectangle([px, py, px + pw, py + 28], fill=NAVY)
        d.text((px + 12, py + 14), place, font=font(SANS_B, 17), fill=WHITE,
               anchor="lm")
        art(d, px + 8, py + 36, pw - 16, 62)
        f, lines = headline_lines(d, headline, pw - 20, max_lines=2,
                                  start=20, minimum=16, max_h=48)
        ty = py + 104
        for line in lines:
            d.text((px + 10, ty), line, font=f, fill=NAVY, anchor="la")
            ty += int(f.size * 1.18)
        bf = font(SANS, 12)
        for j, line in enumerate(wrap_text(d, body, bf, pw - 20)):
            d.text((px + 10, ty + 2 + j * 14), line, font=bf,
                   fill=(40, 40, 40), anchor="la")


# ----------------------------------------------------------------- briefs

# (number, place, headline, body) — stories 5..13.
BRIEFS = [
    ("5", "VOYAGER 1", "NASA confirms Voyager 1 one light-day out",
     "The 1977 probe, 16bn miles away, is the first human-made object "
     "to reach the mark."),
    ("6", "OTTAWA", "Carney resets Canada's China ties",
     "Ottawa adjusts the relationship as it seeks the right deal with "
     "Washington."),
    ("7", "PARIS", "Mélenchon 'could win', minister says",
     "France's justice minister says the hard-left leader could take "
     "the top job."),
    ("8", "TOKYO", "India and Japan review defence ties",
     "Ministers meet in Tokyo to deepen security cooperation between "
     "the two powers."),
    ("9", "WASHINGTON", "US proposes tougher green-card rules",
     "Employment-based green cards face longer hiring processes under "
     "the new proposals."),
    ("10", "EAST LIBYA", "Cocaine and millions of pills seized",
     "A major drugs haul is seized in eastern Libya, officials say."),
    ("11", "MOGADISHU", "Somalia accuses UAE of secret bases",
     "Mogadishu says the UAE built military bases on its soil without "
     "federal approval."),
    ("12", "ANTALYA", "COP31 climate talks continue",
     "Negotiators press on in Turkey as the summit runs into its final "
     "stretch."),
    ("13", "AUSTRALIA", "Duckett's 133 puts England on top",
     "Ben Duckett hits 133 in the third ODI against Australia."),
]


def draw_brief(d, x, y, num, place, headline, body, col_w):
    r = 13
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    d.text((x + r, y + r), num, font=font(SANS_B, 13 if len(num) < 2 else 11),
           fill=WHITE, anchor="mm")
    tx = x + 2 * r + 8
    tw = col_w - 2 * r - 8
    f, lines = headline_lines(d, place + ": " + headline, tw, max_lines=2,
                              start=15, minimum=12)
    ty = y
    for line in lines:
        d.text((tx, ty), line, font=f, fill=NAVY, anchor="la")
        ty += int(f.size * 1.18)
    bf = font(SANS, 12)
    for j, line in enumerate(wrap_text(d, body, bf, tw)[:2]):
        d.text((tx, ty + 2 + j * 15), line, font=bf, fill=(40, 40, 40),
               anchor="la")


def draw_briefs(d):
    d.rectangle([28, 692, 996, 988], fill=PANEL_BG, outline=NAVY, width=3)
    d.rectangle([28, 692, 996, 720], fill=NAVY)
    d.text((44, 706), "AROUND THE WORLD IN BRIEF", font=font(SANS_B, 19),
           fill=WHITE, anchor="lm")
    d.text((980, 706), "9 more stories from the day", font=font(SANS, 14),
           fill=CREAM, anchor="rm")
    col_w = 306
    for i, (num, place, headline, body) in enumerate(BRIEFS):
        cx = 44 + (i % 3) * (col_w + 16)
        cy = 734 + (i // 3) * 82
        draw_brief(d, cx, cy, num, place, headline, body, col_w)


# -------------------------------------------------------------------- main

def main():
    for row in LANDMASK:
        assert len(row) == 104, f"landmask row has {len(row)} cells"
    assert len(LANDMASK) == 24
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_hero(d)
    draw_panels(d)
    draw_map(d)
    draw_briefs(d)
    d.text((512, 1008),
           "All 13 stories verified from reporting first published on 19 November 2026  ·  "
           "Drawn entirely by code — no photographs",
           font=font(SANS, 12), fill=(90, 90, 90), anchor="mm")
    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
