# 🐳 Option 1 — Run with Docker (Recommended) 
Recommended for Developers. This is the easiest way to run the app. No Python installation required. 

## 1. Clone the repository 
```bash 
git clone https://github.com/SandrAdora/convertPDF2Word.git cd convertPDF2Word
```
## 2. Build Docker 
```bash
docker build -t pdf2word .
```
## 3. Run the Container 
```bash 
docker run -p 5001:5001 \
  -v ~/Downloads:/app/converted_files \
  pdf2word
```
## 4. Open the App 
```bash
http://localhost:5001
```
Converted files will appear in the downloads folder

# 🖥️ Option 2 — Run Locally (Without Docker)
For developers or users who prefer running the app directly.
### Prerequites
0. have an [IDE](https://code.visualstudio.com/download) installed
1. Have [Python](https://www.python.org/downloads/) installed
2. have [pip](https://pypi.org/project/pip/) installed


## Build app
```bash
git clone https://github.com/SandrAdora/convertPDF2Word.git
cd convertPDF2Word

```
## Create a virtual environment 
### Windows 
```bash 
# creates a virtual environment called my virt environment
python -m venv <my-virt-envrionment>

# activate virt environment
virt-env\Scripts\activate

# install the requirements
pip install -r requirements.txt

# run app 
python app.py
```
### LINUX
```bash 
# creates a virtual environment called my virt environment
python3 -m venv <my-virt-envrionment>

# activate virtual envirnment
source my-virt-environment/bin/acivate

# install requirements 
pip install -r requirements.txt

```
### open app 
[* localhost:5001](http://localhost:5001)

### Location of converted files 
converted_files/
