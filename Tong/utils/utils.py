import string, random


def code_generator(size=6, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

def stripforurl(string):
    return ''.join(i for i in string if i.isalnum())