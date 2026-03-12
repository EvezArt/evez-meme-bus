#!/usr/bin/env python3
"""
ably_publisher.py — Publish meme bus events to Ably evez-ops channel.

On every new meme event: publish to Ably `evez-ops`.
Payload: {event_id, meme_hash, guard_verdict, timestamp}
"""

import os
import json
import hashlib
from datetime import datetime, timezone

try:
    from ably import AblyRest
    HAS_ABLY = True
except ImportError:
    HAS_ABLY = False
    print("[ABLY] ably-python not installed. pip install ably")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def publish_event(event_id: str, meme_hash: str, guard_verdict: str,
                 extra: dict = None) -> bool:
    """
    Publish a meme bus event to Ably evez-ops channel.
    Returns True on success, False on failure.
    """
    api_key = os.environ.get("ABLY_API_KEY")
    if not api_key:
        print("[ABLY] ABLY_API_KEY not set — skipping publish")
        return False
    if not HAS_ABLY:
        print("[ABLY] ably library not available")
        return False

    payload = {
        "event_id": event_id,
        "meme_hash": meme_hash,
        "guard_verdict": guard_verdict,
        "source": "evez-meme-bus",
        "timestamp": _now(),
        **(extra or {})
    }

    try:
        client = AblyRest(api_key)
        channel = client.channels.get("evez-ops")
        channel.publish("meme_event", payload)
        print(f"[ABLY] Published {event_id[:8]} | verdict={guard_verdict}")
        return True
    except Exception as e:
        print(f"[ABLY] Publish failed: {e}")
        return False


if __name__ == "__main__":
    publish_event(
        event_id="test_" + hashlib.sha256(b"test").hexdigest()[:8],
        meme_hash="abc123",
        guard_verdict="PASS",
        extra={"test": True}
    )
