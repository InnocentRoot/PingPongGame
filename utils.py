""" Module to store some used utilities """
from settings import GAME_MODE
import os.path as path


def debug(message, message_type="INFO"):
    if (GAME_MODE == "DEBUG"):
        print(f"[{message_type}]: {message}")


def load_image(image):
    image_path = path.join(path.dirname(path.abspath(__file__)), 'images', '{0}')
    return image_path.format(image)
