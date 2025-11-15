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

    def rate_encode(self, image, time_steps=None):
        """Rate-code image to spike train"""
        if time_steps is None:
            time_steps = self.parameters.time_steps
        normalized = image.reshape(-1)
        spike_trains = np.random.rand(len(normalized), time_steps) < normalized[:, np.newaxis]
        return spike_trains.astype(float)

    def train_epoch(self, data, labels):
        """Train for one epoch"""
        losses = []
        for sample, label in zip(data, labels):
            spike_train = self.rate_encode(sample)
            for t in range(spike_train.shape[1]):
                output = self.forward(spike_train[:, t])
            losses.append(0.0)  # Placeholder
        return np.mean(losses)

    def save_weights(self, path):
        """Save network weights"""
        weights = np.array([n.weights for n in self.neurons])
        np.savetxt(path, weights, delimiter=',')
    
    def load_weights(self, path):
        """Load network weights"""
        weights = np.loadtxt(path, delimiter=',')
        for i, neuron in enumerate(self.neurons):
            if i < len(weights):
                neuron.weights = weights[i]

    def apply_stdp_update(self, pre_spikes, post_spikes):
        """Apply STDP to all synapses"""
        for i, neuron in enumerate(self.neurons):
            if post_spikes[i]:
                for j, pre_spike in enumerate(pre_spikes):
                    dt = 1  # Time difference
                    neuron.apply_stdp(bool(pre_spike), True, dt, 
                                    self.parameters.tau_plus,
                                    self.parameters.stdp_learning_rate)

    def inference(self, spike_train, time_threshold=50):
        """Perform inference on spike train"""
        class_votes = np.zeros(self.output_size)
        
        for t in range(spike_train.shape[1]):
            output_spikes = self.forward(spike_train[:, t])
            for neuron_id, spike in enumerate(output_spikes):
                if spike:
                    class_id = neuron_id % self.output_size
                    class_votes[class_id] += 1
        
        return np.argmax(class_votes)

    def evaluate(self, data, labels):
        """Evaluate network on dataset"""
        predictions = []
        for sample in data:
            spike_train = self.rate_encode(sample)
            pred = self.inference(spike_train)
            predictions.append(pred)
        
        accuracy = np.mean(np.array(predictions) == labels)
        return accuracy

    def train_batch(self, batch_data, batch_labels):
        """Train on a batch of samples"""
        for sample, label in zip(batch_data, batch_labels):
            spike_train = self.rate_encode(sample)
            for t in range(spike_train.shape[1]):
                output = self.forward(spike_train[:, t])
                self.apply_stdp_update(spike_train[:, t], output)

    def get_layer_spikes(self, spike_train):
        """Get spike activity for visualization"""
        layer_activity = []
        for t in range(spike_train.shape[1]):
            spikes = self.forward(spike_train[:, t])
            layer_activity.append(spikes)
        return np.array(layer_activity)

    def get_weight_statistics(self):
        """Get statistics about network weights"""
        all_weights = np.concatenate([n.weights for n in self.neurons])
        return {
            'mean': np.mean(all_weights),
            'std': np.std(all_weights),
            'min': np.min(all_weights),
            'max': np.max(all_weights)
        }

    def validate_input(self, inputs):
        """Validate input dimensions"""
        if inputs.shape[0] != self.input_size:
            raise ValueError(f'Expected input size {self.input_size}, got {inputs.shape[0]}')

    def run(self):
        """Main execution method"""
        print("Initializing SNN...")
        print(f"Network: {self.parameters.neuron_count} neurons")
        print(f"Training epochs: {self.parameters.epochs}")
        print("Ready for training or inference")
