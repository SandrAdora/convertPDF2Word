from flask import Flask, request, jsonify, send_file, render_template
import os
from pdf2docx import Converter
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
from pathlib import Path
import time

app = Flask(__name__, template_folder='./templates/', static_folder='./templates/static/')
downloads_path = Path.home() / "Downloads"


def find_images(pdf_path):
    """Check if PDF has images and return (count, has_images)"""
    doc = fitz.open(pdf_path)
    image_count = 0
    for page in doc:
        images = page.get_images(full=True)
        image_count += len(images)
    return image_count, image_count > 0
    
@app.route('/convert', methods=['POST'])
def convert():
    file_obj = request.files.get("myfile")
    destpath = request.form.get("destPath")

    if not file_obj:
        return jsonify({"Error": "No file uploaded"}), 400

    if not file_obj.filename.lower().endswith(".pdf"):
        return jsonify({"Error": "Only PDF files are supported"}), 400

    # Secure filename
    filename = secure_filename(file_obj.filename)
    filename_docx, _ = os.path.splitext(filename)
    
    # if user does not specify a storage path 
    # default path C-Downloadsfolder
    if not destpath:
        destpath = downloads_path
    
    # Ensure destination folder exists if specified 
    if destpath and not os.path.exists(destpath):
        os.makedirs(destpath)

    # Save uploaded PDF and docx file temporarily 
    
    temp_pdf_path = os.path.join(destpath, filename)
    file_obj.save(temp_pdf_path)
    filename_docx = filename_docx+'.docx'
    temp_docx_path = os.path.join(destpath, filename_docx)

    # Check for images
    img_count, _ = find_images(temp_pdf_path)

    # Convert PDF → DOCX
    cv = Converter(temp_pdf_path)
    cv.convert(temp_docx_path, start=0, end=None)  
    cv.close()
    if temp_docx_path:
        return render_template(
            'convert.html',
            message=" ✅ Conversion successful",
            image_count=img_count,
            time_used_for_conversion=time.process_time(),
            download_file=temp_docx_path
        )
    else:
        return render_template(
            'convert.html',
            message="❌ Conversion Failure "
        )

@app.route("/download/<path:filename>")
def download(filename):
    destpath = request.form.get("destPath")
    if not destpath:
        return send_file(filename, as_attachment=True)
    else:
        filename = os.path.basename(filename)
        return send_file(os.path.join(destpath, filename), as_attachment=True)

def refresh_page():
    return request.args.get("download-clicked")

@app.route("/", methods=['GET'])
def home():
    """This is the root"""
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)
