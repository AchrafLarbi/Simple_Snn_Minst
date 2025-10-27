import argparse

class Parameters:
    """Configuration parameters for SNN"""
    
    neuron_count = argparse.IntRange(10, 1000, '10')
    learning_rate = argparse.FloatRange(0.0001, 1.0, '0.01')
    time_steps = argparse.IntRange(10, 1000, '100')
    batch_size = argparse.IntRange(1, 256, '32')
    epochs = argparse.IntRange(1, 100, '10')

    # STDP parameters
    tau_plus = argparse.FloatRange(1.0, 100.0, '20.0')
    tau_minus = argparse.FloatRange(1.0, 100.0, '20.0')
    stdp_learning_rate = argparse.FloatRange(0.00001, 0.01, '0.0001')
