import sys
import math
import ctypes
import numpy as np

import OpenGL.GL as gl
import OpenGL.GLUT as glut


# Vertex data
data = np.zeros(12, [("position", np.float32, 3), ("rotationAngle", np.float32, 3)])
data["position"] = [(-0.5, +0.5, -0.5), (+0.5, +0.5, -0.5), (-0.5, +0.5, +0.5), (+0.5, +0.5, +0.5), (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5), (+0.5, +0.5, -0.5), (+0.5, -0.5, -0.5), (-0.5, +0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, +0.5, +0.5), (-0.5, -0.5, +0.5)]

# Shader code
vertexShaderCode = """
    uniform xAngle;
    uniform yAngle;
    uniform zAngle;
    attribute vec3 position;
    void main() {
        float xCos = cos(xAngle)
        float xSin = sin(xAngle)
        float yCos = cos(yAngle)
        float ySin = sin(yAngle)
        float zCos = cos(zAngle)
        float zSin = sin(zAngle)
        float oldX = 
        float oldY =
        float oldZ =
        float x =
        float y =
        float z =
        gl_Position = vec4(vec3(x,y,z), 1.0);
    }
"""

fragmentShaderCode = """
    uniform vec4 color;
    void main() {
        gl_FragColor = color;
    }
"""

def display():

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 12)
    data["rotationAngle"]

    glut.glutSwapBuffers()


def reshape(width, height):

    gl.glViewport(0, 0, width, height)


def keyboard (key, x, y):
    if key == b'\x1b':
        sys.exit( )

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('Hello world!')
glut.glutReshapeWindow(512, 512)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

# Compile and link shader code
program = gl.glCreateProgram()
vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

gl.glShaderSource(vertexShader, vertexShaderCode)
gl.glShaderSource(fragmentShader, fragmentShaderCode)

gl.glCompileShader(vertexShader)
if not gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS):
    error = gl.glGetShaderInfoLog(vertexShader).decode()
    print(error)
    raise RuntimeError("Vertex shader compilation error")

gl.glCompileShader(fragmentShader)
if not gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS):
    error = gl.glGetShaderInfoLog(fragmentShader).decode()
    print(error)
    raise RuntimeError("Fragment shader compilation error")

gl.glAttachShader(program, vertexShader)
gl.glAttachShader(program, fragmentShader)

gl.glLinkProgram(program)
if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
    print(gl.glGetProgramInfoLog(program))
    raise RuntimeError("Linking error")

gl.glDetachShader(program, vertexShader)
gl.glDetachShader(program, fragmentShader)

gl.glUseProgram(program)


# Buffer stuff
buffer = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

stride = data.strides[0]
offset = ctypes.c_void_p(0)

loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, offset)


loc = gl.glGetUniformLocation(program, "color")
gl.glUniform4f(loc, 0.0, 0.0, 1.0, 1.0)


glut.glutMainLoop()
