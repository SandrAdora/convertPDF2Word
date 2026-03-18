FROM python:3.12-slim
WORKDIR /app

# Install Tesseract OCR + language packs (English + German)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-deu \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app:app"]