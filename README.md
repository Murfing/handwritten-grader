📝 Automated Handwritten Assessment Pipeline

An end-to-end prototype designed to digitize and grade handwritten student short answers using State-of-the-Art (SOTA) AI models. This project connects a Transformer-based OCR engine with a Large Language Model (LLM) to replicate human grading workflows.

🚀 Project Overview

The goal of this project is to automate the grading process for handwritten exams. It takes raw images of student answers, extracts the text, and assigns a score and feedback based on a strict teacher-defined rubric.

Key Features

Handwriting Recognition: Uses Microsoft TrOCR (Transformer OCR), a model fine-tuned on the IAM handwriting dataset, for high-accuracy text extraction.

AI Grading: Uses Google Gemini 2.5 Flash to evaluate the extracted text against a JSON rubric, providing scores and constructive feedback.

Robust Pipeline: Includes automatic rate-limiting (to handle API quotas), incremental saving (to prevent data loss), and error handling.

Modular Design: Separate modules for OCR, Grading, and Configuration.

🛠️ Architecture

The pipeline follows a sequential flow:

Input: Reads images (.jpg) from the data/images directory.

Preprocessing: Filename parsing to identify Student ID and Question ID.

OCR Engine (TrOCR): Converts the image into a text string.

Grading Agent (Gemini): Takes the OCR Text + Rubric and generates a JSON evaluation.

Output: Appends the results to data/output/results.csv.

⚙️ Setup & Installation

1. Clone the Repository

git clone <your-repo-url>
cd handwritten-grader


2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

This project requires PyTorch (for TrOCR) and the Google GenAI SDK.

pip install torch torchvision transformers pillow pandas python-dotenv google-genai


4. Configure Environment Variables

Create a .env file in the root directory and add your Google Gemini API key:

GOOGLE_API_KEY=your_api_key_here


📂 Project Structure

handwritten-grader/
│
├── config/
│   └── rubric.json         # Defines questions, max marks, and grading criteria
│
├── data/
│   ├── images/             # Input images (Format: studentID_questionID.jpg)
│   ├── output/             # Generated CSV results
│   └── ground_truth.csv    # (Optional) Teacher scores for validation
│
├── src/
│   ├── config.py           # Central configuration management
│   ├── ocr_engine.py       # TrOCR implementation (Hugging Face)
│   ├── grading_model.py    # Gemini API wrapper for grading logic
│   ├── pipeline.py         # Main script orchestration
│   └── utils.py            # Logger and helper functions
│
├── .env                    # API Keys (Excluded from Git)
└── README.md               # Project documentation


🏃‍♂️ Usage

1. Prepare Data

Place your handwritten images in data/images/.

Ensure filenames match the format: student01_q1.jpg.

Update config/rubric.json to match your questions.

2. Run the Pipeline

Execute the pipeline module from the root directory:

python -m src.pipeline
