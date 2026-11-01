# AI Resume Analyzer

![ResumeAI](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)

An intelligent, full-stack application designed to optimize resume-to-job alignment using Natural Language Processing (NLP). 

**ResumeAI** acts as a personal career assistant, parsing complex resume formats (PDF/DOCX) to extract technical skills and cross-reference them with job descriptions. It features a custom **Weighted Scoring Algorithm** that simulates Applicant Tracking Systems (ATS), providing users with a realistic "Match Score," missing keyword identification, and actionable insights to improve their hiring potential.

Built with a focus on performance and detailed analytics, it includes a persistent database history and a premium, responsive UI.

## 🚀 Features

*   **Smart Parsing**: Extracts text from PDF and DOCX resumes.
*   **Skill Extraction**: Identifies 100+ technical skills (programming languages, tools, frameworks) using regex patterns and natural language processing techniques.
*   **ATS Scoring Algorithm**: Calculates a Weighted Match Score based on:
    *   **Skill Overlap (70%)**: Direct matching of required skills.
    *   **Contextual Similarity (30%)**: Text analysis using TF-IDF and Cosine Similarity (with Jaccard fallback).
*   **Visual Reports**: Premium UI with interactive charts and score visualizations.
*   **Leaderboard Mode**: Upload multiple resumes to see a ranked comparison against a single job description.
*   **Persistence**: Built-in SQLite database to store and retrieve past analysis history.

## 🛠 Tech Stack

*   **Backend**: Python, Flask
*   **Database**: SQLite (built-in)
*   **NLP/ML**: 
    *   `scikit-learn` (TF-IDF, Cosine Similarity)
    *   `spaCy` (Optional/Fallback support for NER)
    *   `PyPDF2` & `python-docx` (File parsing)
*   **Frontend**: HTML5, CSS3 (Custom Glassmorphism Design), Jinja2 Templating

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/resume-analyzer.git
    cd resume-analyzer
    ```

2.  **Create a virtual environment** (Optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    *Note: If you encounter issues with `scikit-learn` or `spaCy`, the app is designed to gracefully degrade to simpler analytical methods.*

## 🏃 Usage

1.  **Run the application**:
    ```bash
    python app.py
    ```
    The app will initialize the SQLite database automatically.

2.  **Open your browser**:
    Navigate to `http://127.0.0.1:5000`.

3.  **Analyze**:
    *   Upload one or more resume files.
    *   Paste the Job Description.
    *   Click "Analyze & Optimize".

4.  **View History**:
    Click the "View History" link on the home page to see past results saved in the database.

## 📂 Project Structure

```
resume-analyzer/
├── app.py                 # Main Flask application entry point
├── db_utils.py            # SQLite database interactions
├── app_utils/
│   ├── resume_parser_v2.py# Core logic for text cleaning and skill extraction
├── model/
│   ├── analyzer.py        # Scoring algorithms (TF-IDF, Cosine Sim, etc.)
├── static/
│   └── css/
│       └── style.css      # Premium UI styles
├── templates/
│   ├── index.html         # Home/Upload page
│   ├── result.html        # Single analysis report
│   ├── compare.html       # Multi-resume leaderboard
│   └── history.html       # Analysis history view
├── instance/              # DB storage (optional location)
├── uploads/               # Temporary storage for uploaded files
└── requirements.txt       # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
