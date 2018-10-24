from itertools import accumulate
import json


class DiscreteDistribution:
    def __init__(self, population, weights=None):
        self.population = [value for value in population]

        if weights:
            self.weights = [weight for weight in weights]
        else:
            self.weights = [0 for _ in population]

    @classmethod
    def from_dict(cls, a_dict):
        return DiscreteDistribution(a_dict['population'], a_dict['weights'])

    @property
    def cumulative_weights(self):
        return list(accumulate(self.weights))

    @property
    def probability_distribution(self):
        sum_weights = sum(self.weights)
        return [weight/sum_weights for weight in self.weights]

    @property
    def cumulative_distribution(self):
        sum_weights = sum(self.weights)
        return [cumulative_weight/sum_weights for cumulative_weight in self.cumulative_weights]

    @property
    def complementary_cumulative_distribution(self):
        return [1 - val for val in self.cumulative_distribution]

    def add(self, value, weight=1):
        index = self.population.index(value)
        self.weights[index] += weight

    def add_to_index(self, index, weight=1):
        self.weights[index] += weight


class DiscreteDistributionSerializer(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'population': o.population,
                'weights': o.weights
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
