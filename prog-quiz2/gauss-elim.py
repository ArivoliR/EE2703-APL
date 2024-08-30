'''
Arivoli Ramamoorthy
EE23B008
Programming quiz-2
'''
def gausselim(A, B):
    n = len(A)
    
    for i in range(n):
        # Normalize the pivot row
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        B[i] /= pivot

        # Eliminate column below pivot
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            B[k] -= factor * B[i]

    # Sub back and solve for B[0] <-> x1
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            B[i] -= A[i][j] * B[j]

    return B

#Tests:
'''
A = [ [2,3, 4], [1,-1, 2], [1, 5, 3] ]
B = [6, 0.5, 2]
Bout = gausselim(A, B)
Bexp = [10.5,  1. , -4.5]
s = 0
for i in range(len(Bout)):
    s += abs(Bout[i] - Bexp[i])
#print(Bout)
#print(Bexp)
if s < 0.01:
  print("PASS")
else:
  print("FAIL")

A = [ [2,3], [1,-1] ]
B = [6,1/2]
Bout = gausselim(A, B)
Bexp = [1.5, 1. ]
s = 0
for i in range(len(Bout)):
    s += abs(Bout[i] - Bexp[i])
#print(Bout)
#print(Bexp)
if s < 0.01:
  print("PASS")
else:
  print("FAIL")

A = [[0.26399197, 0.7078364 , 0.74605183, 0.52658905],
       [0.3187093 , 0.69157511, 0.55497212, 0.72189566],
       [0.96727446, 0.57382705, 0.74889902, 0.76056476],
       [0.58070383, 0.97389366, 0.26139946, 0.00913732]]
B = [0.0140597 , 0.46419182, 0.20868931, 0.65451389]
Bout = gausselim(A, B)
Bexp = [ 0.19335079,  0.96322792, -1.54304119,  0.82112907]
s = 0
for i in range(len(Bout)):
    s += abs(Bout[i] - Bexp[i])
if s < 0.01:
  print("PASS")
else:
  print("FAIL")
'''
