import sys

import numpy as np
from OpenGL.GL import *
from PySide6.QtCore import Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow, QApplication

from util import read_shader
from loguru import logger

vert_shader_code = read_shader(__file__, "vertex_shader.glsl")
frag_shader_code = read_shader(__file__, "fragment_shader.glsl")
frag_shader_code2 = read_shader(__file__, "fragment_shader2.glsl")


class GLWidget(QOpenGLWidget):

    def __init__(self) -> None:
        super().__init__()
        self.shader_program = None
        self.VAO = None

    def init_shaders(self):
        """Initialize the shaders"""
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vert_shader_code)
        glCompileShader(vertex_shader)

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(frag_shader, frag_shader_code)
        glCompileShader(frag_shader)

        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, vertex_shader)
        glAttachShader(self.shader_program, frag_shader)
        glLinkProgram(self.shader_program)

        frag_shader2 = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(frag_shader2, frag_shader_code2)
        glCompileShader(frag_shader2)

        self.shader_program2 = glCreateProgram()
        glAttachShader(self.shader_program2, vertex_shader)
        glAttachShader(self.shader_program2, frag_shader2)
        glLinkProgram(self.shader_program2)

        # Check for any linking errors
        success = glGetProgramiv(self.shader_program, GL_LINK_STATUS)
        if not success:
            infoLog = glGetProgramInfoLog(self.shader_program)
            logger.error("ERROR::SHADER::PROGRAM::LINKING_FAILED\n", infoLog)

        glDeleteShader(vertex_shader)
        glDeleteShader(frag_shader)

        logger.info("Shader Initialized")

    def initialize_geometry(self):
        """Initialize the geometry"""
        vertices = np.array([
            0.5, -0.5, 0.0,  # bottom right
            -0.5, -0.5, 0.0,  # bottom left
            -0.5,  0.5, 0.0,   # top left
            0.5, -0.5, 0.0,  # bottom right
            0.5, 0.5, 0.0,  # top right
            -0.5, 0.5, 0.0,  # top left
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 2,  # Triangle 1
            3, 4, 5  # Triangle 2
        ], dtype=np.uint32)

        self.VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def initializeGL(self):
        super().initializeGL()
        # Init the shaders first
        self.init_shaders()
        # Init the geometry
        self.initialize_geometry()

        # Draw in wireframe
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def resizeGL(self, w, h):
        super().resizeGL(w, h)
        glViewport(0, 0, w, h)

    def paintGL(self):
        super().paintGL()
        # Fill the viewport with this color
        glClearColor(0.3, 0.1, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Render our geometry
        glUseProgram(self.shader_program)
        glBindVertexArray(self.VAO)
        # glDrawArrays(GL_TRIANGLES, 0, 3)
        # glDrawArrays(GL_TRIANGLES, 3, 3)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        # Draw triangles Outline
        glUseProgram(self.shader_program2)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("OpenGL With Qt")
    screen_geometry = window.screen().geometry()
    desired_geometry = (800, 600)
    window.setGeometry((screen_geometry.width() - desired_geometry[0]) // 2,
                       (screen_geometry.height() - desired_geometry[1]) // 2,
                       *desired_geometry)
    window.setCentralWidget(GLWidget())
    window.show()
    sys.exit(app.exec())
