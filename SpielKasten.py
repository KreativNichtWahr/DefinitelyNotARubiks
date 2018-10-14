import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
glut.glutInit()
Vbos = gl.glGenBuffers(2)
print(Vbos)
b = gl.glGenBuffers(1)
print(b)
