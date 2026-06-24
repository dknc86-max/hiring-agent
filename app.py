from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import tempfile
from score import main
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)
load_dotenv()

@app.route("/")
def index():
    return render_template("index.html")

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
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        result = main(tmp_path)
        return render_template("result.html", result=result, candidate_name=os.path.basename(tmp_path).replace(".pdf", ""))
    except Exception as e:
        flash(f"Error processing resume: {str(e)}", "error")
        return redirect(url_for("index"))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)