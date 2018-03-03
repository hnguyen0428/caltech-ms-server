from flask import Flask, request
import utility
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def home():
    return 'Caltech Hackathon'


@app.route('/video/upload', methods=['POST'])
def video_upload():
    if request.method == 'POST':
        f = request.files['file']

        f.save(secure_filename(f.filename))
    return "process video"


if __name__ == '__main__':
    app.run()
