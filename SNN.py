import numpy as np
from Neuron import Neuron

class SNN:
    """Spiking Neural Network implementation"""
    def __init__(self, parameters):
        self.parameters = parameters
        self.input_size = 784  # 28x28 MNIST
        self.output_size = 10
        self.neurons = [Neuron(self.input_size) for _ in range(self.parameters.neuron_count)]
    
    def forward(self, inputs):
        """Forward pass through network"""
        outputs = []
        for neuron in self.neurons:
            potential = neuron.forward(inputs)
            spike = neuron.spike(potential)
            outputs.append(spike)
        return np.array(outputs)
