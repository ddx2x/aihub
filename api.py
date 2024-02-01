from main import app
from fastapi import File,UploadFile,Form


@app.post("/ai/ocr")
async def index(pdf: UploadFile = File(None)):
    if pdf:
        print(pdf)
    return {"respose": "ok"}

