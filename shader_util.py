from typing import Tuple

import numpy as np
from OpenGL.GL import *
from loguru import logger

from util import read_shader


class Shader:

    def __init__(self, vertex_path: str, frag_path: str, module_path: str):
        """
        Initializes and compiles the vertex and fragment shaders.

        Args:
        vertex_path (str): Path to the vertex shader file.
        shader_path (str): Path to the fragment shader file.
        module_path (str): Module path used to read shader files.
        """
        vert_code = read_shader(module_path, vertex_path)
        frag_code = read_shader(module_path, frag_path)

        # Vertex shader
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vert_code)
        glCompileShader(vertex_shader)

        success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not success:
            infoLog = glGetShaderInfoLog(vertex_shader)
            logger.error("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n", infoLog)

        # Fragment shader
        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(frag_shader, frag_code)
        glCompileShader(frag_shader)

        success = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if not success:
            infoLog = glGetShaderInfoLog(frag_shader)
            logger.error("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n", infoLog)

        # Shader Program
        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, vertex_shader)
        glAttachShader(self.shader_program, frag_shader)
        glLinkProgram(self.shader_program)

        success = glGetProgramiv(self.shader_program, GL_LINK_STATUS)
        if not success:
            infoLog = glGetProgramInfoLog(self.shader_program)
            logger.error("ERROR::SHADER::PROGRAM::LINKING_FAILED\n", infoLog)

        # Delete the shaders as they are no longer required
        glDeleteShader(vertex_shader)
        glDeleteShader(frag_shader)

        logger.info(f"Shader (Vertex: '{vertex_path}' Frag: '{frag_path}') Initialized")

    def use(self):
        """
        Activates the shader program.
        """
        glUseProgram(self.shader_program)

    def set_bool(self, uniform_name: str, value: bool):
        """
        Set a boolean uniform.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        value (bool): The boolean value to set.
        """
        glUniform1i(glGetUniformLocation(self.shader_program, uniform_name), int(value))

    def set_int(self, uniform_name: str, value: int):
        """
        Set an integer uniform.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        value (int): The integer value to set.
        """
        glUniform1i(glGetUniformLocation(self.shader_program, uniform_name), value)

    def set_float(self, uniform_name: str, value: float):
        """
        Set a float uniform.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        value (float): The float value to set.
        """
        glUniform1f(glGetUniformLocation(self.shader_program, uniform_name), value)

    def set_vec2f(self, uniform_name: str, value: Tuple[float, float]):
        """
        Set a vec2 uniform value.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        value (Tuple[float, float]): The tuple of two float values to set.
        """
        glUniform2f(glGetUniformLocation(self.shader_program, uniform_name), *value)

    def set_vec3f(self, uniform_name: str, value: Tuple[float, float, float]):
        """
        Set a vec3 uniform value.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        value (Tuple[float, float, float]): The tuple of three float values to set.
        """
        glUniform3f(glGetUniformLocation(self.shader_program, uniform_name), *value)

    def set_vec4f(self, uniform_name: str, value: Tuple[float, float, float, float]):
        """
        Set a vec4 uniform value.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        value (Tuple[float, float, float, float]): The tuple of four float values to set.
        """
        glUniform4f(glGetUniformLocation(self.shader_program, uniform_name), *value)

    def set_mat2fv(self, uniform_name: str, matrix: np.ndarray):
        """
        Set a mat2 uniform value.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        matrix (np.ndarray): The 2x2 numpy array representing the matrix.
        """
        glUniformMatrix2fv(glGetUniformLocation(self.shader_program, uniform_name), 1, GL_FALSE, matrix)

    def set_mat3fv(self, uniform_name: str, matrix: np.ndarray):
        """
        Set a mat3 uniform value.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        matrix (np.ndarray): The 3x3 numpy array representing the matrix.
        """
        glUniformMatrix3fv(glGetUniformLocation(self.shader_program, uniform_name), 1, GL_FALSE, matrix)

    def set_mat4fv(self, uniform_name: str, matrix: np.ndarray):
        """
        Set a mat4 uniform value.

        Args:
        uniform_name (str): The name of the uniform variable in the shader.
        matrix (np.ndarray): The 4x4 numpy array representing the matrix.
        """
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, uniform_name), 1, GL_FALSE, matrix)
