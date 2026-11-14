#!/usr/bin/env python3
"""Render the README images (images/*.png) with ImageMagick from fonts/ttf.

Usage:  python3 scripts/render.py
Requires: ImageMagick (`convert`) and HarfBuzz utils (`hb-view`).
"""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "fonts", "ttf", "KVANTUMA1451.ttf")
OUT = os.path.join(ROOT, "images")
os.makedirs(OUT, exist_ok=True)

BG, INK, MUTED, GOLD, WINE, CREAM = "#F0ECDD", "#1a1a1a", "#4a4a4a", "#C5B484", "#B05A67", "#F0ECDD"


def convert(*args):
    subprocess.run(["convert", *args], check=True)


def specimen():
    W, H = 960, 1135
    a = ["-size", f"{W}x{H}", f"xc:{BG}", "-font", FONT]
    a += ["-fill", WINE, "-draw", f"rectangle 0,757 {W},{H}"]
    t = lambda size, color, x, y, s: ["-pointsize", str(size), "-fill", color, "-annotate", f"+{x}+{y}", s]
    a += t(118, MUTED, 40, 130, "KVANTUMA 1451")
    a += t(150, INK, 40, 340, "Aa Ee Rr")
    a += t(150, INK, 40, 520, "Яя Жж Єє")
    a += t(560, GOLD, 600, 560, "ж")
    a += t(150, WINE, 40, 700, "Публікатор")
    a += t(64, INK, 50, 830, "abcdefghijklm")
    a += t(64, INK, 50, 925, "nopqrstuvwxyz")
    a += t(64, CREAM, 50, 1020, "0123456789 +=<>{}")
    a += t(64, INK, 50, 1105, "абвгґдеєжзиіїйк")
    convert(*a, os.path.join(OUT, "specimen.png"))


def hb_line(text, size, color, path):
    """Shape one line with HarfBuzz (applies liga/calt, e.g. ->) into a transparent PNG."""
    subprocess.run(["hb-view", FONT, text, f"--font-size={size}", "--margin=0",
                    f"--foreground={color.lstrip('#')}", "--background=00000000",
                    f"--output-file={path}"], check=True)


def sample(name, title, lines, size=54, width=1500):
    import tempfile
    pad = 60
    lh = int(size * 1.55)
    H = pad * 2 + 60 + lh * len(lines)
    a = ["-size", f"{width}x{H}", f"xc:{BG}", "-font", FONT,
         "-pointsize", "30", "-fill", WINE, "-annotate", f"+{pad}+{pad + 24}", title]
    with tempfile.TemporaryDirectory() as tmp:
        y = pad + 60
        for i, ln in enumerate(lines):
            p = os.path.join(tmp, f"{i}.png")
            hb_line(ln, size, INK, p)
            a += [p, "-gravity", "NorthWest", "-geometry", f"+{pad}+{y}", "-composite"]
            y += lh
        convert(*a, os.path.join(OUT, name + ".png"))


def alphabets():
    sample("alphabets", "ALPHABETS", [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "abcdefghijklmnopqrstuvwxyz",
        "АБВГҐДЕЁЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
        "абвгґдеёєжзиіїйклмнопрстуфхцчшщъыьэюя",
        "0123456789  .,:;!?'()-+=<>{}  ->",
    ], size=52)


def english():
    sample("english", "ENGLISH", [
        "The quick brown fox jumps over the lazy dog.",
        "Pack my box with five dozen liquor jugs!",
        "How vexingly quick daft zebras jump?",
        "if (x + 1 = 5) -> { go home }",
    ])


def ukrainian():
    sample("ukrainian", "УКРАЇНСЬКА", [
        "Чуєш їх, доцю, га? Кумедна ж ти, прощайся без ґольфів!",
        "Єнот і їжак ходили в гості до щура.",
        "Щастя -> {любов + дружба} = життя.",
        "Ґанок, цвях, ялинка, юшка, об'єм.",
    ])


def russian():
    sample("russian", "РУССКИЙ", [
        "Съешь ещё этих мягких французских булок, да выпей чаю.",
        "Широкая электрификация южных губерний даст мощный толчок.",
        "Ёж, щука, ферзь, цирк, шмель, объём, эхо.",
        "2 + 2 = 4, 7 > 3, 1 < 5 -> да!",
    ])


def glyph_sheet():
    chars = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "АБВГҐДЕЁЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
             "абвгґдеёєжзиіїйклмнопрстуфхцчшщъыьэюя"
             "0123456789.,:;!?'()-+=<>{}^")
    cols, cell, pad = 16, 90, 40
    rows = -(-len(chars) // cols)
    W, H = cols * cell + pad * 2, rows * cell + pad * 2
    a = ["-size", f"{W}x{H}", f"xc:{BG}", "-font", FONT, "-pointsize", "52", "-fill", INK]
    for i, ch in enumerate(chars):
        x = pad + (i % cols) * cell + 14
        y = pad + (i // cols) * cell + 64
        a += ["-annotate", f"+{x}+{y}", ch]
    convert(*a, os.path.join(OUT, "glyphs.png"))


if __name__ == "__main__":
    for f in (specimen, alphabets, english, ukrainian, russian, glyph_sheet):
        f()
        print("rendered", f.__name__)
