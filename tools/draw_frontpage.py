#!/usr/bin/env python3
"""Draw the 1024x1024 front page for news-image-20261121.

Deterministic: fixed text, fixed colours, fixed geometry, no timestamps,
no randomness. Output: entry.png next to main.ts (same directory as this
script's parent).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (17, 17, 17)
RED = (166, 25, 46)
GREY = (85, 85, 85)
LIGHT_GREY = (180, 175, 165)
RULE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SERIF_B = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SERIF_I = os.path.join(FONT_DIR, "NotoSerif-Italic.ttf")
SANS = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
SANS_I = os.path.join(FONT_DIR, "NotoSans-Italic.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real text widths. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def draw_illustration(draw, x0, y0, x1, y1):
    """Flat-colour night scene over Guasave, Sinaloa. No text inside."""
    # Sky
    draw.rectangle([x0, y0, x1, y0 + 118], fill=(34, 53, 92))
    # Stars (fixed positions)
    stars = [(18, 14), (52, 30), (96, 10), (140, 26), (188, 12), (232, 34),
             (268, 16), (305, 28), (70, 48), (160, 52), (250, 50), (120, 66)]
    for sx, sy in stars:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(245, 240, 220))
    # Moon
    draw.ellipse([x0 + 258, y0 + 8, x0 + 296, y0 + 46], fill=(245, 233, 200))
    draw.ellipse([x0 + 270, y0 + 18, x0 + 282, y0 + 30], fill=(228, 212, 170))
    # Helicopter (body, tail, rotor, skids, cockpit window)
    hx, hy = x0 + 118, y0 + 34
    draw.ellipse([hx - 26, hy - 8, hx + 26, hy + 14], fill=(22, 22, 30))
    draw.rectangle([hx + 24, hy - 2, hx + 52, hy + 8], fill=(22, 22, 30))
    draw.rectangle([hx - 34, hy - 12, hx + 34, hy - 8], fill=(22, 22, 30))
    draw.rectangle([hx - 4, hy + 14, hx + 4, hy + 22], fill=(22, 22, 30))
    draw.rectangle([hx + 48, hy - 12, hx + 52, hy - 2], fill=(22, 22, 30))
    draw.rectangle([hx + 8, hy - 4, hx + 20, hy + 6], fill=(247, 214, 120))
    # Mountains
    draw.polygon([(x0, y0 + 118), (x0 + 70, y0 + 62), (x0 + 130, y0 + 118)],
                 fill=(22, 35, 58))
    draw.polygon([(x0 + 90, y0 + 118), (x0 + 190, y0 + 52),
                  (x0 + 290, y0 + 118)], fill=(18, 30, 50))
    draw.polygon([(x0 + 240, y0 + 118), (x0 + 300, y0 + 78),
                  (x1, y0 + 118)], fill=(22, 35, 58))
    # Searchlight beam, over the mountains down to the ground line
    draw.polygon([(hx - 10, hy + 12), (hx + 10, hy + 12),
                  (hx + 46, y0 + 122), (hx - 46, y0 + 122)],
                 fill=(232, 217, 138))
    # Desert ground
    draw.rectangle([x0, y0 + 118, x1, y1], fill=(181, 122, 62))
    draw.rectangle([x0, y0 + 118, x1, y0 + 128], fill=(201, 143, 78))
    # Road with headlights
    draw.polygon([(x0 + 120, y1), (x0 + 150, y0 + 128),
                  (x0 + 180, y0 + 128), (x0 + 210, y1)], fill=(60, 58, 58))
    for i, ry in enumerate((y0 + 140, y0 + 152, y0 + 166)):
        w = 3 + i * 2
        cx = x0 + 165
        draw.rectangle([cx - w // 2, ry, cx + w // 2, ry + 5], fill=(245, 240, 200))
    # Town: small buildings with lit windows
    for bx, bw, bh in ((8, 34, 26), (52, 26, 34), (250, 40, 30), (296, 26, 22)):
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(74, 52, 38))
        draw.rectangle([x0 + bx + 6, y1 - bh + 6, x0 + bx + 14, y1 - bh + 14],
                       fill=(247, 214, 120))
        draw.rectangle([x0 + bx + bw - 14, y1 - bh + 6, x0 + bx + bw - 6,
                        y1 - bh + 14], fill=(247, 214, 120))
    # Frame
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


STORIES = [
    ("UKRAINE", "Missile strike hits Zelenskyy's hometown",
     "Russian missiles hit Kryvyi Rih twice, killing a boy, 7, and a woman, 20, and wounding 60."),
    ("CLIMATE", "COP31 talks run into overtime with no deal",
     "Talks in Antalya drag past their deadline with no deal yet; fossil fuels are absent from the draft."),
    ("MARKETS", "AI sell-off rattles world markets",
     "The S&P 500 fell 3.7% and the Nikkei 5.06% as investors fear AI spending will not pay off."),
    ("WORLD COURT", "Myanmar guilty of Rohingya genocide",
     "In a 9-6 ruling, the court found Myanmar guilty of genocide against the Rohingya - a first."),
    ("UKRAINE", "Russia's biggest November barrage",
     "404 drones and 111 missiles struck overnight; debris crashed in Poland. Warsaw cries provocation."),
    ("IRAN", "Trump weighs new strikes on Iran",
     "The US president weighs fresh strikes as Israel presses for action; oil traders face sanctions."),
    ("SPACE", "BepiColombo reaches Mercury orbit",
     "After eight years and 10 billion km, the ESA-JAXA orbiters arrive - only the second ever at Mercury."),
    ("PERU", "6.9 quake strikes Peru's Junin region",
     "A magnitude 6.9 earthquake struck the Junin region of Peru, shaking towns in the central Andes."),
    ("INDIA", "12 dead in India after suspect drinks",
     "At least 12 died and over 180 were hospitalised after suspected contaminated drinks in India."),
    ("UKRAINE", "Trump tells Europe to defund Ukraine",
     "After his summit with Putin, the US president told European allies to stop funding Ukraine."),
    ("GAZA", "Four killed in Gaza amid the truce",
     "At least four were killed in Israeli bombardments, including food-delivery workers, amid the truce."),
    ("HEALTH", "Mosquitoes cut dengue cases by 69%",
     "Brazilian researchers say mosquitoes carrying a bacterium cut dengue cases by 69% in trials."),
    ("SPACE", "Voyager 1, one light-day from Earth",
     "Voyager 1 is the first human-made object one light-day from Earth - about 26 billion km out."),
    ("BRAZIL", "Bolsonaro hospitalised under house arrest",
     "Brazil's ex-president was hospitalised with stomach issues while under house arrest."),
    ("GENEVA", "UN talks press on over AI weapons rules",
     "Negotiators in Geneva agree to keep working on rules governing AI weapons."),
]

IN_BRIEF_LEFT = [
    "Markets: S&P 500 6,910 -3.7% - FTSE 10,346 -1.02% - Brent $89.95 +0.57%",
    "Ebola death toll passes 5,700",
    "Salvadoran troops fight gangs in Haiti",
    "French police sentenced over racist beating of Michel Zecler",
]
IN_BRIEF_RIGHT = [
    "EU-Indonesia deal after ten years of talks",
    "Russian cargo ship ablaze in the Baltic after drone strike",
    "Denmark says it thwarted an assassination plot",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 26                      # left margin
    right = W - 26               # right edge of content
    content_w = right - mx       # 972

    # ---- Top thin rule ----
    draw.rectangle([mx, 8, right, 10], fill=RULE)

    # ---- Masthead ----
    f_mast = font(SERIF_B, 70)
    mast = "The World Today"
    mw = draw.textlength(mast, font=f_mast)
    draw.text(((W - mw) / 2, 14), mast, font=f_mast, fill=INK)

    # ---- Dateline (large, unmistakable) ----
    f_date = font(SANS_B, 26)
    date = "Saturday 21 November 2026"
    dw = draw.textlength(date, font=f_date)
    draw.text(((W - dw) / 2, 96), date, font=f_date, fill=RED)
    f_date_small = font(SANS, 12)
    small = "WORLD EDITION  |  No. 326  |  ALL THE NEWS OF THE DAY"
    sw = draw.textlength(small, font=f_date_small)
    draw.text(((W - sw) / 2, 128), small, font=f_date_small, fill=GREY)

    # ---- Red rule ----
    draw.rectangle([mx, 150, right, 154], fill=RED)

    # ---- Markets ticker ----
    f_tick = font(SANS, 13)
    tick = "S&P 500  6,910  -3.7%      FTSE 100  10,346  -1.02%      Brent crude  $89.95  +0.57%      Nikkei  -5.06%"
    tw = draw.textlength(tick, font=f_tick)
    draw.text(((W - tw) / 2, 160), tick, font=f_tick, fill=INK)
    draw.rectangle([mx, 182, right, 183], fill=LIGHT_GREY)

    # ---- Lead story ----
    lead_x = mx
    lead_w = 626
    ill_x0, ill_y0 = 668, 192
    ill_x1, ill_y1 = right, 372
    f_kick = font(SANS_B, 12)
    draw.text((lead_x, 192), "MEXICO  -  CARTEL CRACKDOWN", font=f_kick, fill=RED)
    f_lead_h = font(SERIF_B, 32)
    lead_head = "Mexico captures cartel boss 'El Chapo Isidro'"
    lh_lines = wrap(draw, lead_head, f_lead_h, lead_w)
    y = draw_lines(draw, lead_x, 214, lh_lines, f_lead_h, INK, 38)
    f_lead_b = font(SERIF, 14)
    lead_body = ("Fausto Isidro Meza Flores, leader of the Beltran Leyva cartel and one of "
                 "the FBI's 10 Most Wanted, was captured overnight in Guasave, Sinaloa, "
                 "with US intelligence help.")
    lb_lines = wrap(draw, lead_body, f_lead_b, lead_w)
    y = draw_lines(draw, lead_x, y + 8, lb_lines, f_lead_b, INK, 18)
    f_by = font(SERIF_I, 12)
    draw.text((lead_x, y + 8), "By The World Today staff  -  Guasave, Sinaloa",
              font=f_by, fill=GREY)

    # Illustration panel (right of lead)
    draw_illustration(draw, ill_x0, ill_y0, ill_x1, ill_y1)
    f_cap = font(SERIF_I, 11)
    cap = "Night falls over Guasave, Sinaloa, where the cartel boss was seized."
    cap_lines = wrap(draw, cap, f_cap, ill_x1 - ill_x0)
    draw_lines(draw, ill_x0, ill_y1 + 6, cap_lines, f_cap, GREY, 14)

    # ---- Rule above story grid ----
    draw.rectangle([mx, 424, right, 426], fill=RULE)

    # ---- Story grid: 3 columns x 5 stories ----
    f_label = font(SANS_B, 10)
    f_head = font(SERIF_B, 18)
    f_body = font(SERIF, 12)
    col_gap = 14
    col_w = (content_w - 2 * col_gap) // 3   # 314
    col_xs = [mx, mx + col_w + col_gap, mx + 2 * (col_w + col_gap)]
    grid_top = 438
    grid_bottom = 908
    columns = [STORIES[0:5], STORIES[5:10], STORIES[10:15]]
    for ci, col in enumerate(columns):
        x = col_xs[ci]
        y = grid_top
        for label, headline, body in col:
            draw.text((x, y), label, font=f_label, fill=RED)
            y += 12
            h_lines = wrap(draw, headline, f_head, col_w)
            if len(h_lines) > 2:
                h_lines = h_lines[:2]
                h_lines[-1] = h_lines[-1].rstrip() + " ..."
            y = draw_lines(draw, x, y, h_lines, f_head, INK, 20)
            b_lines = wrap(draw, body, f_body, col_w)
            if len(b_lines) > 3:
                b_lines = b_lines[:3]
                b_lines[-1] = b_lines[-1].rstrip() + " ..."
            y = draw_lines(draw, x, y + 2, b_lines, f_body, INK, 14)
            y += 4
            # divider between stories (not after the last in a column)
            if (label, headline, body) is not col[-1]:
                draw.rectangle([x, y, x + col_w, y], fill=LIGHT_GREY)
                y += 5
        if y > grid_bottom + 2:
            raise SystemExit("column %d overflows grid: bottom y=%d > %d"
                             % (ci, y, grid_bottom))
        # vertical rule between columns
        if ci < 2:
            vx = x + col_w + col_gap // 2
            draw.line([vx, grid_top, vx, grid_bottom], fill=LIGHT_GREY, width=1)

    # ---- Rule above In Brief ----
    draw.rectangle([mx, 918, right, 920], fill=RULE)

    # ---- In Brief strip (two columns) ----
    f_ib_h = font(SANS_B, 13)
    draw.text((mx, 928), "IN BRIEF", font=f_ib_h, fill=RED)
    f_ib = font(SANS, 12)
    ib_y = 950
    mid = mx + content_w // 2 + 8
    for item in IN_BRIEF_LEFT:
        draw.text((mx, ib_y), "-  " + item, font=f_ib, fill=INK)
        ib_y += 15
    ib_y = 950
    for item in IN_BRIEF_RIGHT:
        draw.text((mid, ib_y), "-  " + item, font=f_ib, fill=INK)
        ib_y += 15

    # ---- Footer ----
    f_foot = font(SANS, 10)
    foot = "The World Today  -  Saturday 21 November 2026"
    fw = draw.textlength(foot, font=f_foot)
    draw.text(((W - fw) / 2, 1006), foot, font=f_foot, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote %s %dx%d" % (OUT, W, H))


if __name__ == "__main__":
    main()
