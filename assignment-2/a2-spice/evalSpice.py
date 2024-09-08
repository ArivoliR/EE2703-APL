import numpy as np


def evalSpice(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError("Please give the name of a valid SPICE file as input")

    components = {"V": [], "I": [], "R": []}
    nodes = {"GND": 0}
    node_index = 1

    def parse_line(line):
        # Remove comments
        if "#" in line:
            line = line[: line.index("#")]

        line = line.strip()
        if not line or line == ".circuit" or line == ".end":
            return

        parts = line.split()
        if len(parts) < 4:
            raise ValueError("Malformed circuit file")

        component_type = parts[0][0].upper()
        if component_type not in "VIR":
            raise ValueError("Only V, I, R elements are permitted")

        if component_type == "R":
            components["R"].append(parts[:4])
        elif component_type in "VI":
            if len(parts) < 5 or parts[3].lower() != "dc":
                raise ValueError("Malformed circuit file")
            components[component_type].append([parts[0], parts[1], parts[2], parts[4]])

    circuit_started = False
    circuit_ended = False
    for line in lines:
        if line.strip() == ".circuit":
            circuit_started = True
            continue
        if line.strip() == ".end":
            circuit_ended = True
            break
        if circuit_started:
            parse_line(line)

    if not circuit_started or not circuit_ended:
        raise ValueError("Malformed circuit file")

    # Mapping nodes to indices
    for comp in components["V"] + components["I"] + components["R"]:
        for node in comp[1:3]:
            if node not in nodes:
                nodes[node] = node_index
                node_index += 1

    # Number of nodes (excluding GND) and voltage sources
    N = len(nodes) - 1
    M = len(components["V"])

    # Initialize matrix and RHS vector
    matrix = np.zeros((N + M, N + M))
    b = np.zeros(N + M)

    # Fill matrix for resistors
    for comp in components["R"]:
        _, n1, n2, R = comp
        try:
            R = float(R)
            if R < 0:
                raise ValueError(f"Negative resistance value: {R}")
            elif R == 0:
                print(f"Warning: Zero resistance {comp} treated as a wire")
                components["V"].append([f"V_{n1}_{n2}", n1, n2, "0"])
            else:
                for node in [n1, n2]:
                    if node != "GND":
                        idx = nodes[node] - 1
                        matrix[idx, idx] += 1 / R
                if n1 != "GND" and n2 != "GND":
                    i, j = nodes[n1] - 1, nodes[n2] - 1
                    matrix[i, j] -= 1 / R
                    matrix[j, i] -= 1 / R
        except ValueError:
            raise ValueError(f"Invalid resistance specification: {comp}")

    # Fill matrix for voltage sources
    for i, comp in enumerate(components["V"]):
        _, n1, n2, V = comp
        try:
            V = float(V)
            if n1 != "GND":
                matrix[N + i, nodes[n1] - 1] = 1
                matrix[nodes[n1] - 1, N + i] = 1
            if n2 != "GND":
                matrix[N + i, nodes[n2] - 1] = -1
                matrix[nodes[n2] - 1, N + i] = -1
            b[N + i] = V
        except ValueError:
            raise ValueError(f"Invalid voltage source specification: {comp}")

    # Handle current sources
    for comp in components["I"]:
        _, n1, n2, I = comp
        try:
            I = float(I)
            if I == 0:
                print(f"Warning: Zero current source {comp} ignored")
            else:
                if n1 != "GND":
                    b[nodes[n1] - 1] -= I
                if n2 != "GND":
                    b[nodes[n2] - 1] += I
        except ValueError:
            raise ValueError(f"Invalid current source specification: {comp}")

    # Check for disconnected subcircuits
    if np.linalg.matrix_rank(matrix[:N, :N]) < N - 1:
        raise ValueError("Circuit contains disconnected subcircuits")

    # Solve the matrix
    try:
        solution = np.linalg.solve(matrix, b)
    except np.linalg.LinAlgError:
        raise ValueError("Circuit error: no solution")

    # Extract voltages and currents
    voltages = {"GND": 0.0}
    for node, idx in nodes.items():
        if node != "GND":
            voltages[node] = float(solution[idx - 1])

    currents = {
        comp[0]: float(solution[N + i]) for i, comp in enumerate(components["V"])
    }

    # Sort voltages dictionary by node name
    sorted_voltages = dict(
        sorted(voltages.items(), key=lambda x: (x[0] != "GND", x[0]))
    )
    return sorted_voltages, currents


if __name__ == "__main__":
    try:
        voltages, currents = evalSpice("sample_circuit.spice")
        print(f"({voltages}, {currents})")
    except Exception as e:
        print(f"{type(e).__name__}: {str(e)}")
