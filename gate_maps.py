gate_map_2 = {
    "H1": lambda qc: qc.h(0),
    "H2": lambda qc: qc.h(1),
    "C1": lambda qc: qc.cx(0, 1),
    "C2": lambda qc: qc.cx(1, 0),
}
gate_map_3 = {
    "H1": lambda qc: qc.h(0),
    "H2": lambda qc: qc.h(1),
    "H3": lambda qc: qc.h(2),
    "C1": lambda qc: qc.cx(0, 1),
    "C2": lambda qc: qc.cx(1, 0),
}