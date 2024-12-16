# Importing libraries

import numpy as np
import copy
import matplotlib.pyplot as plt
import seaborn as sns


class DRV:
    """ A model for discrete random variables where outcomes are numeric """
    def __init__(self, dist=None, type=None, min_max=None, mean_std=None, bins=None, num_samples=None):
        self.dist = {} if dist is None else copy.deepcopy(dist)
        self.type = type
        self.min_max = min_max
        self.mean_std = mean_std
        self.bins = bins
        self.num_samples = num_samples

        if self.type == 'uniform':
            self.generate_uniform()
        elif self.type == 'normal' and mean_std is not None:
            self.generate_normal(mean_std, bins, num_samples)

    def generate_uniform(self):
        """ Generates a uniform distribution with specified bins and range"""
        min_val, max_val = self.min_max
        bin_edges = np.linspace(min_val, max_val, num=self.bins + 1)
        bin_centers = bin_edges[:-1] + (bin_edges[1:] - bin_edges[:-1]) / 2
        self.dist = dict(zip(bin_centers, np.full(self.bins, 1 / self.bins)))

    def generate_normal(self, mean_std, bins, num_samples):
        """Generates a normal distribution with specified mean, standard deviation, bins, and number of samples"""
        mean, std_dev = mean_std
        samples = np.random.normal(mean, std_dev, size=num_samples)
        bin_edges = np.linspace(np.min(samples), np.max(samples), bins + 1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_widths = bin_edges[1:] - bin_edges[:-1]
        self.dist = dict(zip(bin_centers, bin_widths))

    def __getitem__(self, x):
        return self.dist.get(x, 0.0)

    def __setitem__(self, x, p):
        self.dist[x] = p

    def expected_value(self):
        """Compute the expected value of the distribution"""
        values, probabilities = np.array(list(self.dist.keys())), np.array(list(self.dist.values()))
        return np.sum(values * probabilities)

    def standard_deviation(self):
        """Compute the standard deviation of the distribution"""
        values, probabilities = np.array(list(self.dist.keys())), np.array(list(self.dist.values()))
        expected_val = self.expected_value()
        variance = np.sum(((values - expected_val) ** 2) * probabilities)
        return np.sqrt(variance)

    def sample(self):
        """Randomly sample a value from the distribution"""
        values, probabilities = np.array(list(self.dist.keys())), np.array(list(self.dist.values()))
        sampled_value = np.random.choice(values, p=probabilities)
        return sampled_value

    def plot(self, title='', xscale='', yscale='', show_cumulative=False, log_scale=False, trials=0, bins=20):
        """Display the DRV distribution"""
        plt.figure(figsize=(10, 6))

        if trials == 0:
            plt.bar(self.dist.keys(), self.dist.values())
        else:
            sample = [self.sample() for i in range(trials)]
            sns.displot(sample, stat='probability', bins=bins, cumulative=show_cumulative, log_scale=log_scale)

        plt.title(title)
        plt.xlabel('Value')
        plt.ylabel('Probability')
        plt.show()

    def multiply(self, other):
        """Multiply two DRV distributions"""
        result_dist = {}
        for x, px in self.dist.items():
            for y, py in other.dist.items():
                result_dist[x * y] = px * py
        return DRV(dist=result_dist)
