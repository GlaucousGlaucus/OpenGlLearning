import sys
from typing import Optional

import PySide6.QtCore
import PySide6.QtGui
from OpenGL.GL import *
from PySide6.QtCore import Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow, QApplication


class OpenGLWidget(QOpenGLWidget):
    def initializeGL(self):
        glViewport(0, 0, 800, 600)
        print("OpenGL Version:", glGetString(GL_VERSION).decode())

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)

    def keyReleaseEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        super().keyReleaseEvent(event)

    def setupGeometry(self):
        vertices = [
            -0.5, -0.5, 0,
            0.5, -0.5, 0,
            0, 0.5, 0
        ]
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        glBufferData(GL_ARRAY_BUFFER, len(vertices), vertices, GL_STATIC_DRAW)

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
