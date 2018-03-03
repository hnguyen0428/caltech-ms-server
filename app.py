from flask import Flask, request
from werkzeug.utils import secure_filename

import os


app = Flask(__name__)


@app.route('/')
def home():
    return 'Caltech Hackathon'


@app.route('/video/upload', methods=['POST'])
def video_upload():
    if request.method == 'POST':
        f = request.files['file']

        filename = secure_filename(f.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basedir, filename)
        print(path)
        f.save(path)
    return "process video"


if __name__ == '__main__':
    app.run()
