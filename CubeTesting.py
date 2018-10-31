import sys
import math
import ctypes
import numpy as np

import OpenGL.GL as gl
import OpenGL.GLUT as glut



class wholeCube():

    def __init__(self, blob, blobIndices, lines, lineIndices, coordinateAxes):

        # Rotation angles
        self.blob, self.blobIndices = blob, blobIndices
        self.lines, self.lineIndices = lines, lineIndices
        self.coordinateAxes = coordinateAxes

        self.alpha, self.beta, self.theta = 0.0, 0.0, 0.0

        self.initGlut()
        self.initProgram()


    def initGlut(self):

        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
        glut.glutCreateWindow("Rubik's Cube")
        glut.glutReshapeWindow(512, 512)
        glut.glutReshapeFunc(self.reshape)
        glut.glutKeyboardFunc(self.keyboard)
        glut.glutDisplayFunc(self.display)

        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)


    def initProgram(self):

        # Shader code
        vertexShaderCode = """
            uniform vec3 angles;
            attribute vec3 position;
            attribute vec4 color;
            varying vec4 v_color;
            mat4 modelMatrix;
            mat4 viewMatrix;
            mat4 projectionMatrix;
            void main() {
                modelMatrix = mat4(1,0,0,0,  0,cos(angles.y),-sin(angles.y),0,  0,sin(angles.y),cos(angles.y),0,  0,0,0,1) *
                                   mat4(cos(angles.z),0,sin(angles.z),0,  0,1,0,0,  -sin(angles.z),0,cos(angles.z),0,  0,0,0,1) *
                                   mat4(cos(angles.x),-sin(angles.x),0,0,  sin(angles.x),cos(angles.x),0,0,  0,0,1,0,  0,0,0,1);
                viewMatrix = mat4(1,0,0,0,  0,1,0,0,  0,0,1,0,  0,0,1.5,1);
                projectionMatrix = mat4(1,0,0,0,  0,1,0,0,  0,0,1,1, 0,0,0,0);
                vec4 temporary = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
                gl_Position = temporary / temporary.w;
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

    # Glut funcs
    def reshape(self, width, height):

        gl.glViewport(0, 0, width, height)


    def keyboard(self, key, x, y):

        if key == b'\x1b':

            self.alpha += 1 * math.pi/180
            self.beta += 2 * math.pi/180
            self.theta += 5 * math.pi/180

        elif key == b'a':
            self.theta += 10 * math.pi/180

        elif key == b'd':
            self.theta -= 10 * math.pi/180

        elif key == b's':
            self.beta -= 10* math.pi/180

        elif key == b'w':
            self.beta += 10* math.pi/180

        self.display()


    def display(self):

        loc = gl.glGetUniformLocation(self.program, "angles")
        gl.glUniform3f(loc, self.alpha, self.beta, self.theta)

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.createVbosAndDraw()

        glut.glutSwapBuffers()


    # Buffer stuff
    def createVbosAndDraw(self):

        Vbos = gl.glGenBuffers(5)

        posLoc = gl.glGetAttribLocation(self.program, "position")
        colorLoc = gl.glGetAttribLocation(self.program, "color")
        posOffset = ctypes.c_void_p(0)
        colorOffset = ctypes.c_void_p(self.blob.dtype["position"].itemsize)
        blobStride = self.blob.strides[0]
        linesStride = self.lines.strides[0]
        coordinateAxesStride = self.coordinateAxes.strides[0]

        # Cube itself
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[2])
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.blobIndices.nbytes, self.blobIndices, gl.GL_DYNAMIC_DRAW)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[0])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.blob.nbytes, self.blob, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, blobStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, blobStride, colorOffset)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[2])
        gl.glDrawElements(gl.GL_TRIANGLES, self.blobIndices.size, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        # Lines for visibility's sake
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[3])
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.lineIndices.nbytes, self.lineIndices, gl.GL_DYNAMIC_DRAW)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[1])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.lines.nbytes, self.lines, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, linesStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, linesStride, colorOffset)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[3])
        gl.glDrawElements(gl.GL_LINES, self.lineIndices.size, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        # Coordinate axes
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[4])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.coordinateAxes.nbytes, self.coordinateAxes, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, coordinateAxesStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, coordinateAxesStride, colorOffset)

        gl.glDrawArrays(gl.GL_LINES, 0, 6)



if __name__ == "__main__":

    # Vertex data
    data = np.zeros(8, [("position", np.float32, 3), ("color", np.float32, 4)])
    data["position"] = [(+0.5, +0.5, +0.5), (-0.5, +0.5, +0.5), (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5), (+0.5, -0.5, -0.5), (+0.5, +0.5, -0.5), (-0.5, +0.5, -0.5), (-0.5, -0.5, -0.5)]
    data["color"] = [(1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0)]
    dataIndices = np.array([3,0,1, 3,1,2, 4,5,0, 4,0,3, 7,6,5, 7,5,4, 2,1,6, 2,6,7, 0,5,6, 0,6,1, 2,7,4, 2,4,3], dtype = np.int32)

    edgeData = np.zeros(8, [("position", np.float32, 3), ("color", np.float32, 4)])
    edgeData["position"] = [(+0.5, +0.5, +0.5), (-0.5, +0.5, +0.5), (-0.5, -0.5, +0.5), (+0.5, -0.5, +0.5), (+0.5, -0.5, -0.5), (+0.5, +0.5, -0.5), (-0.5, +0.5, -0.5), (-0.5, -0.5, -0.5)]
    edgeData["color"] = np.ones(4, dtype = np.float32)
    edgeDataIndices = np.array([0,1, 1,2, 2,3, 3,0, 4,7, 7,6, 6,5, 5,4, 0,5, 1,6, 2,7, 3,4], dtype = np.int32)

    axesData = np.zeros(6, [("position", np.float32, 3), ("color", np.float32, 4)])
    axesData["position"] = [(0.0, 0.0, 0.0), (0.8, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.8, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.8)]
    axesData["color"] = [(1.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)]


    # Final Rubik's Cube
    testCube = wholeCube(data, dataIndices, edgeData, edgeDataIndices, axesData)

    # And finally the Mainloop()
    glut.glutMainLoop()
