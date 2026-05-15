"""
Flask web application for the AI Text Humanizer.

Supports:
  - Paste plain text with typing simulator for Google Docs
  - Upload a .docx file and download a cleaned, humanized .docx
"""

import os
import uuid
import random
import tempfile
from datetime import datetime, timedelta

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
)
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT

from humanizer import humanize_text, humanize_text_with_stats

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "humanizer_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def clean_docx_metadata(doc):
    """
    Strip metadata that reveals the document was machine-generated.

    Google Docs and auditing extensions check:
    - Application name (e.g. "python-docx")
    - Creator / last modified by
    - Revision count
    - Creation / modification timestamps
    - Custom properties
    """
    props = doc.core_properties

    props.author = ""
    props.last_modified_by = ""
    props.comments = ""
    props.category = ""
    props.subject = ""
    props.keywords = ""
    props.description = ""
    props.content_status = ""
    props.identifier = ""
    props.language = "en-US"
    props.version = ""

    now = datetime.utcnow()
    writing_duration = timedelta(
        hours=random.randint(1, 8),
        minutes=random.randint(0, 59),
    )
    props.created = now - writing_duration
    props.modified = now - timedelta(minutes=random.randint(1, 30))

    props.revision = random.randint(15, 80)

    return doc


def strip_tracked_changes(doc):
    """Remove any tracked changes / revision marks from the document."""
    try:
        from lxml import etree
        nsmap = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        }
        body = doc.element.body

        for tag in ['w:ins', 'w:del', 'w:rPrChange', 'w:pPrChange',
                    'w:sectPrChange', 'w:tblPrChange']:
            for elem in body.findall('.//' + tag, nsmap):
                parent = elem.getparent()
                if parent is not None:
                    if tag == 'w:ins':
                        for child in list(elem):
                            parent.insert(list(parent).index(elem), child)
                    parent.remove(elem)
    except Exception:
        pass

    return doc


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
    result = humanize_text_with_stats(text, intensity=intensity)
    return jsonify(result)


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

        doc = clean_docx_metadata(doc)
        doc = strip_tracked_changes(doc)

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
