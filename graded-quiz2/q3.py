def ohms_law(V, I, R):
    if [V, I, R].count(None) > 1:
        return "Error: Two parameters cannot be None"
    
    if V is not None and I is not None and R is not None:
        return "Error: All parameters are provided"
    
    if V is not None and not isinstance(V, (int, float)):
        return "Error: Invalid type for voltage"
    if I is not None and not isinstance(I, (int, float)):
        return "Error: Invalid type for current"
    if R is not None and not isinstance(R, (int, float)):
        return "Error: Invalid type for resistance"
    
    if V is None:
        return f"Voltage = {round(I * R, 1)}"
    if I is None:
        if R == 0:
            return "Error: Current cannot be zero"
        return f"Current = {round(V / R, 1)}"
    if R is None:
        if I == 0:
            return "Error: Current cannot be zero"
        return f"Resistance = {round(V / I, 1)}"

