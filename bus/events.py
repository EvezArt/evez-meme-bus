from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Callable
import uuid, json, pathlib

@dataclass
class Event:
    id: str
    ts: str
    domain: str
    kind: str
    payload: Dict[str, Any]
    meta: Dict[str, Any]

EVENT_LOG_PATH = pathlib.Path("src/memory/meme_events.jsonl")
EVENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

_subscribers: List[Callable[[Event], None]] = []

def emit_event(domain: str, kind: str, payload: Dict[str, Any], meta: Dict[str, Any] | None = None) -> Event:
    ev = Event(
        id=str(uuid.uuid4()),
        ts=datetime.utcnow().isoformat() + "Z",
        domain=domain,
        kind=kind,
        payload=payload,
        meta=meta or {}
    )
    with EVENT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev.__dict__) + "\n")
    for sub in list(_subscribers):
        sub(ev)
    return ev

def subscribe(handler: Callable[[Event], None]) -> None:
    _subscribers.append(handler)