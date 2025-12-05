# src/utils.py
import json
import os
import logging

def setup_logger(name="GradingPipeline"):
    """Sets up a simple logger to print to console."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def load_rubric(path: str) -> list:
    """Loads the rubric JSON file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Rubric file not found at {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_result(data: dict, output_path: str):
    """Helper to save intermediate JSON results if needed."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)