import sys
import math
import ctypes
import numpy as np

import OpenGL.GL as gl
import OpenGL.GLUT as glut



class wholeCube():

    def __init__(self, objectIndices, lineIndices, coordinateAxes, listWithCubies):

        # Set important variables and launch both init funcs
        self.lineIndices = lineIndices
        self.objectIndices = objectIndices
        self.coordinateAxes = coordinateAxes
        self.listWithCubies = np.array([*listWithCubies])
        self.cubeSideOrder = np.arange(27).reshape(3,3,3)
        for i in range(27):
            self.cubeSideOrder[i//9][(i - i%3 - 2*(i//3))%3][2-i%3] = i
        self.whatCubesToRotate = np.array([])
        self.multQuat = np.array([0.0,0.0,0.0,0.0], dtype = np.float32)
        #self.xRotPos, self.yRotPos, self.zRotPos = 0,1,2
        #self.angles = [0.0, 0.0, 0.0]
        #self.difStartPosXRot, self.difStartYRot, self.difStartZRot = 0.0, 0.0, 0.0
        self.sideIsAboutToRotate = False
        #self.aroundWhichAxis = 0
        #self.whichSideTurned = ""
        self.initGlut()
        self.initProgram()


    def initGlut(self):

        # Glut init
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH)
        glut.glutCreateWindow("Rubik's Cube")
        glut.glutReshapeWindow(512, 512)
        glut.glutReshapeFunc(self.reshape)
        glut.glutKeyboardFunc(self.keyboard)
        glut.glutDisplayFunc(self.display)
        # Depth / Cull init
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDepthFunc(gl.GL_LESS)
        #gl.glDepthRange(-1.0, 1.0)
        #gl.glEnable(gl.GL_CULL_FACE)
        #gl.glCullFace(gl.GL_BACK)

    def initProgram(self):

        # Shader code
        vertexShaderCode = """
            attribute vec3 position;
            attribute vec4 color;
            varying vec4 v_color;
            mat4 viewMatrix;
            mat4 projectionMatrix;
            void main() {
                viewMatrix = mat4(1,0,0,0,  0,1,0,0,  0,0,1,0,  0,0,-4.5,1);
                projectionMatrix = mat4(1,0,0,0,  0,1,0,0,  0,0,0,-1, 0,0,-1.5,0);
                vec4 temporary = projectionMatrix * viewMatrix * vec4(position, 1.0);
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

        """
        # Left
        if key == b'a':

            self.angles[1] -= 10 * math.pi/180

        # Right
        elif key == b'd':

            self.angles[1] += 10 * math.pi/180
        """

        # Down
        if key == b's':

            print(self.listWithCubies)
            betraege = []
            listWithQuats = self.vertexToQuat(self.listWithCubies, betraege)
            self.multQuat = np.array([1.0,0.0,0.0,0.0], dtype = np.float32)
            listWithMultQuats = self.quatMult(listWithQuats, self.multQuat)
            self.quatToVertex(self.listWithCubies, listWithMultQuats, betraege)
            print(self.listWithCubies)
            self.display()
            #self.angles[0] += 10* math.pi/180

            #if abs(self.angles[0] - self.difStartPosXRot) > math.pi/4:
            #    self.angles.append(self.angles[1])
            #    self.angles.pop(1)
            #    temp = self.yRotPos
            #    self.yRotPos = self.zRotPos
            #    self.zRotPos = temp
            #    self.difStartPosXRot += math.pi/2

        """
        # Up
        elif key == b'w':

            self.angles[0] -= 10* math.pi/180

            if abs(self.angles[0] - self.difStartPosXRot) > math.pi/4:
                self.angles.append(self.angles[1])
                self.angles.pop(1)
                temp = self.yRotPos
                self.yRotPos = self.zRotPos
                self.zRotPos = temp
                self.difStartPosXRot -= math.pi/2

        elif key == b'f':

            self.sideIsAboutToRotate = True
            self.whichSideTurned = "f"

            self.cubeSideOrder[0] = np.rot90(self.cubeSideOrder[0], 3)
            self.whatCubesToRotate = self.cubeSideOrder[0]

            self.aroundWhichAxis = 2

        elif key == b't':


            self.sideIsAboutToRotate = True
            self.whichSideTurned = "t"

            self.cubeSideOrder = np.rot90(self.cubeSideOrder, 3, axes = (0,1))
            self.cubeSideOrder[0] = np.rot90(self.cubeSideOrder[0], 3)
            self.whatCubesToRotate = self.cubeSideOrder[0]
            self.cubeSideOrder = np.rot90(self.cubeSideOrder, axes = (0,1))

            #for i in [x for x in self.listWithCubies if np.where(x == self.listWithCubies)[0][0] in self.whatCubesToRotate]:
            #    i["axisInverted"][0] = True

            self.aroundWhichAxis = 1

        elif key == b'r':

            self.sideIsAboutToRotate = True
            self.cubeSideOrder = np.rot90(self.cubeSideOrder, axes = (0,2))
            self.cubeSideOrder[0] = np.rot90(self.cubeSideOrder[0], 3)
            self.whatCubesToRotate = self.cubeSideOrder[0]

            self.cubeSideOrder = np.rot90(self.cubeSideOrder, 3, axes = (0,2))
            print(self.cubeSideOrder)
            self.aroundWhichAxis = 0


        elif key == b'k':

            self.sideIsAboutToRotate = True
            self.whatCubesToRotate = self.cubeSideOrder[0]
            self.aroundWhichAxis = 2

        self.display()
        """

    def display(self):

        #loc = gl.glGetUniformLocation(self.program, "angles")
        #gl.glUniform3f(loc, self.angles[self.xRotPos], self.angles[self.yRotPos], self.angles[self.zRotPos])
        """
        if self.sideIsAboutToRotate:

            for _ in range(18):
                for i in [x for x in self.listWithCubies if np.where(x == self.listWithCubies)[0][0] in self.whatCubesToRotate]:
                    for e in i["animationAngles"]:
                        #print(i["animationAngles"])
                        e[self.aroundWhichAxis] += math.pi/36

                gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

                for i in self.listWithCubies:
                    self.drawCubies(i)
                self.drawAxes()

                glut.glutSwapBuffers()
        """
        #else:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        #gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        #gl.glClearDepth(1.0)
        for i in self.listWithCubies:
            print(i)
            self.drawCubies(i)

        self.drawAxes()

        glut.glutSwapBuffers()

        self.sideIsAboutToRotate = False

    # Buffer stuff
    def drawCubies(self, objectToDraw, outLines = True):

        Vbos = gl.glGenBuffers(4)

        posLoc = gl.glGetAttribLocation(self.program, "position")
        colorLoc = gl.glGetAttribLocation(self.program, "color")
        #angleLoc = gl.glGetAttribLocation(self.program, "animationAngles")
        posOffset = ctypes.c_void_p(0)
        colorOffset = ctypes.c_void_p(objectToDraw.dtype["position"].itemsize)
        #angleOffset = ctypes.c_void_p(objectToDraw.dtype["position"].itemsize + objectToDraw.dtype["color"].itemsize)

        objectStride = objectToDraw.strides[0]

        # Cube itself
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[0])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, objectToDraw.nbytes, objectToDraw, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, objectStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, objectStride, colorOffset)

        #gl.glEnableVertexAttribArray(angleLoc)
        #gl.glVertexAttribPointer(angleLoc, 3, gl.GL_FLOAT, False, objectStride, angleOffset)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, objectToDraw.size)

        """"
        if not outLines:

            outlines = np.zeros(8, [("position", np.float32, 3), ("color", np.float32, 4)])
            outlines["position"] = objectToDraw["position"]
            outlines["color"] = np.ones(4, dtype = np.float32)

            # Lines for visibility's sake
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[3])
            gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.lineIndices.nbytes, self.lineIndices, gl.GL_DYNAMIC_DRAW)

            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[1])
            gl.glBufferData(gl.GL_ARRAY_BUFFER, outlines.nbytes, outlines, gl.GL_DYNAMIC_DRAW)

            gl.glEnableVertexAttribArray(posLoc)
            gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, objectStride, posOffset)

            gl.glEnableVertexAttribArray(colorLoc)
            gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, objectStride, colorOffset)

            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[3])
            gl.glDrawElements(gl.GL_LINES, self.lineIndices.size, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        """

    def drawAxes(self):

        Vbo = gl.glGenBuffers(1)

        posLoc = gl.glGetAttribLocation(self.program, "position")
        colorLoc = gl.glGetAttribLocation(self.program, "color")
        posOffset = ctypes.c_void_p(0)
        colorOffset = ctypes.c_void_p(self.coordinateAxes.dtype["position"].itemsize)

        axesStride = self.coordinateAxes.strides[0]

        # Coordinate axes
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.coordinateAxes.nbytes, self.coordinateAxes, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, axesStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, axesStride, colorOffset)

        gl.glDrawArrays(gl.GL_LINES, 0, 6)



    def vertexToQuat(self, cube, betraege):

        listWithQuats = np.empty(27, dtype = np.object_)
        listWithQuats.fill(np.array([], dtype = np.object_))
        normalizedCuby = np.zeros(36, [("position", np.float32, 4)])

        for cubyIndex, cuby in enumerate(cube):
            for index, vertex in enumerate(cuby):
                # Normalize Ortsvektoren and store Beträge
                betraege.append(math.sqrt(math.pow(vertex["position"][0],2) + math.pow(vertex["position"][1],2) + math.pow(vertex["position"][2],2)))
                normalizedCuby[index]["position"][:3] = np.divide(vertex["position"],np.array([math.sqrt(math.pow(vertex["position"][0],2) + math.pow(vertex["position"][1],2) + math.pow(vertex["position"][2],2))],dtype=np.float32))

            listWithQuats[cubyIndex] = normalizedCuby
            normalizedCuby = np.zeros(36, [("position", np.float32, 4)])

        return listWithQuats



    def quatMult(self, listWithQuats, multQuat):

        listWithMultQuats = np.empty(27, dtype = np.object_)
        listWithMultQuats.fill(np.array([], dtype = np.object_))
        multipliedCuby = np.zeros(36, [("position", np.float32, 4)])
        invMultQuat = np.zeros(4, dtype = np.float32)
        invMultQuat[:3] = (-1) * multQuat[:3]
        for index, e in enumerate(invMultQuat):
            if e == -0.0:
                invMultQuat[index] = 0.0

        for cubyIndex, cuby in enumerate(listWithQuats):
            for index, vertex in enumerate(cuby):

                firstMultResult = np.array([
                                            multQuat[0]*vertex["position"][3] + multQuat[1]*vertex["position"][2] - multQuat[2]*vertex["position"][1] + multQuat[3]*vertex["position"][0],
                                            -multQuat[0]*vertex["position"][2] + multQuat[1]*vertex["position"][3] + multQuat[2]*vertex["position"][0] + multQuat[3]*vertex["position"][1],
                                            multQuat[0]*vertex["position"][1] - multQuat[1]*vertex["position"][0] + multQuat[2]*vertex["position"][3] + multQuat[3]*vertex["position"][2],
                                            -multQuat[0]*vertex["position"][0] - multQuat[1]*vertex["position"][1] - multQuat[2]*vertex["position"][2] + multQuat[3]*vertex["position"][3]
                                            ],
                                            dtype = np.float32
                )

                temp = list((firstMultResult[0]*invMultQuat[3], firstMultResult[1]*invMultQuat[2], firstMultResult[2]*invMultQuat[1], firstMultResult[3]*invMultQuat[0],
                -firstMultResult[0]*invMultQuat[2], firstMultResult[1]*invMultQuat[3], firstMultResult[2]*invMultQuat[0], firstMultResult[3]*invMultQuat[1],
                firstMultResult[0]*invMultQuat[1], firstMultResult[1]*invMultQuat[0], firstMultResult[2]*invMultQuat[3], firstMultResult[3]*invMultQuat[2],
                -firstMultResult[0]*invMultQuat[0], firstMultResult[1]*invMultQuat[1], firstMultResult[2]*invMultQuat[2], firstMultResult[3]*invMultQuat[3]))

                for damn, e in enumerate(temp):
                    if e == -0.0:
                        temp[damn] = 0.0

                invMultResult = np.zeros(4, dtype = np.float32)

                for dude in range(4):
                    invMultResult[dude] = (temp[4*dude] + temp[4*dude + 1] + temp[4*dude + 2] + temp[4*dude + 3])

                multipliedCuby[index]["position"] = invMultResult

            listWithMultQuats[cubyIndex] = multipliedCuby
            multipliedCuby = np.zeros(36, [("position", np.float32, 4)])

        return listWithMultQuats



    def quatToVertex(self, cube, listWithMultQuats, betraege):

        listWithTransformedCubies = np.empty(27, dtype = np.object_)
        listWithTransformedCubies.fill(np.array([], dtype = np.object_))
        finalCuby = np.zeros(36, [("position", np.float32, 3)])

        for cubyIndex, cuby in enumerate(listWithMultQuats):
            for index, vertex in enumerate(cuby):

                finalCuby[index]["position"] = np.multiply(vertex["position"][:3], betraege[36*cubyIndex + index])

            listWithTransformedCubies[cubyIndex] = finalCuby
            finalCuby = np.zeros(36, [("position", np.float32, 3)])

        for cubyIndex in range(27):
            cube[cubyIndex]["position"] = listWithTransformedCubies[cubyIndex]["position"]

        print(cube)




def createNewCubyData(amount, cubyWidth, *tRC): # tRC = topRightCorner, but the verteces' colors are also part of that n-tuple (second half)

    listWithCubies = []
    cubyData = np.zeros(8, [("position", np.float32, 3)])
    dataIndices = np.array([0,1,3, 1,2,3, 5,0,4, 0,3,4, 6,5,7, 5,4,7, 1,6,2, 6,7,2, 5,6,0, 6,1,0, 7,4,2, 4,3,2], dtype = np.int32)

    for i in range(amount):
        cubyData["position"] = [tRC[i], (tRC[i][0]-cubyWidth, tRC[i][1], tRC[i][2]), (tRC[i][0]-cubyWidth, tRC[i][1]-cubyWidth, tRC[i][2]), (tRC[i][0], tRC[i][1]-cubyWidth, tRC[i][2]), (tRC[i][0], tRC[i][1]-cubyWidth, tRC[i][2]-cubyWidth), (tRC[i][0], tRC[i][1], tRC[i][2]-cubyWidth), (tRC[i][0]-cubyWidth, tRC[i][1], tRC[i][2]-cubyWidth), (tRC[i][0]-cubyWidth, tRC[i][1]-cubyWidth, tRC[i][2]-cubyWidth)]
        convertedData = np.zeros(36, [("position", np.float32, 3), ("color", np.float32, 4)])

        for count, e in enumerate(dataIndices):
            convertedData["position"][count] = cubyData["position"][e]
            try:
                convertedData["color"][count] = tRC[amount][i * 36 + count]         # Skip the topRightCorner positions and the colors for the cubes which have already been treated
            except:
                print("Weird, you did not finish filling in the arguments...")

        listWithCubies.append(convertedData)

    return listWithCubies



if __name__ == "__main__":

    # Cuby data
    dataIndices = np.array([0,1,3, 1,2,3, 5,0,4, 0,3,4, 6,5,7, 5,4,7, 1,6,2, 6,7,2, 5,6,0, 6,1,0, 7,4,2, 4,3,2], dtype = np.int32)
    edgeDataIndices = np.array([0,1, 1,2, 2,3, 3,0, 4,7, 7,6, 6,5, 5,4, 0,5, 1,6, 2,7, 3,4], dtype = np.int32)

    axesData = np.zeros(6, [("position", np.float32, 3), ("color", np.float32, 4)])
    axesData["position"] = [(0.0, 0.0, 0.0), (3.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 3.0)]
    axesData["color"] = [(1.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)]

    # Final Rubik's Cube
    testCube = wholeCube(
            dataIndices, edgeDataIndices, axesData,
            createNewCubyData(
                    27, 1.0,
                    # topRightCorner positions
                    (1.7,1.7,1.7), (0.5,1.7,1.7), (-0.7,1.7,1.7),
                    (1.7,0.5,1.7), (0.5,0.5,1.7), (-0.7,0.5,1.7),
                    (1.7,-0.7,1.7), (0.5,-0.7,1.7), (-0.7,-0.7,1.7),

                    (1.7,1.7,0.5), (0.5,1.7,0.5), (-0.7,1.7,0.5),
                    (1.7,0.5,0.5), (0.5,0.5,0.5), (-0.7,0.5,0.5),
                    (1.7,-0.7,0.5), (0.5,-0.7,0.5), (-0.7,-0.7,0.5),

                    (1.7,1.7,-0.7), (0.5,1.7,-0.7), (-0.7,1.7,-0.7),
                    (1.7,0.5,-0.7), (0.5,0.5,-0.7), (-0.7,0.5,-0.7),
                    (1.7,-0.7,-0.7), (0.5,-0.7,-0.7), (-0.7,-0.7,-0.7),

                    # colors
                    #dataIndices = np.array([0,1,3, 1,2,3, 5,0,4, 0,3,4, 6,5,7, 5,4,7, 1,6,2, 6,7,2, 5,6,0, 6,1,0, 7,4,2, 4,3,2], dtype = np.int32)

                    # Six arguments = six verteces' colors = one face
                    # Six lines = six faces = one cube
                    # 9 blocks of six lines each = front cubes
                    [
                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                    (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),




                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),




                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                    (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                    (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                    (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),
                    ]
            )
    )

    # And finally the Mainloop()
    glut.glutMainLoop()
