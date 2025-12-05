# src/grading_model.py
from abc import ABC, abstractmethod
import json
import logging
from google import genai
from google.genai import types
from .config import Config

class GradingModel(ABC):
    """Abstract Base Class for Grading Models."""
    @abstractmethod
    def grade(self, student_text: str, question_data: dict) -> dict:
        pass

class GeminiGradingModel(GradingModel):
    def __init__(self):
        self.logger = logging.getLogger("GradingPipeline")
        # Initialize the new Google GenAI Client
        self.client = genai.Client(api_key=Config.GOOGLE_API_KEY)
        self.model_name = Config.GEMINI_MODEL_NAME

    def grade(self, student_text: str, question_data: dict) -> dict:
        """
        Sends the text + rubric to Gemini and expects a strict JSON response.
        """
        question_text = question_data.get('question_text', 'Unknown Question')
        rubric_text = question_data.get('rubric', '')
        max_marks = question_data.get('max_marks', 10)

        # Prompt Engineering
        prompt = f"""
        You are a strict but fair teacher grading a handwritten answer.
        
        ### Question:
        {question_text}

        ### Rubric:
        {rubric_text}
        (Max Marks: {max_marks})

        ### Student Answer (extracted via OCR):
        "{student_text}"

        ### Task:
        Evaluate the student answer based ONLY on the rubric.
        - If the text implies the correct answer despite OCR errors, be lenient on spelling.
        - If the text is gibberish or empty, give 0.

        ### Output Format:
        Return valid JSON only. Do not add markdown formatting like ```json.
        {{
            "score": <float>,
            "feedback": "<short constructive feedback>"
        }}
        """

        try:
            # We use the new client.models.generate_content method
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"  # Enforces JSON output
                )
            )

            # Parse the JSON response
            result = json.loads(response.text)
            
            # Add metadata
            result['max_marks'] = max_marks
            return result

        except Exception as e:
            self.logger.error(f"Grading failed for question '{question_text}': {e}")
            # Return a default error score
            return {
                "score": 0,
                "feedback": f"Error during grading: {str(e)}",
                "max_marks": max_marks
            }