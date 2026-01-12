from fastapi import APIRouter, File, UploadFile, HTTPException
from backend.core.engine import AnalysisEngine
import shutil
import os

router = APIRouter()

TEMP_FILE_PATH = "temp_uploaded_data.csv"

@router.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):
    """
    Endpoint to analyze XAUUSD data.
    Requires a CSV file (MT5 export).
    Fetches Macro data from Yahoo Finance automatically.
    """
    try:
        # Save uploaded file temporarily
        with open(TEMP_FILE_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run Analysis
        engine = AnalysisEngine(csv_path=TEMP_FILE_PATH)
        result = engine.run_analysis()
        
        # Cleanup
        if os.path.exists(TEMP_FILE_PATH):
            os.remove(TEMP_FILE_PATH)
            
        if "error" in result:
             raise HTTPException(status_code=400, detail=result['error'])
             
        return result
        
    except Exception as e:
        # Cleanup on error
        if os.path.exists(TEMP_FILE_PATH):
            os.remove(TEMP_FILE_PATH)
        raise HTTPException(status_code=500, detail=str(e))
