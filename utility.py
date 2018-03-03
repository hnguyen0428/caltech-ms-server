
import random
import string

path = 'video/'

def generate_filename(n=60):
    filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
    result = path + filename
    return result
