import os
import uuid
import sys
import tempfile  # <-- NEW: Python's built-in temporary storage manager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from starlette.background import BackgroundTask

from engine.config import SUPPORTED_CONVERSIONS
from main import get_converter_class, process_file

app = FastAPI(title="Quick Convert Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route all file handling to the Operating System's hidden temporary workspace
SYSTEM_TEMP_DIR = tempfile.gettempdir()

@app.post("/api/convert")
async def api_convert(
    file: UploadFile = File(...),
    targetFormat: str = Form(None)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename provided")

    original_ext = os.path.splitext(file.filename)[1].lower()
    
    # Create the invisible input path in the system temp folder
    input_path = os.path.join(SYSTEM_TEMP_DIR, f"{uuid.uuid4().hex}_{file.filename}")
    
    # Save directly to the temporary workspace
    with open(input_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  
            buffer.write(chunk)

    allowed_exts = SUPPORTED_CONVERSIONS.get(original_ext, [])
    if not allowed_exts:
        if os.path.exists(input_path): os.remove(input_path)
        raise HTTPException(status_code=400, detail=f"Format not supported: {original_ext}")

    if not targetFormat:
        targetFormat = allowed_exts[0]
    elif targetFormat not in allowed_exts:
        if os.path.exists(input_path): os.remove(input_path)
        raise HTTPException(status_code=400, detail=f"Conversion blocked: {original_ext} -> {targetFormat}")

    base_name = os.path.splitext(os.path.basename(file.filename))[0]
    output_filename = f"{uuid.uuid4().hex[:6]}_{base_name}{targetFormat}"
    
    # Set the output path to the system temp folder as well
    output_path = os.path.join(SYSTEM_TEMP_DIR, output_filename)

    # Process the file invisibly in the background
    success = await run_in_threadpool(process_file, input_path, output_path)

    # Purge the original temporary input file immediately
    try:
        if os.path.exists(input_path):
            os.remove(input_path)
    except Exception as e:
        print(f"Warning: Failed to clean up temp file {input_path} - {e}")

    if success:
        return {
            "success": True,
            "download_url": f"/api/download/{output_filename}",
            "filename": output_filename,
            "target": targetFormat
        }
    else:
        return {"success": False, "error": "Conversion process failed"}

@app.get("/")
async def root():
    return RedirectResponse(url="/quick_convert_home_page/code.html")

@app.get("/api/download/{filename}")
async def api_download(filename: str):
    # Locate the converted file in the system temp directory
    file_path = os.path.join(SYSTEM_TEMP_DIR, filename)
    if os.path.exists(file_path):
        # Serve it to the user and permanently delete it from the OS
        return FileResponse(
            file_path, 
            filename=filename,
            background=BackgroundTask(os.remove, file_path) 
        )
    raise HTTPException(status_code=404, detail="File not found or already deleted")

# Serve the frontend statically
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory {FRONTEND_DIR} not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)