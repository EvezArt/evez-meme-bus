import pathlib, time, textwrap
from bus.events import subscribe, emit_event, Event

OUT = pathlib.Path("assets/output_memes")

def _render(image_path: str, caption: str, slot: str) -> str:
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        w, h = img.size
        font_size = max(20, w // 25)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
        wrapped = "\n".join(textwrap.wrap(caption, width=40))
        draw.rectangle([0, h - font_size * 3, w, h], fill=(0, 0, 0, 180))
        draw.text((10, h - font_size * 3 + 4), wrapped, font=font, fill=(255, 255, 255, 255))
        OUT.mkdir(parents=True, exist_ok=True)
        stem = pathlib.Path(image_path).stem
        out_path = OUT / f"{stem}_{slot}.png"
        img.save(out_path)
        return str(out_path)
    except Exception as e:
        print(f"[LayoutAgent] render error: {e}")
        return ""

def handle_event(ev: Event):
    if ev.domain == "ethics" and ev.kind == "MEME_APPROVED":
        image_path = ev.payload.get("image_path", "")
        caption = ev.payload.get("caption", "")
        slot = ev.payload.get("slot", "unknown")
        out = _render(image_path, caption, slot)
        if out:
            emit_event("meme", "MEME_RENDERED",
                {"output_path": out, "caption": caption, "slot": slot},
                {"source_agent": "LayoutAgent"})
            print(f"[LayoutAgent] rendered {out}")

def start():
    subscribe(handle_event)

if __name__ == "__main__":
    start()
    print("[LayoutAgent] ready...")
    while True:
        time.sleep(60)
