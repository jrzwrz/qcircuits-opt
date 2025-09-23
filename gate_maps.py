gate_map_2 = {
    "H1": lambda qc: qc.h(0),
    "H2": lambda qc: qc.h(1),
    "C1": lambda qc: qc.cx(0, 1),
    "C2": lambda qc: qc.cx(1, 0),
    "S1": lambda gc: gc.s(0),
    "S2": lambda gc: gc.s(1)
}

gate_map_3 = {
    "H1": lambda qc: qc.h(0),
    "H2": lambda qc: qc.h(1),
    "H3": lambda qc: qc.h(2),
    "C12": lambda qc: qc.cx(0, 1),
    "C13": lambda qc: qc.cx(0, 2),
    "C21": lambda qc: qc.cx(1, 0),
    "C23": lambda qc: qc.cx(1, 2),
    "C31": lambda qc: qc.cx(2, 0),
    "C32": lambda qc: qc.cx(2, 1),
    "S1": lambda gc: gc.s(0),
    "S2": lambda gc: gc.s(1),
    "S3": lambda gc: gc.s(2)
}