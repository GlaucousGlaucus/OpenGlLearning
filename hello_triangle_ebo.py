import ctypes
import sys

import numpy as np
from OpenGL.GL import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QOpenGLFunctions, QSurfaceFormat, QOpenGLContext
from PySide6.QtOpenGL import QOpenGLShaderProgram, QOpenGLShader, QOpenGLVertexArrayObject, QOpenGLBuffer
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow, QApplication

from util import read_shader

vert_shader_code = read_shader("vertex_shader.glsl")
frag_shader_code = read_shader("fragment_shader.glsl")


class GL(QOpenGLFunctions):

    def __init__(self, context: QOpenGLContext) -> None:
        super().__init__()
        self.context = context


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
        # Vertex data for a simple square made of two triangles

        self.initShaders()
        self.initGeometry()

    def initShaders(self):
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

        glDeleteShader(vertex_shader)
        glDeleteShader(frag_shader)

    def initGeometry(self):
        """Geometry initialization goes here"""
        self.triangle_vertex_array = np.array([
            # -0.5, -0.5, 0.0,  # Bottom left
            # 0.5, -0.5, 0.0,   # Bottom right
            # 0.5,  0.5, 0.0,   # Top right
            # -0.5,  0.5, 0.0  # Top left
            -0.5, -0.5, 0.0,  # Bottom left
            0.5, -0.5, 0.0,  # Bottom right
            0.0, 0.5, 0.0  # Top left
        ], dtype=np.float32)

        # Indices for the two triangles that compose the square
        self.indices = np.array([
            0, 1, 2,  # First triangle
            0, 2, 3   # Second triangle
        ], dtype=np.uint)

        self.vertex_array_object = glGenVertexArrays(1)
        self.array_buffer = glGenBuffers(1)

        glBindVertexArray(self.vertex_array_object)

        glBindBuffer(GL_ARRAY_BUFFER, self.array_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.triangle_vertex_array.nbytes, self.triangle_vertex_array, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def resizeGL(self, w: int, h: int) -> None:
        super().resizeGL(w, h)
        glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        """Rendering goes here"""
        super().paintGL()
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.shader_program)
        glBindVertexArray(self.vertex_array_object)
        glDrawArrays(GL_TRIANGLES, 0, 3)


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
