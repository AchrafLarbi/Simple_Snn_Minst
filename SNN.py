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

    def load_mnist_data(self, folder_path):
        """Load MNIST dataset from folder"""
        from pathlib import Path
        from PIL import Image
        
        images, labels = [], []
        for digit_folder in Path(folder_path).iterdir():
            if digit_folder.is_dir():
                digit = int(digit_folder.name)
                for img_file in digit_folder.glob('*.png'):
                    img = Image.open(img_file).convert('L')
                    images.append(np.array(img).flatten() / 255.0)
                    labels.append(digit)
        return np.array(images), np.array(labels)
