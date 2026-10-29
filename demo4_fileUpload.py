from fastapi import FastAPI, UploadFile, File
import os


# * Create app : Register App
app = FastAPI()

# Upload Directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file:UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": file_path
    }