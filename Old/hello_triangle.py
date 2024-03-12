import ctypes
import sys

import numpy as np
from OpenGL.GL import *
from PySide6.QtCore import Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow, QApplication

from util import read_shader

vert_shader_code = read_shader("../vertex_shader.glsl")
frag_shader_code = read_shader("../fragment_shader.glsl")


class GLWidget(QOpenGLWidget):

    def __init__(self) -> None:
        super().__init__()

        self.frag_shader = None
        self.shader_program = None
        self.vertex_shader = None
        self.vao = None
        self.triangle_vertex_array = None
        self.vbo = None

    def initializeGL(self) -> None:
        glViewport(0, 0, 800, 600)
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.loadShaders()
        self.initGeometry()

    def resizeGL(self, w: int, h: int) -> None:
        super().resizeGL(w, h)
        glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        """Rendering goes here"""
        super().paintGL()

        glUseProgram(self.shader_program)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

    def initGeometry(self):
        """Geometry initialization goes here"""
        self.triangle_vertex_array = np.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0
        ], dtype="float32")

        # Create a VBO and store the data in it
        self.vbo = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.triangle_vertex_array.nbytes, self.triangle_vertex_array, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def loadShaders(self):
        self.vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vertex_shader, vert_shader_code)
        glCompileShader(self.vertex_shader)

        if not glGetShaderiv(self.vertex_shader, GL_COMPILE_STATUS):
            print("Compile shader Error:", glGetShaderInfoLog(self.vertex_shader))
        else:
            print("Vertex Shader Loaded")

        self.frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.frag_shader, frag_shader_code)
        glCompileShader(self.frag_shader)

        if not glGetShaderiv(self.frag_shader, GL_COMPILE_STATUS):
            print("Compile shader Error:", glGetShaderInfoLog(self.frag_shader))
        else:
            print("Fragment Shader Loaded")

        # Load the shader program

        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, self.vertex_shader)
        glAttachShader(self.shader_program, self.frag_shader)
        glLinkProgram(self.shader_program)

        if not glGetProgramiv(self.shader_program, GL_LINK_STATUS):
            print("Link Program Error:", glGetProgramInfoLog(self.shader_program, 512, None))
        else:
            print("Shader Program Loaded")

        # Use Shader Program and delete shaders as they are not needed anymore
        glDeleteShader(self.vertex_shader)
        glDeleteShader(self.frag_shader)


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
