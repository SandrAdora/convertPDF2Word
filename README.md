
# 📄 convertPDF2Word — PDF → DOCX Converter (Flask + Python)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-App-000000?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Stars](https://img.shields.io/github/stars/SandrAdora/convertPDF2Word?style=social)
![Forks](https://img.shields.io/github/forks/SandrAdora/convertPDF2Word?style=social)

A lightweight web application that converts PDF files into editable Word documents (`.docx`).  
Built with **Flask**, **PyMuPDF**, and **pdf2docx**, and fully containerized with **Docker** for easy deployment.

---

## Key Features

- Convert any PDF into a `.docx` file  
- Detects number of images inside the PDF  
- Clean web interface (HTML templates included)  
- Works locally or inside Docker  
- Supports saving output directly into the user’s **Downloads** folder  
- Fast, reliable conversion using `pdf2docx` and `PyMuPDF`

---

## 🚀 App Features

* Upload one or multiple PDF files
* Optional custom output path
* Fast server‑side conversion
* Clean neon‑glow UI with loading animations
* Download converted files instantly
* Automatic return to the homepage after download

## How it works

### 1. Upload your PDF

* Click the Upload Your PDF file field
* Select one or more .pdf files* (Optional) Enter a custom output path
* Start the conversion

### 2. Click 📄 Convert File

* The app hides the form and shows a Loading… screen
* The server processes your file(s)

### 3. View the conversion status

* After processing, you’ll see:
* Conversion message
* Number of images extracted
* Time used for conversion
* A Download button

### 4. Download your Word file

* Click 📥 Download file
* Your .docx file downloads immediately

After a short delay, the app automatically returns to the homepage


## 🛠️ Tech Stack
## Layer Technology

* Backend:
	
   * Python, 
   * Flask

### Frontend:

* HTML, 
* TailwindCSS, 
* FontAwesome

### libaries: 

* pymupdf -> used to search images in pdf- files
* pdf2docx -> used to convert pdf to docx

### UX:

* Neon glow effects, 
* blur backgrounds, 
* loading states

## Running the App Locally 

1. Clone the repository: 
```bash
git clone https://github.com/SandrAdora/convertPDF2Word.git
cd pdf-to-word-converter
``` 
2. Install Dependencies:
```bash 
pip install -r requirements.txt
```
3. Start the flask server:
```bash
python app.py
```
4. Open your Browser and type in your url:
```bash
localhost:5000
```

## 🧪 Example Workflow

Upload example.pdf

Click Convert

Watch the loading animation

Download example.docx

Automatically return to the homepage

## 🛡️ Notes & Limitations
Conversion quality depends on the PDF structure

Very large PDFs may take longer

Complex layouts (tables, forms) may require manual cleanup


# Application: PDF To DOCX Converter 

<img width="1914" height="938" alt="2026-02-15" src="https://github.com/user-attachments/assets/eb5a974f-33b2-48d4-bfe3-4702aa61fbc1" />

