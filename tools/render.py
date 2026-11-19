"""Draw the 19 November 2026 world-news poster, v3 (1024x1024, PIL only).

A broadsheet front page: masthead naming the day, six featured stories
with drawn scenes (the Shenzhen trilateral as hero, the GTA VI launch,
the Rohingya verdict, Cyclone Akvan, the Crimean Bridge strike and
Anthropic's market debut), a dotted world map with 22 numbered pins,
and sixteen short briefs covering the rest of the day.

Deterministic: no randomness, no clock, no network. Running this module
twice produces byte-identical PNGs.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (20, 33, 61)
NAVY_DARK = (13, 22, 43)
RED = (201, 42, 42)
CREAM = (247, 241, 227)
PAPER = (255, 253, 247)
INK = (24, 28, 38)
GREY = (90, 96, 110)
LIGHT_BLUE = (214, 228, 240)
GOLD = (232, 180, 60)
MAP_BG = (232, 238, 245)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_width, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def layout_flow(draw, segments, max_width):
    """Word-wrap mixed-style segments [(text, font, fill), ...].

    Returns a list of lines; each line is a list of (word, font, fill).
    """
    words = []
    for text, fnt, fill in segments:
        for word in text.split():
            words.append((word, fnt, fill))
    lines, cur, cur_w = [], [], 0.0
    for word, fnt, fill in words:
        ww = draw.textlength(word, font=fnt)
        add = ww
        if cur:
            add += draw.textlength(" ", font=cur[-1][1])
        if cur and cur_w + add > max_width:
            lines.append(cur)
            cur, cur_w = [(word, fnt, fill)], ww
        else:
            cur.append((word, fnt, fill))
            cur_w += add
    if cur:
        lines.append(cur)
    return lines


def draw_flow(draw, x, y, lines, leading):
    """Draw lines produced by layout_flow; returns y below the last line."""
    for line in lines:
        cx = x
        prev_fnt = None
        for word, fnt, fill in line:
            if prev_fnt is not None:
                cx += draw.textlength(" ", font=prev_fnt)
            draw.text((cx, y), word, font=fnt, fill=fill)
            cx += draw.textlength(word, font=fnt)
            prev_fnt = fnt
        y += leading
    return y


def panel(draw, x0, y0, x1, y1, fill=PAPER, outline=NAVY, width=2):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)


def header_strip(draw, x0, y0, x1, y1, left, right=None,
                 left_size=12, right_size=11):
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    f_left = font(SANS_BOLD, left_size)
    draw.text((x0 + 8, y0 + (y1 - y0 - left_size) // 2 - 1), left,
              font=f_left, fill=(255, 255, 255))
    if right:
        f_right = font(SANS, right_size)
        tw = draw.textlength(right, font=f_right)
        draw.text((x1 - 8 - tw, y0 + (y1 - y0 - right_size) // 2 - 1), right,
                  font=f_right, fill=(200, 210, 225))


# ------------------------------------------------------------------- scenes
def draw_skyline(draw, x0, y0, x1, y1):
    """Night skyline of Shenzhen with three flags above the towers."""
    draw.rectangle([x0, y0, x1, y1], fill=(26, 42, 74))
    for i in range(22):
        sx = x0 + 10 + (i * 41) % (x1 - x0 - 18)
        sy = y0 + 6 + (i * 19) % 26
        r = 1 if i % 3 else 2
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 240, 180))
    base = y1
    heights = [46, 72, 58, 88, 66, 98, 78, 56, 92, 70, 82, 50, 74, 64]
    bw = (x1 - x0) // len(heights)
    for i, hgt in enumerate(heights):
        bx0 = x0 + i * bw + 2
        bx1 = x0 + (i + 1) * bw - 2
        top = base - hgt
        draw.rectangle([bx0, top, bx1, base], fill=(10, 16, 32))
        if i % 4 == 1:  # antenna
            midx = (bx0 + bx1) // 2
            draw.line([midx, top - 10, midx, top], fill=(10, 16, 32), width=2)
            draw.ellipse([midx - 2, top - 13, midx + 2, top - 9], fill=RED)
        for row in range(3, hgt - 5, 10):
            for col in range(3, bw - 6, 8):
                if (row // 10 + col // 8 + i) % 3 == 0:
                    wx, wy = bx0 + col, top + row
                    draw.rectangle([wx, wy, wx + 3, wy + 4],
                                   fill=(255, 214, 110))
    draw.rectangle([x0, base - 3, x1, base], fill=GOLD)
    # three flags on poles, left to right: US, China, Russia
    flag_y = y0 + 8
    flag_w, flag_h = 44, 28
    for fx_off, kind in [(12, "us"), (106, "cn"), (200, "ru")]:
        fx = x0 + fx_off
        pole_x = fx + flag_w // 2
        draw.line([pole_x, flag_y - 4, pole_x, flag_y + flag_h + 22],
                  fill=(200, 200, 200), width=2)
        if kind == "us":
            for s in range(7):
                draw.rectangle([fx, flag_y + s * 4, fx + flag_w,
                                flag_y + s * 4 + 4],
                               fill=RED if s % 2 == 0 else (255, 255, 255))
            draw.rectangle([fx, flag_y, fx + 19, flag_y + 13],
                           fill=(30, 50, 110))
            for r in range(2):
                for c in range(4):
                    draw.ellipse([fx + 3 + c * 4, flag_y + 3 + r * 5,
                                  fx + 5 + c * 4, flag_y + 5 + r * 5],
                                 fill=(255, 255, 255))
        elif kind == "cn":
            draw.rectangle([fx, flag_y, fx + flag_w, flag_y + flag_h],
                           fill=(222, 41, 16))
            draw.ellipse([fx + 6, flag_y + 6, fx + 17, flag_y + 17],
                         fill=(255, 222, 0))
            for sx, sy in [(24, 6), (31, 10), (31, 17), (24, 21)]:
                draw.ellipse([fx + sx, flag_y + sy, fx + sx + 3,
                              flag_y + sy + 3], fill=(255, 222, 0))
        else:
            cols = [(255, 255, 255), (0, 90, 180), (210, 30, 30)]
            for s, col in enumerate(cols):
                hh = 10 if s == 2 else 9
                draw.rectangle([fx, flag_y + s * 9, fx + flag_w,
                                flag_y + s * 9 + hh], fill=col)
        draw.rectangle([fx, flag_y, fx + flag_w, flag_y + flag_h],
                       outline=(0, 0, 0), width=1)


def draw_vice_city(draw, x0, y0, x1, y1):
    """Sunset over Vice City: orange sky, sun, palms, neon sign."""
    for i in range(y1 - y0):
        t = i / max(1, (y1 - y0 - 1))
        r = int(255 - 60 * t)
        g = int(140 - 40 * t)
        b = int(90 + 90 * t)
        draw.line([x0, y0 + i, x1, y0 + i], fill=(r, g, b))
    cx, cy = (x0 + x1) // 2 + 34, y0 + 22
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(255, 244, 190))
    draw.rectangle([x0, y1 - 10, x1, y1], fill=(30, 30, 90))
    for px, lean in [(x0 + 26, -1), (x1 - 30, 1)]:
        top_x, top_y = px + lean * 6, y0 + 16
        draw.line([px, y1 - 10, top_x, top_y], fill=(20, 10, 30), width=4)
        for dx, dy in [(-20, 3), (-16, 11), (-8, 15), (8, 15), (16, 11),
                       (20, 3)]:
            draw.line([top_x, top_y, top_x + dx, top_y + dy],
                      fill=(20, 10, 30), width=3)
    fnt = font(SANS_BOLD, 20)
    txt = "VICE CITY"
    tw = draw.textlength(txt, font=fnt)
    tx = (x0 + x1 - tw) // 2
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        draw.text((tx + dx, y0 + 32 + dy), txt, font=fnt,
                  fill=(255, 255, 255))
    draw.text((tx, y0 + 32), txt, font=fnt, fill=(255, 60, 160))


def draw_courthouse(draw, x0, y0, x1, y1):
    """The Peace Palace in The Hague: columns under a dark roof."""
    draw.rectangle([x0, y0, x1, y1], fill=LIGHT_BLUE)
    midx = (x0 + x1) // 2
    draw.polygon([(x0 + 6, y0 + 24), (midx, y0 + 4), (x1 - 6, y0 + 24)],
                 fill=NAVY)
    draw.ellipse([midx - 6, y0 + 12, midx + 6, y0 + 24], fill=GOLD)
    draw.rectangle([x0 + 10, y0 + 24, x1 - 10, y0 + 29], fill=(255, 255, 255))
    for i in range(4):
        cx = x0 + 24 + i * ((x1 - x0 - 48) // 3)
        draw.rectangle([cx - 4, y0 + 29, cx + 4, y1 - 7],
                       fill=(255, 255, 255))
    draw.rectangle([x0 + 10, y1 - 7, x1 - 10, y1 - 2], fill=(255, 255, 255))


def draw_cyclone(draw, x0, y0, x1, y1):
    """Cyclone Akvan: spiral over a dark Bay of Bengal, coast below."""
    draw.rectangle([x0, y0, x1, y1], fill=(18, 38, 74))
    cx, cy = (x0 + x1) // 2 + 12, (y0 + y1) // 2 - 3
    for ring in range(3):
        r = 7 + ring * 7
        draw.arc([cx - r, cy - r, cx + r, cy + r],
                 start=40 + ring * 55, end=300 + ring * 55,
                 fill=(255, 255, 255), width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for i in range(8):
        rx = x0 + 6 + (i * 13) % (x1 - x0 - 12)
        ry = y0 + 4 + (i * 11) % (y1 - y0 - 20)
        draw.line([rx, ry, rx - 3, ry + 7], fill=(140, 180, 220), width=2)
    draw.rectangle([x0, y1 - 8, x1, y1], fill=(30, 110, 70))


def draw_bridge(draw, x0, y0, x1, y1):
    """The Kerch Bridge: deck on pylons over water, smoke from one span."""
    draw.rectangle([x0, y0, x1, y1], fill=(168, 198, 224))
    # water
    draw.rectangle([x0, y1 - 16, x1, y1], fill=(42, 92, 142))
    for i in range(6):
        wx = x0 + 8 + i * 17
        draw.line([wx, y1 - 8, wx + 8, y1 - 8], fill=(190, 220, 245), width=1)
    deck_y = y0 + 30
    tower_top = y0 + 8
    midx = (x0 + x1) // 2
    # cables from the centre tower
    for ex in (x0 + 6, x0 + 32, x1 - 32, x1 - 6):
        draw.line([midx, tower_top, ex, deck_y], fill=(52, 58, 66), width=1)
    # pylons
    for px, top in [(x0 + 16, y0 + 20), (midx, tower_top), (x1 - 16, y0 + 20)]:
        draw.rectangle([px - 2, top, px + 2, y1 - 16], fill=(52, 58, 66))
    # deck
    draw.rectangle([x0, deck_y, x1, deck_y + 4], fill=(52, 58, 66))
    # strike glow + smoke plume on the right span
    draw.ellipse([x1 - 38, deck_y - 5, x1 - 24, deck_y + 2], fill=(232, 120, 50))
    draw.ellipse([x1 - 36, y0 + 13, x1 - 20, y0 + 22], fill=(128, 132, 140))
    draw.ellipse([x1 - 30, y0 + 2, x1 - 10, y0 + 14], fill=(168, 173, 181))


def draw_chart(draw, x0, y0, x1, y1):
    """A record market debut: rising chart line over a night skyline."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_DARK)
    for gx in range(x0 + 18, x1, 18):
        draw.line([gx, y0, gx, y1], fill=(52, 72, 102), width=1)
    for gy in range(y0 + 15, y1, 15):
        draw.line([x0, gy, x1, gy], fill=(52, 72, 102), width=1)
    heights = [10, 16, 12, 20, 14, 18, 11]
    bw = (x1 - x0) // len(heights)
    for i, hgt in enumerate(heights):
        draw.rectangle([x0 + i * bw + 1, y1 - hgt, x0 + (i + 1) * bw - 1, y1],
                       fill=(5, 8, 16))
    pts = [(4, 40), (20, 34), (36, 37), (52, 25), (68, 28), (84, 14),
           (100, 6)]
    abs_pts = [(x0 + px, y0 + py) for px, py in pts]
    draw.line(abs_pts, fill=GOLD, width=3, joint="curve")
    for px, py in abs_pts:
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    lx, ly = abs_pts[-1]
    draw.polygon([(lx + 8, ly - 1), (lx - 1, ly - 6), (lx + 1, ly + 5)],
                 fill=GOLD)


