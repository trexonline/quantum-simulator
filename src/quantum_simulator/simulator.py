from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate
from quantum_simulator.gate_operations.apply_cx import apply_cx
from quantum_simulator.gate_operations.apply_u import apply_u
import numpy as np


def simulate(qc: QuantumCircuit, parameters: dict | None = None) -> np.ndarray:
    """Simulates a transpiled quantum circuit using np.einsum() and returns the final state vector.
    The circuit is expected to contain only 'cx' and 'u' gates."""
    number_of_qubits=qc.num_qubits
    psi=np.zeros(2**number_of_qubits)
    psi[0]=1
    psi_converted = np.reshape(psi,[2]*number_of_qubits)

    for instr, qargs, _ in qc.data:
        qubit_indices = [qc.find_bit(q).index for q in qargs]

        if instr.name == "cx":
            cx=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
            psi_converted=apply_cx(psi_converted,cx,qubit_indices[0], qubit_indices[1])
        elif instr.name == "u":
            u=UGate(instr.params[0],instr.params[1],instr.params[2]).to_matrix()
            psi_converted=apply_u(psi_converted,u,qubit_indices[0])
        else:
            continue
    
    psi_final = np.reshape(np.asarray(psi_converted), (2**number_of_qubits,))
    return psi_final