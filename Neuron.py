import numpy as np

class Neuron:
    """Basic neuron model for SNN"""
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size) * 0.1
        self.bias = 0.0
