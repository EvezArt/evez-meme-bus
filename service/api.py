from fastapi import FastAPI
from bus.events import EVENT_LOG_PATH
import json, pathlib

app = FastAPI(title="EVEZ Meme Bus", version="1.0.0")

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/readyz")
def ready():
    return {"status": "ready", "log": str(EVENT_LOG_PATH)}

@app.get("/queue-status")
def queue_status():
    if not EVENT_LOG_PATH.exists():
        return {"total": 0, "by_kind": {}}
    events = [json.loads(l) for l in EVENT_LOG_PATH.read_text().splitlines() if l.strip()]
    counts: dict = {}
    for ev in events:
        k = ev.get("kind", "?")
        counts[k] = counts.get(k, 0) + 1
    return {"total": len(events), "by_kind": counts}

@app.get("/tail")
def tail_log(n: int = 20):
    if not EVENT_LOG_PATH.exists():
        return {"events": []}
    lines = EVENT_LOG_PATH.read_text().splitlines()
    return {"events": [json.loads(l) for l in lines[-n:] if l.strip()]}

@app.get("/drafts")
def list_drafts():
    out = pathlib.Path("assets/output_memes")
    if not out.exists():
        return {"drafts": []}
    return {"drafts": [f.name for f in out.iterdir() if f.is_file()]}
