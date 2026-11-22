#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

Deterministic: no clock, no randomness, no network. Same bytes every run.
Reads only the fonts below. Writes entry.png (1024x1024) next to this file
when run directly, or to $MAKEFUN_OUTPUT_DIR/entry.png when set.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (25, 23, 19)
RED = (158, 27, 27)
BLUE = (31, 58, 95)
GRAY = (90, 86, 76)
LIGHT_RULE = (180, 172, 154)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, lh=None, align="left", box_w=None):
    """Draw lines starting at (x, y); returns the y just below the block."""
    if lh is None:
        lh = int(fnt.size * 1.25)
    for line in lines:
        if align == "center":
            w = draw.textlength(line, font=fnt)
            draw.text((x + (box_w - w) / 2, y), line, font=fnt, fill=fill)
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hrule(draw, x0, x1, y, w=1, fill=INK):
    draw.rectangle([x0, y, x1, y + w - 1], fill=fill)


# ---------------------------------------------------------------- motifs

def motif_starburst(draw, x, y, w, h):
    """Explosion flash for the Kryvyi Rih column."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 44, 58))
    cx, cy = x + w // 2, y + h // 2
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 26 if i % 2 == 0 else 10
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=(232, 130, 30))
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(248, 220, 120))
    for sx, sy in ((x + 30, y + 14), (x + w - 34, y + 40), (x + 60, y + h - 12)):
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(200, 200, 190))


def motif_chart(draw, x, y, w, h):
    """Falling market line for the sell-off column."""
    draw.rectangle([x, y, x + w, y + h], fill=(240, 234, 220))
    draw.line([x + 12, y + h - 12, x + w - 12, y + h - 12], fill=GRAY, width=1)
    draw.line([x + 12, y + 10, x + 12, y + h - 12], fill=GRAY, width=1)
    pts = [(x + 20, y + 14), (x + 70, y + 20), (x + 120, y + 18),
           (x + 170, y + 34), (x + 220, y + 30), (x + 270, y + 48)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.polygon([(x + 270, y + 48), (x + 258, y + 44), (x + 266, y + 56)],
                 fill=RED)


def motif_sun(draw, x, y, w, h):
    """Sun over the horizon for the COP31 column."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 96, 92))
    cx, cy = x + w // 2, y + h // 2 - 4
    for i in range(8):
        ang = math.pi * i / 4
        x1 = cx + 22 * math.cos(ang)
        y1 = cy + 22 * math.sin(ang)
        x2 = cx + 29 * math.cos(ang)
        y2 = cy + 29 * math.sin(ang)
        draw.line([x1, y1, x2, y2], fill=(248, 220, 120), width=3)
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(248, 220, 120))
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(16, 60, 60))
    draw.line([x + 20, y + h - 8, x + w - 20, y + h - 8], fill=(248, 220, 120), width=2)


def motif_badge(draw, x, y, w, h):
    """Gold star badge for the cartel-capture column."""
    draw.rectangle([x, y, x + w, y + h], fill=(52, 40, 26))
    cx, cy = x + w // 2, y + h // 2
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        r = 26 if i % 2 == 0 else 11
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=(201, 162, 39))
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(52, 40, 26))
    draw.line([x + 16, y + h - 10, x + w - 16, y + h - 10], fill=(201, 162, 39), width=2)


