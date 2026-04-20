from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import PyPDF2

app = Flask(__name__)

# Configuração de upload
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/extract-text', methods=['POST'])
def extract_text():
	if 'file' not in request.files:
		return jsonify({'error': 'No file part in the request'}), 400
	file = request.files['file']
	if file.filename == '':
		return jsonify({'error': 'No selected file'}), 400
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(filepath)
		try:
			with open(filepath, 'rb') as pdf_file:
				reader = PyPDF2.PdfReader(pdf_file)
				text = ''
				for page in reader.pages:
					text += page.extract_text() or ''
			os.remove(filepath)
			return jsonify({'text': text})
		except Exception as e:
			return jsonify({'error': str(e)}), 500
	else:
		return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
	app.run(debug=True)
