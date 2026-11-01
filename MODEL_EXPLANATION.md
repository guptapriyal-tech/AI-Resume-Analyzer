# Offline AI Resume Analyzer - Model Explanation

This document explains the machine learning logic, algorithms, and methodologies used in the Offline AI Resume Analyzer.

## 1. Core Logic Overview

The system uses a combination of **keyword-based skill extraction** and **statistical text similarity** to evaluate resumes. It does not rely on a single "black box" model but rather a transparent, explainable pipeline.

### The Pipeline:
1.  **Text Extraction**: PDF/DOCX -> Raw Text.
2.  **Preprocessing**: Cleaning, Lowercasing, Stopword Removal.
3.  **Entity Extraction (NER)**: Identifies specific entities (Skills, Orgs).
4.  **Vectorization (TF-IDF)**: Converts text into mathematical vectors.
5.  **Similarity Calculation (Cosine)**: Measures the angle between vectors.

---

## 2. TF-IDF Vectorizer (Term Frequency-Inverse Document Frequency)

### What is it?
TF-IDF is a statistical measure used to evaluate how important a word is to a document in a collection or corpus.

*   **TF (Term Frequency)**: How often a word appears in the resume.
    *   *Logic*: If "Python" appears 5 times, it's likely important.
*   **IDF (Inverse Document Frequency)**: How unique a word is across all documents.
    *   *Logic*: Words like "the", "and", "is" appear everywhere, so they get a low score. Words like "TensorFlow" or "Kubernetes" are rare, so they get a high score.

### Why we use it?
Simple word counts (Bag of Words) are biased towards long documents. TF-IDF balances this by down-weighting common words and up-weighting unique, domain-specific terms. This ensures that a resume doesn't get a high score just because it has many filler words.

---

## 3. Cosine Similarity

### What is it?
Cosine Similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space.

### The Formula:
$$ \text{Cosine Similarity} = \frac{A \cdot B}{||A|| \times ||B||} $$

*   **A**: The vector representation of the Resume.
*   **B**: The vector representation of the Job Description.
*   **Result**: A number between 0 and 1.
    *   **1 (0° angle)**: Perfect match.
    *   **0 (90° angle)**: No similarity.

### How similarity score is calculated:
1.  We convert the **Resume Text** and **Job Description** into TF-IDF vectors.
2.  We calculate the cosine of the angle between these two vectors.
3.  We multiply the result by 100 to get a **percentage score**.

*Example*: If the resume vector points in the same "direction" (uses the same vocabulary) as the job description vector, the angle is small, and the score is high.

---

## 4. Skill Keyword Matching

While Cosine Similarity gives a *holistic* score, it doesn't tell you *specifically* what is missing. For this, we use explicit **Keyword Matching**.

1.  **Database**: We maintain a list of 100+ technical skills (e.g., Python, AWS, React).
2.  **Extraction**: We scan both the resume and the job description for these exact terms.
3.  **Gap Analysis**:
    *   $Skills_{Job} - Skills_{Resume} = Missing Skills$

---

## 5. Named Entity Recognition (NER)

We use **spaCy's en_core_web_sm** model for NER.

### What is NER?
NER classifies named entities in text into undefined categories such as person names, organizations, locations, etc.

*   **PERSON**: To identify the candidate's name.
*   **ORG**: To identify previous companies or universities.
*   **DATE**: To identify work periods.

*Note: In our offline fallback mode (when spaCy is missing), we rely purely on regex-based keyword matching for stability.*
