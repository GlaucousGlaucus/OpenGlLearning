import glfw
from OpenGL.GL import *
import numpy as np

# settings
SCR_WIDTH = 800
SCR_HEIGHT = 600

vertexShaderSource = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

fragmentShaderSource = """
#version 330 core
out vec4 FragColor;
void main()
{
   FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def main():
    # glfw: initialize and configure
    if not glfw.init():
        print("Failed to initialize GLFW")
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # glfw window creation
    window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # build and compile our shader program
    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader, vertexShaderSource)
    glCompileShader(vertexShader)

    fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragmentShader, fragmentShaderSource)
    glCompileShader(fragmentShader)

    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, fragmentShader)
    glLinkProgram(shaderProgram)

    # check for linking errors
    success = glGetProgramiv(shaderProgram, GL_LINK_STATUS)
    if not success:
        infoLog = glGetProgramInfoLog(shaderProgram)
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

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # render loop
    while not glfw.window_should_close(window):
        # input
        processInput(window)

        # render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # draw our first triangle
        glUseProgram(shaderProgram)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        glfw.swap_buffers(window)
        glfw.poll_events()

    # de-allocate all resources once they've outlived their purpose
    glDeleteVertexArrays(1, VAO)
    glDeleteBuffers(1, VBO)
    glDeleteBuffers(1, EBO)
    glDeleteProgram(shaderProgram)

    # glfw: terminate, clearing all previously allocated GLFW resources.
    glfw.terminate()

if __name__ == "__main__":
    main()
