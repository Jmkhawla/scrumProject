from flask import Flask, render_template, request, jsonify
from pdf_qa import generate_qcm_from_pdf
import os
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def home():
    # On ne renvoie plus les questions via Jinja, tout se fait en front-end
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    
    if file and file.filename.lower().endswith(".pdf"):
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        return jsonify({
            "success": True,
            "filename": file.filename
        })

    return jsonify({"success": False, "error": "Fichier non PDF ou invalide."})

@app.route("/delete", methods=["POST"])
def delete():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], files[0]))
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Aucun fichier à supprimer."})

@app.route("/generate/<filename>")
def generate(filename):
    try:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Appel à Groq pour générer le QCM au format JSON
        groq_output = generate_qcm_from_pdf(pdf_path)

        # Parse le JSON renvoyé par Groq
        data = json.loads(groq_output)

        # On s'assure que le format correspond bien à ce que le front-end attend
        return jsonify({
            "quiz": {
                "questions": [
                    {
                        "question": q.get("question", ""),
                        "choices": q.get("choices", []),
                        "answer": q.get("answer", "")
                    } for q in data.get("questions", [])
                ]
            },
            "success": True
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
