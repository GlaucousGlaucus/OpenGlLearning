import ctypes
import sys

import numpy as np
from OpenGL.GL import *
from PySide6.QtCore import Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow, QApplication

from util import read_shader

vert_shader_code = read_shader("vertex_shader.glsl")
frag_shader_code = read_shader("fragment_shader.glsl")


class GLWidget(QOpenGLWidget):

    def __init__(self) -> None:
        super().__init__()
        self.triangle_vertex_array = None
        self.indices = None
        self.shader_program = None
        self.array_buffer = None
        self.index_buffer = None
        self.vertex_array_object = None

    def initializeGL(self) -> None:
        super().initializeGL()
        # build and compile our shader program
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, vert_shader_code)
        glCompileShader(vertexShader)

        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, frag_shader_code)
        glCompileShader(fragmentShader)

        self.shaderProgram = glCreateProgram()
        glAttachShader(self.shaderProgram, vertexShader)
        glAttachShader(self.shaderProgram, fragmentShader)
        glLinkProgram(self.shaderProgram)

        # check for linking errors
        success = glGetProgramiv(self.shaderProgram, GL_LINK_STATUS)
        if not success:
            infoLog = glGetProgramInfoLog(self.shaderProgram)
            print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n", infoLog)

        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)

        # set up vertex data (and buffer(s)) and configure vertex attributes
        vertices = np.array([
            0.5,  0.5, 0.0,  # top right
            0.5, -0.5, 0.0,  # bottom right
            -0.5, -0.5, 0.0,  # bottom left
            -0.5,  0.5, 0.0   # top left
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 3,  # first Triangle
            1, 2, 3   # second Triangle
        ], dtype=np.uint32)

        self.VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def resizeGL(self, w: int, h: int) -> None:
        super().resizeGL(w, h)
        glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        """Rendering goes here"""
        super().paintGL()
        # render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # draw our first triangle
        glUseProgram(self.shaderProgram)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OpenGL with Qt")
        self.opengl_widget = GLWidget()
        self.opengl_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCentralWidget(self.opengl_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    screen_geometry = window.screen().geometry()
    desired_geometry = (800, 600)
    window.setGeometry((screen_geometry.width() - desired_geometry[0]) // 2,
                       (screen_geometry.height() - desired_geometry[1]) // 2,
                       *desired_geometry)
    window.show()
    sys.exit(app.exec())
