import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, flash, redirect
from flask_cors import CORS, cross_origin
from waitress import serve
from .agents import LearningAssistant
root = os.path.dirname(__file__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

load_dotenv(override=True)
together_api_key = os.getenv("TOGETHER_API_KEY")

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'

logging.getLogger('flask_cors').level = logging.DEBUG


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def hello_world():
    return  "hello world"


@app.route('/api/start', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin(origin='*', headers=['Access-Control-Allow-Origin' ])
def start():
    try:

        if 'file' not in request.files:
            return None
        
        file = request.files['file']

        if file.filename == '':
            return None
        
        file_path = os.path.join(root, app.config['UPLOAD_FOLDER'], file.filename)

        if file and allowed_file(file.filename):
            file.save(file_path)
    
        assistant = LearningAssistant()
        extracted_text = assistant.start_process(file_path)
        print(extracted_text)
        return jsonify({"text": extracted_text}), 200

    except Exception as e:
        logging.exception(f"Error in recommendation process: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


    
if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    serve(app, host="0.0.0.0", port=5000)

    # app.run(debug=True, host='0.0.0.0', port=5000)