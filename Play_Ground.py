import sys
import math
import ctypes
import numpy as np

import OpenGL.GL as gl
import OpenGL.GLUT as glut


# Vertex data
data = np.zeros(12, [("position", np.float32, 3)])
data["position"] = [(-0.5, +0.5, -0.5), (+0.5, +0.5, -0.5), (-0.5, +0.5, +0.5), (+0.5, +0.5, +0.5), (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5), (+0.5, +0.5, -0.5), (+0.5, -0.5, -0.5), (-0.5, +0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, +0.5, +0.5), (-0.5, -0.5, +0.5)]

# Shader code --> alpha = z-axis, theta = y-axis, beta = x-axis
vertexShaderCode = """
    uniform float alpha;
    uniform float beta;
    uniform float theta;
    attribute vec3 position;
    void main() {
        float x = (position.x * (cos(alpha)*cos(theta) + cos(alpha)*sin(theta))) + (position.y * (-sin(alpha)*cos(beta) + sin(alpha)*sin(beta)));
        float y = (position.x * (sin(alpha)*cos(theta) + sin(alpha)*sin(theta))) + (position.y * (cos(alpha)*cos(beta) - cos(alpha)*sin(beta)));
        float z = (position.z * (-sin(beta)*cos(beta)*sin(theta) + sin(beta)*cos(beta)*cos(theta)));
        gl_Position = vec4(x, y, z, 1.0);
    }
"""

fragmentShaderCode = """
    uniform vec4 color;
    void main() {
        gl_FragColor = color;
    }
"""

alpha = 0
beta = 0
theta = 0


# Glut funcs
def display():

    global program

    alphaLocation = gl.glGetUniformLocation(program, "alpha")
    betaLocation = gl.glGetUniformLocation(program, "beta")
    thetaLocation = gl.glGetUniformLocation(program, "theta")
    gl.glUniform1f(alphaLocation, alpha)
    gl.glUniform1f(betaLocation, beta)
    gl.glUniform1f(thetaLocation, theta)

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 12)

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
glut.glutDisplayFunc(display)
glut.glutReshapeFunc(reshape)
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

alphaLocation = gl.glGetUniformLocation(program, "alpha")
betaLocation = gl.glGetUniformLocation(program, "beta")
thetaLocation = gl.glGetUniformLocation(program, "theta")
gl.glUniform1f(alphaLocation, alpha)
gl.glUniform1f(betaLocation, beta)
gl.glUniform1f(thetaLocation, theta)


glut.glutMainLoop()
