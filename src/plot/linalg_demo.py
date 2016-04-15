import numpy as np
A = np.array([[2, 0], [0, 5]], dtype=float)
A[0,:]  # first row
A[:,1]  # second column

np.linalg.inv(A)  # inverse matrix
np.linalg.det(A)  # determinant

eig_values, eig_vectors = np.linalg.eig(A)
eig_values
eig_vectors

a = np.array([4, 0])
b = np.array([0, 1])
np.dot(A, a)         # matrix vector product
np.dot(a, b)         # dot product between vectors

B = np.ones((2, 2))  # 2x2 matrix with 1's
np.dot(A, B)         # matrix-matrix product

# cross product between vectors of length 3
np.cross([1, 1, 1], [0, 0, 1])
# Angle between a and b (pi/2)
np.arccos(np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b)))

B = np.array([[1, 2], [3, -4]], dtype=float)
B.T                # the transpose
np.sum(B)          # sum of all elements
np.sum(B, axis=0)  # sum over index 0 (rows)
np.sum(B, axis=1)  # sum over index 1 (columns)

np.max(B)          # max over all elements
B.max()            # max over all elements, alternative syntax
np.min(B)          # min over all elements
B.min()            # min over all elements, alternative syntax
np.abs(B).min()    # min absolute value

# Verify that the inverse is really the inverse
I = np.eye(2)   # identity matrix of size 2
I
np.abs(np.dot(A, np.linalg.inv(A)) - I).max()
np.dot(A, np.linalg.inv(A)) == I  # dangerous!!

np.linalg.norm(A)               # Frobenius norm for matrices
np.sqrt(np.sum(A**2))           # Frobenius norm, direct formula
np.linalg.norm(a)               # l2 norm for vectors

np.triu(B)  # upper triangular part of B
np.tril(B)  # lower triangular part of B
np.ones((3,4))  # 3x4 matrix with 1's
np.eye(3)   # identity matrix of size 3

C = np.array([[1,2,3],[4,5,6],[7,8,9]])
C[np.ix_([0,2], [1])]  # row 0 and 2, then column 1

# Solve linear system
A = np.array([[1, 2], [-2, 2.5]])
x = np.array([-1, 1], dtype=float)  # solution
b = np.dot(A, x)
np.linalg.solve(A, b)

C = np.hstack([A, B]) # stack two arrays horizontally
C
C = np.vstack([A, B]) # stack two arrays vertically
C
np.concatenate([A, B])
np.concatenate([a, b])
np.vstack([a, b])

import sympy as sym
A = sym.Matrix([[2, 0], [0, 5]])
A**-1    # the inverse
A.inv()  # the inverse
A.det()  # the determinant

A.eigenvals()
e = list(A.eigenvals().keys())
e
A.eigenvects()
# Isolate the first eigenvector
v1 = A.eigenvects()[0][2][0]
v1
# Extract the vector elements in a list
v1 = [v1[i,0] for i in range(v1.shape[0])]
v1
# Store all eigenvectors in a list of 2-lists
v = [[t[2][0][i,0] for i in range(t[2][0].shape[0])] for t in A.eigenvects()]
v


A.norm()
a = sym.Matrix([1, 2])
a
a.norm()

A*a
b = sym.Matrix([2, -1])
a.dot(b)

# Solve linear system
x = sym.Matrix([-1, 1])/2
x
b = A*x
x = A.LUsolve(b)  # does it compute x?
x                 # x is a matrix object
# Recreate as one-dim array with sym.Rational elements
x = np.array([x[i,0] for i in range(x.shape[0])])
x
# Find x as one-dim array with float values
x = A.LUsolve(b)
x = np.array([float(x[i,0].evalf()) for i in range(x.shape[0])])
x

# Row operations
A[1,:] + 2*A[0,:]  # [0,5] + 2*[2,0]


