#!/usr/bin/env python3
"""
health.py — Health and metrics endpoint for evez-meme-bus.

Exposes:
  GET /health  -> {status, event_count, last_event_id, uptime}
  GET /events  -> last 20 events
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import time

SPINE_FILE = Path("src/memory/meme_events.jsonl")
START_TIME = time.time()


def get_health() -> dict:
    event_count = 0
    last_event_id = None
    last_hash = None

    if SPINE_FILE.exists():
        lines = [l for l in SPINE_FILE.read_text().strip().splitlines() if l]
        event_count = len(lines)
        if lines:
            last = json.loads(lines[-1])
            last_event_id = last.get("event_id")
            last_hash = last.get("hash", "")[:16]

    return {
        "status": "ok",
        "event_count": event_count,
        "last_event_id": last_event_id,
        "last_hash": last_hash,
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


def get_recent_events(n: int = 20) -> list:
    if not SPINE_FILE.exists():
        return []
    lines = [l for l in SPINE_FILE.read_text().strip().splitlines() if l]
    return [json.loads(l) for l in lines[-n:]]


if __name__ == "__main__":
    import sys
    if "events" in sys.argv:
        for e in get_recent_events():
            print(json.dumps(e))
    else:
        print(json.dumps(get_health(), indent=2))
