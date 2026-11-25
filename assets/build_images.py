#!/usr/bin/env python3
"""Build-time image generator for the Fridge Roast entry README.

Run once:  python3 assets/build_images.py
Produces cover.png + 4 gallery cards (assets/gallery-*.png) with Pillow.
NOT imported by main.py (the submitted entrypoint is pure stdlib);
these are static build-time assets only.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BG = (22, 24, 29)          # deep charcoal
PANEL = (38, 41, 48)
PANEL2 = (48, 52, 62)
GOLD = (212, 175, 105)
TEXT = (240, 238, 232)
MUTED = (168, 172, 182)
BLUE = (110, 180, 235)     # cold / Wi-Fi
WARM = (235, 150, 90)      # warm milk
GREEN = (120, 200, 140)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_fridge(d, x, y, w, h, screen_text=None, screen_sub=None):
    """A simple stainless smart fridge with a touchscreen."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=(58, 62, 72),
                        outline=(120, 126, 138), width=3)
    d.line([x, y + int(h * 0.62), x + w, y + int(h * 0.62)],
           fill=(120, 126, 138), width=3)
    # handles
    d.rounded_rectangle([x + w - 26, y + 30, x + w - 14, y + int(h * 0.55)],
                        radius=6, fill=(150, 156, 168))
    d.rounded_rectangle([x + w - 26, y + int(h * 0.62) + 24, x + w - 14,
                         y + int(h * 0.62) + 110], radius=6, fill=(150, 156, 168))
    # touchscreen
    sx, sy, sw, sh = x + 28, y + 34, 150, 120
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=10, fill=(16, 20, 28),
                        outline=BLUE, width=2)
    if screen_text:
        f = font(FONT_BOLD, 22)
        d.text((sx + 12, sy + 12), screen_text, font=f, fill=TEXT)
    if screen_sub:
        f = font(FONT_REG, 15)
        d.text((sx + 12, sy + 48), screen_sub, font=f, fill=MUTED)
        # progress bar
        d.rounded_rectangle([sx + 12, sy + 82, sx + sw - 12, sy + 96],
                            radius=6, fill=PANEL2)
        d.rounded_rectangle([sx + 12, sy + 82, sx + 12 + int((sw - 24) * 0.73),
                             sy + 96], radius=6, fill=BLUE)


def wifi_symbol(d, cx, cy, s, color):
    for r in (3, 2, 1):
        rr = s * r / 3
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=200, end=340,
              fill=color, width=7)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)


