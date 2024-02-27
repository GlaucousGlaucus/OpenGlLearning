import ctypes
import sys
from typing import Optional

import PySide6.QtCore
import PySide6.QtGui
import numpy as np
from OpenGL.GL import *
from PySide6.QtCore import Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow, QApplication

from util import read_shader

vert_shader_code = read_shader("vertex_shader.glsl")
frag_shader_code = read_shader("fragment_shader.glsl")


class OpenGLWidget(QOpenGLWidget):
    def initializeGL(self):
        glViewport(0, 0, 800, 600)
        print("OpenGL Version:", glGetString(GL_VERSION).decode())

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)

    def keyReleaseEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        super().keyReleaseEvent(event)

    def setupGeometry(self):
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vert_shader_code)
        glCompileShader(vertex_shader)

        # Checking for compilation success
        success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not success:
            info_log = glGetShaderInfoLog(vertex_shader, 512, None)
            print(info_log)

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, frag_shader_code)
        glCompileShader(fragment_shader)

        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)

        # Checking for compilation success
        success = glGetProgramiv(shader_program, GL_LINK_STATUS)
        if not success:
            info_log = glGetProgramInfoLog(shader_program, 512, None)
            print(info_log)

        glUseProgram(shader_program)

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        vertices = np.array([
            -0.5, -0.5, 0,
            0.5, -0.5, 0,
            0, 0.5, 0
        ], dtype='float32')

        vbo = glGenBuffers(1)
        vao = glGenVertexArrays(1)

        glBindVertexArray(vao)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        stride = 3 * ctypes.sizeof(GLfloat)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        glUseProgram(shader_program)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

    def paintGL(self):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.setupGeometry()

    def resizeGL(self, w: int, h: int) -> None:
        super().resizeGL(w, h)
        glViewport(0, 0, w, h)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenGL with Qt")
        self.opengl_widget = OpenGLWidget()
        self.opengl_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCentralWidget(self.opengl_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    screen_geometry = window.screen().geometry()
    desired_geometry = (800, 600)
    window.setGeometry((screen_geometry.width()-desired_geometry[0])//2, (screen_geometry.height()-desired_geometry[1])//2,
                       *desired_geometry)
    window.show()
    sys.exit(app.exec())
