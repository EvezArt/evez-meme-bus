#!/usr/bin/env bash
# deploy-all.sh — EVEZ Meme Bus full stack deploy + start
set -euo pipefail

echo "▶ [DEPLOY] EVEZ Meme Bus"

mkdir -p src/memory assets/input_images assets/corpus_templates assets/output_memes data logs bus agents service loops scripts

pip install --quiet fastapi "uvicorn[standard]" pillow apscheduler openai python-multipart python-dotenv

echo "▶ Starting agents..."
python3 -m agents.image_ingestor  >> logs/image_ingestor.log  2>&1 & echo $! > logs/image_ingestor.pid
python3 -m agents.twitter_context >> logs/twitter_context.log 2>&1 & echo $! > logs/twitter_context.pid
python3 -m agents.corpus_agent    >> logs/corpus_agent.log    2>&1 & echo $! > logs/corpus_agent.pid
python3 -m agents.caption_agent   >> logs/caption_agent.log   2>&1 & echo $! > logs/caption_agent.pid
python3 -m agents.guard_agent     >> logs/guard_agent.log     2>&1 & echo $! > logs/guard_agent.pid
python3 -m agents.layout_agent    >> logs/layout_agent.log    2>&1 & echo $! > logs/layout_agent.pid
python3 -m agents.publisher       >> logs/publisher.log       2>&1 & echo $! > logs/publisher.pid

echo "▶ Starting FastAPI on :8000..."
uvicorn service.api:app --host 0.0.0.0 --port 8000 --reload >> logs/api.log 2>&1 &
echo $! > logs/api.pid

echo "✅ All services running."
echo "   API   → http://localhost:8000/healthz"
echo "   Queue → http://localhost:8000/queue-status"
echo "   Tail  → http://localhost:8000/tail"
echo "   Drop images into assets/input_images/ to trigger the pipeline."
