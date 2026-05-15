"""
Flask web application for the AI Text Humanizer.

Supports:
  - Paste plain text and get humanized output
  - Upload a .docx file and download a humanized .docx
"""

import os
import uuid
import tempfile

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
)
from docx import Document

from humanizer import humanize_text

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "humanizer_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/humanize-text", methods=["POST"])
def humanize_text_api():
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Text is empty"}), 400

    intensity = float(data.get("intensity", 0.5))
    result = humanize_text(text, intensity=intensity)
    return jsonify({"result": result})


@app.route("/api/humanize-docx", methods=["POST"])
def humanize_docx_api():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename or not file.filename.lower().endswith(".docx"):
        return jsonify({"error": "Please upload a .docx file"}), 400

    intensity = float(request.form.get("intensity", 0.5))

    uid = uuid.uuid4().hex
    input_path = os.path.join(UPLOAD_DIR, f"{uid}_input.docx")
    output_path = os.path.join(UPLOAD_DIR, f"{uid}_output.docx")
    file.save(input_path)

    try:
        doc = Document(input_path)
        for para in doc.paragraphs:
            if para.text.strip():
                humanized = humanize_text(para.text, intensity=intensity)
                if para.runs:
                    para.runs[0].text = humanized
                    for run in para.runs[1:]:
                        run.text = ""
                else:
                    para.text = humanized

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        if para.text.strip():
                            humanized = humanize_text(para.text, intensity=intensity)
                            if para.runs:
                                para.runs[0].text = humanized
                                for run in para.runs[1:]:
                                    run.text = ""
                            else:
                                para.text = humanized

        doc.save(output_path)
    except Exception as e:
        return jsonify({"error": f"Failed to process document: {str(e)}"}), 500
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

    original_name = os.path.splitext(file.filename)[0]
    return send_file(
        output_path,
        as_attachment=True,
        download_name=f"{original_name}_humanized.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
