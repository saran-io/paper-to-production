from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path("/Users/sayora/dev/labs/paper-to-production")
ASSETS = ROOT / "content/01-faithfulness/assets"
OUTDIR = ASSETS / "linkedin-carousel-v2"

SIZE = 1080
BG = "#f8f3e9"
GRID = "#e2dccf"
INK = "#161616"
BLUE = "#2f63e0"
RED = "#d84c3f"
PANEL = "#fffdfa"
PANEL_STROKE = "#d9d1c3"
MUTED = "#4f4a42"


TITLE_FONT = "/System/Library/Fonts/SFCompact.ttf"
BODY_FONT = "/System/Library/Fonts/SFNS.ttf"
ROUND_FONT = "/System/Library/Fonts/SFNSRounded.ttf"


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    for x in range(0, SIZE + 1, 90):
        draw.line((x, 0, x, SIZE), fill=GRID, width=1)
    for y in range(0, SIZE + 1, 90):
        draw.line((0, y, SIZE, y), fill=GRID, width=1)


def add_shadow(base: Image.Image, box: tuple[int, int, int, int], radius: int = 20) -> None:
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    x0, y0, x1, y1 = box
    sdraw.rounded_rectangle((x0 + 14, y0 + 16, x1 + 14, y1 + 16), 34, fill=(0, 0, 0, 28))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=radius))
    base.alpha_composite(shadow)


def fit_cover(path: Path, box: tuple[int, int], crop_anchor: str = "center") -> Image.Image:
    img = Image.open(path).convert("RGB")
    centering = {
        "center": (0.5, 0.5),
        "top": (0.5, 0.1),
        "bottom": (0.5, 0.9),
        "left": (0.1, 0.5),
        "right": (0.9, 0.5),
    }.get(crop_anchor, (0.5, 0.5))
    return ImageOps.fit(img, box, method=Image.Resampling.LANCZOS, centering=centering)


def fit_contain(path: Path, box: tuple[int, int]) -> Image.Image:
    img = Image.open(path).convert("RGB")
    img.thumbnail(box, Image.Resampling.LANCZOS)
    return img


def wrap_text(text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    dummy = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if dummy.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_brand(draw: ImageDraw.ImageDraw) -> None:
    draw.ellipse((56, 982, 82, 1008), outline=BLUE, width=3)
    brand_font = load_font(BODY_FONT, 24)
    tag_font = load_font(BODY_FONT, 21)
    draw.text((96, 978), "saran.build", fill=INK, font=brand_font)
    draw.text((96, 1008), "paper-to-production", fill=BLUE, font=tag_font)


def draw_kicker(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, color: str = RED) -> None:
    font = load_font(ROUND_FONT, 20)
    w = int(draw.textlength(text, font=font)) + 30
    draw.rounded_rectangle((x, y, x + w, y + 36), radius=18, outline=color, width=2, fill=(255, 255, 255))
    draw.text((x + 15, y + 8), text, fill=color, font=font)


def draw_text_block(
    draw: ImageDraw.ImageDraw,
    title: str,
    subtitle: str | None,
    body_lines: list[str],
    x: int,
    y: int,
    width: int,
    title_size: int = 72,
    body_size: int = 34,
) -> int:
    title_font = load_font(TITLE_FONT, title_size)
    subtitle_font = load_font(BODY_FONT, 32)
    body_font = load_font(BODY_FONT, body_size)

    draw.text((x, y), title, fill=INK, font=title_font)
    current_y = y + title_size + 14

    if subtitle:
        sub_lines = wrap_text(subtitle, subtitle_font, width)
        for line in sub_lines:
            draw.text((x, current_y), line, fill=BLUE, font=subtitle_font)
            current_y += 38
        current_y += 8

    for raw_line in body_lines:
        if not raw_line:
            current_y += 18
            continue
        wrapped = wrap_text(raw_line, body_font, width)
        for line in wrapped:
            draw.text((x, current_y), line, fill=MUTED if body_size <= 30 else INK, font=body_font)
            current_y += body_size + 10
    return current_y


def panel(base: Image.Image, box: tuple[int, int, int, int]) -> None:
    add_shadow(base, box)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=34, fill=PANEL, outline=PANEL_STROKE, width=2)


