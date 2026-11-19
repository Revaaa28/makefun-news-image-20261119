"""Draw the 19 November 2026 world-news poster (1024x1024, PIL only).

A newspaper front page: masthead naming the day, a hero story (the
first-ever Trump-Xi-Putin trilateral in Shenzhen), three picture panels
(GTA VI launch, ICJ Rohingya verdict, Cyclone Akvan), a dotted world map
with numbered pins for all 13 stories, and nine short briefs.

Deterministic: no randomness, no clock, no network. Running this module
twice produces byte-identical PNGs.
"""

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

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_REG = "DejaVuSerif.ttf"
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


def panel(draw, x0, y0, x1, y1, fill=PAPER, outline=NAVY, width=2):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)


def header_strip(draw, x0, y0, x1, y1, left, right=None):
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    f_left = font(SANS_BOLD, 15)
    draw.text((x0 + 10, y0 + 5), left, font=f_left, fill=(255, 255, 255))
    if right:
        f_right = font(SANS, 13)
        tw = draw.textlength(right, font=f_right)
        draw.text((x1 - 10 - tw, y0 + 6), right, font=f_right,
                  fill=(200, 210, 225))


# ---------------------------------------------------------------- skyline
def draw_skyline(draw, x0, y0, x1, y1):
    """Night skyline of Shenzhen with three flags above the towers."""
    draw.rectangle([x0, y0, x1, y1], fill=(26, 42, 74))
    # stars
    for i in range(26):
        sx = x0 + 12 + (i * 37) % (x1 - x0 - 20)
        sy = y0 + 8 + (i * 23) % 34
        r = 1 if i % 3 else 2
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 240, 180))
    base = y1
    # towers, heights from a fixed pattern (no randomness)
    heights = [62, 96, 78, 118, 88, 130, 104, 74, 122, 92, 108, 66, 98, 84]
    bw = (x1 - x0) // len(heights)
    for i, hgt in enumerate(heights):
        bx0 = x0 + i * bw + 2
        bx1 = x0 + (i + 1) * bw - 2
        top = base - hgt
        draw.rectangle([bx0, top, bx1, base], fill=(10, 16, 32))
        if i % 4 == 1:  # antenna
            draw.line([ (bx0 + bx1) // 2, top - 14, (bx0 + bx1) // 2, top],
                      fill=(10, 16, 32), width=2)
            draw.ellipse([(bx0 + bx1) // 2 - 2, top - 17,
                          (bx0 + bx1) // 2 + 2, top - 13], fill=RED)
        # lit windows in a fixed checker pattern
        for row in range(3, hgt - 6, 12):
            for col in range(4, bw - 8, 10):
                if (row // 12 + col // 10 + i) % 3 == 0:
                    wx = bx0 + col
                    wy = top + row
                    draw.rectangle([wx, wy, wx + 4, wy + 5],
                                   fill=(255, 214, 110))
    # ground glow
    draw.rectangle([x0, base - 4, x1, base], fill=GOLD)
    # three flags on poles, left to right: US, China, Russia
    flag_y = y0 + 14
    flag_w, flag_h = 52, 32
    xs = [x0 + 16, x0 + 118, x0 + 220]
    for fx, kind in zip(xs, ("us", "cn", "ru")):
        draw.line([fx + flag_w // 2, flag_y - 6, fx + flag_w // 2,
                   flag_y + flag_h + 30], fill=(200, 200, 200), width=2)
        if kind == "us":
            for s in range(7):
                draw.rectangle([fx, flag_y + s * 5, fx + flag_w,
                                flag_y + s * 5 + 5],
                               fill=RED if s % 2 == 0 else (255, 255, 255))
            draw.rectangle([fx, flag_y, fx + 22, flag_y + 16], fill=(30, 50, 110))
            for r in range(3):
                for c in range(4):
                    draw.ellipse([fx + 3 + c * 5, flag_y + 3 + r * 5,
                                  fx + 5 + c * 5, flag_y + 5 + r * 5],
                                 fill=(255, 255, 255))
        elif kind == "cn":
            draw.rectangle([fx, flag_y, fx + flag_w, flag_y + flag_h],
                           fill=(222, 41, 16))
            draw.ellipse([fx + 8, flag_y + 7, fx + 20, flag_y + 19],
                         fill=(255, 222, 0))
            for sx, sy in [(28, 8), (36, 12), (36, 20), (28, 24)]:
                draw.ellipse([fx + sx, flag_y + sy, fx + sx + 4, flag_y + sy + 4],
                             fill=(255, 222, 0))
        else:
            for s, col in enumerate([(255, 255, 255), (0, 90, 180), (210, 30, 30)]):
                draw.rectangle([fx, flag_y + s * 11, fx + flag_w,
                                flag_y + s * 11 + 11], fill=col)
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
    # sun
    cx, cy = (x0 + x1) // 2 + 40, y0 + 30
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(255, 244, 190))
    # sea strip
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(30, 30, 90))
    # palms: leaning trunk, fronds fanning down from the crown
    for px, lean in [(x0 + 34, -1), (x1 - 38, 1)]:
        top_x, top_y = px + lean * 8, y0 + 24
        draw.line([px, y1 - 12, top_x, top_y], fill=(20, 10, 30), width=4)
        for k, (dx, dy) in enumerate([(-22, 4), (-18, 13), (-9, 17),
                                      (9, 17), (18, 13), (22, 4)]):
            draw.line([top_x, top_y, top_x + dx, top_y + dy],
                      fill=(20, 10, 30), width=3)
    fnt = font(SANS_BOLD, 26)
    txt = "VICE CITY"
    tw = draw.textlength(txt, font=fnt)
    tx = (x0 + x1 - tw) // 2
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        draw.text((tx + dx, y0 + 40 + dy), txt, font=fnt, fill=(255, 255, 255))
    draw.text((tx, y0 + 40), txt, font=fnt, fill=(255, 60, 160))


def draw_courthouse(draw, x0, y0, x1, y1):
    """The Peace Palace in The Hague: columns under a dark roof."""
    draw.rectangle([x0, y0, x1, y1], fill=LIGHT_BLUE)
    midx = (x0 + x1) // 2
    # roof
    draw.polygon([(x0 + 8, y0 + 42), (midx, y0 + 10), (x1 - 8, y0 + 42)],
                 fill=NAVY)
    draw.ellipse([midx - 9, y0 + 20, midx + 9, y0 + 38], fill=GOLD)
    # entablature + columns
    draw.rectangle([x0 + 14, y0 + 42, x1 - 14, y0 + 50], fill=(255, 255, 255))
    for i in range(5):
        cx = x0 + 34 + i * ((x1 - x0 - 68) // 4)
        draw.rectangle([cx - 6, y0 + 50, cx + 6, y1 - 10], fill=(255, 255, 255))
    draw.rectangle([x0 + 14, y1 - 10, x1 - 14, y1 - 4], fill=(255, 255, 255))
    # steps
    draw.rectangle([x0 + 30, y1 - 4, x1 - 30, y1], fill=(150, 170, 195))


def draw_cyclone(draw, x0, y0, x1, y1):
    """Cyclone Akvan: spiral over a dark Bay of Bengal, coast below."""
    draw.rectangle([x0, y0, x1, y1], fill=(18, 38, 74))
    cx, cy = (x0 + x1) // 2 + 30, (y0 + y1) // 2 - 2
    # spiral arms
    for ring in range(3):
        r = 9 + ring * 10
        draw.arc([cx - r, cy - r, cx + r, cy + r],
                 start=40 + ring * 55, end=300 + ring * 55,
                 fill=(255, 255, 255), width=4)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    # rain slashes
    for i in range(14):
        rx = x0 + 8 + (i * 23) % (x1 - x0 - 16)
        ry = y0 + 6 + (i * 13) % (y1 - y0 - 26)
        draw.line([rx, ry, rx - 4, ry + 10], fill=(140, 180, 220), width=2)
    # coast strip
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(30, 110, 70))
    draw.text((x0 + 8, y1 - 11), "", font=font(SANS, 10), fill=(255, 255, 255))

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
    2: (-80.2, 25.8),    # Vice City (Miami)
    3: (4.3, 52.1),      # The Hague
    4: (89.0, 16.0),     # Bay of Bengal
    5: (-25.0, 15.0),    # Voyager 1 (deep space, Atlantic marker)
    6: (-75.7, 45.4),    # Ottawa
    7: (2.35, 48.85),    # Paris
    8: (139.7, 35.7),    # Tokyo
    9: (-77.0, 38.9),    # Washington
    10: (22.6, 32.8),    # Derna, Libya
    11: (45.3, 2.0),     # Mogadishu
    12: (30.7, 36.9),    # Antalya
    13: (146.0, -38.0),  # Melbourne
}


# Small pixel nudges so pins that sit close together on a 1024-wide map
# (Ottawa/Washington, The Hague/Paris, Derna/Antalya) do not cover each
# other. The numbers stay next to their true locations.
PIN_OFFSETS = {2: (-16, 8), 3: (0, -13), 6: (-15, -9), 7: (-13, 11),
               9: (13, 9), 10: (-11, 9), 12: (11, -9)}


def is_land(lon, lat):
    for lo0, lo1, la0, la1 in LAND_BOXES:
        if lo0 <= lon <= lo1 and la0 <= lat <= la1:
            return True
    return False


def draw_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 238, 245))
    step = 6
    for gy in range(y0 + 4, y1 - 3, step):
        for gx in range(x0 + 4, x1 - 3, step):
            lon = (gx - x0) / (x1 - x0) * 360.0 - 180.0
            lat = 90.0 - (gy - y0) / (y1 - y0) * 180.0
            if is_land(lon, lat):
                draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=NAVY)
    # pins on top, in number order so overlaps resolve predictably
    fnt = font(SANS_BOLD, 11)
    for num in sorted(PINS):
        lon, lat = PINS[num]
        px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
        py = y0 + (90.0 - lat) / 180.0 * (y1 - y0)
        dx, dy = PIN_OFFSETS.get(num, (0, 0))
        px, py = px + dx, py + dy
        r = 10
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        label = str(num)
        tw = draw.textlength(label, font=fnt)
        th = fnt.size
        draw.text((px - tw / 2, py - th / 2 - 1), label, font=fnt,
                  fill=(255, 255, 255))


