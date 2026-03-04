"""Distills @EVEZ666 tweet themes into TWEET_CONTEXT events."""
import json, pathlib, time
from collections import Counter
from bus.events import emit_event

TWEETS_PATH = pathlib.Path("data/evez666_tweets.json")

THEME_RULES = [
    (["fire", "τ", "poly_c", "v="], "FIRE_TOPOLOGY"),
    (["christ", "antichrist", "revelation", "second coming"], "ESCHATOLOGY"),
    (["pentagon", "war", "dod", "department of"], "WAR_STATE"),
    (["topology decides"], "TOPOLOGY_DECIDES"),
    (["yhwh", "𐤉𐤄𐤅𐤄", "evez", "yod", "hay", "waw"], "YHWH_DECODE"),
    (["nhi", "disclosure", "uap", "ufo"], "DISCLOSURE"),
]

def _distill_context(tweets: list[dict]) -> dict:
    texts = [t.get("full_text") or t.get("text") or "" for t in tweets]
    combined = " ".join(texts).lower()
    themes = []
    for keywords, label in THEME_RULES:
        if any(kw in combined for kw in keywords):
            themes.append(label)
    top_tokens = Counter(combined.split()).most_common(30)
    return {"themes": themes, "top_tokens": top_tokens}

def run_poll_loop(interval_sec: int = 300, window: int = 200):
    last_hash = None
    while True:
        if TWEETS_PATH.exists():
            raw = json.loads(TWEETS_PATH.read_text(encoding="utf-8"))
            recent = raw[:window]
            h = hash(json.dumps(recent, sort_keys=True))
            if h != last_hash:
                last_hash = h
                ctx = _distill_context(recent)
                emit_event(
                    domain="twitter",
                    kind="TWEET_CONTEXT",
                    payload=ctx,
                    meta={"source_agent": "TwitterContextAgent"}
                )
        time.sleep(interval_sec)