"""Create the repository's deterministic 1280x640 social-preview image."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "social-preview.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def rounded_box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, outline: str) -> None:
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=2)


def main() -> None:
    image = Image.new("RGB", (1280, 640), "#07111f")
    draw = ImageDraw.Draw(image)

    # Subtle layered background, kept high-contrast for small social cards.
    draw.ellipse((860, -240, 1450, 350), fill="#0d3542")
    draw.ellipse((970, 250, 1450, 730), fill="#132949")
    draw.line((70, 80, 70, 560), fill="#2dd4bf", width=8)

    draw.text((112, 82), "AGENT RECOVERY", font=font(27, True), fill="#5eead4")
    draw.text((108, 142), "RECOVERY.yaml", font=font(68, True), fill="#f8fafc")
    draw.text((112, 240), "Verify state before retrying.", font=font(36), fill="#cbd5e1")
    draw.text(
        (112, 294),
        "A deterministic recovery statechart for side-effecting AI agents.",
        font=font(23),
        fill="#94a3b8",
    )

    y1, y2 = 405, 477
    boxes = [
        ((112, y1, 284, y2), "VERIFY"),
        ((342, y1, 526, y2), "CONTAIN"),
        ((584, y1, 802, y2), "COMPENSATE"),
        ((860, y1, 1034, y2), "RESUME"),
    ]
    for index, (coords, label) in enumerate(boxes):
        rounded_box(draw, coords, "#101f33", "#2dd4bf")
        bbox = draw.textbbox((0, 0), label, font=font(20, True))
        text_width = bbox[2] - bbox[0]
        draw.text(((coords[0] + coords[2] - text_width) / 2, 430), label, font=font(20, True), fill="#e2e8f0")
        if index < len(boxes) - 1:
            start = coords[2] + 12
            end = boxes[index + 1][0][0] - 12
            draw.line((start, 441, end, 441), fill="#5eead4", width=3)
            draw.polygon([(end, 441), (end - 10, 435), (end - 10, 447)], fill="#5eead4")

    draw.text((112, 535), "github.com/HadjievK/AgentRecovery", font=font(22, True), fill="#f8fafc")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
