import random
import string


def randomDbNameGenerator():
    asciiLowerCase = ''.join(random.choice(string.ascii_lowercase) for i in range(0,2))
    asciiUpperCase = ''.join(random.choice(string.ascii_uppercase) for i in range(0,2))
    asciiLetters = ''.join(random.choice(string.ascii_letters) for i in range(0,2))
    digits = ''.join(random.choice(string.digits) for i in range(0,2))

    return '{}{}{}{}'.format(asciiLowerCase,asciiUpperCase,asciiLetters,digits)

def punctuation():
    return ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']