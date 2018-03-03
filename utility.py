
import random
import string

path = 'videos/'

def generate_filename(n=60):
    filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))
    result = path + filename
    return result
