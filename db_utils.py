
import sqlite3
import json
from datetime import datetime
import os

DB_NAME = "resume_analyzer.db"

def init_db():
    """Initializes the SQLite database with necessary tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Table to store analysis results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        job_description TEXT,
        match_percentage REAL,
        resume_skills TEXT,  -- Stored as JSON string
        missing_skills TEXT, -- Stored as JSON string
        suggestions TEXT,    -- Stored as JSON string
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized successfully.")

def save_analysis(filename, job_description, match_percentage, resume_skills, missing_skills, suggestions):
    """Saves a new analysis result to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO analysis_results (filename, job_description, match_percentage, resume_skills, missing_skills, suggestions)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        filename,
        job_description,
        match_percentage,
        json.dumps(resume_skills),  # Convert list/dict to JSON string
        json.dumps(missing_skills),
        json.dumps(suggestions)
    ))
    
    conn.commit()
    conn.close()

def get_recent_analyses(limit=10):
    """Retrieves the most recent analysis results."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Access columns by name
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM analysis_results 
    ORDER BY timestamp DESC 
    LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append({
            'id': row['id'],
            'filename': row['filename'],
            'match_percentage': row['match_percentage'],
            'timestamp': row['timestamp'],
            # We don't need full details for the list view usually
        })
    
    conn.close()
    return results

def get_analysis_by_id(analysis_id):
    """Retrieves a specific analysis result."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM analysis_results WHERE id = ?", (analysis_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row['id'],
            'filename': row['filename'],
            'job_description': row['job_description'],
            'match_percentage': row['match_percentage'],
            'resume_skills': json.loads(row['resume_skills']),
            'missing_skills': json.loads(row['missing_skills']),
            'suggestions': json.loads(row['suggestions']),
            'timestamp': row['timestamp']
        }
    return None
