from flask import Flask, request
from werkzeug.utils import secure_filename
from utility import allowed_file
from flask_uploads import UploadSet, configure_uploads, IMAGES

import os

UPLOAD_FOLDER = 'videos/'

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/')
def home():
    return 'Caltech Hackathon'


@app.route('/video/upload', methods=['POST'])
def video_upload():
    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         return 'No file part'
    #
    #     file = request.files['file']
    #
    #     # if user does not select file, browser also
    #     # submit a empty part without filename
    #     if file.filename == '':
    #         return 'No selected file'
    #
    #     if file and allowed_file(file.filename):
    #         filename = photos.save(file)
    #
    #         return filename

    return "File uploaded"


if __name__ == '__main__':
    app.run(debug=True)

