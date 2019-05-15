from PyQt5.QtWidgets import (QOpenGLWidget)
from PyQt5.QtGui import (QOpenGLContext, QSurfaceFormat, QSurface)
from PyQt5.QtCore import Qt
import time
import numpy as np
import math
import ctypes
import OpenGL.GL as gl
import random


# class that holds the cube embedded in a qOpenGLWidget
class Cube(QOpenGLWidget):
    # Transfer parent and window's dimensions
    def __init__(self, parent, length = 500, width = 500):
        # Call parent class constructor
        super().__init__()
        self.initUI(length, width)

    # For all window related stuff
    def initUI(self, length, width):
        # Resize the window
        self.resize(length, width)

    # Protectet function which gets executed as right after the constructor has been called, meaning that this is the place to put all OpenGL init related calls
    def initializeGL(self):

        # Nested function, as it is only being called here, makes it more ordered and will show more use in the future
        def createNewCubeData(cubeType, cubyFaceWidth, cubyRoundedPartWidth, fTRC, colors):

            # Final list which will contain all the cubies
            listWithCubies = []
            # Sets the "roundness" factor of the rounded parts
            feinKoernigkeit = 2

            # One cuby per loop
            for cuby in range(cubeType**3):
                # Empty numpy array --> 36 : Faces; (feinKoernigkeit*6)*12 : Rounded edge parts; ((feinKoernigkeit**2)*3)*8 : Rounded corner parts
                cubyData = np.zeros(36 + (feinKoernigkeit*6)*12 + ((feinKoernigkeit**2)*3)*8, [("position", np.float32, 3), ("color", np.float32, 4)])
                # Top right corner --> x-value: substract one unit each cuby, but reset after 3 have passed; y-value: substract one unit after 3 have passed and reset after 9 have passed, z-value: substract one unit after 9 have passed and (only theoretically) reset after 27 have passed
                tRC = (fTRC[0]-cuby+(cuby//3 * 3), fTRC[1]-(cuby//3)+(cuby//9 * 3), fTRC[2]-(cuby//9))
                # Colored Faces
                # Fill the first 36 indexes
                cubyData["position"][:36] = [
                    # Front
                    # Each line three vertices (therefore one triangle), 2 lines of code = one face
                    # Start with tRC, move left, move right and down
                    # Start with last two moves, move left and down
                    # Repeat this same principle in a similar way
                    tRC, (tRC[0]-cubyFaceWidth, tRC[1], tRC[2]), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]),
                    tRC, (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]), (tRC[0], tRC[1]-cubyFaceWidth, tRC[2]),
                    # Right
                    (tRC[0]+cubyRoundedPartWidth, tRC[1], tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]+cubyRoundedPartWidth, tRC[1], tRC[2]-cubyRoundedPartWidth), (tRC[0]+cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth),
                    (tRC[0]+cubyRoundedPartWidth, tRC[1], tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]+cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]+cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth),
                    # Back
                    (tRC[0]-cubyFaceWidth, tRC[1], tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1], tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyFaceWidth, tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth),
                    (tRC[0]-cubyFaceWidth, tRC[1], tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyFaceWidth, tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth),
                    # Left
                    (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1], tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1], tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth),
                    (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1], tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth),
                    # Top
                    (tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth),
                    (tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth),
                    # Down
                    (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth),
                    (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth),
                ]

                # Fill the colors in one at a time
                for colorIndex in range(36):
                    # Increment the index by 36 after each cuby
                    cubyData["color"][colorIndex] = colors[cuby*36 + colorIndex]

                # Rounded edge parts
                    # Middle
                        # Front Top
                # Top corners of the first rectangle to trace
                oldTopCorners = [(tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth)]
                # Amount of layers (rectangles) depends on the feinKoernigkeit factor
                for korn in range(feinKoernigkeit):

                    # Bottom corners of each new layer (rectangle) --> usage of cos and sin funcs because of the curvature of the group of rectangles we want to implement
                    # IMPORTANT: which value gets which func: sin and cos have a differently increasing slope, therefore, in order to prevent INWARD curvature, get it the correct way around
                    oldBottomCorners = [(tRC[0], tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth)]
                    # Array indexes: each rectangle takes 6 indexes (6 vertices) & Value: First two top corners, then first botton, repeat last top and finally two bottom
                    cubyData["position"][(36+korn*6):(42+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    # The old bottom corners are the next rectangle's top ones
                    oldTopCorners = oldBottomCorners

                    # Same array indexes and only black as a color
                    cubyData["color"][(36+korn*6):(42+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Front Down
                oldTopCorners = [(tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0], tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6)+korn*6):((42+feinKoernigkeit*6)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6)+korn*6):((42+feinKoernigkeit*6)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Back Top
                oldTopCorners = [(tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0], tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-(1+math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-(1+math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*2)+korn*6):((42+feinKoernigkeit*6*2)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*2)+korn*6):((42+feinKoernigkeit*6*2)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Back Down
                oldTopCorners = [(tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0], tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-(1+math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-(1+math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*3)+korn*6):((42+feinKoernigkeit*6*3)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*3)+korn*6):((42+feinKoernigkeit*6*3)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                    # Equator
                        # Front Right
                oldTopCorners = [(tRC[0], tRC[1]-cubyFaceWidth, tRC[2]), tRC]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0]+(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-(1-math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth), (tRC[0]+(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1], tRC[2]-(1-math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*4)+korn*6):((42+feinKoernigkeit*6*4)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*4)+korn*6):((42+feinKoernigkeit*6*4)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Front Left
                oldTopCorners = [(tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]), (tRC[0]-cubyFaceWidth, tRC[1], tRC[2])]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0]-cubyFaceWidth-(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-(1-math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth-(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1], tRC[2]-(1-math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*5)+korn*6):((42+feinKoernigkeit*6*5)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*5)+korn*6):((42+feinKoernigkeit*6*5)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Back Right
                oldTopCorners = [(tRC[0], tRC[1]-cubyFaceWidth, tRC[2]-cubyFaceWidth-2*cubyRoundedPartWidth), (tRC[0], tRC[1], tRC[2]-cubyFaceWidth-2*cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0]+(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyFaceWidth-(1+math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth), (tRC[0]+(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1], tRC[2]-cubyFaceWidth-(1+math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*6)+korn*6):((42+feinKoernigkeit*6*6)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*6)+korn*6):((42+feinKoernigkeit*6*6)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Back Left
                oldTopCorners = [(tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyFaceWidth-2*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1], tRC[2]-cubyFaceWidth-2*cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0]-cubyFaceWidth-(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyFaceWidth-(1+math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth-(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1], tRC[2]-cubyFaceWidth-(1+math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*7)+korn*6):((42+feinKoernigkeit*6*7)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*7)+korn*6):((42+feinKoernigkeit*6*7)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                    # Standing
                        # Right Top
                oldTopCorners = [(tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0]+(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]+(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*8)+korn*6):((42+feinKoernigkeit*6*8)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*8)+korn*6):((42+feinKoernigkeit*6*8)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Left Top
                oldTopCorners = [(tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0]-cubyFaceWidth-(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth-(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*9)+korn*6):((42+feinKoernigkeit*6*9)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*9)+korn*6):((42+feinKoernigkeit*6*9)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Right Down
                oldTopCorners = [(tRC[0], tRC[1]-cubyFaceWidth-cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0], tRC[1]-cubyFaceWidth-cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0]+(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]+(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*10)+korn*6):((42+feinKoernigkeit*6*10)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*10)+korn*6):((42+feinKoernigkeit*6*10)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                        # Left Down
                oldTopCorners = [(tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth-cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth-cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [(tRC[0]-cubyFaceWidth-(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth-(math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                    cubyData["position"][((36+feinKoernigkeit*6*11)+korn*6):((42+feinKoernigkeit*6*11)+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
                    oldTopCorners = oldBottomCorners

                    cubyData["color"][((36+feinKoernigkeit*6*11)+korn*6):((42+feinKoernigkeit*6*11)+korn*6)] = [(0.0,0.0,0.0,1.0) for _ in range(6)]

                # Rounded corner parts
                    # Top
                        # Right Front
                # Same as withe the rounded edge parts, only that you begin with one top corner
                oldTopCorners = [(tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth)]
                # Again, the amount of triangles depends on the feinKoernigkeit factor
                for korn in range(feinKoernigkeit):

                    # Using tuples inside the lists because of list comprehension: bottom corners --> the higher the korn index, the more corners in the list (one additional with each iteration)
                    oldBottomCorners = [
                                        (tRC[0]+math.sin((k/(1+korn))*(math.pi/2)) * (math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth),
                                        tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth,
                                        tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth-((1-math.cos((k/(1+korn))*(math.pi/2))) * math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth)) for k in range(korn+2)
                    ]
                    # List with tuples of vertices (triangles)
                    tempList = []
                    # Only after the first iteration
                    if korn != 0:
                        # Add triangles --> ALWAYS IN PAIRS OF TWO (amount of triangles is uneven, so you add the first and then the rest in pairs)
                        tempList = [(oldTopCorners[k], oldTopCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+2], oldTopCorners[k+1]) for k in range(korn)]
                    # Insert the first triangle at the first index
                    tempList.insert(0, (oldTopCorners[0], oldBottomCorners[0], oldBottomCorners[1]))

                    # Remove tuple "coat" which only purpose was to be able to use list comprehension
                    tempList2 = []
                    # Iterate through the first list
                    for e in tempList:
                        # Append as many elements to the tempList2 as there is elements (vertices) in e (tuple)
                        for d in range(len([*e])):
                            tempList2.append(e[d])

                    # Seems complicated and, well, it is: 36 --> faces; feinKoernigkeit*6*12 --> rounded edge parts;
                    #                                     -((0**korn)-1)*(korn**2)*3*1) --> 1) -((0**korn)-1) = 0 on the first iteration and = 1 on every other (needed because of the power in the next segment which can't be 0 but has to)
                    #                                                                       2) (korn**2)*3*1) --> amount of vertices used in the previous iteration
                    cubyData["position"][((36+feinKoernigkeit*6*12-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((korn+1)**2)*3*1))] = tempList2
                    # Same indexes as before, and again only black as color
                    cubyData["color"][((36+feinKoernigkeit*6*12-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((korn+1)**2)*3*1))] = [(0.0,0.0,0.0,1.0) for _ in range(len(tempList2))]
                    # Same procedure as with the rounded edge parts
                    oldTopCorners = oldBottomCorners
                        # Left Front
                oldTopCorners = [(tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [
                                        (tRC[0]-cubyFaceWidth-math.sin((k/(1+korn))*(math.pi/2)) * (math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth),
                                        tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth,
                                        tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth-((1-math.cos((k/(1+korn))*(math.pi/2))) * math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth)) for k in range(korn+2)
                    ]

                    tempList = []
                    if korn != 0:
                        tempList = [(oldTopCorners[k], oldTopCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+2], oldTopCorners[k+1]) for k in range(korn)]
                    tempList.insert(0, (oldTopCorners[0], oldBottomCorners[0], oldBottomCorners[1]))

                    tempList2 = []
                    for e in tempList:
                        for d in range(len([*e])):
                            tempList2.append(e[d])

                    cubyData["position"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*1-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*1+((korn+1)**2)*3*1))] = tempList2
                    cubyData["color"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*1-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*1+((korn+1)**2)*3*1))] = [(0.0,0.0,0.0,1.0) for _ in range(len(tempList2))]
                    oldTopCorners = oldBottomCorners

                        # Right Back
                oldTopCorners = [(tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [
                                        (tRC[0]+(math.cos((k/(1+korn))*(math.pi/2))) * (math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth),
                                        tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth,
                                        tRC[2]-cubyFaceWidth-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth-((1+math.sin((k/(1+korn))*(math.pi/2))) * math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth)) for k in range(korn+2)
                    ]

                    tempList = []
                    if korn != 0:
                        tempList = [(oldTopCorners[k], oldTopCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+2], oldTopCorners[k+1]) for k in range(korn)]
                    tempList.insert(0, (oldTopCorners[0], oldBottomCorners[0], oldBottomCorners[1]))

                    tempList2 = []
                    for e in tempList:
                        for d in range(len([*e])):
                            tempList2.append(e[d])

                    cubyData["position"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*2-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*2+((korn+1)**2)*3*1))] = tempList2
                    cubyData["color"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*2-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*2+((korn+1)**2)*3*1))] = [(0.0,0.0,0.0,1.0) for _ in range(len(tempList2))]
                    oldTopCorners = oldBottomCorners
                        # Left Back
                oldTopCorners = [(tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [
                                        (tRC[0]-cubyFaceWidth-(math.cos((k/(1+korn))*(math.pi/2))) * (math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth),
                                        tRC[1]+(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth,
                                        tRC[2]-cubyFaceWidth-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth-((1+math.sin((k/(1+korn))*(math.pi/2))) * math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth)) for k in range(korn+2)
                    ]

                    tempList = []
                    if korn != 0:
                        tempList = [(oldTopCorners[k], oldTopCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+2], oldTopCorners[k+1]) for k in range(korn)]
                    tempList.insert(0, (oldTopCorners[0], oldBottomCorners[0], oldBottomCorners[1]))

                    tempList2 = []
                    for e in tempList:
                        for d in range(len([*e])):
                            tempList2.append(e[d])

                    cubyData["position"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*3-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*3+((korn+1)**2)*3*1))] = tempList2
                    cubyData["color"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*3-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*3+((korn+1)**2)*3*1))] = [(0.0,0.0,0.0,1.0) for _ in range(len(tempList2))]
                    oldTopCorners = oldBottomCorners

                    # Down
                        # Right Front
                oldTopCorners = [(tRC[0], tRC[1]-cubyFaceWidth-cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [
                                        (tRC[0]+math.sin((k/(1+korn))*(math.pi/2)) * (math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth),
                                        tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth,
                                        tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth-((1-math.cos((k/(1+korn))*(math.pi/2))) * math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth)) for k in range(korn+2)
                    ]

                    tempList = []
                    if korn != 0:
                        tempList = [(oldTopCorners[k], oldTopCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+2], oldTopCorners[k+1]) for k in range(korn)]
                    tempList.insert(0, (oldTopCorners[0], oldBottomCorners[0], oldBottomCorners[1]))

                    tempList2 = []
                    for e in tempList:
                        for d in range(len([*e])):
                            tempList2.append(e[d])

                    cubyData["position"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*4-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*4+((korn+1)**2)*3*1))] = tempList2
                    cubyData["color"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*4-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*4+((korn+1)**2)*3*1))] = [(0.0,0.0,0.0,1.0) for _ in range(len(tempList2))]
                    oldTopCorners = oldBottomCorners
                        # Left Front
                oldTopCorners = [(tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth-cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [
                                        (tRC[0]-cubyFaceWidth-math.sin((k/(1+korn))*(math.pi/2)) * (math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth),
                                        tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth,
                                        tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth-((1-math.cos((k/(1+korn))*(math.pi/2))) * math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth)) for k in range(korn+2)
                    ]

                    tempList = []
                    if korn != 0:
                        tempList = [(oldTopCorners[k], oldTopCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+2], oldTopCorners[k+1]) for k in range(korn)]
                    tempList.insert(0, (oldTopCorners[0], oldBottomCorners[0], oldBottomCorners[1]))

                    tempList2 = []
                    for e in tempList:
                        for d in range(len([*e])):
                            tempList2.append(e[d])

                    cubyData["position"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*5-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*5+((korn+1)**2)*3*1))] = tempList2
                    cubyData["color"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*5-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*5+((korn+1)**2)*3*1))] = [(0.0,0.0,0.0,1.0) for _ in range(len(tempList2))]
                    oldTopCorners = oldBottomCorners

                        # Right Back
                oldTopCorners = [(tRC[0], tRC[1]-cubyFaceWidth-cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [
                                        (tRC[0]+(math.cos((k/(1+korn))*(math.pi/2))) * (math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth),
                                        tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth,
                                        tRC[2]-cubyFaceWidth-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth-((1+math.sin((k/(1+korn))*(math.pi/2))) * math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth)) for k in range(korn+2)
                    ]

                    tempList = []
                    if korn != 0:
                        tempList = [(oldTopCorners[k], oldTopCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+2], oldTopCorners[k+1]) for k in range(korn)]
                    tempList.insert(0, (oldTopCorners[0], oldBottomCorners[0], oldBottomCorners[1]))

                    tempList2 = []
                    for e in tempList:
                        for d in range(len([*e])):
                            tempList2.append(e[d])

                    cubyData["position"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*6-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*6+((korn+1)**2)*3*1))] = tempList2
                    cubyData["color"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*6-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*6+((korn+1)**2)*3*1))] = [(0.0,0.0,0.0,1.0) for _ in range(len(tempList2))]
                    oldTopCorners = oldBottomCorners
                        # Left Back
                oldTopCorners = [(tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth-cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
                for korn in range(feinKoernigkeit):

                    oldBottomCorners = [
                                        (tRC[0]-cubyFaceWidth-(math.cos((k/(1+korn))*(math.pi/2))) * (math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth),
                                        tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth,
                                        tRC[2]-cubyFaceWidth-(1-math.sin((math.pi/2) * (korn+1)/feinKoernigkeit))*cubyRoundedPartWidth-((1+math.sin((k/(1+korn))*(math.pi/2))) * math.sin((math.pi/2) * (korn+1)/feinKoernigkeit)*cubyRoundedPartWidth)) for k in range(korn+2)
                    ]

                    tempList = []
                    if korn != 0:
                        tempList = [(oldTopCorners[k], oldTopCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+1], oldBottomCorners[k+2], oldTopCorners[k+1]) for k in range(korn)]
                    tempList.insert(0, (oldTopCorners[0], oldBottomCorners[0], oldBottomCorners[1]))

                    tempList2 = []
                    for e in tempList:
                        for d in range(len([*e])):
                            tempList2.append(e[d])

                    cubyData["position"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*7-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*7+((korn+1)**2)*3*1))] = tempList2
                    cubyData["color"][((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*7-((0**korn)-1)*(korn**2)*3*1)):((36+feinKoernigkeit*6*12+((feinKoernigkeit**2)*3)*7+((korn+1)**2)*3*1))] = [(0.0,0.0,0.0,1.0) for _ in range(len(tempList2))]
                    oldTopCorners = oldBottomCorners
                # Append the newly created cuby data to the list0
                listWithCubies.append(cubyData)
            # Return final list
            return listWithCubies


        # Final Rubik's Cube - or at least a list with all you need for the cube's correct display
        listWithConditionsInitiales = [createNewCubeData(
                        # Cube type, cubyFace ratio, rounded part ratio
                        3, 0.8696, 0.0652,
                        # FirstTopRightCorner position
                        (1.4348,1.4348,1.5),

                        # Colors

                        # Six tuples = six verteces' colors = one face
                        # Six lines = six faces = one cube
                        # 9 blocks of six lines each = one layer of cubes
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
        ]


        # Other vars
            # Convert list to numpy array
        self.listWithCubies = np.array(listWithConditionsInitiales[0])
            # 3-dimensional numpy array, used to keep track of the cubies' positions
        self.cubeOrder = np.arange(27).reshape(3,3,3)
            # Angles for whole cube rotations
        self.angles = [0.0,0.0,0.0]
            # Keeps track of where in the list above what axis rotation or angle value is stored (because they change positions)
        self.xRotPos, self.yRotPos, self.zRotPos = 0,1,2
            # Keeps track of how many times the cube has been turned alongside one certain axis (increments by 90° every 45° away from the nearest value that is congruent 0 mod(90°))
        self.difStartPosXRot, self.difStartYRot, self.difStartZRot = 0.0, 0.0, 0.0

            # Reorder the 3-dimensional array because I choose (don't ask me why) a different layou to start with
        for i in range(27):
            self.cubeOrder[i//9][(i - i%3 - 2*(i//3))%3][2-i%3] = i

            # numpy array which stores the cubies to rotate
        self.whatCubesToRotate = np.array([])
            # Default angle value (in radians, OpenGL works that way) for every step of the side rotation animation
        self.angleValue = 10*math.pi/180
            # Cursors old x position (when it is clicked)
        self.oldMouseXPos = 0
            # Same for y
        self.oldMouseYPos = 0

        # Depth and Cull init
        # Enable depth test to have OpenGL check what vertices are in front of others
        gl.glEnable(gl.GL_DEPTH_TEST)
        # Don't remember this, isn't actually important
        gl.glDepthMask(gl.GL_TRUE)
        # Default
        gl.glDepthFunc(gl.GL_LESS)

        # Launch program init
        self.initProgram()


    # OpenGL shader compilation and program creation
    def initProgram(self):

        # Shader code
            # Vertex shader
                # uniform     --> angles: whole cube rotation angles (keeps the same value for every vertex)
                # attribute   --> position: vertex's position
                #             --> color: vertex's color
                # varying     --> v_color: transmits the color to the fragment shader
                # mat4        --> ModelViewProjectionMatrix, standard stuff
                # void main() --> main function which OpenGL executes
                        # 1) modelMatrix entries depending on angles
                        # 2) viewMatrix static, just there to zoom out a bit
                        # 3) projectionMatrix --> perspective projection
                        # 4) vertex calc with "4th" value (is there for the distance effect)
                        # 5) gl_position --> OpenGL's only input (vertex)
                        # 6) v_color -->  OpenGL's only input (color)
        vertexShaderCode = """
            uniform vec3 angles;
            attribute vec3 position;
            attribute vec4 color;
            varying vec4 v_color;
            mat4 modelMatrix;
            mat4 viewMatrix;
            mat4 projectionMatrix;
            void main() {
                modelMatrix = mat4(1,0,0,0,  0,cos(angles.x),-sin(angles.x),0,  0,sin(angles.x),cos(angles.x),0,  0,0,0,1) *
                              mat4(cos(angles.y),0,sin(angles.y),0,  0,1,0,0,  -sin(angles.y),0,cos(angles.y),0,  0,0,0,1) *
                              mat4(cos(angles.z),-sin(angles.z),0,0,  sin(angles.z),cos(angles.z),0,0,  0,0,1,0,  0,0,0,1);
                viewMatrix = mat4(1,0,0,0,  0,1,0,0,  0,0,1,0,  0,0,-4.5,1);
                projectionMatrix = mat4(1,0,0,0,  0,1,0,0,  0,0,0,-1, 0,0,-1.5,0);
                vec4 temporary = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
                gl_Position = temporary / temporary.w;
                v_color = color;
            }
        """
            # fragment shader
                # varying --> same variable as before
                # void main() --> same
                    # 1) gl_FragColor --> OpenGL's only input (color final stage)
        fragmentShaderCode = """
            varying vec4 v_color;
            void main() {
                gl_FragColor = v_color;
            }
        """

        # Compile and link shader code
            # Create program
        self.program = gl.glCreateProgram()
            # Create shaders
        vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

            # Link shader to shader code
        gl.glShaderSource(vertexShader, vertexShaderCode)
        gl.glShaderSource(fragmentShader, fragmentShaderCode)

            # Compile shader code
        gl.glCompileShader(vertexShader)
            # Error raising in case something goes wrong
        if not gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(vertexShader).decode()
            print(error)
            raise RuntimeError("Vertex shader compilation error")

        gl.glCompileShader(fragmentShader)
        if not gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(fragmentShader).decode()
            print(error)
            raise RuntimeError("Fragment shader compilation error")

            # Attach shader to program
        gl.glAttachShader(self.program, vertexShader)
        gl.glAttachShader(self.program, fragmentShader)

            # Put it all together or finalise the program
        gl.glLinkProgram(self.program)
            # More error raising
        if not gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self.program))
            raise RuntimeError("Linking error")

            # Detach shader, as no longer needed
        gl.glDetachShader(self.program, vertexShader)
        gl.glDetachShader(self.program, fragmentShader)

            # Declare the program as the one being used
        gl.glUseProgram(self.program)


    # Protectet function called whenever the window is resized
    def resizeGL(self, width, height):

        # Store the windows new dimensions
        self.width = width
        self.height = height
        # Provoke an immediate refresh of the canvas
        self.repaint()


    # Protectet function called once when initiated, and each time repaint() or update() is called
    def paintGL(self):

        # Let the cube stay a cube
        if self.width < self.height:
            # Window's width is restricting one of the cubes dimensions, therfore set both to that value & set the viewports corner in order for the cube to be centered
            gl.glViewport(0, int((self.height/2) - (self.width/2)), self.width, self.width)
        else:
            # Same but the other way around
            gl.glViewport(int((self.width/2) - (self.height/2)), 0, self.height, self.height)

        # Get location of angles inside the program
        loc = gl.glGetUniformLocation(self.program, "angles")
        # Uplaod new 3 float type uniform values of angles to that location
        gl.glUniform3f(loc, self.angles[self.xRotPos], self.angles[self.yRotPos], self.angles[self.zRotPos])

        # Clear both color and depth buffer before redrawing
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # Draw one cuby at a time
        for i in self.listWithCubies:
            self.drawCubies(i)


    # Buffer stuff
    def drawCubies(self, objectToDraw):
        # Create 4 Vbos (Vertex buffers, memory storage on the GPU for any vertex related data)
        Vbos = gl.glGenBuffers(4)

        # Get location of both position and color attribute
        posLoc = gl.glGetAttribLocation(self.program, "position")
        colorLoc = gl.glGetAttribLocation(self.program, "color")

        # Set the posOffset (offset in amount of bytes), 0 for the position, but as a C variable
        posOffset = ctypes.c_void_p(0)
        # .dtype["position"].itemsize (numpy ndarray attribute) returns the size in bytes of the "position" field
        colorOffset = ctypes.c_void_p(objectToDraw.dtype["position"].itemsize)
        # .strides[0] returns complete dimension (0) length in bytes
        objectStride = objectToDraw.strides[0]

        # Usage of Vbos
        # Specifies to which target the buffer is bound (GL_ARRAY_BUFFER)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[0])
        # Upload data to buffer --> target, complete length in bytes of data, data, way of usage (GL_DYNAMIC_DRAW because the image is frequently redrawn)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, objectToDraw.nbytes, objectToDraw, gl.GL_DYNAMIC_DRAW)

        # Enable "connection" or "communication" between your Buffer and the position attribute in your program, the VertexAttribArray is kind of the interpreter of the buffer data and transmits this data to the program in a specific way
        gl.glEnableVertexAttribArray(posLoc)
        # "Interpretation rules" for the VertexAttribArray --> location, value type, don't remember (again, not important), data length in bytes, offset
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, objectStride, posOffset)

        # Same for the color attribute
        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, objectStride, colorOffset)

        # Finally draw the vertices --> option GL_TRIANGLES: every 3 consecutive vertices form a triangle, amount of entries in data
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, objectToDraw.size)


    # Called by mainWindow
    def mouseClicked(self, mouseClickEvent):

        # Set cursor positions at click time
        self.oldMouseXPos = mouseClickEvent.x()
        self.oldMouseYPos = mouseClickEvent.y()


    # Again, called by mainWindow
    def mouseMoved(self, mouseMoveEvent):

        # Calculate the difference between the clicked and the new cursor position
        diffOldNewX = mouseMoveEvent.x() - self.oldMouseXPos
        diffOldNewY = mouseMoveEvent.y() - self.oldMouseYPos

        # Update the old cursor position
        self.oldMouseXPos = mouseMoveEvent.x()
        self.oldMouseYPos = mouseMoveEvent.y()

        # Convert cursor drag into angle values (higher ratio for y value because of most screens being built a certain way)
        self.angles[1] -= (diffOldNewX / 9) * math.pi/180
        self.angles[0] -= (diffOldNewY / 8) * math.pi/180

        # Redraw immediately
        self.update()


    # Handles the cubes rotations
    def keyboard(self, key):

        # Cube rotations
            # Arrow keys (not recommended)
                # Left
        if key == Qt.Key_Left:

            for _ in range(40):
                self.angles[1] -= 0.25*math.pi/180
                self.repaint()
                time.sleep(0.0015)

                # Right
        elif key == Qt.Key_Right:

            for _ in range(40):
                self.angles[1] += 0.25*math.pi/180
                self.repaint()
                time.sleep(0.0015)

                # Down
        elif key == Qt.Key_Down:

            if abs(self.angles[0] - self.difStartPosXRot) > math.pi/4:
                self.angles.append(self.angles[1])
                self.angles.pop(1)
                temp = self.yRotPos
                self.yRotPos = self.zRotPos
                self.zRotPos = temp
                self.difStartPosXRot += math.pi/2

            for _ in range(40):
                self.angles[0] += 0.25*math.pi/180
                self.repaint()
                time.sleep(0.0015)

                # Up
        elif key == Qt.Key_Up:

            if abs(self.angles[0] - self.difStartPosXRot) > math.pi/4:
                self.angles.append(self.angles[1])
                self.angles.pop(1)
                temp = self.yRotPos
                self.yRotPos = self.zRotPos
                self.zRotPos = temp
                self.difStartPosXRot -= math.pi/2

            for _ in range(40):
                self.angles[0] -= 0.25*math.pi/180
                self.repaint()
                time.sleep(0.0015)


        # Side rotations, sides are being turned via the according letter on the keyboard, second condition is for the scramble function
            # Front
        elif key == Qt.Key_F or key == "f":

            self.rotateCubeSide(0, 0)

            # Back
        elif key == Qt.Key_B or key == "b":

            self.rotateCubeSide(0, 0, (0,1), 2, True)

            # Top
        elif key == Qt.Key_T or key == "t":

            self.rotateCubeSide(2, 0, (0,1), 3)

            # Down
        elif key == Qt.Key_D or key == "d":

            self.rotateCubeSide(2, 0, (0,1), 1, True)

            # Right
        elif key == Qt.Key_R or key == "r":

            self.rotateCubeSide(1, 0, (0,2), 1)

            # Left
        elif key == Qt.Key_L or key == "l":

            self.rotateCubeSide(1, 0, (0,2), 3, True)

            # Middle
        elif key == Qt.Key_M or key == "m":

            self.rotateCubeSide(1, 1, (0,2), 3, True)

            # Equator
        elif key == Qt.Key_E or key == "e":

            self.rotateCubeSide(2, 1, (0,1), 1, True)

            # Standing
        elif key == Qt.Key_S or key == "s":

            self.rotateCubeSide(0, 1)

        elif key == Qt.Key_H:

            self.scramble(30)


        self.update()

    # Rotates cube side
    def rotateCubeSide(self, sideRotationMatricesArrayIndex, layer, axes = (0,1), amountForth = 0, invertAngle = False):
        
        if invertAngle:
            self.angleValue = -self.angleValue

        self.cubeOrder = np.rot90(self.cubeOrder, amountForth, axes = axes)
        self.whatCubesToRotate = self.cubeOrder[layer]
        self.cubeOrder[layer] = np.rot90(self.cubeOrder[layer], 3)
        self.cubeOrder = np.rot90(self.cubeOrder, 4-amountForth, axes = axes)

        sideRotationMatricesArray = (
            np.array([[np.cos(self.angleValue),np.sin(self.angleValue),0,0] , [-np.sin(self.angleValue),np.cos(self.angleValue),0,0] , [0,0,1,0] , [0,0,0,1]]),
            np.array([[1,0,0,0] , [0,np.cos(self.angleValue),np.sin(self.angleValue),0] , [0,-np.sin(self.angleValue),np.cos(self.angleValue),0] , [0,0,0,1]]),
            np.array([[np.cos(self.angleValue),0,-np.sin(self.angleValue),0] , [0,1,0,0] , [np.sin(self.angleValue),0,np.cos(self.angleValue),0] , [0,0,0,1]])
        )

        oldTime = time.time()

        for _ in range(int(round((math.pi/2)/abs(self.angleValue)))):
            for cuby in [x for x in self.listWithCubies if np.where(x == self.listWithCubies)[0][0] in self.whatCubesToRotate]:
                for vertex in cuby:
                    vertex["position"] = (sideRotationMatricesArray[sideRotationMatricesArrayIndex] @ np.array([vertex["position"][0], vertex["position"][1], vertex["position"][2], 1]))[:3]
            self.repaint()
            time.sleep(0.0015)

        self.angleValue = abs(self.angleValue)


    def scramble(self, amountOfMoves):

        self.angleValue = math.pi/6
        listWithMoves = [random.choice("fbtdrlmes") for _ in range(amountOfMoves)]
        for move in listWithMoves:
            self.keyboard(move)

        self.angleValue = 10*math.pi/180
