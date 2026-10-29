from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os
import shutil

#For File Upload : StaticFiles (directory configuration: utilities for server files map) ,UploadFile, File, shutil (used for copy,delete,move,archive), OS
app = FastAPI()

# Step 1: Ensure the 'uploads' directory exists
UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Step 2: static files configuration : http://localhost:8000/files/<filename>
app.mount("/files", StaticFiles(directory=UPLOAD_DIRECTORY), name="files")

# Step 3: File upload endpoint
@app.post("/upload")
async def upload_file(file:UploadFile = File(...)):
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    
    # Check if the file already exists
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    if os.path.exists(file_location):
        raise HTTPException(status_code=400, detail=f"File '{filename}' already exists.")
    
    # Save the uploaded file to the 'uploads' directory
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "message": f"Successfully uploaded '{filename}'",
        "filename": filename,
        "file_path": file_location,
        "file_url": f"http://localhost:8000/files/{filename}"
        }

# Step 4: Get File endpoint
@app.get("/files/{filename}")
async def get_file(filename: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")
    
    return {
        "filename": filename,
        "file_path": file_location,
        "file_url": f"http://localhost:8000/files/{filename}"
    }