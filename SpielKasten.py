import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut

vertex_code = """

    uniform float scale;
    uniform mat4 matCam;
    attribute vec4 color;
    attribute vec3 position;
    varying vec4 v_color;
    void main()
    {
        gl_Position = matCam*vec4(scale*position, 1.0);
        v_color = color;
    } """

fragment_code = """
    varying vec4 v_color;
    void main()
    {
        gl_FragColor = v_color;
    } """

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    #gl.glDrawArrays(gl.GL_TRIANGLES, 0, 12)

    gl.glDrawElements(gl.GL_TRIANGLES, len(index), gl.GL_UNSIGNED_INT, ctypes.c_void_p(0)) # render nothing (i.e. only the background color)
    glut.glutSwapBuffers()

def reshape(width,height):
    gl.glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == '\033':
        sys.exit( )

def timer(fps):
    global clock
    clock += 0.0005*1000.0/fps
    print(clock)
#    eye = np.array([0,0,1])
#    center = np.array([0,clock,0])
#    up = np.array([0,1,0])
#    mat = computeLookAtMatrix(eye, center, up)
    theta = clock;
    mat = np.array([[np.cos(theta), 0, np.sin(theta), 0],
                [0, 1, 0, 0],
                [-np.sin(theta), 0, np.cos(theta), 0],
                [0, 0, 0, 1]])
    loc = gl.glGetUniformLocation(program, "matCam")
    gl.glUniformMatrix4fv(loc, 1, False, mat)



    #glut.glutTimerFunc(1000/fps, timer, fps)
    glut.glutPostRedisplay()


# GLUT init
# --------------------------------------
glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('Hello world!')
glut.glutReshapeWindow(512,512)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
#glut.glutTimerFunc(1000/60, timer, 60)

# Build data
# --------------------------------------
data = np.zeros(8, [("position", np.float32, 3),
                    ("color",    np.float32, 4)])

data['color']    = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1),
                    (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]

data['position'] = [ (-1,-1,1),
                     (1,-1,1),
                        (1,1,1),
                        (-1,1,1),
                        (-1,-1,-1),
                        (1,-1,-1),
                        (1,1,-1),
                        (-1,1,-1)]

index = np.array([0,1,2,
                2,3,0,
                1,5,6,
                6,2,1,
                7,6,5,
                5,4,7,
                4,0,3,
                3,7,4,
                4,5,1,
                1,0,4,
                3,2,6,
                6,7,3])

# Build & activate program
# --------------------------------------

# Request a program and shader slots from GPU
program  = gl.glCreateProgram()
vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

# Set shaders source
gl.glShaderSource(vertex, vertex_code)
gl.glShaderSource(fragment, fragment_code)

# Compile shaders
gl.glCompileShader(vertex)
gl.glCompileShader(fragment)

# Attach shader objects to the program
gl.glAttachShader(program, vertex)
gl.glAttachShader(program, fragment)

# Build program
gl.glLinkProgram(program)

# Get rid of shaders (no more needed)
gl.glDetachShader(program, vertex)
gl.glDetachShader(program, fragment)

# Make program the default program
gl.glUseProgram(program)


# Build buffer
# --------------------------------------

# Request a buffer slot from GPU
buffer = gl.glGenBuffers(1)

# Make this buffer the default one
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

# Upload data
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

# same for index buffer
buffer_index= gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, buffer_index)
gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, gl.GL_STATIC_DRAW)


# Bind attributes
# --------------------------------------
stride = data.strides[0]
offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, offset)

offset = ctypes.c_void_p(data.dtype["position"].itemsize)
loc = gl.glGetAttribLocation(program, "color")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, buffer_index)

# Bind uniforms
# --------------------------------------
loc = gl.glGetUniformLocation(program, "scale")
gl.glUniform1f(loc, 0.5)
clock = 0

#loc = gl.glGetUniformLocation(program, "matCam")
#print(loc)
#gl.glUniformMatrix4fv(loc, 1, False, np.eye(4))

# Enter mainloop
# --------------------------------------
glut.glutMainLoop()
