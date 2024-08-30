import io
from collections import defaultdict

def circuit_count(msg):
    dict = defaultdict(lambda: 0)
    sfp = io.StringIO(msg)
    inside_circuit = False

    for line in sfp.readlines():
        line = line.strip()

        if line == ".circuit":
            inside_circuit = True
        elif line == ".end":
            inside_circuit = False
        elif inside_circuit:
            parts = line.split()
            if parts:
                type = parts[0][0].upper()
                dict[type] += 1

    return dict

