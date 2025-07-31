import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


load_dotenv()
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FOLDER = os.path.join(BASE_DIR, os.getenv('AUDIO_FOLDER'))
TEMPLATES_FOLDER = os.path.join(BASE_DIR, os.getenv('TEMPLATES_FOLDER'))

@app.get("/{folder}/{phone}")
async def serve_audio(folder: str, phone: str):
    filename = phone
    if not filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    file_path = os.path.join(AUDIO_FOLDER, folder, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="audio/wav")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(TEMPLATES_FOLDER, "index.html"), "r") as f:
        return f.read()

if __name__ == "__main__":
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    uvicorn.run("app:app", host=host, port=port, reload=True)