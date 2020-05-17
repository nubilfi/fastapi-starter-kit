"""
Just a utils function
"""
import random
import string


def random_lower_string() -> str:
    """generate random lowercase str"""
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    """generate a random email"""
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_username() -> str:
    """generate a random username"""
    return random_lower_string()