def motif_flags(draw, x, y, w, h):
    """Two overlapping circles for the diplomacy column."""
    draw.rectangle([x, y, x + w, y + h], fill=(31, 58, 95))
    draw.ellipse([x + w // 2 - 34, y + 12, x + w // 2 - 2, y + 44],
                 fill=(200, 60, 50))
    draw.ellipse([x + w // 2 + 2, y + 12, x + w // 2 + 34, y + 44],
                 fill=(240, 230, 210))
    draw.ellipse([x + w // 2 - 16, y + 12, x + w // 2 + 16, y + 44],
                 outline=(248, 220, 120), width=2)
    draw.line([x + 24, y + h - 10, x + w - 24, y + h - 10],
              fill=(248, 220, 120), width=2)


def motif_ice(draw, x, y, w, h):
    """Icebergs and a flag for the Greenland column."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 230, 238))
    draw.polygon([(x + 30, y + h - 8), (x + 80, y + 16), (x + 130, y + h - 8)],
                 fill=(255, 255, 255), outline=(120, 150, 170))
    draw.polygon([(x + 170, y + h - 8), (x + 215, y + 26), (x + 260, y + h - 8)],
                 fill=(255, 255, 255), outline=(120, 150, 170))
    draw.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 140, 170))
    draw.line([x + w - 40, y + 12, x + w - 40, y + 34], fill=RED, width=3)
    draw.polygon([(x + w - 40, y + 12), (x + w - 18, y + 18), (x + w - 40, y + 24)],
                 fill=RED)


def lead_scene(draw, x, y, w, h):
    """Night over the Gulf: sky, sea, a base silhouette, a missile arc."""
    draw.rectangle([x, y, x + w, y + h], fill=(22, 35, 58))
    for i in range(3):
        draw.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3],
                       fill=(22 + i * 6, 35 + i * 8, 58 + i * 10))
    for sx, sy in ((x + 24, y + 16), (x + 90, y + 30), (x + 170, y + 12),
                   (x + 250, y + 26), (x + 290, y + 44), (x + 140, y + 48)):
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(230, 230, 210))
    # missile arc: a curved trail ending in a small missile body
    arc = [(x + 40, y + h - 60), (x + 120, y + 60), (x + 210, y + 46),
           (x + 272, y + 78)]
    draw.line(arc, fill=(232, 130, 30), width=5, joint="curve")
    # fading trail dots behind the missile head
    for i, (tx, ty) in enumerate(((x + 236, y + 60), (x + 218, y + 54),
                                  (x + 200, y + 50))):
        r = 5 - i
        draw.ellipse([tx - r, ty - r, tx + r, ty + r], fill=(248, 200, 90))
    # missile body at the head of the arc, nose cone pointing up-right
    draw.ellipse([x + 262, y + 66, x + 284, y + 86], fill=(230, 230, 215))
    draw.polygon([(x + 282, y + 70), (x + 292, y + 76), (x + 282, y + 84)],
                 fill=(232, 130, 30))
    draw.ellipse([x + 262, y + 68, x + 282, y + 88], fill=(248, 220, 120))
    # sea
    draw.rectangle([x, y + h - 52, x + w, y + h], fill=(16, 60, 72))
    draw.line([x + 10, y + h - 40, x + w - 10, y + h - 40], fill=(90, 160, 170), width=2)
    draw.line([x + 30, y + h - 26, x + w - 40, y + h - 26], fill=(90, 160, 170), width=2)
    # base silhouette on the shore
    draw.rectangle([x + 18, y + h - 96, x + 78, y + h - 52], fill=(12, 18, 30))
    draw.rectangle([x + 86, y + h - 84, x + 126, y + h - 52], fill=(12, 18, 30))
    draw.pieslice([x + 86, y + h - 108, x + 126, y + h - 68], 180, 360,
                  fill=(12, 18, 30))
    for wx in (x + 28, x + 44, x + 60, x + 96, x + 112):
        draw.rectangle([wx, y + h - 88, wx + 5, y + h - 82], fill=(248, 220, 120))


# ---------------------------------------------------------------- layout

FEATURED = [
    ("CONFLICT — UKRAINE", "Russian missile hits Zelenskyy's hometown",
     "Two killed and dozens wounded in the city centre; a second strike "
     "hit rescuers as they arrived.", motif_starburst),
    ("MARKETS", "AI sell-off drags Wall Street into correction",
     "The Nasdaq falls 5.3%, wiping out its 2026 gains, as the S&P 500 "
     "drops 3.7% into correction.", motif_chart),
    ("CLIMATE — ANTALYA", "COP31 runs past deadline in Antalya",
     "Fossil-fuel wording is dropped from the draft as the talks "
     "deadlock past deadline.", motif_sun),
    ("MEXICO", "FBI most-wanted cartel boss captured",
     "Chapo Isidro is seized in a Sinaloa raid; gunfights and "
     "roadblocks follow, at least 11 dead.", motif_badge),
    ("DIPLOMACY", "Trump defends Putin ties; Zelenskyy hits back",
     "\"He's a killer,\" says Ukraine's president after the US president "
     "calls Putin a friend.", motif_flags),
    ("GREENLAND", "Denmark backs US security deal, 109–0",
     "Parliament ratifies the pact unanimously, clearing the way for two "
     "new American bases.", motif_ice),
]

AROUND = [
    ("NORTH KOREA", "Yongbyon enrichment plant expands — IAEA"),
    ("TECH", "Nvidia halts H200 chip exports to China"),
    ("EUROPE", "UK and EU seal post-Brexit reset deal"),
    ("HEALTH", "Cancer pill leaves tumours undetectable in 1 in 12"),
    ("EUROPE", "Gen Z walkouts in 25 countries on Youth Day"),
    ("ENERGY", "Hormuz attacks cut oil shipments 15%"),
    ("DENMARK", "Envoy to be expelled over murder plot"),
    ("USA", "FBI probes apparent hack of crime database"),
    ("USA", "Man convicted over LA's Palisades fire"),
    ("NEW YORK", "Mamdani: close Rikers Island by 2032"),
    ("PERU", "6.9 quake strikes Junín region"),
    ("IRAQ", "Basra energy-plant fire kills 4, injures 36"),
    ("GAZA", "Remains of 129 found in central Gaza rubble"),
    ("YEMEN", "Houthis report 70 Saudi raids on eight areas"),
    ("BALTIC", "Russian cargo ship ablaze after drone strike"),
    ("INDIA", "Modi opens SCO civilisational talks in Delhi"),
    ("VENEZUELA", "US signs new military deal"),
    ("UKRAINE", "Zelenskyy: Crimea bridge strikes “fair reply”"),
    ("ASIA", "EU–Indonesia deal agreed after 10 years"),
    ("USA", "Vance won't back Trump claim on Iran weapon"),
    ("MARKETS", "Anthropic shares slide; IPO raised $81.3bn"),
    ("RUSSIA", "WhatsApp and Telegram calls restricted"),
    ("BRAZIL", "Bacteria mosquitoes cut child dengue cases"),
    ("UKRAINE", "Kyiv homes burn after overnight strikes"),
]


def draw_frontpage():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top bar + masthead
    d.rectangle([0, 0, W, 8], fill=INK)
    title = "THE WORLD TODAY"
    tf = SERIF_B(74)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    date_line = "SATURDAY 21 NOVEMBER 2026"
    df = SANS_B(20)
    dw = d.textlength(date_line, font=df)
    d.text(((W - dw) / 2, 96), date_line, font=df, fill=RED)
    hrule(d, 24, 1000, 122, 3)
    hrule(d, 24, 1000, 128, 1)

    # lead story
    lx, ly, lw, lh = 24, 140, 312, 196
    lead_scene(d, lx, ly, lw, lh)
    tx = 356
    d.text((tx, 140), "CONFLICT — THE GULF", font=SANS_B(14), fill=RED)
    y = 162
    y = text_block(d, tx, y, ["IRAN STRIKES", "BAHRAIN"],
                   SERIF_B(44), lh=50)
    deck = ("Iran's Revolutionary Guards say they hit two US bases. "
            "Bahrain reports a fire at a civilian industrial site — "
            "and no injuries.")
    y = text_block(d, tx, y + 8, wrap(d, deck, SANS(17), 644),
                   SANS(17), lh=23, fill=(51, 48, 42))
    assert y <= 340, "lead deck overflow: %d" % y
    hrule(d, 24, 1000, 348, 1)

    # featured rows: 3 columns x 2 rows
    cols = [24, 356, 688]
    col_w = 312
    for row in range(2):
        top = 360 + row * 208
        for ci in range(3):
            kicker, head, deck_text, motif = FEATURED[row * 3 + ci]
            x = cols[ci]
            motif(d, x, top, col_w, 60)
            d.text((x, top + 68), kicker, font=SANS_B(13), fill=RED)
            hy = top + 88
            hl = wrap(d, head, SERIF_B(21), col_w)
            assert len(hl) <= 3, "headline too long: %r" % head
            hy = text_block(d, x, hy, hl, SERIF_B(21), lh=26)
            dl = wrap(d, deck_text, SANS(14), col_w)
            assert len(dl) <= 3, "deck too long: %r" % deck_text
            dy = text_block(d, x, hy + 4, dl, SANS(14), lh=18,
                            fill=(51, 48, 42))
            assert dy <= top + 200, "column overflow: %d" % dy
        if row == 0:
            hrule(d, 24, 1000, top + 200, 1, LIGHT_RULE)

    # around the world
    ay = 784
    hrule(d, 24, 1000, ay, 1)
    d.text((24, ay + 8), "AROUND THE WORLD", font=SANS_B(15), fill=INK)
    d.text((1000 - d.textlength("21 NOVEMBER 2026", font=SANS_B(13)), ay + 9),
           "21 NOVEMBER 2026", font=SANS_B(13), fill=RED)
    iy = ay + 34
    row_h = 15
    per_col = 12
    for i, (tag, head) in enumerate(AROUND):
        col = i // per_col
        row = i % per_col
        x = 24 if col == 0 else 524
        y = iy + row * row_h
        tfnt = SANS_B(12)
        hfnt = SANS(12)
        tag_w = d.textlength(tag + "  ", font=tfnt)
        d.text((x, y), tag, font=tfnt, fill=RED)
        d.text((x + tag_w, y), head, font=hfnt, fill=INK)
        assert x + tag_w + d.textlength(head, font=hfnt) <= (500 if col == 0 else 1000), \
            "list item too long: %r" % head
    # footer
    foot = "The World Today  •  Saturday 21 November 2026  •  All stories verified against wire reporting"
    ff = SANS(10)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 1006), foot, font=ff, fill=GRAY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = draw_frontpage()
    img.save(os.path.join(out_dir, "entry.png"))
    # also drop a copy beside the script when run locally
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    img.save(os.path.join(repo, "entry.png"))


if __name__ == "__main__":
    main()
