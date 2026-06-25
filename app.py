from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import tempfile
import uuid
import threading
from score import main
from config import MOCK_MODE
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)
load_dotenv(override=True)

evaluations = {}

@app.route("/")
def index():
    return render_template("index.html")

def run_evaluation(file_path, eval_id):
    try:
        evaluations[eval_id]['status'] = 'running'
        evaluations[eval_id]['progress'] = 10
        evaluations[eval_id]['message'] = 'Extracting resume data...'
        
        score, resume_data = main(file_path)
        
        if score is None:
            raise ValueError("Failed to evaluate the resume. The parser or LLM API returned empty data.")
        
        evaluations[eval_id]['status'] = 'complete'
        evaluations[eval_id]['progress'] = 100
        evaluations[eval_id]['result'] = score.model_dump() if score else None
        
        # Save candidate metadata
        candidate_name = 'Candidate'
        email = None
        phone = None
        github_url = None
        if resume_data and hasattr(resume_data, 'basics') and resume_data.basics:
            if resume_data.basics.name:
                candidate_name = resume_data.basics.name
            email = resume_data.basics.email
            phone = resume_data.basics.phone
            if resume_data.basics.profiles:
                github_profile = next((p for p in resume_data.basics.profiles if p.network and p.network.lower() == 'github'), None)
                if github_profile:
                    github_url = github_profile.url
        
        evaluations[eval_id]['candidate_name'] = candidate_name
        evaluations[eval_id]['email'] = email
        evaluations[eval_id]['phone'] = phone
        evaluations[eval_id]['github_url'] = github_url
    except Exception as e:
        evaluations[eval_id]['status'] = 'error'
        evaluations[eval_id]['error'] = str(e)
    finally:
        if os.path.exists(file_path):
            os.unlink(file_path)

@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        flash("No file uploaded", "error")
        return redirect(url_for("index"))
    
    file = request.files["resume"]
    if file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("index"))
    
    if not file.filename.lower().endswith(".pdf"):
        flash("Please upload a PDF file", "error")
        return redirect(url_for("index"))
    
    eval_id = str(uuid.uuid4())
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name
    
    evaluations[eval_id] = {'status': 'starting', 'progress': 0, 'message': 'Starting...'}
    
    thread = threading.Thread(target=run_evaluation, args=(tmp_path, eval_id))
    thread.start()
    
    return render_template("evaluate.html", eval_id=eval_id, filename=file.filename)

@app.route("/progress/<eval_id>")
def get_progress(eval_id):
    return jsonify(evaluations.get(eval_id, {'status': 'not_found'}))

@app.route("/result/<eval_id>")
def result_page(eval_id):
    eval_data = evaluations.get(eval_id)
    if not eval_data:
        flash("Evaluation not found", "error")
        return redirect(url_for("index"))
    
    if eval_data.get('status') != 'complete':
        flash("Evaluation is still in progress or failed", "error")
        return redirect(url_for("index"))
    
    result_dict = eval_data.get('result')
    candidate_name = eval_data.get('candidate_name', 'Candidate')
    email = eval_data.get('email')
    phone = eval_data.get('phone')
    github_url = eval_data.get('github_url')
    
    # Calculate overall score for circular gauge
    total_score = 0
    if result_dict and 'scores' in result_dict:
        scores = result_dict['scores']
        for cat in ['open_source', 'self_projects', 'production', 'technical_skills']:
            if cat in scores and isinstance(scores[cat], dict):
                total_score += min(scores[cat].get('score', 0), scores[cat].get('max', 100))
        
        bonus = result_dict.get('bonus_points', {}).get('total', 0) if result_dict.get('bonus_points') else 0
        deductions = result_dict.get('deductions', {}).get('total', 0) if result_dict.get('deductions') else 0
        total_score = max(0, min(120, total_score + bonus - deductions))
            
    return render_template("result.html", result=result_dict, candidate_name=candidate_name, total_score=total_score, email=email, phone=phone, github_url=github_url)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)