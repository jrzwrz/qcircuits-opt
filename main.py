from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford

qc = QuantumCircuit(2)

qc.h(0)
qc.h(0)

cliff = Clifford(qc)

print("Clifford object:")
print(cliff)

print("\nClifford matrix:")
print(cliff.to_matrix())
