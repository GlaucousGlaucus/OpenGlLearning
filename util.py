import os

import numpy as np
from PySide6.QtGui import QImage


def read_shader(mod_file_path: str, filepath: str) -> str:
    """
    Reads a shader file and returns it in string format
    :param mod_file_path: File path of the module that is calling this function
    :param filepath: Relative File path of the shader file with respect to the module calling this function
    :return: the code in the shader file in string format
    """
    mod_file_path = os.path.dirname(mod_file_path)
    filepath = os.path.join(mod_file_path, filepath)
    with open(filepath, 'r') as shader_file:
        return shader_file.read()


def q_image_to_numpy(incoming_image: QImage):
    """Converts a QImage into an opencv MAT format"""
    incoming_image = incoming_image.convertToFormat(QImage.Format.Format_RGBA8888)

    width = incoming_image.width()
    height = incoming_image.height()

    ptr = incoming_image.constBits()
    arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
    return arr[::-1]
