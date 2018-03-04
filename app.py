from flask import Flask, request
from werkzeug.utils import secure_filename
from utility import *

import os

VIDEOS_FOLDER = '/var/www/html/caltech-ms-server/videos/'

app = Flask(__name__)
# app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER
app.config['VIDEOS_FOLDER'] = VIDEOS_FOLDER


@app.route('/')
def home():
    return 'Caltech Hackathon'


@app.route('/video/upload', methods=['POST'])
def video_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            ext = extension(file.filename)
            filename = generate_filename(ext)

            path = os.path.join(app.config['VIDEOS_FOLDER'], filename)
            file.save(path)

            audio_filename = extract_wav(filename, app.config['VIDEOS_FOLDER'])

            return filename, audio_filename

    return "File uploaded"


if __name__ == '__main__':
    app.run(debug=True)

