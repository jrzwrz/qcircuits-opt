import pickle
from qiskit.quantum_info import Clifford
from qiskit import QuantumCircuit, qasm2
from qiskit.circuit.library import *
from generate_cayley_graph import Node
from testing import *
from shortest_path import *
import pandas as pd
import time

GateCountRange = range(5,51) #so as to include 50
QubitCountRange = range(2,3) #so as to include 2 (note: we are sticking to 2 qubits)
R = 20 #Number of circuits for given gate and qubit count
gset = [HGate(),CXGate(),SGate()] #CliffordSet


#We define a pandas DataFrame to store the results.
Dat = pd.DataFrame(columns = ['Original Circuit',
                              'Original Circuit QASM',
                              'Qubit Count',
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
                              '% Gate Count Reduction',
                              '% Depth Reduction',
                              '% H Reduction',
                              '% S Reduction',
                              '% CX Reduction'
                              ])


#Now we iterate through different gate and qubit counts
exec_count=0
for GateCount in GateCountRange:
    for QubitCount in QubitCountRange:
        for _ in range(R):
            qc = generate_random_circuit(gset, GateCount, QubitCount)
            qc_qasm = qasm2.dumps(qc)
            qc_depth = qc.depth()
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
                              'Qubit Count':QubitCount,
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
                              'Time':t,
                       '% Gate Count Reduction':(GateCount - qc_opt_gc)*100/GateCount,
                       '% Depth Reduction':(qc_depth - qc_opt_depth)*100/qc_depth,
                              '% H Reduction': 0 if qc_countsdict['h'] == 0 else (qc_countsdict['h'] - qc_opt_countsdict['h'])*100/qc_countsdict['h'],
                              '% S Reduction': 0 if qc_countsdict['s'] == 0 else (qc_countsdict['s'] - qc_opt_countsdict['s'])*100/qc_countsdict['s'],
                              '% CX Reduction': 0 if qc_countsdict['cx'] == 0 else (qc_countsdict['cx'] - qc_opt_countsdict['cx'])*100/qc_countsdict['cx']}
            Dat.loc[exec_count] = DataRow
            exec_count+=1


#We export the DataFrame as a .pkl as well as a .csv, so that they can be dealt with separately. 

Dat.to_pickle("./random_dat.pkl")  
Dat.to_csv('out.csv')