def paste_center(base: Image.Image, img: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    px = x0 + (x1 - x0 - img.width) // 2
    py = y0 + (y1 - y0 - img.height) // 2
    base.paste(img, (px, py))


def make_slide_1() -> Image.Image:
    base = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(base)
    draw_grid(draw)
    draw_kicker(draw, "SPRINT 01", 64, 62)
    draw_text_block(
        draw,
        "FAITHFULNESS",
        "How I turned papers into a real RAG evaluation system",
        [
            "Applied AI engineering,",
            "not paper cosplay.",
        ],
        64,
        120,
        250,
        title_size=58,
        body_size=25,
    )
    draw.text((64, 336), "real problem -> method -> audit", fill=BLUE, font=load_font(BODY_FONT, 20))

    box = (472, 74, 1008, 934)
    panel(base, box)
    poster = fit_cover(ASSETS / "faithfulness-concept-poster-v1.png", (box[2] - box[0] - 42, box[3] - box[1] - 42), "center")
    paste_center(base, poster, box)
    draw_brand(ImageDraw.Draw(base))
    return base


def make_slide_2() -> Image.Image:
    base = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(base)
    draw_grid(draw)
    draw_kicker(draw, "THE PROBLEM", 64, 62)
    draw_text_block(
        draw,
        "THE REAL PROBLEM",
        None,
        [
            "A RAG answer can sound fluent and still invent a price, feature, or merged fact.",
            "",
            "are the claims actually supported by retrieved context?",
        ],
        64,
        120,
        900,
        title_size=68,
        body_size=31,
    )

    draw.text((64, 338), "Faithfulness asks one question.", fill=BLUE, font=load_font(BODY_FONT, 24))
    box = (74, 400, 1006, 926)
    panel(base, box)
    asset = fit_cover(ASSETS / "faithfulness-for-humans-preview-v2.jpg", (box[2] - box[0] - 30, box[3] - box[1] - 30), "center")
    paste_center(base, asset, box)
    draw_brand(ImageDraw.Draw(base))
    return base


def make_slide_3() -> Image.Image:
    base = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(base)
    draw_grid(draw)
    draw_kicker(draw, "PROOF", 64, 62)
    draw_text_block(
        draw,
        "REAL FAILURE MODES",
        None,
        [
            "wrong price",
            "unsupported feature",
            "merged listings",
            "poor retrieval",
            "correct but unsupported",
        ],
        64,
        120,
        310,
        title_size=54,
        body_size=30,
    )
    draw.text((64, 384), "These are production failures, not benchmark trivia.", fill=BLUE, font=load_font(BODY_FONT, 24))

    box = (410, 150, 1008, 936)
    panel(base, box)
    asset = fit_contain(ASSETS / "failure-buckets-card.jpg", (box[2] - box[0] - 34, box[3] - box[1] - 34))
    paste_center(base, asset, box)
    draw_brand(ImageDraw.Draw(base))
    return base


def make_slide_4() -> Image.Image:
    base = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(base)
    draw_grid(draw)
    draw_kicker(draw, "CAUTION", 64, 62)
    draw_text_block(
        draw,
        "DON'T TRUST A CLEAN NUMBER",
        None,
        [
            "A clean seed-set result is not the same as a production-trustworthy metric.",
            "",
            "Current repo state: heuristic seed run only.",
        ],
        64,
        120,
        330,
        title_size=50,
        body_size=30,
    )

    draw.text((64, 394), "This is the credibility slide.", fill=BLUE, font=load_font(BODY_FONT, 22))
    box = (420, 154, 1008, 936)
    panel(base, box)
    asset = fit_contain(ASSETS / "metric-honesty-card.jpg", (box[2] - box[0] - 34, box[3] - box[1] - 34))
    paste_center(base, asset, box)
    draw_brand(ImageDraw.Draw(base))
    return base


def make_slide_5() -> Image.Image:
    base = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(base)
    draw_grid(draw)
    draw_kicker(draw, "TAKEAWAY", 64, 62)
    draw_text_block(
        draw,
        "WHAT THE PAPERS CHANGED",
        None,
        [
            "RAGAS -> evaluator loop",
            "FActScore -> atomic claims",
            "Reliability without Validity -> judge audit",
        ],
        64,
        120,
        330,
        title_size=50,
        body_size=30,
    )
    draw.text((64, 386), "Papers as inputs. System as output.", fill=BLUE, font=load_font(BODY_FONT, 24))

    box = (420, 154, 1008, 936)
    panel(base, box)
    asset = fit_contain(ASSETS / "paper-map-card.jpg", (box[2] - box[0] - 34, box[3] - box[1] - 34))
    paste_center(base, asset, box)
    draw.text((64, 910), "Full writeup in the first comment", fill=RED, font=load_font(BODY_FONT, 26))
    draw_brand(ImageDraw.Draw(base))
    return base


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    slides = [
        ("slide-01-hook.png", make_slide_1()),
        ("slide-02-problem.png", make_slide_2()),
        ("slide-03-failure-buckets.png", make_slide_3()),
        ("slide-04-metric-honesty.png", make_slide_4()),
        ("slide-05-paper-map.png", make_slide_5()),
    ]

    for name, image in slides:
        image.convert("RGB").save(OUTDIR / name, quality=95)

    preview = Image.new("RGB", (SIZE * 2, SIZE * 3), BG)
    positions = [
        (0, 0),
        (SIZE, 0),
        (0, SIZE),
        (SIZE, SIZE),
        (0, SIZE * 2),
    ]
    for (name, image), (x, y) in zip(slides, positions):
        preview.paste(image.convert("RGB"), (x, y))
    preview.save(OUTDIR / "carousel-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
