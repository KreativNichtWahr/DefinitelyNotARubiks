from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt
import numpy as np
import math
import ctypes
import OpenGL.GL as gl

class Cube(QOpenGLWidget):


    def __init__(self, parent):

        super().__init__(parent)
        #self.initializeGL()


    def initializeGL(self):

        # Vertex data
        self.data = np.zeros(12, [("position", np.float32, 3), ("color", np.float32, 4)])
        self.data["position"] = [(-0.5, +0.5, -0.5), (+0.5, +0.5, -0.5), (-0.5, +0.5, +0.5), (+0.5, +0.5, +0.5), (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5), (+0.5, +0.5, -0.5), (+0.5, -0.5, -0.5), (-0.5, +0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, +0.5, +0.5), (-0.5, -0.5, +0.5)]
        self.data["color"] = [(0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)]

        self.edgeData = np.zeros(8, [("position", np.float32, 3), ("color", np.float32, 4)])
        self.edgeData["position"] = [(+0.5, +0.5, +0.5), (-0.5, +0.5, +0.5), (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5), (+0.5, -0.5, -0.5), (+0.5, +0.5, -0.5), (-0.5, +0.5, -0.5), (-0.5, -0.5, -0.5)]
                                #[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1], [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]
        self.edgeData["color"] = np.ones(4, dtype = np.float32)
        self.edgeDataIndices = np.array([0,1, 1,2, 2,3, 3,0, 4,7, 7,6, 6,5, 5,4, 0,5, 1,6, 2,7, 3,4], dtype = np.int32)

        # Angle values (along all three axes)
        self.alpha = 0.0
        self.beta = 0.0
        self.theta = 0.0

        # Matrix multiplication for a rotation along the three axes
        self.finalRotationMatrix = (
            np.array([[1,0,0,0] , [0,np.cos(self.beta),np.sin(self.beta),0] , [0,-np.sin(self.beta),np.cos(self.beta),0] , [0,0,0,1]]) @
            np.array([[np.cos(self.theta),0,-np.sin(self.theta),0] , [0,1,0,0] , [np.sin(self.theta),0,np.cos(self.theta),0] , [0,0,0,1]]) @
            np.array([[np.cos(self.alpha),np.sin(self.alpha),0,0] , [-np.sin(self.alpha),np.cos(self.alpha),0,0] , [0,0,1,0] , [0,0,0,1]])
        )

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

        # Compile and link shader code
        self.program = gl.glCreateProgram()
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

        gl.glAttachShader(self.program, vertexShader)
        gl.glAttachShader(self.program, fragmentShader)

        gl.glLinkProgram(self.program)
        if not gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self.program))
            raise RuntimeError("Linking error")

        gl.glDetachShader(self.program, vertexShader)
        gl.glDetachShader(self.program, fragmentShader)

        gl.glUseProgram(self.program)


        gl.glEnable(gl.GL_DEPTH_TEST)


    def resizeGL(self, width, height):

        gl.glViewport(0, 0, width, height)


    def paintGL(self):

        xTransform = self.finalRotationMatrix[0,:3]
        yTransform = self.finalRotationMatrix[1,:3]
        zTransform = self.finalRotationMatrix[2,:3]

        loc = gl.glGetUniformLocation(self.program, "xTransform")
        gl.glUniform3f(loc, xTransform[0], xTransform[1], xTransform[2])
        loc = gl.glGetUniformLocation(self.program, "yTransform")
        gl.glUniform3f(loc, yTransform[0], yTransform[1], yTransform[2])
        loc = gl.glGetUniformLocation(self.program, "zTransform")
        gl.glUniform3f(loc, zTransform[0], zTransform[1], zTransform[2])

        gl.glClear(gl.GL_COLOR_BUFFER_BIT |gl.GL_DEPTH_BUFFER_BIT)

        self.createVbos()




    # Buffer stuff - Needs to be improved via the usage of Vaos
    def createVbos(self):

        # Preparatory stuff
        Vbos = gl.glGenBuffers(3)
        posLoc = gl.glGetAttribLocation(self.program, "position")
        colorLoc = gl.glGetAttribLocation(self.program, "color")
        posOffset = ctypes.c_void_p(0)
        colorOffset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
        dataStride = self.data.strides[0]
        edgeDataStride = self.edgeData.strides[0]

        # Cube itself
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[0])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.data.nbytes, self.data, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, dataStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, dataStride, colorOffset)

        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 12)

        # Lines for visibility's sake
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[2])
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.edgeDataIndices.nbytes, self.edgeDataIndices, gl.GL_DYNAMIC_DRAW)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[1])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.edgeData.nbytes, self.edgeData, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, edgeDataStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, edgeDataStride, colorOffset)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[2])

        gl.glDrawElements(gl.GL_LINES, self.edgeDataIndices.size, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))



    # Handles the cubes rotations
    def keyboard(self, key):

        if key == Qt.Key_S:

            #sys.exit( )

            self.alpha += 1 * math.pi/180
            self.beta += 2 * math.pi/180
            self.theta += 5 * math.pi/180

        elif key == Qt.Key_Left:
            self.theta -= 10 * math.pi/180

        elif key == Qt.Key_Right:
            self.theta += 10 * math.pi/180

        elif key == Qt.Key_Down:
            self.beta -= 10* math.pi/180

        elif key == Qt.Key_Up:
            self.beta += 10* math.pi/180

        self.finalRotationMatrix = (
            np.array([[1,0,0,0] , [0,np.cos(self.beta),np.sin(self.beta),0] , [0,-np.sin(self.beta),np.cos(self.beta),0] , [0,0,0,1]]) @
            np.array([[np.cos(self.theta),0,-np.sin(self.theta),0] , [0,1,0,0] , [np.sin(self.theta),0,np.cos(self.theta),0] , [0,0,0,1]]) @
            np.array([[np.cos(self.alpha),np.sin(self.alpha),0,0] , [-np.sin(self.alpha),np.cos(self.alpha),0,0] , [0,0,1,0] , [0,0,0,1]])
        )


        self.paintGL()
