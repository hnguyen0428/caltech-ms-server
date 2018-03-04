from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from utility import *

import os

base_url = 'http://18.144.27.216/video/'
VIDEOS_FOLDER = '/var/www/html/caltech-ms-server/videos/'
EDITED_VIDEOS_FOLDER = '/var/www/html/caltech-ms-server/edited_videos/'

app = Flask(__name__)
app.config['VIDEOS_FOLDER'] = VIDEOS_FOLDER
app.config['EDITED_VIDEOS_FOLDER'] = EDITED_VIDEOS_FOLDER


@app.route('/')
def home():
    return 'Caltech Hackathon'


@app.route('/video/upload', methods=['POST'])
def video_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(
                error="No file part"
            )

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return jsonify(
                error="No selected file"
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            path = os.path.join(app.config['VIDEOS_FOLDER'], filename)
            file.save(path)

            return jsonify(
                url=base_url+filename
            )

    return jsonify(
        error="Could not upload file"
    )


@app.route('/video/<filename>', methods=['GET'])
def retrieve_video(filename):
    dir = app.config['VIDEOS_FOLDER']
    return send_from_directory(dir, filename)


if __name__ == '__main__':
    app.run(debug=True)