BRIEFS = [
    (5, "VOYAGER 1: NASA confirms Voyager 1 one light-day out",
     "The 1977 probe, 16bn miles away, is the first human-made object to reach the mark."),
    (6, "OTTAWA: Carney strikes a tariff deal with Xi",
     "Ottawa resets its China ties as it seeks the right deal with Washington."),
    (7, "PARIS: M\u00e9lenchon \u2018could win\u2019, minister says",
     "France\u2019s justice minister says the hard-left leader could take the top job."),
    (8, "TOKYO: India and Japan review defence ties",
     "Ministers meet in Tokyo to deepen security cooperation between the two powers."),
    (9, "WASHINGTON: US proposes tougher green-card rules",
     "Employment-based green cards face longer hiring processes under the new proposals."),
    (10, "EAST LIBYA: Cocaine and millions of pills seized",
     "A major drugs haul is seized in eastern Libya, officials say."),
    (11, "MOGADISHU: Somalia accuses UAE of secret bases",
     "Mogadishu says the UAE built military bases on its soil without federal approval."),
    (12, "ANTALYA: COP31 climate talks continue",
     "Negotiators press on in Turkey as a draft deal draws fire; the summit closes Friday."),
    (13, "AUSTRALIA: Duckett\u2019s 133 puts England on top",
     "Ben Duckett hits 133 in the third ODI as England seal the series 2\u20131."),
]


