import numpy as np

alpha = 0.0
beta = 0.0
theta = 0.0
finalRotationMatrix = (
    np.array([[1,0,0,0] , [0,np.cos(beta),np.sin(beta),0] , [0,-np.sin(beta),np.cos(beta),0] , [0,0,0,1]]) @
    np.array([[np.cos(theta),0,-np.sin(theta),0] , [0,1,0,0] , [np.sin(theta),0,np.cos(theta),0] , [0,0,0,1]]) @
    np.array([[np.cos(alpha),np.sin(alpha),0,0] , [-np.sin(alpha),np.cos(alpha),0,0] , [0,0,1,0] , [0,0,0,1]])
)

print(finalRotationMatrix)

a = np.vsplit(finalRotationMatrix, (1,2,3))
print(a)

xTransform = a[0]
yTransform = a[1]
zTransform = a[2]

print(xTransform, yTransform, zTransform)

xTransform = finalRotationMatrix[0,:3]
yTransform = finalRotationMatrix[1,:3]
zTransform = finalRotationMatrix[2,:3]

print(xTransform, yTransform, zTransform)
