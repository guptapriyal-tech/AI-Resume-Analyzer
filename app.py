import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import app_utils.resume_parser_v2 as rp
from model.analyzer import calculate_similarity, check_missing_skills, generate_suggestions

app = Flask(__name__)
app.secret_key = 'super_secret_key'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import db_utils

# Initialize DB on start
db_utils.init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        files = request.files.getlist('file')
        job_description = request.form['job_description']

        if not files or files[0].filename == '':
            flash('No selected file')
            return redirect(request.url)

        results = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                try:
                    if filename.lower().endswith('.pdf'):
                        resume_text = rp.get_pdf_text(file_path)
                    elif filename.lower().endswith('.docx'):
                        resume_text = rp.extract_text_from_docx(file_path)
                    else:
                        continue # Skip unsupported

                    resume_skills = rp.extract_skills(resume_text)

                    if job_description:
                        jd_skills = rp.extract_skills(job_description)
                        match_percentage = calculate_similarity(resume_text, job_description, resume_skills, jd_skills)
                        missing_skills = check_missing_skills(resume_skills, jd_skills)
                        suggestions = generate_suggestions(missing_skills)
                    else:
                        match_percentage = 0
                        missing_skills = []
                        suggestions = []
                        jd_skills = []
                    
                    # Save to DB
                    db_utils.save_analysis(filename, job_description, match_percentage, resume_skills, missing_skills, suggestions)

                    results.append({
                        'filename': filename,
                        'match_percentage': match_percentage,
                        'resume_skills': resume_skills,
                        'missing_skills': missing_skills,
                        'suggestions': suggestions,
                        'resume_text': resume_text
                    })

                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    flash(f"Error processing {filename}")

        if not results:
             flash('No valid files processed')
             return redirect(request.url)

        if len(results) == 1:
            # Single Resume Mode
            res = results[0]
            return render_template('result.html', 
                                   resume_text=res['resume_text'][:500] + "...",
                                   match_percentage=res['match_percentage'],
                                   resume_skills=res['resume_skills'], # Passed as list of dicts
                                   missing_skills=res['missing_skills'],
                                   suggestions=res['suggestions'])
        else:
            # Multiple Resume Comparison Mode
            # Sort by match percentage descending
            results.sort(key=lambda x: x['match_percentage'], reverse=True)
            return render_template('compare.html', results=results, job_description=job_description)
                
    return render_template('index.html')

@app.route('/history')
def history():
    analyses = db_utils.get_recent_analyses(50)
    return render_template('history.html', analyses=analyses)

@app.route('/analysis/<int:analysis_id>')
def view_analysis(analysis_id):
    res = db_utils.get_analysis_by_id(analysis_id)
    if res:
         return render_template('result.html', 
                                   resume_text="Stored in database...", # We don't store full text currently for efficiency
                                   match_percentage=res['match_percentage'],
                                   resume_skills=res['resume_skills'], 
                                   missing_skills=res['missing_skills'],
                                   suggestions=res['suggestions'])
    else:
        flash('Analysis not found')
        return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)
