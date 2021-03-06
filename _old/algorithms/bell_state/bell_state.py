from .. import *

def bell_state(img_path = IMG_PATH, hardware = False):
    qreg = QuantumRegister(2, 'q')
    creg = ClassicalRegister(2, 'c')
    qc   = QuantumCircuit(qreg, creg)

    # Create bell state itself by putting first qubit into superposition and then applying a CNOT gate between the two qubits
    qc.h(qreg[0])
    qc.cx(qreg[0], qreg[1])

    # Measure both qubits
    qc.measure(qreg[0], creg[0])
    qc.measure(qreg[1], creg[1])

    # Run circuit and output
    if hardware:
        provider = IBMQ.get_provider(hub='ibm-q')
        backend  = least_busy(provider.backends())
    else:
        backend = BasicAer.get_backend('qasm_simulator')

    result   = execute(qc, backend, shots = 1024).result()
    counts   = result.get_counts(qc)
    print(counts)

    qc.draw(output = "mpl", filename = join(img_path, 'circuit.jpg'))
    plot_histogram(counts).savefig(join(img_path, 'histogram.jpg'))