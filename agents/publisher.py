"""Publisher — moves approved rendered memes to drafts/, optionally posts to X."""
import os, pathlib, shutil
from bus.events import subscribe, emit_event, Event

DRAFTS_DIR = pathlib.Path("assets/drafts")
AUTO_POST = os.environ.get("MEME_AUTO_POST", "false").lower() == "true"

def handle_event(ev: Event):
    if ev.domain == "meme" and ev.kind == "MEME_RENDERED":
        out_path = ev.payload.get("output_path", "")
        if out_path.startswith("RENDER_FAILED"):
            return

        # Always save to drafts
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
        draft_path = DRAFTS_DIR / pathlib.Path(out_path).name
        shutil.copy2(out_path, draft_path)

        if AUTO_POST:
            _post_to_twitter(ev.payload["caption"], str(draft_path))
        else:
            emit_event(
                domain="publish",
                kind="MEME_DRAFT_SAVED",
                payload={**ev.payload, "draft_path": str(draft_path)},
                meta={"source_agent": "Publisher"}
            )

def _post_to_twitter(caption: str, image_path: str):
    """Post meme to Twitter via Composio TWITTER_CREATION_OF_A_POST."""
    # Wired via external agent call — see scripts/post_meme.py
    emit_event(
        domain="publish",
        kind="MEME_QUEUED_FOR_POST",
        payload={"caption": caption, "image_path": image_path},
        meta={"source_agent": "Publisher"}
    )

def start():
    subscribe(handle_event)