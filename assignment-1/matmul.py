"""
Program to output the product of two given matrices
Inputs: (matrix1, matrix2)
Output: matrix1*matrix2

Arivoli Ramamoorthy
EE23B008
"""


def matrix_multiply(matrix1, matrix2):

    # Ensures that both inputs are lists
    if not isinstance(matrix1, list) or not isinstance(matrix2, list):
        raise TypeError("Both inputs must be lists")

    # Raises error if the matrix inputted is empty
    if len(matrix1) == 0 or len(matrix2) == 0:
        raise ValueError("Null matrix")

    # Ensure that matrix1 and matrix2 are lists of lists
    if not all(isinstance(row, list) for row in matrix1):
        raise TypeError("matrix1 must be a list of lists")
    if not all(isinstance(row, list) for row in matrix2):
        raise TypeError("matrix2 must be a list of lists")

    # Checks if the number of columns in matrix1 matches the number of rows in matrix2
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Incompatible matrix dimension")

    # Checks if all rows in matrix1 and matrix2 are of same length
    if any(len(row) != len(matrix1[0]) for row in matrix1):
        raise ValueError("Incompatible matrix, row lengths are not same")
    if any(len(row) != len(matrix2[0]) for row in matrix2):
        raise ValueError("Incompatible matrix, row lengths are not same")

    # Checks if all elements in matrix1 and matrix2 are either integers or floats.
    if not all(isinstance(item, (int, float)) for row in matrix1 for item in row):
        raise TypeError("All elements of matrix1 must be integers or floats")
    if not all(isinstance(item, (int, float)) for row in matrix2 for item in row):
        raise TypeError("All elements of matrix2 must be integers or floats")

    # Initializing output matrix with zeros
    out = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]

    # iterating over rows of matrix1
    for i in range(len(matrix1)):
        # iterating over coloumns of matrix2
        for j in range(len(matrix2[0])):
            # iterating over coloumns of matrix1 and rows of matrix2
            for k in range(len(matrix2)):
                out[i][j] += matrix1[i][k] * matrix2[k][j]

    return out
