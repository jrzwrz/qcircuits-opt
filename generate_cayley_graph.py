from qiskit.quantum_info import Clifford
from qiskit import QuantumCircuit
import time

def H(pos, num):
    return Clifford.from_label('I'*(num-pos-1)+'H'+'I'*pos)

def S(pos, num):
    return Clifford.from_label('I'*(num-pos-1)+'S'+'I'*pos)

def CX(ctrl, tgt, num):
    if ctrl == tgt: return None
    else:
        cxc = QuantumCircuit(num)  # We create the CX circuit since the label call doesnt exist for multi-qubit... 
        cxc.cx(ctrl,tgt)
        return (Clifford(cxc)) # Clifford Operation Composition

#Based on number of circuits, we have the following generators:
def get_generators(n: int):
    H_n = [ ('H'+str(i), H(i,n)) for i in range(n)]

    # not used?
    #S_n = [('S'+str(i), S(i,n)) for i in range(n)]

    CX_ijn = []
    for i in range(n):
        for j in range(n):
            if i!=j: CX_ijn.append(('CX'+str(i)+str(j),CX(i,j,n)))

    generators = H_n+CX_ijn
    return generators


class Node:
    def __init__(self, clifford, name=""):
        self.clifford = clifford
        self.edges = {}  # generator_name -> neighbor Node
        self.name = name  # optional: keep track of generator used
        self.key = self.get_clifford_key()

    def get_clifford_key(self):
        return self.clifford.tableau.tobytes()


def build_cayley_graph(generators, start, max_nodes=None):
    start_node = Node(start, "identity")
    nodes = {start_node.key: start_node}

    # use list instead of deque
    queue = [start_node]

    while queue:
        current = queue.pop(0)

        for gen_name, gen_op in generators:
            new_cliff = current.clifford.compose(gen_op)
            #new_key = clifford_key(new_cliff)
            new_node = Node(new_cliff, gen_name)

            if new_node.key not in nodes:
                new_node = Node(new_cliff, gen_name)
                nodes[new_node.key] = new_node
                queue.append(new_node)

            # connect edge
            current.edges[gen_name] = nodes[new_node.key]

        if max_nodes and len(nodes) >= max_nodes:
            break

    return nodes


if __name__=='__main__':
    n = 2
    generators = get_generators(n=n)
    identity = Clifford.from_circuit(QuantumCircuit(n))
    start = time.time()
    graph = build_cayley_graph(generators, identity)
    print(f"Time elapsed: {time.time()-start}s")

    print("Generated nodes:", len(graph))
    # for k, node in list(graph.items())[:5]:
    #     print("Node:", node.name, " | Outgoing edges:", list(node.edges.keys()))