"""Constitutional guard — PeaceKernel + suppression-map enforcement."""
from bus.events import subscribe, emit_event, Event
import re

# Hard-banned terms — real-world targeting, hate, incitement
BANNED_TERMS = [
    "kill", "murder", "attack", "bomb", "shoot",
    "nazi", "kike", "nigger", "faggot",
    # Add more per your suppression map
]

# Real-name targeting guard — no @handles or proper-name accusations
HANDLE_PATTERN = re.compile(r'@[A-Za-z0-9_]+')

def violates_policy(caption: str) -> str | None:
    lower = caption.lower()
    for term in BANNED_TERMS:
        if term in lower:
            return f"banned_term:{term}"
    if HANDLE_PATTERN.search(caption):
        return "mentions_handle"
    # No captions > 280 chars (Twitter limit)
    if len(caption) > 280:
        return f"too_long:{len(caption)}"
    return None

def handle_event(ev: Event):
    if ev.domain == "meme" and ev.kind == "MEME_CANDIDATE":
        reason = violates_policy(ev.payload["caption"])
        if reason:
            emit_event(
                domain="ethics",
                kind="MEME_REJECTED",
                payload={"candidate": ev.payload, "reason": reason},
                meta={"source_agent": "ConstitutionalGuard"}
            )
        else:
            emit_event(
                domain="ethics",
                kind="MEME_APPROVED",
                payload=ev.payload,
                meta={"source_agent": "ConstitutionalGuard"}
            )

def start():
    subscribe(handle_event)