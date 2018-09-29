import numpy as np

# important funcs
a = np.arange(15).reshape(3, 5)     # Creates an array with numbers from 0 to 14 and rearanges it so it becomes a 3 x 5 matrix
print(a)
print(a.ndim)                       # Amount of dimensions
print(a.shape)                      # Amount of values per dimension
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

# exp and sqrt and sin and etc.


# indexing, sliciing and iterating
