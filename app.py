from flask import Flask, request, jsonify, send_file, render_template
import os
import tempfile
from pdf2docx import Converter
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
from pathlib import Path
import time
import pytesseract
from PIL import Image
from docx import Document

# ---------------------------------------------------------
# 1. Base directories
# ---------------------------------------------------------
OUTPUTDIR = Path(tempfile.gettempdir()) / "convertpdf2word"
OUTPUTDIR.mkdir(exist_ok=True)

app = Flask(__name__, template_folder='./templates/', static_folder='./templates/static/')

# ---------------------------------------------------------
# 2. Helpers
# ---------------------------------------------------------
def find_images(pdf_path):
    doc = fitz.open(pdf_path)
    image_count = 0
    for page in doc:
        image_count += len(page.get_images(full=True))
    doc.close()
    return image_count, image_count > 0


def is_scanned_pdf(pdf_path):
    """Returns True if the PDF has no extractable text (i.e. it is image-based)."""
    doc = fitz.open(pdf_path)
    total_text = "".join(page.get_text() for page in doc).strip()
    doc.close()
    return len(total_text) < 50


def ocr_pdf_to_docx(pdf_path, docx_path):
    """Convert a scanned (image-based) PDF to DOCX using OCR."""
    doc = fitz.open(pdf_path)
    word_doc = Document()

    for page_num in range(len(doc)):
        page = doc[page_num]
        # Render at 2x zoom for better OCR accuracy
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img)
        word_doc.add_paragraph(text)
        if page_num < len(doc) - 1:
            word_doc.add_page_break()

    doc.close()
    word_doc.save(str(docx_path))

# ---------------------------------------------------------
# 3. Convert route
# ---------------------------------------------------------
@app.route('/convert', methods=['POST'])
def convert():
    file_obj = request.files.get("myfile")

    if not file_obj:
        return jsonify({"Error": "No file uploaded"}), 400

    if not file_obj.filename.lower().endswith(".pdf"):
        return jsonify({"Error": "Only PDF files are supported"}), 400

    filename = secure_filename(file_obj.filename)
    filename_docx = Path(filename).stem + ".docx"

    temp_pdf_path = OUTPUTDIR / filename
    temp_docx_path = OUTPUTDIR / filename_docx

    file_obj.save(temp_pdf_path)

    img_count, _ = find_images(temp_pdf_path)
    scanned = is_scanned_pdf(temp_pdf_path)

    try:
        if scanned:
            ocr_pdf_to_docx(temp_pdf_path, temp_docx_path)
            method = "OCR"
        else:
            cv = Converter(str(temp_pdf_path))
            cv.convert(str(temp_docx_path), start=0, end=None)
            cv.close()
            method = "Direct"
    except Exception as e:
        return render_template('convert.html', message="❌ Conversion failed")

    if not temp_docx_path.exists():
        return render_template('convert.html', message="❌ Conversion failed")

    return render_template(
        'convert.html',
        message="✅ Conversion successful",
        image_count=img_count,
        time_used_for_conversion=round(time.process_time(), 2),
        download_file=temp_docx_path.name,
        method=method
    )

# ---------------------------------------------------------
# 4. Download route
# ---------------------------------------------------------
@app.route("/download/<path:filename>")
def download(filename):
    filename = os.path.basename(filename)
    file_path = OUTPUTDIR / filename

    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True)

# ---------------------------------------------------------
# 5. Home route
# ---------------------------------------------------------
@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

# ---------------------------------------------------------
# 6. Run app
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
