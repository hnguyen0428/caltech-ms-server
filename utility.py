import random
import string
import subprocess

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'wmv', 'avi'])

def allowed_file(filename):
    filename.replace(" ", "")
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_filename(extension, n=60):
    filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
    filename = filename + '.' + extension
    return filename

def extension(filename):
    i = 0
    for char in filename:
        if char == '.':
            break
        i += 1

    i += 1
    return filename[i:]


def extract_wav(filename, abs_path):
    path = abs_path + filename

    audio_filename = filename + '.wav'
    command = 'ffmpeg -i ' + path + ' -ab 160k -ac 2 -ar 44100 -vn ' + audio_filename
    subprocess.call(command, shell=True)
    return abs_path + audio_filename

