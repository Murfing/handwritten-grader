# 📝 Automated Handwritten Assessment Pipeline

## Project Overview

The goal of this project is to **automate the grading process for handwritten exams**. It takes raw images of student answers, extracts the text using advanced OCR, and assigns a score with detailed feedback based on a teacher-defined rubric.

## 🛠️ Architecture

The pipeline follows a sequential flow:

```
Input Images → Preprocessing → OCR Engine (TrOCR) → Grading Agent (Gemini) → CSV Output
```

### Pipeline Flow

1. **Input**: Reads images (`.jpg`, `.png`, `.jpeg`) from the `data/images` directory
2. **Preprocessing**: Filename parsing to identify Student ID and Question ID
3. **OCR Engine (TrOCR)**: Converts the handwritten image into a text string
4. **Grading Agent (Gemini)**: Evaluates the OCR text against the rubric and generates a JSON evaluation
5. **Output**: Appends results incrementally to `data/output/results.csv`

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://ai.google.dev/))
- (Optional) CUDA-compatible GPU for faster TrOCR inference

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/handwritten-grader.git
cd handwritten-grader
```

### 2. Create a Virtual Environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

This project requires PyTorch (for TrOCR) and the Google GenAI SDK.

```bash
pip install torch torchvision transformers pillow pandas python-dotenv google-generativeai
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

⚠️ **Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

---

## 📂 Project Structure

```
handwritten-grader/
│
├── config/
│   └── rubric.json              # Defines questions, max marks, and grading criteria
│
├── data/
│   ├── images/                  # Input images (Format: studentID_questionID.jpg)
│   ├── output/                  # Generated CSV results
│   └── ground_truth.csv         # (Optional) Teacher scores for validation
│
├── src/
│   ├── __init__.py
│   ├── config.py                # Central configuration management
│   ├── ocr_engine.py            # TrOCR implementation (Hugging Face)
│   ├── grading_model.py         # Gemini API wrapper for grading logic
│   ├── pipeline.py              # Main script orchestration
│   └── utils.py                 # Logger and helper functions
│
├── .env                         # API Keys (Excluded from Git)
├── .gitignore
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 🏃‍♂️ Usage

### 1. Prepare Your Data

#### Organize Images
Place your handwritten answer images in `data/images/`.

**Filename Format**: `{studentID}_{questionID}.jpg`

Examples:
- `student01_q1.jpg`
- `student02_q2.jpg`
- `alice_q3.jpg`

#### Configure Rubric
Update `config/rubric.json` to match your questions. Example structure:

```json
[
  {
    "question_id": "q1",
    "question_text": "Explain the water cycle.",
    "max_marks": 10,
    "rubric": {
      "evaporation": 3,
      "condensation": 3,
      "precipitation": 2,
      "collection": 2
    }
  }
]
```

### 2. Run the Pipeline

Execute the pipeline from the root directory:

```bash
python -m src.pipeline
```

### 3. View Results

Results are saved incrementally to `data/output/results.csv`:

| student_id | question_id | ocr_text | score | max_marks | feedback |
|------------|-------------|----------|-------|-----------|----------|
| student01 | q1 | The water cycle... | 8 | 10 | Good explanation... |

---

## 📊 Output Format

The pipeline generates a CSV file with the following columns:

- **student_id**: Extracted from filename
- **question_id**: Extracted from filename
- **ocr_text**: Raw text extracted by TrOCR
- **score**: Points awarded (0 to max_marks)
- **max_marks**: Maximum possible score
- **feedback**: Detailed explanation from Gemini

---

## 🔧 Configuration

### Modifying OCR Settings

Edit `src/ocr_engine.py` to change the TrOCR model:

```python
# For base model (faster, less accurate)
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

# For large model (slower, more accurate)
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')
```

### Adjusting Rate Limits

Modify the sleep duration in `src/pipeline.py`:

```python
if i < len(files) - 1:
    logger.info("   > Sleeping 10s...")
    time.sleep(10)  # Change this value
```

### Changing Gemini Model

Edit `src/grading_model.py`:

```python
self.model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Change model here
```

---
