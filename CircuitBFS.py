from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
from typing import Tuple
from gate_maps import gate_map_2, gate_map_3
import numpy as np
import time

class CircuitBFS:

    def __init__(self, n, gate_map):
        self.n = n
        self._known_states = {}
        self.gate_map = gate_map
        self._known_states_set = set()

    def bfs(self, target: Clifford):
        queue = []
        queue.append([])

        # while queue not empty, keep searching
        while queue:
            current_word = queue.pop(0)

            current_im_word = tuple(current_word)
            current_circuit = self.word_to_gate(current_im_word)

            hsh = hash(bytes(current_circuit.tableau.data))
            if hsh in self._known_states_set:
                continue

            self._known_states[current_im_word] = current_circuit
            self._known_states_set.add(hsh)

            if (current_circuit == target):
                return current_word, current_circuit

            for generator in self.gate_map.keys():
                next_word = current_word + [generator]
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
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.h(0)
    qc.cx(0, 2)
    return Clifford(qc)

if __name__=='__main__':
    n = 3
    target = get_sample_target(n)
    qbfs = CircuitBFS(n, gate_map_3)
    start_time = time.time()
    word, circuit = qbfs.bfs(target)
    print(word)
    print(f'Ran for {(time.time() - start_time)} seconds')