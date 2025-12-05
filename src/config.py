# src/config.py
import os
from dotenv import load_dotenv

# Load .env file immediately when this module is imported
load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMAGES_DIR = os.path.join(BASE_DIR, "data", "images")
    OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")
    RUBRIC_PATH = os.path.join(BASE_DIR, "config", "rubric.json")
    
    # Model Settings
    OCR_LANG = "en"
    # User requested Gemini 2.5 Flash. 
    # If this fails (due to regional availability), switch to "gemini-1.5-flash"
    GEMINI_MODEL_NAME = "gemini-2.5-flash" 

    @staticmethod
    def validate():
        if not Config.GOOGLE_API_KEY:
            raise ValueError("Missing GOOGLE_API_KEY in .env file.")