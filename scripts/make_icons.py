"""Generate a full-bleed Mario-style tools icon (no rounded white pad)."""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]

# Palette aligned with the homepage / Mario tools look
SKY = (229, 37, 33)
SKY_D = (200, 28, 24)
CLOUD = (252, 252, 252)
CLOUD_S = (126, 200, 255)
GRASS = (0, 184, 0)
GRASS_D = (0, 136, 0)
DIRT = (160, 90, 40)
DIRT_H = (196, 138, 72)
DIRT_D = (107, 58, 20)
BUSH = (0, 168, 0)
BUSH_D = (0, 112, 0)
PIPE = (0, 168, 0)
PIPE_H = (60, 220, 60)
PIPE_D = (0, 112, 0)
INK = (0, 0, 0)
METAL = (216, 216, 216)
METAL_H = (244, 244, 244)
METAL_D = (120, 120, 120)
WOOD = (176, 106, 40)
WOOD_D = (120, 70, 24)
HAMMER = (80, 80, 80)
HAMMER_H = (140, 140, 140)

SIZE = 64  # logical pixels; upscale with NEAREST


def px(draw: ImageDraw.ImageDraw, x: int, y: int, c: tuple[int, int, int]) -> None:
    draw.point((x, y), fill=c)


def rect(draw: ImageDraw.ImageDraw, x0, y0, x1, y1, c) -> None:
    draw.rectangle((x0, y0, x1, y1), fill=c)


def main() -> None:
    img = Image.new("RGB", (SIZE, SIZE), SKY)
    d = ImageDraw.Draw(img)

    # Sky dither bands
    for y in range(0, 40):
        for x in range(SIZE):
            c = SKY_D if ((x // 2 + y // 2) % 5 == 0) else SKY
            px(d, x, y, c)

    # Clouds
    def cloud(cx: int, cy: int) -> None:
        body = [
            (1, 0), (2, 0), (3, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
            (1, 3), (2, 3), (3, 3), (4, 3),
        ]
        shade = {(1, 3), (2, 3), (3, 3), (2, 2), (3, 2)}
        for dx, dy in body:
            px(d, cx + dx, cy + dy, CLOUD_S if (dx, dy) in shade else CLOUD)

    cloud(4, 4)
    cloud(48, 7)

    # Dirt + grass
    for y in range(44, SIZE):
        for x in range(SIZE):
            tile = ((x // 4) + (y // 4)) % 3
            c = (DIRT_H, DIRT, DIRT_D)[tile]
            if x % 4 == 3 or y % 4 == 3:
                c = INK
            px(d, x, y, c)

    # Jagged grass top
    for x in range(SIZE):
        tip = 42 + (x % 4 == 0)
        for y in range(tip, 46):
            px(d, x, y, GRASS_D if y == tip else GRASS)

    # Bush with eyes (left)
    bush = [
        "  ##  ",
        " #### ",
        "######",
        " ## ##",
        "######",
    ]
    bx, by = 6, 37
    for j, row in enumerate(bush):
        for i, ch in enumerate(row):
            if ch == "#":
                c = INK if j == 3 and i in (2, 4) else (BUSH_D if j >= 4 else BUSH)
                px(d, bx + i, by + j, c)

    # Pipe (right)
    px0, py0 = 48, 30
    rect(d, px0 - 1, py0, px0 + 8, py0 + 3, INK)
    rect(d, px0, py0 + 1, px0 + 7, py0 + 2, PIPE)
    px(d, px0, py0 + 1, PIPE_H)
    px(d, px0 + 7, py0 + 1, PIPE_D)
    rect(d, px0, py0 + 3, px0 + 7, 45, PIPE)
    for y in range(py0 + 3, 46):
        px(d, px0, y, PIPE_H)
        px(d, px0 + 7, y, PIPE_D)
        px(d, px0 - 1, y, INK)
        px(d, px0 + 8, y, INK)

    # Crossed tools: silver wrench \
    def thick_diag(x0, y0, steps, colors, step=(1, 1), width=3) -> None:
        for i in range(steps):
            x = x0 + i * step[0]
            y = y0 + i * step[1]
            for woff in range(width):
                xx = x + (woff - width // 2) * (-step[1])
                yy = y + (woff - width // 2) * step[0]
                if 0 <= xx < SIZE and 0 <= yy < SIZE:
                    px(d, xx, yy, colors[min(woff, len(colors) - 1)])

    # Wrench shaft
    thick_diag(18, 14, 22, [INK, METAL_H, METAL, METAL_D, INK], step=(1, 1), width=5)
    # Wrench jaw
    rect(d, 14, 12, 22, 16, METAL)
    rect(d, 14, 12, 17, 20, METAL)
    rect(d, 16, 14, 19, 17, SKY)  # jaw opening shows sky
    for x in range(14, 23):
        px(d, x, 12, INK)
    for y in range(12, 21):
        px(d, 14, y, INK)

    # Hammer / (wood handle + dark head)
    thick_diag(42, 13, 20, [INK, WOOD, WOOD, WOOD_D, INK], step=(-1, 1), width=4)
    # Head
    rect(d, 38, 11, 47, 16, HAMMER)
    rect(d, 39, 12, 46, 15, HAMMER_H)
    for x in range(38, 48):
        px(d, x, 11, INK)
        px(d, x, 16, INK)
    for y in range(11, 17):
        px(d, 38, y, INK)
        px(d, 47, y, INK)

    # Save crisp source + exports (full bleed square, no rounded pad)
    img.save(ROOT / "icon-source-64.png", format="PNG")
    big = img.resize((1024, 1024), Image.Resampling.NEAREST)
    big.save(ROOT / "icon-source.png", format="PNG")

    for name, out_size in {
        "favicon.png": 32,
        "apple-touch-icon.png": 180,
        "icon-192.png": 192,
        "icon-512.png": 512,
    }.items():
        img.resize((out_size, out_size), Image.Resampling.NEAREST).save(
            ROOT / name, format="PNG"
        )
        print("wrote", name)


if __name__ == "__main__":
    main()
