import random
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford


def random_clifford_circuit(n_qubits, n_gates):
    """
    Generate a random Clifford circuit where H, S, and CNOT appear with equal probability.
    
    Args:
        n_qubits (int): number of qubits
        n_gates (int): number of gates
    
    Returns:
        list of str: list of gates as strings (e.g., 'h0', 's1', 'cx01')
    """
    circuit = []
    
    for _ in range(n_gates):
        # Step 1: pick gate type equally
        gate_type = random.choice(['h', 's', 'cx', 'cx']) # add/remove elements to change probability of having each gate
        
        # Step 2: pick qubit(s)
        if gate_type in ['h', 's']:
            qubit = random.randint(0, n_qubits - 1)
            circuit.append(f'{gate_type}{qubit}')
        else:  # 'cx'
            # pick an ordered pair
            control, target = random.sample(range(n_qubits), 2)
            circuit.append(f'cx{control}{target}')
    
    print(f"Start with circuit: {circuit}")
    return circuit


def string_to_circuit(gate_list, n_qubits):
    """
    Given a list of gate symbols (like 'h0', 's1', 'cx01'), create and draw a Qiskit circuit.
    
    Args:
        gate_list (list of str): gates in symbolic form
        n_qubits (int): number of qubits
    
    Returns:
        QuantumCircuit: Qiskit circuit object
    """
    qc = QuantumCircuit(n_qubits)
    
    for gate in gate_list:
        if gate[0] == 'h':
            qubit = int(gate[1:])
            qc.h(qubit)
        elif gate[0] == 's':
            qubit = int(gate[1:])
            qc.s(qubit)
        elif gate[:2] == 'cx':
            control = int(gate[2])
            target = int(gate[3])
            qc.cx(control, target)
        else:
            raise ValueError(f"Unknown gate symbol: {gate}")
    
    return qc

def get_random_clifford(n_qubits, n_gates):
    circuit_string = random_clifford_circuit(n_qubits, n_gates)
    qc = string_to_circuit(circuit_string, n_qubits)
    return Clifford(qc)

def generate_random_circuit(generator_gates, n_gates, n_qubits): 

    """
    Given a list of generator gates, create a random circuit.
    
    Args:
        gate_list (list of str): gates in symbolic form
        n_qubits (int): number of qubits
    
    Returns:
        QuantumCircuit: Qiskit circuit object
    """
    
    qc = QuantumCircuit(n_qubits)

    for i in range(n_gates):

        gate = random.choice(generator_gates)
        gate_qub = gate.num_qubits
         
        qubits = random.sample(range(n_qubits), gate_qub)
        qc.append(gate,qubits)
    
    return qc
  


if __name__=='__main__':
    cliff = get_random_clifford(2, 4)
    print(cliff)