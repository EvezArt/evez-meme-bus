"""Composites captions onto images using Pillow. Emits MEME_RENDERED."""
import pathlib
from bus.events import subscribe, emit_event, Event

OUTPUT_DIR = pathlib.Path("assets/output_memes")

def _render(image_path: str, caption: str, slot: str) -> str:
    """Render caption onto image and return output path."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        W, H = img.size

        # Try to load a bold font, fall back to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=max(24, W // 25))
        except Exception:
            font = ImageFont.load_default()

        # Word-wrap caption
        words = caption.split()
        lines, line = [], ""
        for word in words:
            test = f"{line} {word}".strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] > W - 40:
                if line:
                    lines.append(line)
                line = word
            else:
                line = test
        if line:
            lines.append(line)

        # Draw bottom caption with black outline + white fill
        text_block = "\n".join(lines)
        bbox = draw.multiline_textbbox((0, 0), text_block, font=font)
        text_h = bbox[3] - bbox[1]
        y = H - text_h - 20
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            draw.multiline_text((20 + dx, y + dy), text_block, font=font, fill="black", align="center")
        draw.multiline_text((20, y), text_block, font=font, fill="white", align="center")

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        stem = pathlib.Path(image_path).stem
        out_path = OUTPUT_DIR / f"{stem}_{slot[:20]}.jpg"
        img.save(str(out_path), "JPEG", quality=92)
        return str(out_path)
    except Exception as e:
        return f"RENDER_FAILED:{e}"

def handle_event(ev: Event):
    if ev.domain == "ethics" and ev.kind == "MEME_APPROVED":
        out_path = _render(
            ev.payload["image_path"],
            ev.payload["caption"],
            ev.payload.get("slot", "MEME")
        )
        emit_event(
            domain="meme",
            kind="MEME_RENDERED",
            payload={**ev.payload, "output_path": out_path},
            meta={"source_agent": "LayoutAgent"}
        )

def start():
    subscribe(handle_event)