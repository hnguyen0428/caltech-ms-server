from __future__ import print_function

from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utility import *
import video_parser
from video_parser import HighlightMaker

import os

base_url = 'http://52.53.158.244/video/'
VIDEOS_FOLDER = '/var/www/html/caltech-ms-server/videos/'
EDITED_VIDEOS_FOLDER = '/var/www/html/caltech-ms-server/edited_videos/'

# base_url = 'http://127.0.0.1:5000/video/'
# VIDEOS_FOLDER = '/Users/hnguyen0428/Unsynced Files/CSRelated/caltech-ms-server/videos/'
# EDITED_VIDEOS_FOLDER = '/Users/hnguyen0428/Unsynced Files/CSRelated/caltech-ms-server/edited_videos/'

app = Flask(__name__)
CORS(app)

app.config['VIDEOS_FOLDER'] = VIDEOS_FOLDER
app.config['EDITED_VIDEOS_FOLDER'] = EDITED_VIDEOS_FOLDER


@app.route('/')
def home():
    return 'Caltech Hackathon'


def process_video(filename):
    hm = HighlightMaker()
    hm.extractHighlight(filename)


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

            process_video(filename)

            return jsonify(
                url=base_url+filename
            )

    return jsonify(
        error="Could not upload file"
    )


@app.route('/video/<filename>', methods=['GET'])
def retrieve_video(filename):
    dir = app.config['EDITED_VIDEOS_FOLDER']
    return send_from_directory(dir, filename)


if __name__ == '__main__':
    app.run(debug=True)

