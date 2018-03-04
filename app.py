from flask import Flask, request
from werkzeug.utils import secure_filename
from utility import allowed_file

import os

UPLOAD_FOLDER = '/var/www/html/caltech-ms-server/videos/'

app = Flask(__name__)
# app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return filename

    return "File uploaded"


if __name__ == '__main__':
    app.run(debug=True)

