import os


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
