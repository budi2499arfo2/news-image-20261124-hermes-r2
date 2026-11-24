#!/usr/bin/env python3
"""Render the one-page broadsheet for Tuesday, 24 November 2026.

Run: python3 draw.py  -> writes entry.png next to this file.
All news copy lives here, in this file only.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 34
INK = (18, 18, 18)
PAPER = (252, 250, 244)
GREY = (90, 90, 88)
RULE = (30, 30, 30)
ACCENT = (158, 28, 20)  # deep newspaper red, used sparingly

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def fit_font(path, size, text, max_w):
    """Shrink until the text fits max_w; never below size // 2."""
    f = font(path, size)
    while size > 10 and f.getlength(text) > max_w:
        size -= 1
        f = font(path, size)
    return f


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, text, f, leading, color=INK):
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def centered(draw, y, text, f, color=INK):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=color)
    return y + f.size


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    y = 16

    # ---- top strip ----
    f_small = font(SANS, 15)
    f_small_b = font(SANS_B, 15)
    d.text((x0, y), "No. 328", font=f_small, fill=GREY)
    tag = "THE DAY'S WORLD NEWS  •  ONE PAGE"
    w = d.textlength(tag, font=f_small_b)
    d.text(((W - w) / 2, y), tag, font=f_small_b, fill=GREY)
    price = "Price $2.00"
    w = d.textlength(price, font=f_small)
    d.text((x1 - w, y), price, font=f_small, fill=GREY)
    y += 22
    rule(d, x0, y, x1, 3)
    y += 10

    # ---- masthead ----
    f_mast = fit_font(SERIF_B, 78, "THE WORLD TODAY", x1 - x0)
    y = centered(d, y, "THE WORLD TODAY", f_mast) + 2
    rule(d, x0, y, x1, 2)
    y += 7
    f_date = font(SERIF_B, 25)
    y = centered(d, y, "Tuesday, November 24, 2026", f_date)
    y += 4
    rule(d, x0, y, x1, 4)
    y += 10

    # ---- lead story: climate / COP31 ----
    f_kick = font(SANS_B, 17)
    d.text((x0, y), "CLIMATE  •  ANTALYA, TURKEY", font=f_kick, fill=ACCENT)
    y += 26
    f_head = fit_font(SERIF_B, 46, "COP31 COLLAPSES WITHOUT A DEAL", x1 - x0)
    d.text((x0, y), "COP31 COLLAPSES WITHOUT A DEAL", font=f_head, fill=INK)
    y += f_head.size + 8
    f_deck = font(SERIF, 22)
    y = para(d, x0, y, x1 - x0,
             "After two weeks of talks, 194 nations leave the Antalya summit "
             "with no agreement as the words \u201cfossil fuels\u201d are stripped "
             "from the final text \u2014 the first climate summit to end "
             "empty-handed since Copenhagen in 2009.",
             f_deck, 29)
    y += 6
    # fact strip under the lead
    rule(d, x0, y, x1, 1, GREY)
    y += 8
    f_fact = font(SANS_B, 15)
    facts = ("LONGEST COP EVER  •  90 NATIONS BACK ELECTRIFICATION PLEDGE: "
             "22% \u2192 35% BY 2035  •  COP32: ADDIS ABABA")
    y = para(d, x0, y, x1 - x0, facts, f_fact, 21, color=GREY)
    y += 4
    rule(d, x0, y, x1, 1, GREY)
    y += 10

    # ---- two-column middle: security + business ----
    col_w = (x1 - x0 - 28) // 2
    cx = x0 + col_w + 28
    top_mid = y

    # left column: security — NATO Black Sea patrols
    ly = top_mid
    d.text((x0, ly), "SECURITY  •  BLACK SEA", font=f_kick, fill=ACCENT)
    ly += 25
    f_h2 = fit_font(SERIF_B, 28, "NATO Steps Up Black Sea Patrols", col_w)
    ly = para(d, x0, ly, col_w,
              "NATO Steps Up Black Sea Patrols",
              f_h2, 33)
    ly += 4
    f_body = font(SERIF, 18)
    ly = para(d, x0, ly, col_w,
              "NATO begins a six-month maritime patrol in the Black Sea "
              "with 12 warships from seven allies, its largest deployment "
              "there since 2022, to shield grain shipping lanes.",
              f_body, 24)
    ly += 8
    ly = para(d, x0, ly, col_w,
              "Britain and France pledge 300 more air-defence missiles for "
              "Ukraine as Russian drone attacks on Odesa\u2019s ports rise "
              "for a third straight week.",
              f_body, 24)

    # right column: business — gold record, Fed rate outlook
    ry = top_mid
    d.text((cx, ry), "BUSINESS  •  MARKETS", font=f_kick, fill=ACCENT)
    ry += 25
    f_h2b = fit_font(SERIF_B, 28, "Gold Hits Record as Fed Signals Cuts", col_w)
    ry = para(d, cx, ry, col_w,
              "Gold Hits Record as Fed Signals Cuts",
              f_h2b, 33)
    ry += 4
    ry = para(d, cx, ry, col_w,
              "Gold tops $4,100 an ounce for the first time as traders bet "
              "the U.S. Federal Reserve will cut rates in December, while "
              "the S&P 500 rises 0.8% to a fresh record close.",
              f_body, 24)
    ry += 8
    ry = para(d, cx, ry, col_w,
              "Brent crude holds near $62 a barrel as OPEC+ weighs "
              "extending output cuts into 2027.",
              f_body, 24)

    y = max(ly, ry) + 12
    rule(d, x0, y, x1, 2)
    y += 10

    # ---- in brief ----
    d.text((x0, y), "IN BRIEF", font=f_kick, fill=ACCENT)
    y += 24
    f_brief = font(SERIF, 17)
    briefs = [
        "QATAR \u2014 The Qatari prime minister meets U.S. officials in "
        "Washington to revive stalled talks with Iran.",
        "UKRAINE \u2014 Zelensky urges four-way peace talks with Russia, "
        "Europe and the U.S. \u201cas soon as possible.\u201d",
        "INDONESIA \u2014 A factory fire in Banten kills 26 people; "
        "dozens are reported missing.",
        "NATO \u2014 Rutte vows defence against space threats after "
        "reports of a Russian nuclear-armed satellite.",
    ]
    for b in briefs:
        y = para(d, x0, y, x1 - x0, "\u25aa  " + b, f_brief, 22)
        y += 2
    y += 6
    rule(d, x0, y, x1, 2)
    y += 10

    # ---- sports strip ----
    f_sport_k = font(SANS_B, 17)
    d.text((x0, y), "SPORT  •  FOOTBALL", font=f_sport_k, fill=ACCENT)
    y += 25
    f_sport = font(SERIF_B, 22)
    y = para(d, x0, y, x1 - x0,
             "Champions League tonight: Arsenal host Borussia Dortmund, "
             "Manchester City face Napoli, Real Madrid meet PSV.",
             f_sport, 28)
    y += 2
    f_sport2 = font(SERIF, 18)
    y = para(d, x0, y, x1 - x0,
             "AFC: Daejeon 3\u20132 Beijing Guoan; Kyoto 1\u20130 Pohang; "
             "Kashiwa 2\u20131 Newcastle Jets.",
             f_sport2, 23)
    y += 8
    rule(d, x0, y, x1, 4)
    y += 8
    f_foot = font(SANS, 14)
    centered(d, y, "THE WORLD TODAY  •  TUESDAY, NOVEMBER 24, 2026  •  ALL TIMES GMT",
             f_foot, color=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
