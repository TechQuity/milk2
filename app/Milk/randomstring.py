import string
import random
def id_generator(size=14, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
