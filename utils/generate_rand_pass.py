import random
import string

def generate_password(length=8):
    """
    Generates a random password of the specified length.

    Args:
        length: The desired length of the password (default: 8).

    Returns:
        A randomly generated password string.
    """

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password
