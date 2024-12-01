from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def inner_product(circuit, a):
    circuit.barrier() # Add vertical bars to separate blocks of instructions
    n = len(a)
    for i, bit in enumerate(reversed(a)):
        if bit == '1':
            circuit.cx(i, n)  # Add CNOT gate
    circuit.barrier()


def Hadamards(circuit):
    circuit.barrier()
    for qubit in range(circuit.num_qubits):
        circuit.h(qubit)
    circuit.barrier()


def bernstein_vazirani(a):
    n = len(a)
    circuit = QuantumCircuit(n + 1, n)
    circuit.x(n)
    Hadamards(circuit)
    inner_product(circuit, a)

    for qubit in range(n):
        circuit.h(qubit)
    circuit.barrier()

    for qubit in range(n):
        circuit.measure(qubit, qubit)

    return circuit


a = "01101"
circuit = bernstein_vazirani(a)

backend = AerSimulator()
compiled_circuit = transpile(circuit, backend)
n_shots = 1024
job_sim = backend.run(compiled_circuit, shots=n_shots)
result_sim = job_sim.result()
counts = result_sim.get_counts(compiled_circuit)

# Convert binary counts to decimal
decimal_counts = {int(key, 2): value for key, value in counts.items()}
probs = {key: value / n_shots for key, value in decimal_counts.items()}

print("Probabilities:", probs)
