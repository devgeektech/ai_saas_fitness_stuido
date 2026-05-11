from django.core.mail import EmailMessage
import random
import string
import logging
logger = logging.getLogger(__name__)



# Generate random string
def generate_random_string(length):
    try:
        letters = string.ascii_letters
        code = "".join(random.choice(letters) for i in range(length))
        return code
    except Exception as ex:
        return None
    