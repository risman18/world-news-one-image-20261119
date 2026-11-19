#!/usr/bin/env python3
"""news-image-20261119 v1: a vintage broadsheet front page summing up
Thursday 19 November 2026, drawn with PIL (stdlib + Pillow only).

Writes /output/entry.png (1024x1024, JPEG bytes). Deterministic: no
randomness, no clock, no network; the same inputs always give the
same bytes.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

W, H = 1024, 1024
PAPER = (245, 237, 217)      # cream newsprint
INK = (22, 38, 76)           # navy
RED = (142, 43, 31)          # breaking-news red
FAINT = (120, 110, 88)       # thin-rule grey-brown

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w):
    """Largest font size <= size that fits max_w, for a single line."""
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, size)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, f, fill, x0=0, x1=W):
    w = draw.textlength(text, font=f)
    draw.text(((x0 + x1 - w) / 2, y), text, font=f, fill=fill)


def rule(draw, y, x0, x1, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def crop_to(img, tw, th, y_frac=0.5):
    """Center-crop (horizontally centred, vertical bias y_frac) to tw:th."""
    sw, sh = img.size
    target = tw / th
    if sw / sh > target:  # too wide: trim sides
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        box = (x0, 0, x0 + nw, sh)
    else:  # too tall: trim top/bottom around y_frac
        nh = int(sw / target)
        cy = int(sh * y_frac)
        y0 = max(0, min(sh - nh, cy - nh // 2))
        box = (0, y0, sw, y0 + nh)
    return img.crop(box).resize((tw, th), Image.LANCZOS)


def panel(page, draw, img, x, y, w, head, body):
    """One illustrated story panel: image, big headline, short caption."""
    im_h = 196
    pic = crop_to(img, w, im_h)
    draw.rectangle([x - 1, y - 1, x + w + 1, y + im_h + 1], outline=INK, width=2)
    page.paste(pic, (x, y))
    hy = y + im_h + 10
    hf = fit(draw, head, SERIF_B, 25, w)
    center(draw, hy, head, hf, INK, x, x + w)
    bf = font(SERIF, 16)
    lines = wrap(draw, body, bf, w)[:3]
    ly = hy + 36
    for ln in lines:
        center(draw, ly, ln, bf, INK, x, x + w)
        ly += 21


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # Outer double border.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

    # ---- Masthead ----
    f_title = fit(d, "THE WORLD TODAY", SERIF_B, 66, 940)
    center(d, 34, "THE WORLD TODAY", f_title, INK)
    rule(d, 118, 40, W - 40, width=3)
    f_date = font(SERIF_B, 27)
    center(d, 128, "Thursday, 19 November 2026", f_date, INK)
    f_tag = font(SANS, 15)
    center(d, 164, "T H E   D A Y ' S   N E W S ,   I N   O N E   P A G E",
           f_tag, FAINT)
    rule(d, 190, 40, W - 40, width=1)

    # ---- Breaking banner ----
    d.rectangle([40, 200, W - 40, 240], fill=RED)
    f_break = font(SANS_B, 26)
    center(d, 206, "\u2605  BREAKING NEWS  \u2605", f_break, PAPER)

    # ---- Lead story: three leaders meet in Shenzhen ----
    f_lead = fit(d, "THREE LEADERS MEET IN SHENZHEN", SERIF_B, 42, 944)
    center(d, 254, "THREE LEADERS MEET IN SHENZHEN", f_lead, INK)
    f_sub = font(SERIF, 20)
    sub = [
        "Trump, Xi and Putin sit down together at APEC \u2014 their first trilateral meeting.",
        "Xi hugged Trump on the tarmac; Ukraine, Iran and nuclear arms on the table.",
    ]
    ly = 306
    for ln in sub:
        center(d, ly, ln, f_sub, INK)
        ly += 26

    shenzhen = Image.open(ROOT / "assets" / "panel-shenzhen.jpg").convert("RGB")
    lead = crop_to(shenzhen, 944, 218, y_frac=0.62)
    d.rectangle([39, 367, 985, 586], outline=INK, width=2)
    page.paste(lead, (40, 368))

    rule(d, 604, 40, W - 40, width=2)

    # ---- Three more stories ----
    stories = [
        ("panel-bridge.jpg", "BRIDGE HIT AGAIN",
         "Ukraine strikes the Crimean Bridge a third time in a week. "
         "The rail span is hit overnight; traffic halts."),
        ("panel-vicecity.jpg", "VICE CITY OPENS",
         "GTA VI rolls out worldwide after 13 years. 17 million copies "
         "pre-sold; early reviews near-perfect."),
        ("panel-vangogh.jpg", "VAN GOGH: $190.4M",
         "Chestnut Trees in Blossom sets a Van Gogh record at Sotheby's, "
         "after a Nazi-era dispute is settled."),
    ]
    col_w, gap, x0 = 304, 16, 40
    for i, (fname, head, body) in enumerate(stories):
        img = Image.open(ROOT / "assets" / fname).convert("RGB")
        panel(page, d, img, x0 + i * (col_w + gap), 622, col_w, head, body)

    # ---- Also today strip ----
    rule(d, 934, 40, W - 40, width=2)
    f_also = font(SANS_B, 15)
    f_also_t = font(SERIF, 15)
    body = ("EU proposes a \u20ac45bn loan for Ukraine  \u2022  "
            "Cyclone Akvan nears India's east coast  \u2022  "
            "Voyager 1 reaches one light-day from Earth  \u2022  "
            "US and Iran trade fire across the Gulf  \u2022  "
            "Jeffries poised to be first Black Speaker")
    label = "ALSO TODAY:  "
    lw = d.textlength(label, font=f_also)
    lines = wrap(d, body, f_also_t, 944 - lw)[:2]
    y = 946
    for i, ln in enumerate(lines):
        d.text((40, y), label, font=f_also, fill=RED)
        d.text((40 + lw, y), ln, font=f_also_t, fill=INK)
        y += 20
        label = ""  # label only on the first line
        lw = 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "entry.png"
    page.save(out, format="JPEG", quality=90, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
