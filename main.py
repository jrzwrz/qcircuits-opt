from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
from typing import Tuple
from gate_maps import gate_map_2, gate_map_3

class CircuitBFS:

    def __init__(self, n, gate_map):
        self.n = n
        self._known_states = {}
        self.gate_map = gate_map

    def bfs(self, target: Clifford):
        queue = []
        queue.append([])

        # while queue not empty, keep searching
        while queue:
            current_word = queue.pop(0)

            current_im_word = tuple(current_word)
            current_circuit = self.word_to_gate(current_im_word)
            self._known_states[current_im_word] = current_circuit

            if (current_circuit == target):
                return current_word, current_circuit

            for generator in self.gate_map.keys():
                next_word = current_word + [generator]
                next_circuit = self.word_to_gate(tuple(next_word))

                if (next_circuit not in self._known_states.values()):
                    queue.append(next_word)
        return None, None


    def word_to_gate(self, word: Tuple[str]):
        if (word in self._known_states):
            return self._known_states[word]

        qc = QuantumCircuit(self.n)
        for letter in word:
            if letter in self.gate_map:
                self.gate_map[letter](qc)

        cliff = Clifford(qc)
        return cliff

def get_sample_target(n):
    qc = QuantumCircuit(n)
    qc.h(0)
    qc.h(1)
    qc.h(1)
    qc.h(2)
    qc.cx(1, 0)
    qc.h(1)
    qc.h(0)
    qc.cx(1, 0)
    return Clifford(qc)

if __name__=='__main__':
    n = 3
    target = get_sample_target(n)
    qbfs = CircuitBFS(n, gate_map_3)
    word, circuit = qbfs.bfs(target)
    print(word)