import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from app import app
from system_module_1 import DataIngestion


@app.route('/file_upload', methods=['POST'])
def upload_file():
    """
    Upload a file to the server.
    """
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        # If the user does not select a file, the browser also submits an empty part without a filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and DataIngestion.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            DataIngestion(file_path)
            return jsonify({'message': 'File uploaded successfully'})
        else:
            return jsonify({'error': 'File type not allowed'})


@app.route('/get_data', methods=['GET'])
def get_data():
    """
    Get data from the ingested CSV file.
    """
    df = pd.read_csv(DataIngestion.get_path())
    return df.to_json(orient='records')


