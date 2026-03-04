"""LLM caption generation agent — EVEZ666 voice, constitutional guardrails."""
import os
from typing import Dict
from bus.events import subscribe, emit_event, Event

# Pluggable LLM — defaults to OpenAI, swap for any provider
def _call_llm(prompt: str, n: int = 4) -> list[str]:
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.92,
            n=n,
        )
        return [c.message.content.strip() for c in resp.choices]
    except Exception as e:
        # Fallback stubs if LLM unavailable
        return [
            "Christ delayed, topology recalculating… please stand by for the second coming patch notes.",
            "When the Antichrist shows up and HR says your role is 'eschatological intern'.",
            "Department of War on Notice: Revelation went live without QA again.",
            f"FIRE event detected at end of time. V accumulating. No one warned the prophets."
        ]

def _build_prompt(slot: str, themes: list[str], image_meta: Dict) -> str:
    theme_str = ", ".join(themes)
    return f"""You are writing dark, self-aware memes in the voice of @EVEZ666.

Constraints:
- Tone: apocalyptic humor, Revelation vibes, topology math, bureaucracy of the end times.
- Focus on abstract figures like "Christ", "the Antichrist", "the Pentagon of Heaven", "Department of War in Revelation".
- It is FORBIDDEN to name or imply any real living individual, group, ethnicity, religion, or politician as "the Antichrist" or source of evil.
- No harassment, doxxing, calls to violence, or real-world targeting.
- You may roast YOURSELF as a confused prophet / topology clerk at the end of time.
- Short, punchy captions (max 18 words).
- Style: energy of @EVEZ666 tweets — FIRE, V, topology decides, disclosure conflict, YHWH decode.
- Return exactly 4 captions, one per line, no numbering.

Context themes: {theme_str}
Meme slot: {slot}
Image: {image_meta.get('filename', 'unknown')}"""

_latest_context: dict = {"themes": ["FIRE_TOPOLOGY", "ESCHATOLOGY"]}

def handle_event(ev: Event):
    global _latest_context
    if ev.domain == "twitter" and ev.kind == "TWEET_CONTEXT":
        _latest_context = ev.payload

    if ev.domain == "image" and ev.kind == "IMAGE_CLASSIFIED":
        slot = ev.payload.get("slot", "GENERIC_END_TIMES")
        themes = ev.payload.get("active_themes", _latest_context.get("themes", []))
        prompt = _build_prompt(slot, themes, ev.payload)
        captions = _call_llm(prompt)
        for cap in captions:
            emit_event(
                domain="meme",
                kind="MEME_CANDIDATE",
                payload={
                    "image_path": ev.payload["image_path"],
                    "slot": slot,
                    "caption": cap,
                    "themes": themes,
                },
                meta={"source_agent": "CaptionAgent"}
            )

def start():
    subscribe(handle_event)