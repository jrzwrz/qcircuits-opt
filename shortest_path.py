import pickle
from qiskit.quantum_info import Clifford
from qiskit import QuantumCircuit
from generate_cayley_graph import Node
from testing import get_random_clifford, random_clifford_circuit
import time

def dijkstra(nodes, start_key, target_key):
    dist = {k: float("inf") for k in nodes}
    prev = {k: None for k in nodes}
    dist[start_key] = 0

    heap = [(0, start_key)]
    while heap:
        d, u = heap.pop(0)
        if d > dist[u]:
            continue
        if u == target_key:
            break

        for gen_name, v in nodes[u].edges.items():
            # all weights are set to 1 for now
            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                prev[v] = (u, gen_name)
                heap.append((dist[v], v))

    # reconstruct path
    if dist[target_key] == float("inf"):
        return None  # no path
    path = []
    u = target_key
    while prev[u]:
        u_prev, gen = prev[u]
        path.append(gen)
        u = u_prev
    return list(reversed(path)), dist[target_key]

def opt_subroutine(qc):

    with open(f"cayley_graph_2_qubits.pkl", "rb") as f:
        nodes = pickle.load(f)

        n_qubits = qc.num_qubits
    
    
        identity = Node(Clifford.from_circuit(QuantumCircuit(n_qubits)))
    
        target = Node(Clifford(qc))
    
        result = dijkstra(nodes, identity.key, target.key)

        if result is None:
            qc_opt = None
            
        else:
            path, dist = result

            qc_opt = QuantumCircuit(n_qubits)
            for gate in path:
                if gate.startswith("H"):
                    pos = int(gate[1])
                    qc_opt.h(pos)
                elif gate.startswith("S"):
                    pos = int(gate[1])
                    qc_opt.s(pos)
                elif gate.startswith("CX"):
                    ctrl, tgt = int(gate[2]), int(gate[3])
                    qc_opt.cx(ctrl,tgt)

        return qc_opt

    

def opt_subroutine_with_time(qc): #This takes in the optimization subroutine and it also computes the time within the optimization process.
    start_time = time.time()
    qc_opt = opt_subroutine(qc)
    t = (time.time() - start_time)
    return qc_opt,t


if __name__=='__main__':
    with open(f"cayley_graph_2_qubits.pkl", "rb") as f:
        nodes = pickle.load(f)
    
    n_qubits = 2
    n_start_gates = 4

    identity = Node(Clifford.from_circuit(QuantumCircuit(n_qubits)))

    target = Node(get_random_clifford(n_qubits, n_start_gates))

    shortest_circuit, length = dijkstra(nodes, identity.key, target.key)
    print(f"Shortest circuit: {shortest_circuit}")
    print(f"Reduced from {n_start_gates} to {length}")