# ---------------------------------------------------------------- world map
# Coarse land shapes as longitude/latitude boxes (union), tapered in
# smaller pieces so the dotted map reads as continents, not rectangles.
LAND_BOXES = [
    # North America
    (-168, -135, 58, 71), (-135, -95, 50, 70), (-95, -55, 45, 62),
    (-125, -100, 30, 49), (-100, -67, 30, 45), (-117, -86, 15, 32),
    (-92, -77, 8, 18), (-58, -20, 60, 84),
    # South America
    (-79, -35, -5, 11), (-75, -38, -35, -5), (-73, -53, -56, -35),
    # Europe
    (-10, 30, 36, 45), (-10, 25, 45, 60), (5, 30, 58, 71),
    (-5, 2, 50, 59),
    # Africa
    (-17, 35, 15, 32), (-10, 42, -5, 15), (12, 35, -35, -5),
    (43, 51, -26, -12),
    # Asia
    (40, 180, 55, 75), (40, 140, 35, 55), (75, 135, 20, 40),
    (68, 89, 8, 32), (97, 110, 5, 28), (95, 141, -11, 6),
    (129, 146, 31, 46), (35, 60, 12, 32),
    # Oceania
    (113, 154, -39, -11), (166, 179, -47, -34),
]

# Story number -> (longitude, latitude) for the map pins.
PINS = {
    1: (114.0, 22.5),    # Shenzhen
    2: (-80.2, 25.8),    # Vice City (Florida)
    3: (4.3, 52.1),      # The Hague
    4: (86.5, 20.2),     # Odisha coast
    5: (35.5, 45.0),     # Crimea (Kerch Bridge)
    6: (-74.0, 40.7),    # New York
    7: (51.5, 26.5),     # The Gulf
    8: (-77.0, 38.9),    # Washington
    9: (35.2, 31.8),     # Jerusalem
    10: (125.8, 39.8),   # Yongbyon, North Korea
    11: (34.3, 31.4),    # Gaza
    12: (4.35, 50.85),   # Brussels
    13: (4.35, 50.85),   # Brussels
    14: (-77.0, 38.9),   # Washington
    15: (-75.7, 45.4),   # Ottawa
    16: (2.35, 48.85),   # Paris
    17: (139.7, 35.7),   # Tokyo
    18: (-77.0, 38.9),   # Washington
    19: (22.0, 32.5),    # Eastern Libya
    20: (45.3, 2.0),     # Mogadishu
    21: (30.7, 36.9),    # Antalya
    22: (145.0, -37.8),  # Australia
}

