import sys
import math
import ctypes
import numpy as np

import OpenGL.GL as gl
import OpenGL.GLUT as glut


# Vertex data
data = np.zeros(12, [("position", np.float32, 3), ("color", np.float32, 4)])
data["position"] = [(-0.5, +0.5, -0.5), (+0.5, +0.5, -0.5), (-0.5, +0.5, +0.5), (+0.5, +0.5, +0.5), (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5), (+0.5, +0.5, -0.5), (+0.5, -0.5, -0.5), (-0.5, +0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, +0.5, +0.5), (-0.5, -0.5, +0.5)]
data["color"] = [(0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)]

edgeData = np.zeros(12, [("position", np.float32, 3), ("color", np.float32, 4)])
edgeData["position"] = [(-0.5, +0.5, -0.5), (+0.5, +0.5, -0.5), (-0.5, +0.5, +0.5), (+0.5, +0.5, +0.5), (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5), (+0.5, +0.5, -0.5), (+0.5, -0.5, -0.5), (-0.5, +0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, +0.5, +0.5), (-0.5, -0.5, +0.5)]
edgeData["color"] = [(1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0)]

# Shader code
vertexShaderCode = """
    uniform vec3 xTransform;
    uniform vec3 yTransform;
    uniform vec3 zTransform;
    attribute vec3 position;
    attribute vec4 color;
    varying vec4 v_color;
    void main() {
        float x = position.x*xTransform.x + position.y*xTransform.y + position.z*xTransform.z;
        float y = position.x*yTransform.x + position.y*yTransform.y + position.z*yTransform.z;
        float z = position.x*zTransform.x + position.y*zTransform.y + position.z*zTransform.z;
        gl_Position = vec4(x, y, z, 1.0);
        v_color = color;
    }
"""

fragmentShaderCode = """
    varying vec4 v_color;
    void main() {
        gl_FragColor = v_color;
    }
"""

alpha = 0.0
beta = 0.0
theta = 0.0

# Matrix multiplication
finalRotationMatrix = (
    np.array([[1,0,0,0] , [0,np.cos(beta),np.sin(beta),0] , [0,-np.sin(beta),np.cos(beta),0] , [0,0,0,1]]) @
    np.array([[np.cos(theta),0,-np.sin(theta),0] , [0,1,0,0] , [np.sin(theta),0,np.cos(theta),0] , [0,0,0,1]]) @
    np.array([[np.cos(alpha),np.sin(alpha),0,0] , [-np.sin(alpha),np.cos(alpha),0,0] , [0,0,1,0] , [0,0,0,1]])
)


# Glut funcs

def reshape(width, height):

    gl.glViewport(0, 0, width, height)


def keyboard (key, x, y):

    print(key)

    global alpha
    global beta
    global theta
    global finalRotationMatrix

    if key == b'\x1b':

        #sys.exit( )

        alpha += 1 * math.pi/180
        beta += 2 * math.pi/180
        theta += 5 * math.pi/180

    elif key == b'a':
        theta -= 10 * math.pi/180

    elif key == b'd':
        theta += 10 * math.pi/180

    elif key == b's':
        beta -= 10* math.pi/180

    elif key == b'w':
        beta += 10* math.pi/180

    finalRotationMatrix = (
        np.array([[1,0,0,0] , [0,np.cos(beta),-np.sin(beta),0] , [0,np.sin(beta),np.cos(beta),0] , [0,0,0,1]]) @
        np.array([[np.cos(theta),0,-np.sin(theta),0] , [0,1,0,0] , [np.sin(theta),0,np.cos(theta),0] , [0,0,0,1]]) @
        np.array([[np.cos(alpha),-np.sin(alpha),0,0] , [np.sin(alpha),np.cos(alpha),0,0] , [0,0,1,0] , [0,0,0,1]])
    )


    display()


glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow("Rubik's Cube")
glut.glutReshapeWindow(512, 512)
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

# Preparatory stuff
Vaos = gl.glGenVertexArrays(2)
Vbos = gl.glGenBuffers(2)
posLoc = gl.glGetAttribLocation(program, "position")
colorLoc = gl.glGetAttribLocation(program, "color")
posOffset = ctypes.c_void_p(0)
colorOffset = ctypes.c_void_p(data.dtype["position"].itemsize)
dataStride = data.strides[0]
edgeDataStride = edgeData.strides[0]

# Cube itself
gl.glBindVertexArray(Vaos[0])

gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[0])
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

gl.glEnableVertexAttribArray(posLoc)
gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, dataStride, posOffset)

gl.glEnableVertexAttribArray(colorLoc)
gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, dataStride, colorOffset)

# Lines for visibility's sake
gl.glBindVertexArray(Vaos[1])

gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[1])
gl.glBufferData(gl.GL_ARRAY_BUFFER, edgeData.nbytes, edgeData, gl.GL_DYNAMIC_DRAW)

gl.glEnableVertexAttribArray(posLoc)
gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, edgeDataStride, posOffset)

gl.glEnableVertexAttribArray(colorLoc)
gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, edgeDataStride, colorOffset)

gl.glBindVertexArray(0)

def display():

    global program
    global finalRotationMatrix
    global Vbos

    xTransform = finalRotationMatrix[0,:3]
    yTransform = finalRotationMatrix[1,:3]
    zTransform = finalRotationMatrix[2,:3]

    loc = gl.glGetUniformLocation(program, "xTransform")
    gl.glUniform3f(loc, xTransform[0], xTransform[1], xTransform[2])
    loc = gl.glGetUniformLocation(program, "yTransform")
    gl.glUniform3f(loc, yTransform[0], yTransform[1], yTransform[2])
    loc = gl.glGetUniformLocation(program, "zTransform")
    gl.glUniform3f(loc, zTransform[0], zTransform[1], zTransform[2])

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    #gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[0])
    gl.glBindVertexArray(Vaos[0])
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 12)

    #gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[1])
    gl.glBindVertexArray(Vaos[1])
    gl.glDrawArrays(gl.GL_LINES, 0, 12)

    gl.glBindVertexArray(0)

    glut.glutSwapBuffers()


glut.glutDisplayFunc(display)

glut.glutMainLoop()
