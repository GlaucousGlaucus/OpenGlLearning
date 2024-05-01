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
        self.shader_program = None
        self.gl = GL(self.context())
        self.array_buffer = QOpenGLBuffer()
        self.vao = QOpenGLVertexArrayObject()

    def initializeGL(self) -> None:
        super().initializeGL()
        # I have no idea what is going on
        # TODO: Have some idea about what is going on
        self.gl.initializeOpenGLFunctions()
        self.gl.glClearColor(0.2, 0.3, 0.3, 1.0)

        self.shader_program = QOpenGLShaderProgram()
        self.shader_program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex, vert_shader_code)
        self.shader_program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, frag_shader_code)
        self.shader_program.link()
        self.shader_program.bind()

        self.triangle_vertex_array = np.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0
        ], dtype="float32")
        self.array_buffer.create()
        self.vao.create()

        self.array_buffer.bind()
        self.array_buffer.allocate(self.triangle_vertex_array.tobytes(), self.triangle_vertex_array.nbytes)

        self.vao.bind()
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), None)
        self.gl.glEnableVertexAttribArray(0)

        self.shader_program.release()

    def initGeometry(self):
        """Geometry initialization goes here"""

    def resizeGL(self, w: int, h: int) -> None:
        super().resizeGL(w, h)

    def paintGL(self) -> None:
        """Rendering goes here"""
        super().paintGL()

        self.shader_program.bind()
        self.array_buffer.bind()
        self.gl.glDrawArrays(GL_TRIANGLES, 0, 3)
        self.shader_program.release()


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