# Pixel nudges so pins sharing a city (Washington x3, Brussels x2) or a
# crowded corner (Europe, the Levant, the US north-east) do not cover
# each other. The numbers stay next to their true locations.
PIN_OFFSETS = {
    2: (-14, 13), 3: (-6, -12), 5: (-10, -9), 6: (13, -5), 7: (0, 2),
    8: (-15, 3), 9: (-14, -2), 11: (10, 9), 12: (-16, 1), 13: (16, 3),
    14: (14, 10), 15: (-16, -11), 16: (-12, 15), 17: (2, 0),
    18: (-1, 15), 19: (-4, 4), 21: (16, -4),
}

VOYAGER_POS = (-25.0, -2.0)  # deep space marker, South Atlantic ocean


def is_land(lon, lat):
    for lo0, lo1, la0, la1 in LAND_BOXES:
        if lo0 <= lon <= lo1 and la0 <= lat <= la1:
            return True
    return False


def lonlat_to_px(x0, y0, x1, y1, lon, lat):
    px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    py = y0 + (90.0 - lat) / 180.0 * (y1 - y0)
    return px, py


def draw_star(draw, cx, cy, r_out, r_in, fill, outline=None):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=outline)


def draw_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=MAP_BG)
    step = 6
    for gy in range(y0 + 4, y1 - 3, step):
        for gx in range(x0 + 4, x1 - 3, step):
            lon = (gx - x0) / (x1 - x0) * 360.0 - 180.0
            lat = 90.0 - (gy - y0) / (y1 - y0) * 180.0
            if is_land(lon, lat):
                draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=NAVY)
    # Voyager 1 star in the South Atlantic (deep space, off any coast)
    vx, vy = lonlat_to_px(x0, y0, x1, y1, *VOYAGER_POS)
    draw_star(draw, vx, vy, 8, 3.2, GOLD, outline=NAVY)
    # corner labels, over quiet ocean
    f_t = font(SANS_BOLD, 11)
    label = "THE DAY ON THE MAP"
    tw = draw.textlength(label, font=f_t)
    draw.rectangle([x0 + 4, y0 + 3, x0 + 10 + tw, y0 + 19], fill=MAP_BG)
    draw.text((x0 + 7, y0 + 5), label, font=f_t, fill=NAVY)
    f_r = font(SANS, 10)
    right = "NUMBERED PINS: ALL 22 STORIES"
    rw = draw.textlength(right, font=f_r)
    draw.rectangle([x1 - 10 - rw, y0 + 3, x1 - 4, y0 + 19], fill=MAP_BG)
    draw.text((x1 - 7 - rw, y0 + 5), right, font=f_r, fill=NAVY)
    # pins on top, in number order so overlaps resolve predictably
    fnt = font(SANS_BOLD, 9)
    for num in sorted(PINS):
        lon, lat = PINS[num]
        px, py = lonlat_to_px(x0, y0, x1, y1, lon, lat)
        dx, dy = PIN_OFFSETS.get(num, (0, 0))
        px, py = px + dx, py + dy
        r = 7
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        label = str(num)
        tw = draw.textlength(label, font=fnt)
        draw.text((px - tw / 2, py - fnt.size / 2 - 1), label, font=fnt,
                  fill=(255, 255, 255))


