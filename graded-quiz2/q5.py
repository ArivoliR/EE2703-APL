def truth_table_3(operator):
    operator = operator.upper() # i put this since input is case insensitive.
    if operator not in ["AND", "OR", "XOR"]:
        raise ValueError("Invalid operator.")

    truth_table = []
    for A in [False, True]:
        for B in [False, True]:
            for C in [False, True]:
                if operator == "AND":
                    result = A and B and C
                elif operator == "OR":
                    result = A or B or C
                elif operator == "XOR":
                    result = (A != B) != C  
                truth_table.append((A, B, C, result))
    
    return truth_table

