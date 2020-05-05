"""
Config file for env variables
"""
from os.path import join, abspath, dirname
from dotenv import load_dotenv


def set_dotenv():
    """load all variables from .env file"""
    env_path = abspath(join(dirname(__file__), '..', '.env'))

    # Load file from the path.
    load_dotenv(env_path)
