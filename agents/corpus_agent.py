"""Indexes approved war/end-times meme templates in assets/corpus_templates/."""
import pathlib, time
from bus.events import emit_event

CORPUS_DIR = pathlib.Path("assets/corpus_templates")

def run_poll_loop(interval_sec: int = 600):
    last_snapshot: set[str] = set()
    while True:
        CORPUS_DIR.mkdir(parents=True, exist_ok=True)
        files = {p.name for p in CORPUS_DIR.iterdir() if p.is_file()}
        if files != last_snapshot:
            last_snapshot = files
            emit_event(
                domain="corpus",
                kind="CORPUS_UPDATED",
                payload={"templates": list(files)},
                meta={"source_agent": "CorpusAgent"}
            )
        time.sleep(interval_sec)