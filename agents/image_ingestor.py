"""Watches assets/input_images/ for new image files and emits IMAGE_INGESTED events."""
import pathlib, time
from bus.events import emit_event

INPUT_DIR = pathlib.Path("assets/input_images")

def run_poll_loop(interval_sec: int = 60):
    seen: set[str] = set()
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    while True:
        for p in INPUT_DIR.iterdir():
            if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                if p.name not in seen:
                    seen.add(p.name)
                    emit_event(
                        domain="image",
                        kind="IMAGE_INGESTED",
                        payload={"image_path": str(p), "filename": p.name},
                        meta={"source_agent": "ImageIngestor"}
                    )
        time.sleep(interval_sec)