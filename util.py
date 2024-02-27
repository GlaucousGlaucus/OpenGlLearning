def read_shader(filepath: str) -> str:
    """
    Reads a shader file and returns it in string format
    :param filepath: File path of the shader file
    :return: the code in the shader file in string format
    """
    with open(filepath, 'r') as shader_file:
        return shader_file.read()