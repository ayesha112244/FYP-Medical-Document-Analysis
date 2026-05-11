# ============================================================
# FYP - Medical Document Analysis
# api_server.py - FastAPI REST API Server
# Student: Ayesha Sohail (U2386691)
# ============================================================

import os
import sys
import io
import json
import shutil
import subprocess

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

# ── Fix encoding for Windows terminal ────────────────────────
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer,
                              encoding='utf-8', errors='replace')

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR             = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR           = os.path.join(BASE_DIR, "api_uploads")
EXTRACTED_FIELDS_DIR = os.path.join(BASE_DIR, "extracted_fields")
PIPELINE_PATH        = os.path.join(BASE_DIR, "pipeline.py")

# Create upload directory if not exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── FastAPI App ───────────────────────────────────────────────
app = FastAPI(
    title="Medical Document Analysis API",
    description="REST API for extracting data from lab reports",
    version="1.0.0"
)


@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "running", "message": "Medical Document Analysis API"}


@app.post("/extract")
async def extract(
    file: UploadFile = File(...),
    doc_id: str = Form(...),
    selected_type: str = Form(default="")
):
    """
    Extract fields from an uploaded lab report.
    Accepts PDF, PNG, JPEG files.
    Returns extracted JSON data.
    """

    # Step 1: Save uploaded file
    ext      = os.path.splitext(file.filename)[1].lower()
    filename = doc_id + ext
    filepath = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"File save failed: {str(e)}"}
        )

    # Step 2: Run pipeline
    try:
        cmd = [sys.executable, PIPELINE_PATH, filepath]
        if selected_type:
            cmd.append(selected_type)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )
        
    except subprocess.TimeoutExpired:
        return JSONResponse(
            status_code=500,
            content={"error": "Pipeline timed out after 60 seconds"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Pipeline execution failed: {str(e)}"}
        )

    # Step 3: Read JSON output
    json_path = os.path.join(EXTRACTED_FIELDS_DIR, doc_id + ".json")

    if not os.path.exists(json_path):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Extraction failed — JSON not produced",
                "pipeline_output": result.stdout,
                "pipeline_error": result.stderr
            }
        )

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            extracted_data = json.load(f)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"JSON read failed: {str(e)}"}
        )

    # Step 4: Return extracted data
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "doc_id": doc_id,
            "data": extracted_data,
            "pipeline_output": result.stdout
        }
    )