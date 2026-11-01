# Project Architecture

The **Offline AI Resume Analyzer** is structured to be modular, scalable, and easy to maintain.

## Folder Structure

```
resume_analyzer/ (Root)
├── app.py                  # Main Flask application entry point
├── dataset/                # Sample data for testing (resumes, job descriptions)
│   ├── sample_resume.txt
│   └── sample_jd.txt
├── model/                  # ML modules and logic
│   └── analyzer.py         # Handles similarity calculation and ML models
├── static/                 # Static assets
│   └── css/
│       └── style.css       # Stylesheets
├── templates/              # HTML templates for Flask
│   ├── index.html          # Upload page
│   ├── result.html         # Analysis results page
│   └── compare.html        # Multi-resume leaderboard page
├── utils/                  # Utility scripts for parsing and cleaning
│   └── resume_parser.py    # Extracts text from PDF/DOCX and cleans it
└── requirements.txt        # Python dependencies
```

## Component Breakdown

1.  **Frontend (`templates/`, `static/`)**:
    *   **Goal**: Provide a clean, intuitive interface for users.
    *   **Tech**: HTML5, CSS3 (Glassmorphism design), Jinja2 templating.
    *   **Key Features**: Drag-and-drop file upload, real-time feedback, visual skill graphs.

2.  **Backend (`app.py`)**:
    *   **Goal**: Orstrate the entire process.
    *   **Tech**: Flask (Python).
    *   **Responsibility**: Receives files, routes them to parsers, calls ML models, and renders results.

3.  **Data Processing (`utils/resume_parser.py`)**:
    *   **Goal**: Convert raw binary files (PDF/DOCX) into clean, usable text.
    *   **Tech**: PyPDF2, python-docx, Regex, spaCy (for tokenization).

4.  **Machine Learning Engine (`model/analyzer.py`)**:
    *   **Goal**: Understand the semantic similarity between resume and job description.
    *   **Tech**: scikit-learn (TF-IDF, Cosine Similarity), spaCy (NER).
    *   **Logic**:
        *   **Vectorization**: Converts text to numerical vectors using TF-IDF.
        *   **Comparison**: Calculates the cosine angle between vectors to determine match %.
        *   **Gap Analysis**: Identifies missing keywords through direct set operations.

5.  **Data Layer (`dataset/`)**:
    *   **Goal**: Provide out-of-the-box examples for users to test the system immediately.
