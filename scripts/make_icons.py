"""Generate Mario-palette pixel tool icons for the homepage."""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]

SKY = (92, 148, 252)
INK = (26, 26, 26)
RED = (229, 37, 33)
RED_D = (156, 24, 21)
COIN = (251, 208, 0)
COIN_D = (227, 159, 0)
PANEL = (255, 248, 231)
PIPE = (0, 168, 0)
PIPE_D = (0, 124, 0)
WHITE = (255, 255, 255)

SIZE = 32


def thick_line(draw: ImageDraw.ImageDraw, p0, p1, fill, width: int) -> None:
    draw.line([p0, p1], fill=fill, width=width)


def main() -> None:
    img = Image.new("RGB", (SIZE, SIZE), SKY)
    d = ImageDraw.Draw(img)

    # Cream panel + black frame
    d.rectangle((2, 2, 29, 29), fill=PANEL, outline=INK)
    d.line((3, 4, 28, 4), fill=WHITE)

    # Green wrench: jaw + diagonal handle
    d.rectangle((5, 5, 11, 8), fill=PIPE, outline=INK)
    d.rectangle((5, 5, 8, 11), fill=PIPE, outline=INK)
    d.rectangle((7, 7, 9, 9), fill=PANEL)  # jaw opening
    thick_line(d, (9, 9), (20, 20), PIPE, 3)
    thick_line(d, (10, 10), (19, 19), PIPE_D, 1)
    d.rectangle((18, 18, 22, 21), fill=PIPE_D, outline=INK)

    # Gold screwdriver shaft + red handle
    thick_line(d, (23, 6), (12, 17), COIN, 3)
    thick_line(d, (22, 7), (13, 16), COIN_D, 1)
    d.rectangle((21, 4, 25, 7), fill=INK)  # tip
    d.rectangle((9, 17, 14, 22), fill=RED, outline=INK)
    d.line((10, 18, 13, 18), fill=RED_D)
    d.line((10, 20, 13, 20), fill=RED_D)

    # Question / coin block
    d.rectangle((22, 22, 27, 27), fill=COIN, outline=INK)
    d.point((24, 24), fill=WHITE)
    d.point((25, 25), fill=COIN_D)
    d.point((24, 26), fill=INK)

    img.save(ROOT / "icon-source-32.png", format="PNG")
    for name, out_size in {
        "favicon.png": 32,
        "apple-touch-icon.png": 180,
        "icon-192.png": 192,
        "icon-512.png": 512,
    }.items():
        img.resize((out_size, out_size), Image.NEAREST).save(ROOT / name, format="PNG")
        print("wrote", name)


if __name__ == "__main__":
    main()
