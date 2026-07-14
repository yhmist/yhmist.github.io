"""Bake character bitmaps into js/glyphs.js for DOM pixel text."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_LATIN = ROOT / "fonts" / "fusion-pixel-12px-proportional-latin.ttf"
FONT_HANS = ROOT / "fonts" / "fusion-pixel-12px-proportional-zh_hans.ttf"
OUT = ROOT / "js" / "glyphs.js"

TEXTS = [
    "1-1",
    "yhmist",
    "INVEST",
    "ENGLISH",
    "GO",
    "Russell 1000 月度动量选股 · 信号与回测跟踪",
    "英语对话跟读 · 点句跳转、点词查释义",
]

SIZE = 12
# Keep room for descenders while aligning Latin capitals near the top.
BASELINE = 10


def is_cjk(ch: str) -> bool:
    code = ord(ch)
    return (
        0x4E00 <= code <= 0x9FFF
        or 0x3400 <= code <= 0x4DBF
        or 0x3000 <= code <= 0x303F
        or 0xFF00 <= code <= 0xFFEF
    )


def mask_to_image(ch: str, font: ImageFont.FreeTypeFont) -> Image.Image | None:
    mask = font.getmask(ch, mode="1")
    w, h = mask.size
    if w <= 0 or h <= 0:
        return None
    im = Image.new("1", (w, h))
    im.putdata(list(mask))
    return im.convert("L")


def rasterize(ch: str, font: ImageFont.FreeTypeFont) -> list[str]:
    if ch == " ":
        return ["0" * 6 for _ in range(SIZE)]

    glyph = mask_to_image(ch, font)
    if glyph is None:
        return ["0" * 4 for _ in range(SIZE)]

    w, h = glyph.size
    canvas = Image.new("L", (max(w, 1), SIZE), 0)

    if is_cjk(ch) or ch in "·、":
        top = max(0, (SIZE - h) // 2)
    else:
        top = BASELINE - h
        if top < 0:
            top = 0
        if top + h > SIZE:
            top = SIZE - h

    canvas.paste(glyph, (0, top))

    rows = []
    for y in range(SIZE):
        bits = []
        for x in range(w):
            bits.append("1" if canvas.getpixel((x, y)) > 0 else "0")
        rows.append("".join(bits))
    return rows


def main() -> None:
    latin = ImageFont.truetype(str(FONT_LATIN), SIZE)
    hans = ImageFont.truetype(str(FONT_HANS), SIZE)

    chars: list[str] = []
    seen: set[str] = set()
    for text in TEXTS:
        for ch in text:
            if ch not in seen:
                seen.add(ch)
                chars.append(ch)

    glyphs: dict[str, list[str]] = {}
    for ch in chars:
        font = hans if (is_cjk(ch) or ch in "·、") else latin
        glyphs[ch] = rasterize(ch, font)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {"cell": SIZE, "glyphs": glyphs}
    OUT.write_text(
        "window.PX_FONT = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT} ({len(glyphs)} glyphs)")
    for sample in ("y", "h", "I", "选", "GO"[0]):
        g = glyphs.get(sample)
        if not g:
            continue
        print("===", sample)
        for row in g:
            print(row.replace("0", ".").replace("1", "#"))


if __name__ == "__main__":
    main()
