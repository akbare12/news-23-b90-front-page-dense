#!/usr/bin/env python3
"""news-23 b90 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page, 31 stories. PIL only in this builder script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 8  # margin
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DJS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PAPER = (250, 248, 240)
INK = (20, 20, 20)
GRAY = (110, 110, 110)
RED = (178, 0, 20)
DARKRED = (140, 0, 16)
NAVY = (16, 32, 86)
GOLD = (176, 132, 16)
TEAL = (0, 110, 110)
PURPLE = (96, 44, 130)
BLUE = (24, 80, 180)
GREEN = (18, 110, 44)
LIGHT = (238, 236, 228)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, font, fill, leading=None):
    if leading is None:
        leading = font.size + 3
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(d, x_right, y, label, fill):
    f = F(DJB, 10)
    tw = d.textlength(label, font=f)
    w = int(tw) + 12
    x0 = x_right - w
    d.rounded_rectangle([x0, y, x_right, y + 14], radius=3, fill=fill)
    d.text((x0 + 6, y + 2), label, font=f, fill=WHITE)
    return x0


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 50], fill=BLACK)
    d.text((M + 2, 6), "THE WORLD TODAY", font=F(DJS, 34), fill=WHITE)
    dt = "MONDAY 23 NOVEMBER 2026"
    d.text((W - M - 2 - d.textlength(dt, font=F(DJB, 15)), 16), dt,
           font=F(DJB, 15), fill=(232, 184, 64))

    # ---------- kicker ----------
    d.rectangle([0, 50, W, 72], fill=RED)
    d.text((M + 2, 55), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  "
           "US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
           font=F(DJB, 13), fill=WHITE)

    # ---------- number strip (2 rows x 5) ----------
    strip = [
        ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
        ("11,762", "EBOLA CASES, DRC", TEAL), ("10T won", "SEOUL STABILISATION FUND", GOLD),
        ("2%", "BILLIONAIRE TAX IN PARIS", GREEN),
        ("$450M", "SKUBAL DEAL", NAVY), ("165", "RUSSIAN MISSILES/WEEK", RED),
        ("12,000", "CLEARED IN MANCHESTER", TEAL), ("264 kg", "EXPLOSIVES SEIZED", GOLD),
        ("$107.3B", "ANTHROPIC IPO", GREEN),
    ]
    cw = (W - 2 * M) // 5
    y0 = 76
    for i, (num, lab, col) in enumerate(strip):
        cx = M + (i % 5) * cw
        cy = y0 + (i // 5) * 30
        d.text((cx + 4, cy), num, font=F(DJB, 19), fill=col)
        d.text((cx + 4, cy + 21), lab, font=F(DJB, 8), fill=GRAY)
    d.line([M, 138, W - M, 138], fill=(200, 196, 184), width=1)

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", NAVY), ("AMERICAS 8", RED), ("MIDDLE EAST 6", GOLD),
               ("EUROPE 5", TEAL), ("AFRICA 3", PURPLE), ("WORLD 2", (60, 60, 60))]
    rw = (W - 2 * M) // 6
    y = 142
    for i, (lab, col) in enumerate(regions):
        x = M + i * rw
        d.rectangle([x, y, x + rw - 2, y + 18], fill=col)
        tw = d.textlength(lab, font=F(DJB, 10))
        d.text((x + (rw - 2 - tw) / 2, y + 4), lab, font=F(DJB, 10), fill=WHITE)

    # ---------- THE DAY IN UTC ----------
    y = 164
    d.text((M + 2, y), "THE DAY IN UTC", font=F(DJB, 10), fill=INK)
    d.text((M + 96, y), "~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index"
           "   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
           font=F(DJ, 10), fill=INK)
    ap = "~ APPROX"
    d.text((W - M - 2 - d.textlength(ap, font=F(DJ, 9)), y + 1), ap,
           font=F(DJ, 9), fill=GRAY)

    # ---------- heroes ----------
    hy = 182          # scene top
    scene_h = 118
    hw = (W - 2 * M - 12) // 3   # 330
    hx = [M, M + hw + 6, M + 2 * (hw + 6)]

    # --- hero 1 scene: Kospi skyline + chart ---
    x0 = hx[0]
    d.rectangle([x0, hy, x0 + hw, hy + scene_h], fill=(10, 18, 48))
    # buildings with lit windows
    import random
    rnd = random.Random(7)
    bx = x0 + 6
    while bx < x0 + hw - 24:
        bw = rnd.randint(22, 34)
        bh = rnd.randint(38, 78)
        d.rectangle([bx, hy + scene_h - bh, bx + bw, hy + scene_h], fill=(24, 40, 84))
        for wy in range(hy + scene_h - bh + 6, hy + scene_h - 6, 10):
            for wx in range(bx + 4, bx + bw - 5, 9):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
        bx += bw + 4
    # orange chart line (falling then recovering)
    pts = [(x0 + 10, hy + 46), (x0 + 70, hy + 62), (x0 + 130, hy + 40),
           (x0 + 190, hy + 58), (x0 + 250, hy + 30), (x0 + hw - 12, hy + 44)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE)
    d.text((x0 + 8, hy + 6), "-3.3%", font=F(DJB, 26), fill=(255, 70, 70))
    d.rectangle([x0, hy + scene_h - 16, x0 + hw, hy + scene_h], fill=BLACK)
    d.text((x0 + 6, hy + scene_h - 14), "KOSPI 4,708.54   \u00b7   -161 PTS",
           font=F(DJB, 10), fill=WHITE)

    # --- hero 2 scene: Guterres globe ---
    x0 = hx[1]
    d.rectangle([x0, hy, x0 + hw, hy + scene_h], fill=(12, 92, 40))
    d.text((x0 + 10, hy + 12), "150 DELEGATES", font=F(DJB, 26), fill=(255, 214, 90))
    d.text((x0 + 10, hy + 42), "BACK A RISK", font=F(DJB, 26), fill=(255, 214, 90))
    d.text((x0 + 10, hy + 72), "FRAMEWORK", font=F(DJB, 26), fill=(255, 214, 90))
    # globe
    cx, cy, r = x0 + hw - 52, hy + 58, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 225, 200),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - r + 12, cy - r + 8, cx + r - 12, cy + r - 8], outline=(90, 150, 100), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(90, 150, 100), width=1)
    d.line([cx, cy - r, cx, cy + r], fill=(90, 150, 100), width=1)
    d.rectangle([x0, hy + scene_h - 16, x0 + hw, hy + scene_h], fill=BLACK)
    d.text((x0 + 6, hy + scene_h - 14), "UN  \u00b7  BRIDGETOWN", font=F(DJB, 10), fill=WHITE)

    # --- hero 3 scene: Power Index bars (values INSIDE bars) ---
    x0 = hx[2]
    d.rectangle([x0, hy, x0 + hw, hy + scene_h], fill=(245, 240, 226))
    d.text((x0 + 8, hy + 4), "NARROWEST SINCE 2018", font=F(DJB, 10), fill=INK)
    gap = "GAP 5.3"
    d.text((x0 + hw - 8 - d.textlength(gap, font=F(DJB, 10)), hy + 4), gap,
           font=F(DJB, 10), fill=RED)
    bars = [("US", 78.9, NAVY), ("CHINA", 73.6, RED), ("INDIA", 40.5, GOLD)]
    base = hy + scene_h - 22
    bw = 52
    gapx = (hw - 3 * bw) // 4
    for i, (lab, val, col) in enumerate(bars):
        bx = x0 + gapx + i * (bw + gapx)
        bh = int(val * 0.62)  # 78.9 -> 48, 73.6 -> 45, 40.5 -> 25
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
        # value ABOVE the bar (never inside a short bar, never under the header)
        vtxt = f"{val}"
        d.text((bx + (bw - d.textlength(vtxt, font=F(DJB, 13))) / 2, base - bh - 17),
               vtxt, font=F(DJB, 13), fill=INK)
        d.text((bx + (bw - d.textlength(lab, font=F(DJB, 10))) / 2, base - 15),
               lab, font=F(DJB, 10), fill=WHITE)
    d.rectangle([x0, hy + scene_h - 16, x0 + hw, hy + scene_h], fill=BLACK)
    d.text((x0 + 6, hy + scene_h - 14), "ASIA POWER INDEX 2026", font=F(DJB, 10), fill=WHITE)

    # --- hero headlines / bodies / source+chip ---
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
         "Samsung -3.1%, SK Hynix -2.5%.", "KOREA EXCHANGE", "REPORTED", BLUE),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; "
         "150 back a risk framework.", "UNITED NATIONS", "REPORTED", BLUE),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, "
         "narrowest since 2018. India third at 40.5.", "LOWY INSTITUTE", "REPORTED", BLUE),
    ]
    ty = hy + scene_h + 8
    for i, (hl, body, src, chiplab, chipcol) in enumerate(heroes):
        x0 = hx[i]
        lines = wrap(d, hl, F(DJB, 17), hw)
        y = text_lines(d, x0, ty, lines[:2], F(DJB, 17), INK, leading=20)
        blines = wrap(d, body, F(DJ, 11), hw)
        y = text_lines(d, x0, y + 2, blines[:2], F(DJ, 11), (50, 50, 50), leading=14)
        chip_y = y + 4
        d.text((x0, chip_y + 2), src, font=F(DJ, 9), fill=GRAY)
        chip(d, x0 + hw, chip_y, chiplab, chipcol)

    # ---------- MORE OF THE DAY strip ----------
    sy = 402
    d.rectangle([0, sy, W, sy + 20], fill=BLACK)
    d.text((M + 2, sy + 3), "MORE OF THE DAY  \u2014  10 STORIES",
           font=F(DJB, 12), fill=WHITE)

    # ---------- 10 cards ----------
    cards = [
        ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", BLUE, NAVY),
        ("FBI", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", BLUE, (60, 60, 60)),
        ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", BLUE, GOLD),
        ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED", BLUE, TEAL),
        ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", BLUE, RED),
        ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED", BLUE, RED),
        ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", BLUE, PURPLE),
        ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED", BLUE, TEAL),
        ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM", RED, NAVY),
        ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", RED, PURPLE),
    ]
    cw2 = 198
    gap2 = 6
    cy0 = sy + 24
    ch2 = 74
    for i, (cat, hl, body, src, chiplab, chipcol, catcol) in enumerate(cards):
        col, row = i % 5, i // 5
        x0 = M + col * (cw2 + gap2)
        y0 = cy0 + row * (ch2 + 5)
        d.rectangle([x0, y0, x0 + cw2, y0 + ch2], outline=(190, 186, 176), width=1, fill=WHITE)
        d.rectangle([x0, y0, x0 + cw2, y0 + 16], fill=catcol)
        d.text((x0 + 5, y0 + 3), cat, font=F(DJB, 9), fill=WHITE)
        num = str(i + 1)
        d.text((x0 + cw2 - 5 - d.textlength(num, font=F(DJB, 10)), y0 + 3),
               num, font=F(DJB, 10), fill=WHITE)
        hl_lines = wrap(d, hl, F(DJB, 11), cw2 - 10)
        yy = text_lines(d, x0 + 5, y0 + 20, hl_lines[:2], F(DJB, 11), INK, leading=13)
        d.text((x0 + 5, yy + 1), body, font=F(DJ, 10), fill=(60, 60, 60))
        chip_y = y0 + ch2 - 17
        d.text((x0 + 5, chip_y + 2), src, font=F(DJ, 9), fill=GRAY)
        chip(d, x0 + cw2 - 4, chip_y, chiplab, chipcol)

    # ---------- WHERE IT HAPPENED / ALSO strips ----------
    my = cy0 + 2 * ch2 + 5 + 4  # 579
    d.rectangle([0, my, W, my + 20], fill=BLACK)
    d.text((M + 2, my + 3), "WHERE IT HAPPENED", font=F(DJB, 12), fill=WHITE)
    d.text((340, my + 3), "ALSO ON MONDAY", font=F(DJB, 12), fill=WHITE)

    # ---------- map ----------
    mx, my0, mw, mh = M, my + 24, 322, 216
    d.rectangle([mx, my0, mx + mw, my0 + mh], outline=(190, 186, 176), width=1, fill=(242, 240, 232))
    # stylised continents (light green blobs)
    d.polygon([(mx + 18, my0 + 30), (mx + 60, my0 + 14), (mx + 104, my0 + 26),
               (mx + 118, my0 + 66), (mx + 100, my0 + 120), (mx + 72, my0 + 156),
               (mx + 34, my0 + 132), (mx + 12, my0 + 80)], fill=(196, 222, 178))
    d.polygon([(mx + 150, my0 + 22), (mx + 210, my0 + 10), (mx + 268, my0 + 18),
               (mx + 296, my0 + 44), (mx + 272, my0 + 74), (mx + 218, my0 + 84),
               (mx + 172, my0 + 66), (mx + 146, my0 + 44)], fill=(196, 222, 178))
    d.polygon([(mx + 168, my0 + 96), (mx + 206, my0 + 90), (mx + 224, my0 + 118),
               (mx + 206, my0 + 152), (mx + 178, my0 + 140), (mx + 162, my0 + 116)],
              fill=(196, 222, 178))
    d.polygon([(mx + 252, my0 + 158), (mx + 292, my0 + 150), (mx + 306, my0 + 172),
               (mx + 282, my0 + 188), (mx + 254, my0 + 180)], fill=(196, 222, 178))
    # pins: (number, x, y) — all inside blobs, spread >= ~22px
    pins = [(4, 52, 66), (8, 34, 100), (7, 76, 84), (9, 66, 122), (10, 88, 140),
            (2, 120, 162), (6, 186, 44), (11, 216, 34), (12, 246, 30), (13, 276, 40),
            (3, 236, 58), (1, 268, 66), (5, 100, 52)]
    for n, px, py in pins:
        d.ellipse([mx + px - 8, my0 + py - 8, mx + px + 8, my0 + py + 8],
                  fill=RED, outline=WHITE, width=1)
        t = str(n)
        d.text((mx + px - d.textlength(t, font=F(DJB, 9)) / 2, my0 + py - 5),
               t, font=F(DJB, 9), fill=WHITE)
    # legend (3 lines, inside box, white strip behind)
    leg = ["Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
           "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF",
           "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow"]
    ly = my0 + mh - 34
    d.rectangle([mx + 2, ly - 3, mx + mw - 2, my0 + mh - 2], fill=WHITE)
    for ln in leg:
        d.text((mx + 6, ly), ln, font=F(DJ, 9), fill=INK)
        ly += 11

    # ---------- ALSO list (18 items, 2 cols x 9) ----------
    also = [
        "14. Paris: 100+ back 2% billionaire tax",
        "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week",
        "17. COP31: the day after Antalya pact rejected",
        "18. Benghazi: UN demands probe of port attacks  [CLAIM]",
        "19. Israel unity talks resume",
        "20. Gaza: two killed in Israeli strike",
        "21. West Bank settler attacks",
        "22. Iran war: no deal in sight",
        "23. Lebanon seizes 264 kg explosives",
        "24. Bahrain: strike hits plant, 2 hurt",
        "25. Sudan: defences down drones  [CLAIM]",
        "26. DRC: fighting traps Ebola teams",
        "27. Bangladesh: Hasina jailed if she returns",
        "28. Seoul minister quits in exam row",
        "29. SK Telecom -7.3% as hype cools",
        "30. China eases margin rules",
        "31. Seoul readies 10T-won fund",
    ]
    ax = 340
    ay = my0 + 2
    colw = 340
    for i, item in enumerate(also):
        col, row = i // 9, i % 9
        x = ax + col * colw
        y = ay + row * 23
        if "[CLAIM]" in item:
            base_txt, _ = item.split("  [CLAIM]")
            d.text((x, y), base_txt, font=F(DJ, 11), fill=INK)
            tw = d.textlength(base_txt, font=F(DJ, 11))
            d.text((x + tw + 4, y), "[CLAIM]", font=F(DJB, 10), fill=RED)
        else:
            d.text((x, y), item, font=F(DJ, 11), fill=INK)

    # ---------- DATE CHECK ----------
    dy = my0 + mh + 10  # 849
    dh = 62
    d.rectangle([M, dy, W - M, dy + dh], outline=RED, width=2, fill=(255, 244, 244))
    d.text((M + 8, dy + 6), "DATE CHECK", font=F(DJB, 13), fill=RED)
    rt = "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY"
    d.text((W - M - 8 - d.textlength(rt, font=F(DJB, 9)), dy + 8), rt,
           font=F(DJB, 9), fill=RED)
    d.text((M + 8, dy + 26),
           "LEFT OUT \u2014 NOT 23 NOV: Dems 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov)"
           " \u00b7 El Chapo (22 Nov) \u00b7 EU-Indonesia (21 Nov) \u00b7 Nigeria boat (21 Nov)"
           " \u00b7 ICJ Myanmar (19 Nov)",
           font=F(DJ, 10), fill=INK)
    d.text((M + 8, dy + 42),
           "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled"
           " \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
           font=F(DJ, 10), fill=INK)

    # ---------- footer ----------
    fy = dy + dh + 10  # 921
    d.text((M + 2, fy), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=F(DJ, 10), fill=GRAY)
    d.text((M + 2, fy + 15), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
           font=F(DJ, 10), fill=GRAY)
    d.text((M + 2, fy + 30), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
           font=F(DJ, 10), fill=GRAY)
    d.line([M, fy + 48, W - M, fy + 48], fill=GOLD, width=2)
    foot = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
    d.text(((W - d.textlength(foot, font=F(DJB, 13))) / 2, fy + 56), foot,
           font=F(DJB, 13), fill=GOLD)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
