import math
import sys
import time

import numpy as np
from OpenGL.GL import *
from PySide6.QtCore import QTimer, Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication, QMainWindow
from loguru import logger

from shader_util import Shader

VERT_SHADER_PATH = "vertex_shader.glsl"
FRAG_SHADER_PATH = "fragment_shader.glsl"
FRAG_SHADER2_PATH = "fragment_shader2.glsl"


class GLWidget(QOpenGLWidget):

    def __init__(self) -> None:
        super().__init__()
        # self.shader_program = None
        self.VAO = None
        self.shader = None
        self.shader_outline = None

        self.wire_toggle = False
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.repaint_timer = QTimer()
        self.repaint_timer.setInterval(1000 // 60)  # Limit update to 60 fps
        self.repaint_timer.timeout.connect(self.update)
        self.repaint_timer.start()

        self.last_time = None

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        self.wire_toggle = False
        self.update()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_1:
            self.wire_toggle = True
            self.update()

    def init_shaders(self):
        """Initialize the shaders"""
        self.shader = Shader(VERT_SHADER_PATH, FRAG_SHADER_PATH, __file__)
        self.shader_outline = Shader(VERT_SHADER_PATH, FRAG_SHADER2_PATH, __file__)

    def initialize_geometry(self):
        """Initialize the geometry"""
        vertices = np.array([
            0.5, -0.5, 0.0, 1.0, 0.0, 0.0,  # bottom right
            -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,  # bottom left
            -0.5,  0.5, 0.0, 0.0, 0.0, 1.0,   # top left
            0.5, -0.5, 0.0, 1.0, 0.0, 0.0,  # bottom right
            0.5, 0.5, 0.0, 0.0, 1.0, 0.0,  # top right
            -0.5, 0.5, 0.0, 0.0, 0.0, 1.0  # top left
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

        stride = 6 * ctypes.sizeof(GLfloat)
        # Vertex attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, None)
        glEnableVertexAttribArray(0)
        # Color attribute
        offset = ctypes.c_void_p(3 * ctypes.sizeof(GLfloat))
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, offset)
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def initializeGL(self):
        super().initializeGL()
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glEnable(GL_BLEND)
        # Init the shaders first
        self.init_shaders()
        # Init the geometry
        self.initialize_geometry()

        # Draw in wireframe
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Get the max vertex attributes available, normally 16
        max_vertex_attributes = glGetIntegerv(GL_MAX_VERTEX_ATTRIBS)
        logger.info(f"Max Vertex Attributes: {max_vertex_attributes}")

    def resizeGL(self, w, h):
        super().resizeGL(w, h)
        glViewport(0, 0, w, h)

    def paintGL(self):
        super().paintGL()
        self.shader: Shader
        self.shader_outline: Shader
        # Fill the viewport with this color
        glClearColor(0.3, 0.1, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Render our geometry
        time_val = time.time()
        self.last_time = time_val
        col_value = abs(math.sin(time_val))

        self.shader.use()
        vec_4f = (1 / col_value, col_value, 1 - col_value, 1.0)
        self.shader.set_vec4f("factor", vec_4f)
        self.shader.set_float("alpha", abs(math.sin(time_val)))

        glBindVertexArray(self.VAO)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        # Draw triangles Outline
        if self.wire_toggle:
            self.shader_outline.use()
            vec_4f = (1 / col_value, col_value, 1 - col_value, 1.0)
            self.shader_outline.set_vec4f("factor", vec_4f)
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
