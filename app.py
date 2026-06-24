from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import tempfile
import uuid
import threading
from score import main
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)
load_dotenv()

evaluations = {}

@app.route("/")
def index():
    return render_template("index.html")

def run_evaluation(file_path, eval_id):
    try:
        evaluations[eval_id]['status'] = 'running'
        evaluations[eval_id]['progress'] = 10
        evaluations[eval_id]['message'] = 'Extracting resume data...'
        
        result = main(file_path)
        
        evaluations[eval_id]['status'] = 'complete'
        evaluations[eval_id]['progress'] = 100
        evaluations[eval_id]['result'] = result
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)