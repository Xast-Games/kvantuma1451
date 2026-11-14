"""Build TTF / OTF / WOFF2 from sources/KVANTUMA1451.sfd.

Usage:  fontforge -lang=py -script scripts/build.py
"""
import os
import fontforge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFD = os.path.join(ROOT, "sources", "KVANTUMA1451.sfd")

font = fontforge.open(SFD)
for fmt in ("ttf", "otf", "woff2"):
    out = os.path.join(ROOT, "fonts", fmt, "KVANTUMA1451." + fmt)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    try:
        font.generate(out)
        print("wrote", os.path.relpath(out, ROOT))
    except Exception as e:  # e.g. FontForge built without WOFF2
        print("skipped", fmt, "-", e)