def draw_brief(draw, x0, y0, w, num, headline, body):
    r = 13
    cx, cy = x0 + r, y0 + r
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f_num = font(SANS_BOLD, 12)
    label = str(num)
    tw = draw.textlength(label, font=f_num)
    draw.text((cx - tw / 2, cy - 8), label, font=f_num, fill=(255, 255, 255))
    tx = x0 + 2 * r + 8
    f_head = font(SANS_BOLD, 15)
    y = text_block(draw, tx, y0 - 1, headline, f_head, INK, w - 2 * r - 8,
                   leading=18)
    f_body = font(SANS, 12)
    text_block(draw, tx, y + 2, body, f_body, GREY, w - 2 * r - 8, leading=15)


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=NAVY, width=3)

    # ---- masthead: y 16..106
    d.rectangle([14, 14, 1010, 104], fill=NAVY)
    f_title = font(SERIF, 56)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 20), title, font=f_title, fill=(255, 255, 255))
    f_sub = font(SANS_BOLD, 15)
    d.text((26, 80), "ONE DAY  \u00b7  13 STORIES  \u00b7  EVERY REGION",
           font=f_sub, fill=(255, 255, 255))
    f_date = font(SANS_BOLD, 16)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text((1010 - 12 - dw, 79), date, font=f_date, fill=(255, 90, 90))
    d.rectangle([14, 106, 1010, 110], fill=RED)

    # ---- hero: y 118..314
    panel(d, 20, 118, 1004, 314)
    draw_skyline(d, 26, 124, 356, 308)
    tx = 372
    f_kick = font(SANS_BOLD, 15)
    d.text((tx, 130), "1  \u00b7  SHENZHEN  \u00b7  APEC SUMMIT  \u00b7  FIRST-EVER TRILATERAL",
           font=f_kick, fill=RED)
    f_head = font(SERIF, 38)
    y = text_block(d, tx, 156, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                   f_head, INK, 1004 - tx - 16, leading=44)
    f_deck = font(SANS, 17)
    text_block(d, tx, y + 8,
               "The leaders of the US, China and Russia sit down together for "
               "the first time \u2014 with Ukraine, Iran and nuclear arms on the agenda.",
               f_deck, GREY, 1004 - tx - 16, leading=22)

    # ---- three picture panels: y 324..502
    panels = [
        (20, "2  \u00b7  VICE CITY", draw_vice_city,
         "GTA VI LAUNCHES WORLDWIDE",
         "Rockstar\u2019s Vice City epic arrives after 13 years."),
        (352, "3  \u00b7  THE HAGUE", draw_courthouse,
         "WORLD COURT RULES ON ROHINGYA CASE",
         "The Hague delivers its verdict in The Gambia\u2019s case against Myanmar."),
        (684, "4  \u00b7  BAY OF BENGAL", draw_cyclone,
         "CYCLONE AKVAN NEARS INDIA\u2019S COAST",
         "Red alerts in Odisha and Andhra Pradesh; landfall due Friday."),
    ]
    for x0, strip, art, headline, deck in panels:
        x1 = x0 + 320
        panel(d, x0, 324, x1, 508)
        header_strip(d, x0 + 2, 326, x1 - 2, 352, strip)
        art(d, x0 + 8, 358, x1 - 8, 428)
        f_ph = font(SANS_BOLD, 18)
        y = text_block(d, x0 + 10, 434, headline, f_ph, INK, 300, leading=20)
        f_pd = font(SANS, 12)
        text_block(d, x0 + 10, y + 3, deck, f_pd, GREY, 300, leading=14)

    # ---- map: y 518..684
    panel(d, 20, 518, 1004, 684)
    header_strip(d, 22, 520, 1002, 548, "THE DAY ON THE MAP",
                 "numbered pins: all 13 stories")
    draw_map(d, 26, 554, 998, 678)

    # ---- briefs: y 694..986
    panel(d, 20, 694, 1004, 986)
    header_strip(d, 22, 696, 1002, 724, "AROUND THE WORLD IN BRIEF",
                 "9 more stories from the day")
    col_w = 320
    row_h = 86
    for i, (num, headline, body) in enumerate(BRIEFS):
        col, row = i % 3, i // 3
        bx = 30 + col * (col_w + 4)
        by = 736 + row * row_h
        draw_brief(d, bx, by, col_w, num, headline, body)

    # ---- footer
    f_foot = font(SANS, 11)
    foot = ("All 13 stories from reporting first published on 19 November 2026"
            "  \u00b7  Drawn entirely by code \u2014 no photographs")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 994), foot, font=f_foot, fill=GREY)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render().save(out, "PNG")
    print("wrote", out)
