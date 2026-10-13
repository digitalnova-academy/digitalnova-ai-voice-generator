# DigitalNova Academy AI Voice Studio

Responsive frontend + FastAPI backend using `edge-tts` neural voices.

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
Open http://localhost:8000

## Important deployment notes

This MVP uses the unofficial `edge-tts` service. It requires internet access and may be throttled, changed, or unavailable. It is not a guaranteed production-grade free service; review service terms before public/commercial deployment. Add authentication, request rate limiting, abuse prevention, logging, usage quotas, and an approved commercial TTS provider before launching at scale. No API key is required for the MVP. MP3 files are created temporarily and removed after serving.
