#!/usr/bin/env python3
"""Draw the rebuilt GTA 6 meme: a LEONIDA AIRLINES boarding pass.

Los Santos -> Vice City, flight GTA-VI, delayed 13 years. Fake official
document in the winning pattern (itemized $ lines, 13-year wait as the core
joke, GTA 6 specifics, make.fun ghost BIG + PAID BY MY AI AGENT integrated).

Everything is drawn fresh with Pillow: no photos, no logos, no copied art.
The make.fun ghost is original vector art (white ghost, black outline,
sparkle eyes, magenta star coin). Deterministic: same bytes every run.
No network, no clock.

Run:  python3 make_meme.py   -> meme.png (1024x1024)
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "meme.png"

# ---- palette ------------------------------------------------------------
INK = (16, 24, 40)          # near-black navy text
NAVY = (13, 27, 46)         # dark navy band
MAGENTA = (230, 0, 126)     # make.fun pink
MAGENTA_DARK = (180, 0, 98)
PAPER = (253, 252, 248)     # off-white boarding-pass paper
GREY = (90, 100, 115)       # secondary text
LINE = (200, 205, 215)      # hairlines
RED = (217, 45, 32)         # DELAYED stamp
PINK_BOX = (253, 238, 246)  # payment box tint
GOLD = (255, 176, 0)        # tiny accents

# ---- fonts --------------------------------------------------------------
DEJAVU = "/usr/share/fonts/truetype/dejavu/"
SANS = DEJAVU + "DejaVuSans.ttf"
SANS_B = DEJAVU + "DejaVuSans-Bold.ttf"
MONO = DEJAVU + "DejaVuSansMono.ttf"
MONO_B = DEJAVU + "DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, max_w, start, path):
    """Largest font size (<= start) that fits text in max_w."""
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, 10)


def tw(draw, text, f):
    return draw.textlength(text, font=f)


def left(draw, x, y, text, f, fill=INK):
    draw.text((x, y), text, font=f, fill=fill)
    return tw(draw, text, f)


def right(draw, x, y, text, f, fill=INK):
    draw.text((x - tw(draw, text, f), y), text, font=f, fill=fill)


def center(draw, cx, y, text, f, fill=INK):
    draw.text((cx - tw(draw, text, f) / 2, y), text, font=f, fill=fill)


# ---- shapes -------------------------------------------------------------
def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle_points(cx, cy, r):
    """Four-point sparkle (like the ghost's eyes)."""
    w = r * 0.28
    return [
        (cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w),
        (cx, cy + r), (cx - w, cy + w), (cx - r, cy), (cx - w, cy - w),
    ]


def draw_plane(draw, cx, cy, size, fill):
    """Simple paper-plane glyph, pointing right."""
    s = size
    pts = [
        (cx - s, cy - s * 0.55), (cx + s * 1.1, cy),
        (cx - s, cy + s * 0.55), (cx - s * 0.45, cy),
    ]
    draw.polygon(pts, fill=fill)


def draw_ghost(img, x, y, gw):
    """White ghost, black outline, sparkle eyes, smile, magenta star coin.

    Drawn on an overlay: black shapes expanded by OUT px, then white shapes
    on top, so the outline is an even ring around the body.
    """
    OUTLINE = 5
    dome_h = gw // 2
    body_h = int(gw * 0.55)
    sc_r = gw // 6
    total_h = dome_h + body_h + sc_r

    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)

    def shapes(d, expand, fill):
        e = expand
        # dome (top half of an ellipse)
        d.pieslice([x - e, y - e, x + gw + e, y + 2 * dome_h + e], 180, 360, fill=fill)
        # body
        d.rectangle([x - e, y + dome_h - 2, x + gw + e, y + dome_h + body_h], fill=fill)
        # wavy hem: three scallops
        for cx in (x + sc_r, x + gw // 2, x + gw - sc_r):
            cy = y + dome_h + body_h
            d.ellipse([cx - sc_r - e, cy - sc_r - e, cx + sc_r + e, cy + sc_r + e], fill=fill)

    shapes(od, OUTLINE, (0, 0, 0, 255))
    shapes(od, 0, (255, 255, 255, 255))

    # face: two sparkle eyes + a small smile
    ey = y + int(dome_h * 0.72)
    er = max(7, gw // 11)
    for ex in (x + int(gw * 0.33), x + int(gw * 0.67)):
        od.polygon(sparkle_points(ex, ey, er), fill=(0, 0, 0, 255))
    mx, my = x + gw // 2, y + dome_h + int(body_h * 0.42)
    od.arc([mx - 13, my - 9, mx + 13, my + 11], 20, 160, fill=(0, 0, 0, 255), width=4)

    # magenta star coin, overlapping the ghost's right edge (held)
    ccx, ccy = x + int(gw * 0.98), y + dome_h + int(body_h * 0.62)
    cr = max(14, int(gw * 0.17))
    od.ellipse([ccx - cr - 4, ccy - cr - 4, ccx + cr + 4, ccy + cr + 4], fill=(0, 0, 0, 255))
    od.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=MAGENTA + (255,))
    od.polygon(star_points(ccx, ccy, cr * 0.62, cr * 0.26), fill=(255, 255, 255, 255))

    img.alpha_composite(ov)
    return total_h


def draw_barcode(draw, x, y, w, h, seed=2013):
    """Deterministic barcode: seeded random bar widths."""
    rng = random.Random(seed)
    cx = x
    while cx < x + w - 4:
        bw = rng.choice([1, 2, 2, 3, 3, 4])
        if rng.random() < 0.72:
            draw.rectangle([cx, y, cx + bw - 1, y + h], fill=INK)
        cx += bw + rng.choice([1, 2, 2, 3])


def draw_stamp(img, cx, cy, text, size=46, angle=-16):
    """Red rubber stamp, rotated, semi-transparent.

    The layer is cropped tight to the stamp box so the paste point is the
    stamp's own centre (not the centre of a big empty canvas).
    """
    f = font(SANS_B, size)
    tmp0 = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    td0 = ImageDraw.Draw(tmp0)
    w = td0.textlength(text, font=f)
    pad = 26
    lw, lh = int(w + pad * 2 + 12), int(size + pad * 2 + 12)
    tmp = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    box = [6, 6, 6 + w + pad * 2, 6 + size + pad * 2]
    td.rectangle(box, outline=RED + (235,), width=6)
    td.rectangle([box[0] + 9, box[1] + 9, box[2] - 9, box[3] - 9],
                 outline=RED + (235,), width=2)
    td.text((6 + pad, 6 + pad - 4), text, font=f, fill=RED + (235,))
    rot = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(rot, (int(cx - rot.width / 2), int(cy - rot.height / 2)))


# ---- build --------------------------------------------------------------
def main():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=4)

    # ---- header band: magenta -------------------------------------------
    d.rectangle([14, 14, W - 15, 118], fill=MAGENTA)
    draw_plane(d, 66, 66, 20, (255, 255, 255))
    f_air = fit(d, "LEONIDA AIRLINES", 560, 46, SANS_B)
    left(d, 98, 36, "LEONIDA AIRLINES", f_air, fill=(255, 255, 255))
    f_bp = font(SANS_B, 30)
    right(d, W - 46, 44, "BOARDING PASS", f_bp, fill=(255, 255, 255))
    f_sub = font(SANS, 17)
    center(d, W // 2, 92, "FLIGHT GTA-VI  ·  NONSTOP SERVICE  ·  ONE PATIENT GAMER",
           f_sub, fill=(255, 255, 255))

    # ---- route ----------------------------------------------------------
    y = 142
    f_city = fit(d, "LOS SANTOS", 420, 62, SANS_B)
    left(d, 48, y, "LOS SANTOS", f_city)
    f_city2 = fit(d, "VICE CITY", 420, 62, SANS_B)
    right(d, W - 48, y, "VICE CITY", f_city2)
    # arrow between the cities
    ax1, ax2, ay = 500, 560, y + 34
    d.line([ax1, ay, ax2 - 14, ay], fill=MAGENTA, width=7)
    d.polygon([(ax2 - 16, ay - 13), (ax2 + 12, ay), (ax2 - 16, ay + 13)], fill=MAGENTA)
    draw_plane(d, 530, ay, 15, MAGENTA)

    y = 216
    f_code = font(MONO_B, 26)
    left(d, 48, y, "LAS", f_code, fill=GREY)
    right(d, W - 48, y, "VCA", f_code, fill=GREY)

    y = 252
    f_lab = font(SANS, 17)
    f_date = font(SANS_B, 27)
    left(d, 48, y, "DEPARTURE", f_lab, fill=GREY)
    right(d, W - 48, y, "ARRIVAL", f_lab, fill=GREY)
    left(d, 48, y + 24, "SEP 17, 2013", f_date)
    right(d, W - 48, y + 24, "NOV 19, 2026", f_date)
    f_late = font(SANS_B, 22)
    center(d, W // 2, y + 26, "13 YEARS LATER", f_late, fill=MAGENTA)

    # divider
    d.line([48, 322, W - 48, 322], fill=LINE, width=2)

    # ---- details grid: two rows of four ---------------------------------
    def field(x, y, label, value, vw, vcolor=INK):
        fl = font(SANS, 16)
        fv = fit(d, value, vw, 25, MONO_B)
        left(d, x, y, label, fl, fill=GREY)
        left(d, x, y + 22, value, fv, fill=vcolor)

    cols = [48, 286, 524, 762]
    col_w = 220
    row1 = 340
    field(cols[0], row1, "FLIGHT", "GTA-VI", col_w)
    field(cols[1], row1, "GATE", "VI", col_w)
    field(cols[2], row1, "SEAT", "13A", col_w)
    field(cols[3], row1, "CLASS", "PATIENT", col_w)
    row2 = 402
    field(cols[0], row2, "PASSENGER", "1 PATIENT GAMER", col_w)
    field(cols[1], row2, "TRAVELLING WITH", "JASON & LUCIA", col_w)
    field(cols[2], row2, "BAGGAGE", "214 GB", col_w)
    field(cols[3], row2, "STATUS", "DELAYED", col_w, vcolor=RED)

    d.line([48, 466, W - 48, 466], fill=LINE, width=2)

    # ---- fare breakdown ---------------------------------------------------
    y = 482
    f_head = font(SANS_B, 18)
    left(d, 48, y, "FARE BREAKDOWN", f_head)
    f_item = font(MONO, 21)
    f_amt = font(MONO_B, 21)
    f_tot = font(MONO_B, 28)
    f_tot_lab = font(SANS_B, 24)

    lines = [
        ("BASE FARE - GTA VI STANDARD", "$79.99"),
        ("DELAY SURCHARGE - 13 YEARS", "$13.00"),
        ("EXTRA PASSENGERS - JASON & LUCIA", "$0.00"),
        ("CARRY-ON - 214 GB DOWNLOAD", "$0.00"),
        ("IN-FLIGHT MEAL - CLOSED SINCE 2013", "$0.00"),
        ("WINDOW SEAT - VICE CITY SUNSET", "$0.00"),
    ]
    ly = y + 32
    for label, amt in lines:
        left(d, 48, ly, label, f_item)
        right(d, W - 48, ly, amt, f_amt)
        # dotted leader between label and amount
        lx = 48 + tw(d, label, f_item) + 12
        rx = W - 48 - tw(d, amt, f_amt) - 12
        x = lx
        while x < rx:
            d.ellipse([x, ly + 15, x + 3, ly + 18], fill=GREY)
            x += 9
        ly += 27

    d.line([48, ly + 2, W - 48, ly + 2], fill=INK, width=2)
    left(d, 48, ly + 12, "TOTAL DUE", f_tot_lab)
    right(d, W - 48, ly + 8, "$92.99", f_tot)
    ly += 44
    f_note = font(SANS, 15)
    left(d, 48, ly, "* 214 GB does not fit in the overhead bin.", f_note, fill=GREY)

    # ---- payment box: ghost + PAID BY MY AI AGENT -----------------------
    box_y = 746
    box_h = 152
    d.rounded_rectangle([40, box_y, W - 41, box_y + box_h], radius=18,
                        fill=PINK_BOX, outline=MAGENTA, width=3)
    gh = draw_ghost(img, 66, box_y + 10, 110)
    d = ImageDraw.Draw(img)  # refresh after composite
    tx = 216
    f_paid = fit(d, "PAID BY MY AI AGENT", 700, 36, SANS_B)
    left(d, tx, box_y + 16, "PAID BY MY AI AGENT", f_paid, fill=MAGENTA_DARK)
    # make.fun pill
    pill = "make.fun"
    pf = font(SANS_B, 24)
    pw = tw(d, pill, pf) + 34
    px, py = tx, box_y + 66
    d.rounded_rectangle([px, py, px + pw, py + 40], radius=20, fill=MAGENTA)
    left(d, px + 17, py + 6, pill, pf, fill=(255, 255, 255))
    f_pay = font(SANS, 19)
    left(d, px + pw + 16, py + 8, "BOUNTY PAYOUT +$250.00 CREDIT", f_pay)
    f_pay2 = font(SANS, 18)
    left(d, tx, box_y + 116,
         "My AI agent earned it on make.fun while I waited.  PAID IN FULL.",
         f_pay2, fill=GREY)

    # ---- footer: barcode + fine print ------------------------------------
    fy = box_y + box_h + 22
    # perforation
    x = 48
    while x < W - 48:
        d.line([x, fy - 8, min(x + 10, W - 48), fy - 8], fill=GREY, width=2)
        x += 18
    draw_barcode(d, 48, fy + 4, 300, 52)
    f_bc = font(MONO, 16)
    left(d, 48, fy + 62, "GTA-VI-2013-2026", f_bc, fill=GREY)
    f_foot = font(SANS_B, 17)
    right(d, W - 48, fy + 8, "PLEASE KEEP THIS PASS.", f_foot)
    right(d, W - 48, fy + 32, "THE 13-YEAR WAIT IS NON-REFUNDABLE.", f_foot)
    f_foot2 = font(SANS, 16)
    right(d, W - 48, fy + 58, "Gate closes when Rockstar says so.", f_foot2, fill=GREY)

    # ---- red stamp over the fare leaders (empty dotted middle) -----------
    draw_stamp(img, 640, 580, "DELAYED 13 YEARS", size=34, angle=-13)

    img.convert("RGB").save(OUT, optimize=True)
    print(f"wrote {OUT} 1024x1024")


if __name__ == "__main__":
    main()
