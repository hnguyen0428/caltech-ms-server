from flask import Flask, request
import utility

app = Flask(__name__)


@app.route('/')
def home():
    return 'Caltech Hackathon'


@app.route('/video/upload', methods=['POST'])
def video_upload():
    if request.method == 'POST':
        f = request.files['file']

        f.save(utility.generate_filename())
    return "process video"


if __name__ == '__main__':
    app.run()
