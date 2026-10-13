from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
import edge_tts, tempfile, os

BASE = Path(__file__).parent
app = FastAPI(title='DigitalNova Academy AI Voice Generator')
VOICES = {'hi-female':'hi-IN-SwaraNeural','hi-male':'hi-IN-MadhurNeural','en-female':'en-IN-NeerjaNeural','en-male':'en-IN-PrabhatNeural','en-us-female':'en-US-AriaNeural','en-us-male':'en-US-GuyNeural'}
class SpeechRequest(BaseModel):
    text: str = Field(min_length=1,max_length=3000)
    voice: str = 'hi-female'
    speed: int = Field(default=0,ge=-50,le=50)

@app.post('/api/speech')
async def speech(req: SpeechRequest):
    if req.voice not in VOICES:
        raise HTTPException(status_code=400,detail='Unsupported voice')
    fd, path = tempfile.mkstemp(suffix='.mp3')
    os.close(fd)
    try:
        communicate = edge_tts.Communicate(req.text, VOICES[req.voice], rate=f'{req.speed:+d}%')
        await communicate.save(path)
        return FileResponse(path,media_type='audio/mpeg',filename='digitalnova-voice.mp3',background=__import__('starlette.background',fromlist=['BackgroundTask']).BackgroundTask(lambda: os.path.exists(path) and os.remove(path)))
    except Exception as exc:
        if os.path.exists(path): os.remove(path)
        raise HTTPException(status_code=502,detail='Voice service unavailable. Try again shortly.') from exc

app.mount('/',StaticFiles(directory=BASE/'static',html=True),name='static')
