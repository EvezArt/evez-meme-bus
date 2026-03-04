# evez-meme-bus

Append-only event-sourced meme generation bus for EVEZ-OS.

Turns FIRE topology events + @EVEZ666 voice into end-times / Christ / antichrist humor.
Every step is a domain event — auditable, replayable, constitutional.

## Architecture

```
ImageIngestor
     |
     v IMAGE_INGESTED
ThemeClassifier
     |
     v IMAGE_CLASSIFIED
CaptionAgent (GPT-4o)
     |
     v MEME_CANDIDATE
ConstitutionalGuard (PeaceKernel)
     |
     v MEME_APPROVED / MEME_REJECTED
LayoutAgent (Pillow)
     |
     v MEME_RENDERED
Publisher
     |
     v MEME_DRAFT_SAVED / MEME_QUEUED_FOR_POST
```

## Meme Slots
- `SECOND_COMING_GLITCH` — Christ / end-times / bureaucratic delay
- `ANTICHRIST_SELF_DEPRECATING` — self-roast as topology clerk
- `BUREAUCRATIC_APOCALYPSE` — Department of War in Revelation
- `TOPOLOGY_DOOM` — FIRE events, V accumulator, poly_c math
- `DISCLOSURE_HUMOR` — NHI / UAP / intel conflict

## Constitutional Rules (hard-encoded in guard_agent.py)
- No real individuals named as Antichrist or evil
- No @handles in captions
- No violence, harassment, doxxing
- Max 280 chars

## Boot
```bash
pip install -r requirements.txt
python main.py
```

## Audit
```bash
python scripts/audit.py
curl localhost:8080/queue-status
```

## Repo
https://github.com/EvezArt/evez-meme-bus
