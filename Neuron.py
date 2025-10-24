import numpy as np

class Neuron:
    """Basic neuron model for SNN"""
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size) * 0.1
        self.bias = 0.0

    def forward(self, inputs):
        """Compute membrane potential"""
        return np.dot(inputs, self.weights) + self.bias
    
    def spike(self, potential, threshold=1.0):
        """Check if neuron spikes"""
        return potential > threshold