# ------------------------------------------------------------------- briefs
# (number, dateline, headline, one-line body) — stories 7..22.
BRIEFS = [
    (7, "GULF", "Iran attacks Gulf states",
     "Tehran strikes back after US attacks on Qeshm island."),
    (8, "WASHINGTON", "Jeffries set to be first Black House Speaker",
     "Democrats nominate Hakeem Jeffries after their midterm wave."),
    (9, "JERUSALEM", "Herzog asks Eisenkot to form a government",
     "Israel\u2019s president bypasses Netanyahu and taps the former army chief."),
    (10, "YONGYON, NORTH KOREA",
     "North Korea expanded uranium enrichment, IAEA says",
     "Inspectors report growth at the Yongbyon complex."),
    (11, "GAZA", "Israel launches ground operation in central Gaza",
     "Troops move beyond the Yellow Line; four allies demand aid reach "
     "flooded Gaza."),
    (12, "BRUSSELS", "EU proposes \u20ac45bn Ukraine loan",
     "The loan would be repaid only after Russia pays reparations."),
    (13, "BRUSSELS", "EU greenlights Indonesia trade pact",
     "Governments back the deal as a counterweight to US tariffs."),
    (14, "WASHINGTON", "US details $12bn in Venezuelan oil revenue",
     "A State Department report traces oil and mineral money a year after "
     "Maduro\u2019s capture."),
    (15, "OTTAWA", "Carney strikes a tariff deal with Xi",
     "Ottawa resets China ties while it seeks the right deal with Washington."),
    (16, "PARIS", "M\u00e9lenchon \u2018could win\u2019, minister says",
     "France\u2019s justice minister concedes the hard-left leader could take "
     "the top job amid a fourth weekend of cost-of-living protests."),
    (17, "TOKYO", "India and Japan review defence ties",
     "Ministers meet to deepen security cooperation between the two powers."),
    (18, "WASHINGTON", "US proposes tougher green-card rules",
     "Employment-based green cards face longer hiring processes under the plan."),
    (19, "EASTERN LIBYA", "Cocaine and millions of pills seized",
     "Officials announce a major drugs haul in the east of the country."),
    (20, "MOGADISHU", "Somalia accuses UAE of secret bases",
     "Mogadishu says the Emirates built military bases without federal approval."),
    (21, "ANTALYA", "COP31 climate talks grind on",
     "Negotiators press toward Friday\u2019s close as a draft deal draws fire."),
    (22, "SPORT", "Duckett\u2019s 133 seals the series for England",
     "His century in Australia clinches the ODI series 2\u20131; in Wellington, "
     "India and New Zealand open their Test series."),
]

