"""FastAPI control surface — /healthz, /readyz, /queue-status, /audit."""
from fastapi import FastAPI
from bus.storage import count_by_kind
import pathlib

app = FastAPI(title="evez-meme-bus", version="0.1.0")

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/readyz")
def ready():
    log = pathlib.Path("src/memory/meme_events.jsonl")
    return {"ready": True, "event_log_exists": log.exists()}

@app.get("/queue-status")
def queue_status():
    counts = count_by_kind()
    return {
        "candidates": counts.get("MEME_CANDIDATE", 0),
        "approved": counts.get("MEME_APPROVED", 0),
        "rejected": counts.get("MEME_REJECTED", 0),
        "rendered": counts.get("MEME_RENDERED", 0),
        "published": counts.get("MEME_PUBLISHED", 0),
        "drafts_saved": counts.get("MEME_DRAFT_SAVED", 0),
        "all": counts,
    }

@app.get("/audit")
def audit():
    from bus.storage import replay_events
    return {"events": list(replay_events())[-50:]}