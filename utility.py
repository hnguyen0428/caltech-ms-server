import random
import string

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