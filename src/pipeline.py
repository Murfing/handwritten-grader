import os
import time
import pandas as pd
from .config import Config
from .utils import setup_logger, load_rubric
# UPDATED IMPORT
from .ocr_engine import TrOcrEngine
from .grading_model import GeminiGradingModel

def main():
    logger = setup_logger()
    
    # 1. Validation
    try:
        Config.validate()
        rubric_data = load_rubric(Config.RUBRIC_PATH)
        rubric_map = {item['question_id']: item for item in rubric_data}
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        return

    # 2. Initialize Engines
    try:
        # UPDATED INITIALIZATION
        ocr_engine = TrOcrEngine()
        grader = GeminiGradingModel()
    except Exception as e:
        logger.error(f"Engine initialization failed: {e}")
        return
    
    results = []
    output_path = os.path.join(Config.OUTPUT_DIR, "results.csv")

    # 3. Process Images
    if not os.path.exists(Config.IMAGES_DIR):
        logger.error(f"Image directory not found: {Config.IMAGES_DIR}")
        return

    files = sorted([f for f in os.listdir(Config.IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    logger.info(f"Found {len(files)} images to process.")

    # Create empty CSV if not exists
    if not os.path.exists(output_path):
        pd.DataFrame(columns=["student_id", "question_id", "ocr_text", "score", "max_marks", "feedback"]).to_csv(output_path, index=False)

    for i, filename in enumerate(files):
        try:
            name_part = os.path.splitext(filename)[0]
            parts = name_part.split('_')
            
            if len(parts) < 2:
                logger.warning(f"Skipping {filename}: Bad filename format.")
                continue
                
            student_id = parts[0]
            question_id = parts[1]
            
            if question_id not in rubric_map:
                logger.warning(f"Skipping {filename}: Question ID '{question_id}' not found.")
                continue

            # Step A: OCR
            logger.info(f"[{i+1}/{len(files)}] Processing {filename}...")
            image_path = os.path.join(Config.IMAGES_DIR, filename)
            
            print(f"   > Running TrOCR on {filename}...", end="\r") 
            extracted_text = ocr_engine.extract_text(image_path)
            
            if not extracted_text:
                logger.warning(f"   > No text found in {filename}")
                extracted_text = ""
            else:
                clean_preview = extracted_text.replace('\n', ' ')[:30]
                print(f"   > OCR Found: '{clean_preview}...'")

            # Step B: Grading
            question_data = rubric_map[question_id]
            print(f"   > Grading with Gemini...", end="\r")
            grading_result = grader.grade(extracted_text, question_data)
            print(f"   > Graded. Score: {grading_result.get('score')}")

            # Step C: Record Result
            new_row = {
                "student_id": student_id,
                "question_id": question_id,
                "ocr_text": extracted_text,
                "score": grading_result.get("score", 0),
                "max_marks": grading_result.get("max_marks", 0),
                "feedback": grading_result.get("feedback", "")
            }
            results.append(new_row)

            # Incremental Save
            pd.DataFrame([new_row]).to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False)

            # Rate Limit Sleep
            if i < len(files) - 1:
                logger.info("   > Sleeping 10s...")
                time.sleep(10)

        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")

    logger.info(f"Pipeline finished. Final file at {output_path}")

if __name__ == "__main__":
    main()