BRIEF_LEADING = 13


def brief_segments(num, dateline, headline, body):
    f_bold = font(SANS_BOLD, 11)
    f_reg = font(SANS, 10)
    return [(f"{dateline} \u2014 {headline}.", f_bold, INK),
            (body, f_reg, GREY)]


def draw_brief(draw, x, y, w, num, dateline, headline, body):
    """Draw one brief; returns its height in pixels."""
    r = 10
    cx, cy = x + r, y + r
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f_num = font(SANS_BOLD, 10)
    label = str(num)
    tw = draw.textlength(label, font=f_num)
    draw.text((cx - tw / 2, cy - 6), label, font=f_num, fill=(255, 255, 255))
    lines = layout_flow(draw, brief_segments(num, dateline, headline, body),
                        w - 26)
    draw_flow(draw, x + 26, y, lines, BRIEF_LEADING)
    return len(lines) * BRIEF_LEADING


# -------------------------------------------------------------------- render
def side_panel(draw, x0, y0, x1, y1, strip, art, headline, deck):
    """A featured panel: navy strip, small scene left, headline+deck right."""
    panel(draw, x0, y0, x1, y1)
    header_strip(draw, x0 + 2, y0 + 2, x1 - 2, y0 + 22, strip)
    art(draw, x0 + 8, y0 + 28, x0 + 118, y1 - 6)
    tx = x0 + 126
    tw = x1 - tx - 10
    f_ph = font(SANS_BOLD, 15)
    y = text_block(draw, tx, y0 + 27, headline, f_ph, INK, tw, leading=17)
    f_pd = font(SANS, 11)
    text_block(draw, tx, y + 3, deck, f_pd, GREY, tw, leading=13)


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=NAVY, width=3)

    # ---- masthead: y 14..103
    d.rectangle([14, 14, 1010, 98], fill=NAVY)
    f_title = font(SERIF, 44)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 18), title, font=f_title, fill=(255, 255, 255))
    f_date = font(SANS_BOLD, 18)
    d.text((26, 68), "THURSDAY, 19 NOVEMBER 2026", font=f_date,
           fill=(255, 110, 110))
    f_strap = font(SANS_BOLD, 13)
    strap = "ONE DAY  \u00b7  22 STORIES  \u00b7  EVERY REGION"
    sw = d.textlength(strap, font=f_strap)
    d.text((1010 - 12 - sw, 70), strap, font=f_strap, fill=(255, 255, 255))
    d.rectangle([14, 100, 1010, 103], fill=RED)

    # ---- hero, story 1: y 106..246
    panel(d, 20, 106, 1004, 246)
    draw_skyline(d, 26, 112, 340, 240)
    tx = 356
    f_kick = font(SANS_BOLD, 13)
    d.text((tx, 114), "1  \u00b7  SHENZHEN  \u00b7  APEC SUMMIT  \u00b7  FIRST-EVER TRILATERAL",
           font=f_kick, fill=RED)
    f_head = font(SERIF, 28)
    y = text_block(d, tx, 138, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                   f_head, INK, 1004 - tx - 12, leading=33)
    f_deck = font(SANS, 14)
    text_block(d, tx, y + 4,
               "The US, Chinese and Russian presidents hold their first-ever "
               "trilateral summit at APEC \u2014 Ukraine, Iran and nuclear arms "
               "on the table.",
               f_deck, GREY, 1004 - tx - 12, leading=18)

    # ---- story 2, full width: y 254..354
    panel(d, 20, 254, 1004, 354)
    draw_vice_city(d, 26, 260, 306, 348)
    tx = 322
    d.text((tx, 262), "2  \u00b7  VICE CITY  \u00b7  WORLDWIDE", font=f_kick, fill=RED)
    f_head2 = font(SERIF, 24)
    y = text_block(d, tx, 284, "GTA VI LAUNCHES WORLDWIDE",
                   f_head2, INK, 1004 - tx - 12, leading=28)
    f_deck2 = font(SANS, 12)
    text_block(d, tx, y + 4,
               "Rockstar\u2019s Vice City epic lands after 13 years: early "
               "reviews average 99/100, 2.3 million watched live on Twitch, "
               "and 1,600 developers in Bengaluru helped build it.",
               f_deck2, GREY, 1004 - tx - 12, leading=16)

    # ---- stories 3+4: y 362..458
    side_panel(d, 20, 362, 492, 458, "3  \u00b7  THE HAGUE", draw_courthouse,
               "WORLD COURT RULES ON ROHINGYA CASE",
               "The UN\u2019s top court delivers its judgment in The Gambia\u2019s "
               "genocide case against Myanmar.")
    side_panel(d, 512, 362, 1004, 458, "4  \u00b7  ODISHA, INDIA", draw_cyclone,
               "CYCLONE AKVAN NEARS INDIA\u2019S COAST",
               "Red alerts across Odisha and Andhra Pradesh, schools closed; "
               "landfall due Friday.")

    # ---- stories 5+6: y 470..566
    side_panel(d, 20, 470, 492, 566, "5  \u00b7  CRIMEA", draw_bridge,
               "UKRAINE STRIKES CRIMEAN BRIDGE \u2014 THIRD TIME THIS WEEK",
               "Kyiv hits the Kerch bridge again as the Shenzhen talks put "
               "the war centre stage.")
    side_panel(d, 512, 470, 1004, 566, "6  \u00b7  NEW YORK", draw_chart,
               "ANTHROPIC\u2019S RECORD STOCK-MARKET DEBUT",
               "The AI lab\u2019s first day of trading sets a record, capping a "
               "landmark day for AI money.")

    # ---- map: y 574..686
    panel(d, 20, 574, 1004, 686)
    draw_map(d, 26, 580, 998, 666)
    f_cap = font(SANS_BOLD, 10)
    d.text((30, 670),
           "\u2605 VOYAGER 1: NASA\u2019s 1977 probe reaches one light-day from "
           "Earth \u2014 a first for a human-made object",
           font=f_cap, fill=NAVY)

    # ---- briefs: y 694..994
    panel(d, 20, 694, 1004, 994)
    header_strip(d, 22, 696, 1002, 720, "AROUND THE WORLD IN BRIEF",
                 "STORIES 7\u201322", left_size=13, right_size=11)
    col_w = 234
    row_y = 730
    for row_start in range(0, len(BRIEFS), 4):
        row = BRIEFS[row_start:row_start + 4]
        row_h = 0
        for col, (num, dateline, headline, body) in enumerate(row):
            bx = 28 + col * (col_w + 10)
            h = draw_brief(d, bx, row_y, col_w, num, dateline, headline, body)
            row_h = max(row_h, h)
        row_y += row_h + 7

    # ---- footer
    f_foot = font(SANS, 11)
    foot = ("All 22 stories from reporting first published on 19 November 2026"
            "  \u00b7  Drawn entirely by code \u2014 no photographs")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 998), foot, font=f_foot, fill=GREY)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render().save(out, "PNG")
    print("wrote", out)
