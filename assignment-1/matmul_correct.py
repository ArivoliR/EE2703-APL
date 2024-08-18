def matrix_multiply(matrix1, matrix2):
    # This function should be implemented by the students
    # Placeholder implementation that always raises NotImplementedError
    # raise NotImplementedError("Matrix multiplication function not implemented")
    if len(matrix1) == 0 or len(matrix2) == 0:
        raise ValueError("Null matrix")
    
    if any(len(row) != len(matrix1[0]) for row in matrix1):
        raise ValueError("Incompatible matrix")
    if any(len(row) != len(matrix2[0]) for row in matrix2):
        raise ValueError("Incompatible matrix")
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Incompatible matrix")


    if not all(isinstance(item, (int, float)) for row in matrix1 for item in row):
        raise TypeError("All elements of matrix1 must be integers or floats")
    if not all(isinstance(item, (int, float)) for row in matrix2 for item in row):
        raise TypeError("All elements of matrix2 must be integers or floats")

    out = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                out[i][j] += matrix1[i][k] * matrix2[k][j]

    return out
