"""APScheduler-based loop orchestrator — boots all agent poll loops."""
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import agents.image_ingestor as image_ingestor
import agents.twitter_context as twitter_context
import agents.corpus_agent as corpus_agent
import agents.theme_classifier as theme_classifier
import agents.caption_agent as caption_agent
import agents.layout_agent as layout_agent
import agents.guard_agent as guard_agent
import agents.publisher as publisher

def start_all():
    """Subscribe all agents and boot scheduler."""
    theme_classifier.start()
    caption_agent.start()
    layout_agent.start()
    guard_agent.start()
    publisher.start()

    # Run polling loops in background threads
    threading.Thread(target=image_ingestor.run_poll_loop, daemon=True).start()
    threading.Thread(target=twitter_context.run_poll_loop, daemon=True).start()
    threading.Thread(target=corpus_agent.run_poll_loop, daemon=True).start()

    print("[meme-bus] all agents booted")