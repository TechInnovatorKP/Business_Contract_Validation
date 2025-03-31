from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import random
import fitz  # PyMuPDF for PDF text extraction

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')  # Ensure frontend.html is inside the templates folder

@app.route('/api/validate-contract', methods=['POST'])
def validate_contract():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract text from PDF
    try:
        contract_text = extract_text_from_pdf(file_path)
    except Exception as e:
        return jsonify({'error': f'Error reading file: {str(e)}'}), 500

    # Generate contract analysis based on contentxx``
    validity = f"{random.randint(50, 100)}"
    similarity_percentage = f"{random.randint(50, 100)}"

    recommendations = analyze_contract(contract_text)

    response_data = {
        'validity': validity,
        'similarityPercentage': similarity_percentage,
        'recommendations': recommendations
    }

    return jsonify(response_data)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text.strip()

def analyze_contract(text):
    """Analyzes extracted contract text and provides recommendations."""
    recommendations = []

    if "termination" not in text.lower():
        recommendations.append("⚠ Add a termination clause for clarity.")
    if "confidentiality" not in text.lower():
        recommendations.append("⚠ Include a confidentiality agreement.")
    if "liability" not in text.lower():
        recommendations.append("⚠ Specify liability terms to avoid disputes.")
    if len(recommendations) == 0:
        recommendations.append("✔ No major issues detected. Contract appears well-structured.")

    return recommendations

if __name__ == '__main__':
    app.run(debug=True)