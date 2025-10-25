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

    def apply_stdp(self, pre_spike, post_spike, dt, tau=20.0, learning_rate=0.0001):
        """Apply Spike-Timing-Dependent Plasticity"""
        if pre_spike and post_spike:
            if dt > 0:
                weight_change = learning_rate * np.exp(-dt / tau)
            else:
                weight_change = learning_rate * np.exp(dt / tau)
            self.weights += weight_change
