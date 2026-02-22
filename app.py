from flask import Flask, request, jsonify, send_file, render_template
import os
from pdf2docx import Converter
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
from pathlib import Path
import time

# ---------------------------------------------------------
# 1. Base directories
# ---------------------------------------------------------
BASEDIR = Path(__file__).resolve().parent
OUTPUTDIR = BASEDIR / "converted_files"
OUTPUTDIR.mkdir(exist_ok=True)

app = Flask(__name__, template_folder='./templates/', static_folder='./templates/static/')

# ---------------------------------------------------------
# 2. Helper: detect images in PDF
# ---------------------------------------------------------
def find_images(pdf_path):
    doc = fitz.open(pdf_path)
    image_count = 0
    for page in doc:
        images = page.get_images(full=True)
        image_count += len(images)
    return image_count, image_count > 0

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

    # Secure filename
    filename = secure_filename(file_obj.filename)
    filename_docx = Path(filename).stem + ".docx"

    # Always save inside OUTPUTDIR (which may be mounted to host Downloads)
    temp_pdf_path = OUTPUTDIR / filename
    temp_docx_path = OUTPUTDIR / filename_docx

    # Save uploaded PDF
    file_obj.save(temp_pdf_path)

    # Check for images
    img_count, _ = find_images(temp_pdf_path)

    # Convert PDF → DOCX
    cv = Converter(str(temp_pdf_path))
    cv.convert(str(temp_docx_path), start=0, end=None)
    cv.close()
    if not os.path.exists(temp_docx_path):
        return render_template(
            'convert.html',
            message="❌ Conversion failed",)
    else:
        return render_template(
            'convert.html',
            message="✅ Conversion successful",
            image_count=img_count,
            time_used_for_conversion=time.process_time(),
            download_file=temp_docx_path.name  # only filename
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
