from __future__ import print_function

from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utility import *
from conf import *
from video_parser import HighlightMaker
from bing_search import *


import os

# base_url = 'http://52.53.158.244/video/'
# base_url_original = 'http://52.53.158.244/video/original/'
# ROOT_FOLDER = '/var/www/html/caltech-ms-server/'
# VIDEOS_FOLDER = '/var/www/html/caltech-ms-server/videos/'
# EDITED_VIDEOS_FOLDER = '/var/www/html/caltech-ms-server/edited_videos/'

base_url = 'http://127.0.0.1:5000/video/'
base_url_original = 'http://127.0.0.1:5000/video/original/'
ROOT_FOLDER = './'
VIDEOS_FOLDER = './videos/'
EDITED_VIDEOS_FOLDER = './edited_videos/'

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


def speech_process(filename):
    annotations = scrape_important(filename)

    results = []
    for item in annotations:
        results.append({
            'begin': item[0],
            'topic': item[1],
            'link': item[2]
        })

    return jsonify(results=results, url=base_url_original+filename)



@app.route('/video/upload', methods=['POST'])
def video_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if Categories.ENTERTAINMENT not in request.files and Categories.SPEECH not in request.files and Categories.CLASSROOM not in request.files:
            return jsonify(
                error="No file part"
            )
        elif Categories.ENTERTAINMENT in request.files:
            category = Categories.ENTERTAINMENT
        elif Categories.SPEECH in request.files:
            category = Categories.SPEECH
        elif Categories.CLASSROOM in request.files:
            category = Categories.CLASSROOM

        f = request.files[category]

        # if user does not select file, browser also
        # submit a empty part without filename
        if f.filename == '':
            return jsonify(
                error="No selected file"
            )

        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)

            path = os.path.join(app.config['VIDEOS_FOLDER'], filename)
            f.save(path)

            if category == Categories.ENTERTAINMENT or category == Categories.SPEECH:
                process_video(filename)
                return jsonify(
                    url=base_url+filename
                )
            elif category == Categories.CLASSROOM:
                return speech_process(filename)


    return jsonify(
        error="Could not upload file"
    )



@app.route('/video/<filename>', methods=['GET'])
def retrieve_video(filename):
    dir = app.config['EDITED_VIDEOS_FOLDER']
    return send_from_directory(dir, filename)


@app.route('/video/original/<filename>', methods=['GET'])
def retrieve_original_video(filename):
    dir = app.config['VIDEOS_FOLDER']
    return send_from_directory(dir, filename)


if __name__ == '__main__':
    app.run(debug=True)

