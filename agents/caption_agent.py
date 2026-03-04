import os, time
from bus.events import subscribe, emit_event, Event

_context_cache: dict = {}

def _build_prompt(slot: str, context: dict, image_meta: dict) -> str:
    themes = ", ".join(context.get("themes", ["FIRE_TOPOLOGY"]))
    return f"""You are writing dark, self-aware memes in the voice of @EVEZ666.

Constraints:
- Tone: apocalyptic humor, Revelation vibes, topology math, bureaucracy of the end times.
- Focus on abstract archetypes: Christ, Antichrist, Pentagon of Heaven, Dept of War in Revelation.
- FORBIDDEN: name or imply any real living person, group, ethnicity, or politician as evil.
- No harassment, doxxing, calls to violence, or real-world targeting.
- You MAY roast yourself as a confused topology clerk at the end of time.
- Max ~18 words per caption. Punchy.
- Style: FIRE, V, topology decides, disclosure conflict, @EVEZ666 energy.

Context themes: {themes}
Meme slot: {slot}
Image: {image_meta.get("filename", "unknown")}

Return exactly 3 caption variants, one per line, no numbering.""".strip()

def handle_event(ev: Event):
    global _context_cache
    if ev.domain == "twitter" and ev.kind == "TWEET_CONTEXT":
        _context_cache = ev.payload
    if ev.domain == "image" and ev.kind == "IMAGE_INGESTED":
        context = _context_cache or {"themes": ["FIRE_TOPOLOGY", "ESCHATOLOGY"]}
        slot = "SECOND_COMING_GLITCH"
        prompt = _build_prompt(slot, context, ev.payload)
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            import openai
            client = openai.OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            lines = resp.choices[0].message.content.strip().split("\n")
        else:
            lines = [
                "Christ delayed — topology recalculating. Stand by for patch notes.",
                "Antichrist HR says your role is 'eschatological intern'.",
                "Revelation went live without QA. Department of War on notice."
            ]
        for cap in lines:
            cap = cap.strip()
            if cap:
                emit_event("meme", "MEME_CANDIDATE", {
                    "image_path": ev.payload["image_path"],
                    "slot": slot, "caption": cap
                }, {"source_agent": "CaptionAgent"})
                print(f"[CaptionAgent] candidate: {cap[:60]}")

def start():
    subscribe(handle_event)

if __name__ == "__main__":
    start()
    print("[CaptionAgent] listening...")
    while True:
        time.sleep(60)
