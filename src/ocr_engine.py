from abc import ABC, abstractmethod
import logging
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

class OcrEngine(ABC):
    """Abstract Base Class for OCR engines."""
    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        pass

class TrOcrEngine(OcrEngine):
    def __init__(self):
        self.logger = logging.getLogger("GradingPipeline")
        self.logger.info("Loading Microsoft TrOCR model (handwritten)...")
        self.logger.info("This might take a minute to download (~1.5GB) on the first run.")
        
        # Determine device (GPU or CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"Running OCR on device: {self.device}")

        # Load the processor and model from Hugging Face
        self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
        self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten').to(self.device)

    def extract_text(self, image_path: str) -> str:
        """
        Uses Transformer OCR to generate text from the image.
        """
        try:
            # Load image
            image = Image.open(image_path).convert("RGB")
            
            # Preprocess image
            pixel_values = self.processor(images=image, return_tensors="pt").pixel_values.to(self.device)

            # Generate text ids
            generated_ids = self.model.generate(pixel_values, max_new_tokens=100)
            
            # Decode ids to text
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            return generated_text.strip()
            
        except Exception as e:
            self.logger.error(f"TrOCR Failed for {image_path}: {e}")
            return ""