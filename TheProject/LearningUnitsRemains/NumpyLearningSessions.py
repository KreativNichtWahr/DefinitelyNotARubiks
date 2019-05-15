import numpy as np

""" The Basics """

# important funcs
a = np.arange(15).reshape(3, 5)     # Creates an array with numbers from 0 to 14 and rearanges it so it becomes a 3 x 5 matrix
print(a)
print(a.ndim)                       # Amount of dimensions
print(a.shape)                      # Amount of elements per dimension
print(a.size)                       # Total elements in the array
print(a.dtype)                      # Type of the array's elements
print(a.dtype.name)
print(a.itemsize)                   # Size in bytes of the elements
print(a.data)                       # Returns the buffer containing the actual elements of the array


# array creation
b = np.array([2, 3, 4])             # Basic way
c = np.array((2, 3, 4))             # Equivalent way
print(b)
print(c)

d = np.array([[2, 3, 4], [3, 4, 5]])
e = np.array([(2, 3, 4), (3, 4, 5)])
print(d)
print(e)

f = np.array((1.5, 2.3, 5.4), dtype = complex)
g = np.array(( [1.5, 4.6], [2.3, 5.4] ), dtype = complex)
print(f)
print(g)


# placeholder funcs
h = np.zeros( (3, 4), dtype = "int64" )
i = np.ones( (3, 2, 3) )
j = np.empty( (4, 5) )
print(h)
print(i)
print(j)


# in range and linspace
print(np.arange( 10, 30, 5 ))
print(np.arange( 0, 2, 0.3 ))
print(np.linspace( 0, 2, 9 ))
x = np.linspace( -np.pi, np.pi, 100 )
print(x)
print(np.sin(x))


# to large to be printed
print(np.arange( 0, 10000 ).reshape(100, 100))


# basic operations
k = np.array([[1, 5, 100], [2, 5435, 6]])
l = np.array([(2, 3, 4), (3, 4, 5)])
print(k + l)
print(k * l)
print(k < l)

m = np.array([[1, 5], [5435, 6]])
n = np.array([(2, 3), (4, 5)])
print(m @ n)

k += l
print(k)

o = np.random.random( (2, 3) )
print(o)
print(o.sum())
print(o.min())
print(o.max())

print(o.sum(axis = 1))


# universal funcs

# np.exp() and np.sqrt() and np.sin() and np.add() etc.


# indexing, sliciing and iterating
# unidimsional
p = np.arange(10)
print(p)
print(p[2])
print(p[:4])
print(p[:8:-1])
print(p[4:7:2])
p[:4] = 10
print(p)
for i in p:
    print(i**(1/2))

# multidimensional
q = np.fromfunction(lambda i, j: 10*i + j, (5, 4), dtype = int)
print("-" * 100)
print(q)
print(q[2, 1])
print(q[:2, 1])
print(q[2:4,:1:-1])

r = np.fromfunction(lambda i,j,k: 2*i + 5*j + k, (4,4,5), dtype = int)
print(r)
print(r[2,...,2])

print("-" * 100)

for e in q.flat:
    print(e)


""" Shape Manipulation """

# changing the shape of an array
s = np.floor(10*np.random.random((3, 4)))
print(s)
print(s.shape)
print(s.ravel())
print(s.ravel().shape)
print(s.reshape(4, 3))
print(s.T)
print(s.T.shape)
s.resize(2, 6)
print(s)
print(s.reshape(3,-1))
print(s.reshape(-1,2))

# stacking together different arrays
t = np.floor(2*np.random.random((2, 2)))
print(t)
u = np.floor(2*np.random.random((2, 2)))
print(u)
print(np.vstack((t,u)))
print(np.hstack((t,u)))

# + colunm_stack() and row_stack() and concatenate()

# splitting one array into several smaller ones
print(t)
print(np.hsplit(t,2))
print(np.hsplit(t,(1,2)))

# + vsplit() and array_split()


""" Copies and Views """
def arsf(*args):
    print(list(args))
    for e in args:
        print(e)
    print(len(args))
    print(args[0])

arsf(1,2,3,523452)

centerR = np.zeros(8, [("position", np.float32, 3), ("color", np.float32, 4)])
centerR["position"] = [(+1.7, +0.5, +0.5), (+0.7, +0.5, +0.5), (+0.7, -0.5, +0.5), (+1.7, -0.5, +0.5), (+1.7, -0.5, -0.5), (+1.7, +0.5, -0.5), (+0.7, +0.5, -0.5), (+0.7, -0.5, -0.5)]
centerR["color"] = [(0.0, 1.0, 0.5, 1.0), (0.0, 1.0, 0.5, 1.0), (0.0, 1.0, 0.5, 1.0), (0.0, 1.0, 0.5, 1.0), (0.0, 1.0, 0.5, 1.0), (0.0, 1.0, 0.5, 1.0), (0.0, 1.0, 0.5, 1.0), (0.0, 1.0, 0.5, 1.0)]
print(centerR)
dataIndices = np.array([0,1,3, 1,2,3, 5,0,4, 0,3,4, 6,5,7, 5,4,7, 1,6,2, 6,7,2, 5,6,0, 6,1,0, 7,4,2, 4,3,2], dtype = np.int32)

finalData = np.zeros(36, [("position", np.float32, 3)])

for count, i in enumerate(dataIndices):
    finalData["position"][count] = centerR["position"][i]

print(finalData)


tupel = (0, 1)
print(tupel)
print(*tupel)
print([*tupel])

subListIndexes = (0, 9)
print(subListIndexes[0])

convertedData = np.zeros(36, [("position", np.float32, 3), ("color", np.float32, 4), ("animationAngles", np.float32, 3)])
print(convertedData["animationAngles"])

test = np.arange(27)
print(test)
print(test[:9])
print(test[:9].reshape(3,3))
print(np.rot90(test[:9].reshape(3,3)).ravel())

test2 = np.rot90(test[:9].reshape(3,3)).ravel()
print([x for x in test if np.where(test == x) in test2])

cubeSideOrder = np.zeros(27).reshape(3,3,3)
"""
print(cubeSideOrder)
count = 0
for i in range(3):
    for j in range(3):
        for e in range(3):
            cubeSideOrder[i][j][2-e] = count
            count += 1

print(cubeSideOrder)
"""

for i in range(27):
    print((i - i%3 - 2*(i//3))%3)
    cubeSideOrder[i//9][(i - i%3 - 2*(i//3))%3][2-i%3] = i

print(cubeSideOrder)
print(np.rot90(cubeSideOrder, axes = (0,2))[0,:,:])
cubeSideOrder = np.rot90(cubeSideOrder, axes = (0,2))
print(cubeSideOrder)
cubeSideOrder[0,:,:] = np.rot90(cubeSideOrder[0,:,:], 3)
print(cubeSideOrder)
cubeSideOrder = np.rot90(cubeSideOrder, 3, axes = (0,2))
print(cubeSideOrder)
#cubeSideOrder = np.rot90(np.rot90(np.rot90(cubeSideOrder, axes = (0,2))[0,:,:], 3), 3, axes = (0,2))

a = np.ones(8, [("position", np.float32, 3)])
b = np.zeros(8, [("position", np.float32, 3)])
print(a)
a["position"] = b["position"]
print(a)
