import pickle
from qiskit.quantum_info import Clifford
from qiskit import QuantumCircuit, qasm2
from qiskit.circuit.library import *
from generate_cayley_graph import Node
from testing import *
from shortest_path import *
import pandas as pd
import time

#Here, we define some known test cases:

"""
Case 1: CNOT with the Hadamard transform on both sides - resulting in SWAPPED ctrl and tgt qubits.
Case 2: S_0 CX_(01) S_0^3 = CX(0,1) 
Case 3: Identity from paper: cPcPcP2cHcpH = I 
Case 4: (CX_ij H_j)^4 = (P_i)^2

"""

tc1 = QuantumCircuit(2)
tc1.h([0,1])
tc1.cx(0,1)
tc1.h([0,1])

tc2 = QuantumCircuit(2)
tc2.s(0)
tc2.s(0)
tc2.s(0)

tc3 = QuantumCircuit(2)
tc3.h(0)
tc3.s(1)
tc3.cx(1,0)
tc3.h(0)
tc3.cx(1,0)
tc3.s(0)
tc3.s(0) 
tc3.cx(1,0)
tc3.s(0) 
tc3.cx(1,0)
tc3.s(0) 
tc3.cx(1,0)

tc4 = QuantumCircuit(2)
tc4.h(0)
tc4.cx(1,0)
tc4.h(0)
tc4.cx(1,0)
tc4.h(0)
tc4.cx(1,0)
tc4.h(0)
tc4.cx(1,0)

test_cases = [tc1,tc2,tc3,tc4]

Dat = pd.DataFrame(columns = ['Original Circuit',
                              'Original Circuit QASM',
                              'Original Gate Count',
                              'Original Depth',
                              'H_0',
                              'S_0',
                              'CX_0',
                              'Optimized Circuit',
                              'Optimized Circuit QASM',
                              'Optimized Gate Count',
                              'Optimized Depth',
                              'H_Opt',
                              'S_Opt',
                              'CX_Opt',
                              'Time',
                              ])

exec_count=0
for qc in test_cases:

    qc_qasm = qasm2.dumps(qc)
    qc_depth = qc.depth()
    GateCount = len(qc.data)
    qc_gatelist = [i.operation.name for i in qc.data]
    qc_countsdict = {'h':qc_gatelist.count('h'),'s':qc_gatelist.count('s'),'cx':qc_gatelist.count('cx')}
        

    qc_opt,t = opt_subroutine_with_time(qc) 

    qc_opt_qasm = qasm2.dumps(qc_opt)
    qc_opt_gc = len(qc_opt.data)
    qc_opt_depth = qc_opt.depth()
    qc_opt_gatelist = [i.operation.name for i in qc_opt.data]
    qc_opt_countsdict = {'h':qc_opt_gatelist.count('h'),'s':qc_opt_gatelist.count('s'),'cx':qc_opt_gatelist.count('cx')}

    DataRow = {'Original Circuit':qc,
                          'Original Circuit QASM':qc_qasm,
                          'Original Gate Count':GateCount,
                          'Original Depth':qc_depth,
                          'H_0': qc_countsdict['h'],
                          'S_0': qc_countsdict['s'],
                          'CX_0': qc_countsdict['cx'],
                          'Optimized Circuit':qc_opt,
                          'Optimized Circuit QASM':qc_opt_qasm,
                          'Optimized Gate Count':qc_opt_gc,
                          'Optimized Depth':qc_opt_depth,
                          'H_Opt':qc_opt_countsdict['h'],
                          'S_Opt':qc_opt_countsdict['s'],
                          'CX_Opt':qc_opt_countsdict['cx'],
                          'Time':t,}
    Dat.loc[exec_count] = DataRow
    exec_count+=1

Dat.to_pickle("./ex_circs.pkl")  
Dat.to_csv('ex_circs.csv')