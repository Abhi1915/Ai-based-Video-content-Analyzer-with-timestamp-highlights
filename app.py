import os
import shutil
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from utils import transcribe, detect_highlights

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_video(request: Request, file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("✅ File saved:", file_path)

        # Transcribe
        segments = transcribe(file_path)
        print("✅ Transcription done")

        # Highlights
        highlights = detect_highlights(segments)
        print("✅ Highlights generated")

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "results": highlights}
        )

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"error": str(e)}