import numpy as np

def evalSpice(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise ValueError("File not found")

    components = {'V': [], 'I': [], 'R': []}
    nodes = {'GND': 0}
    node_index = 1

    def parse_line(line):
        line = line.split('#')[0].strip()
        parts = line.split()
        if not parts or parts[0] == '.circuit' or parts[0] == '.end':
            return
        
        component_type = parts[0][0]
        if component_type not in 'VIR':
            raise ValueError(f"Unknown component: {parts[0]}")
        
        if component_type == 'R':
            if len(parts) != 4:
                raise ValueError(f"Invalid resistor specification: {line.strip()}")
            components['R'].append(parts)
        elif component_type in 'VI':
            if len(parts) != 5 or parts[3].lower() != 'dc':
                raise ValueError(f"Invalid {component_type} source specification: {line.strip()}")
            components[component_type].append([parts[0], parts[1], parts[2], parts[4]])

    circuit_started = False
    for line in lines:
        line = line.strip()
        if line == '.circuit':
            circuit_started = True
            continue
        if line == '.end':
            break
        if circuit_started:
            parse_line(line)

    if not circuit_started:
        raise ValueError("Invalid circuit file: Missing .circuit")

    # Mapping nodes to indices
    for comp in components['V'] + components['I'] + components['R']:
        for node in comp[1:3]:
            if node not in nodes and node != 'GND':
                nodes[node] = node_index
                node_index += 1

    # Number of nodes (excluding GND) and voltage sources
    N = len(nodes) - 1  # Exclude GND
    M = len(components['V'])

    # Initialize matrix and RHS vector
    matrix = np.zeros((N + M, N + M))
    b = np.zeros(N + M)

    # Fill matrix for resistors
    for comp in components['R']:
        _, n1, n2, R = comp
        R = float(R)
        for node in [n1, n2]:
            if node != 'GND':
                idx = nodes[node] - 1
                matrix[idx, idx] += 1 / R
        if n1 != 'GND' and n2 != 'GND':
            i, j = nodes[n1] - 1, nodes[n2] - 1
            matrix[i, j] -= 1 / R
            matrix[j, i] -= 1 / R

    # Fill matrix for voltage sources
    for i, comp in enumerate(components['V']):
        _, n1, n2, V = comp
        V = float(V)
        if n1 != 'GND':
            matrix[N + i, nodes[n1] - 1] = 1
            matrix[nodes[n1] - 1, N + i] = 1
        if n2 != 'GND':
            matrix[N + i, nodes[n2] - 1] = -1
            matrix[nodes[n2] - 1, N + i] = -1
        b[N + i] = V

    # Handle current sources
    for comp in components['I']:
        _, n1, n2, I = comp
        I = float(I)
        if n1 != 'GND':
            b[nodes[n1] - 1] -= I
        if n2 != 'GND':
            b[nodes[n2] - 1] += I

    # Solve the matrix
    try:
        solution = np.linalg.solve(matrix, b)
    except np.linalg.LinAlgError:
        raise ValueError("The circuit equations are unsolvable. Check for loops of voltage sources or nodes with all current sources.")

    # Extract voltages and currents
    voltages = {'GND': 0.0}
    for node, idx in nodes.items():
        if node != 'GND':
            voltages[node] = round(float(solution[idx - 1]), 10)  # Round to 10 decimal places
    
    currents = {comp[0]: round(float(solution[N + i]), 10) for i, comp in enumerate(components['V'])}  # Round to 10 decimal places

    # Sort voltages dictionary by node name
    sorted_voltages = dict(sorted(voltages.items(), key=lambda x: (x[0] != 'GND', x[0])))

    return sorted_voltages, currents

if __name__ == "__main__":
    voltages, currents = evalSpice('sample_circuit.spice')
    print(f"({voltages},\n {currents})")
