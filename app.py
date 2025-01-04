from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import mimetypes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Create a directory to store uploaded files

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Here, you would add your database logic
        # to store the file information (e.g., filename, path, mimetype)
        mimetype = mimetypes.guess_type(filepath)[0]
        return jsonify({'message': 'File uploaded successfully!', 'filename': filename, 'mimetype': mimetype}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)