def milk_carton(d, x, y, w, h, warm=True):
    d.polygon([(x, y + 26), (x + w // 2, y), (x + w, y + 26), (x + w, y + h),
               (x, y + h)], fill=(235, 238, 242), outline=(150, 156, 168))
    d.polygon([(x, y + 26), (x + w // 2, y), (x + w, y + 26), (x + w // 2, y + 52)],
              fill=(210, 214, 220))
    f = font(FONT_BOLD, 20)
    d.text((x + w // 2, y + 62), "MILK", font=f, fill=(40, 44, 52), anchor="ma")
    col = WARM if warm else BLUE
    f2 = font(FONT_BOLD, 17)
    label = "WARM!" if warm else "COLD"
    d.text((x + w // 2, y + h - 40), label, font=f2, fill=col, anchor="ma")


def cover():
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # soft glow panels
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, fill=PANEL)
    draw_fridge(d, 90, 96, 300, 350, "Updating…", "3:00 AM · 73%")
    # Wi-Fi cold badge (left of line)
    wifi_symbol(d, 560, 190, 90, BLUE)
    d.text((560, 270), "Wi-Fi: ❄ COLD", font=font(FONT_BOLD, 30),
           fill=BLUE, anchor="ma")
    # milk warm badge
    milk_carton(d, 880, 130, 150, 220, warm=True)
    d.text((955, 380), "Milk: WARM", font=font(FONT_BOLD, 30),
           fill=WARM, anchor="ma")
    # the line
    line = ("The fridge installed an update at 3 a.m. "
            "Now it keeps the Wi-Fi cold and the milk warm.")
    f = font(FONT_BOLD, 40)
    lines = wrap(d, "\u201c" + line + "\u201d", f, 1060)
    y = 490
    for ln in lines:
        d.text((640, y), ln, font=f, fill=TEXT, anchor="ma")
        y += 52
    d.text((640, 640), "FRIDGE ROAST · ONE LINE, BIGGEST LAUGH · $5 POOL · 87 CHARACTERS",
           font=font(FONT_BOLD, 20), fill=GOLD, anchor="ma")
    img.save(os.path.join(ROOT, "cover.png"))


def card(path, title, accent, draw_body):
    W, H = 640, 400
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([16, 16, W - 16, H - 16], radius=20, fill=PANEL)
    d.text((32, 28), title, font=font(FONT_BOLD, 26), fill=accent)
    draw_body(d, W, H)
    img.save(path)


def g1_setup(d, W, H):
    draw_fridge(d, 60, 90, 210, 250, "Updating…", "3:00 AM · 73%")
    f = font(FONT_REG, 19)
    y = 120
    for t in ["3:00 AM — the house is asleep.",
              "The fridge decides NOW is the time.",
              "One firmware update later…"]:
        for ln in wrap(d, t, f, 300):
            d.text((300, y), ln, font=f, fill=TEXT)
            y += 28
        y += 22


def g2_turn(d, W, H):
    # left: Wi-Fi cold
    d.rounded_rectangle([32, 90, 300, 330], radius=16, fill=PANEL2)
    wifi_symbol(d, 166, 170, 70, BLUE)
    d.text((166, 240), "Wi-Fi", font=font(FONT_BOLD, 26), fill=TEXT, anchor="ma")
    d.text((166, 280), "❄ COLD", font=font(FONT_BOLD, 26), fill=BLUE, anchor="ma")
    # right: milk warm
    d.rounded_rectangle([340, 90, 608, 330], radius=16, fill=PANEL2)
    milk_carton(d, 424, 100, 100, 130, warm=True)
    d.text((474, 240), "Milk", font=font(FONT_BOLD, 26), fill=TEXT, anchor="ma")
    d.text((474, 280), "WARM", font=font(FONT_BOLD, 26), fill=WARM, anchor="ma")
    d.text((320, 350), "The inversion IS the punchline.",
           font=font(FONT_REG, 20), fill=MUTED, anchor="ma")


def g3_tournament(d, W, H):
    rows = [
        ("26", "candidates across 10 devices", TEXT),
        ("8", "seeds into the knockout bracket", TEXT),
        ("24/25", "tournament winner's brief score", GOLD),
        ("87", "characters — smaller wins exact ties", GREEN),
    ]
    y = 96
    for num, label, col in rows:
        d.text((48, y), num, font=font(FONT_BOLD, 34), fill=col)
        d.text((170, y + 6), label, font=font(FONT_REG, 22), fill=TEXT)
        y += 62
    d.text((48, 350), "Scored criterion by criterion, in brief order.",
           font=font(FONT_REG, 19), fill=MUTED)


def g4_line(d, W, H):
    line = ("The fridge installed an update at 3 a.m. "
            "Now it keeps the Wi-Fi cold and the milk warm.")
    f = font(FONT_BOLD, 34)
    lines = wrap(d, "\u201c" + line + "\u201d", f, 560)
    y = 110
    for ln in lines:
        d.text((320, y), ln, font=f, fill=TEXT, anchor="ma")
        y += 46
    d.text((320, 320), "87 characters · 1 line · no trailing newline",
           font=font(FONT_REG, 20), fill=GOLD, anchor="ma")


def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    cover()
    card(os.path.join(ROOT, "assets", "gallery-1-setup.png"),
         "1 · THE SETUP", BLUE, g1_setup)
    card(os.path.join(ROOT, "assets", "gallery-2-turn.png"),
         "2 · THE TURN", GOLD, g2_turn)
    card(os.path.join(ROOT, "assets", "gallery-3-tournament.png"),
         "3 · THE TOURNAMENT", GREEN, g3_tournament)
    card(os.path.join(ROOT, "assets", "gallery-4-line.png"),
         "4 · THE LINE", GOLD, g4_line)
    print("built cover.png + 4 gallery cards")


if __name__ == "__main__":
    main()
