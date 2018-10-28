from itertools import accumulate
import json


class DiscreteDistribution:
    def __init__(self, population, weights=None):
        self.population = [value for value in population]

        if weights:
            if len(population) is not len(weights):
                raise ValueError('Length of weights does not match length of population.')
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
        self.add_to_index(index, weight)

    def add_to_index(self, index, weight=1):
        self.weights[index] += weight


class BivariateDiscreteDistribution:
    def __init__(self, population_X, population_Y, weights=None):
        self.population_X = [value for value in population_X]
        self.population_Y = [value for value in population_Y]

        if weights:
            if len(population_Y) is not len(weights):
                raise ValueError('Shape of weights do not match expected shape -- Y.')
            for row in weights:
                if len(population_X) is not len(row):
                    raise ValueError('Shape of weights do not match expected shape -- X.')
            self.weights = [[weight for weight in weights_] for weights_ in weights]
        else:
            self.weights = [[0 for _ in population_X] for _ in population_Y]

    @classmethod
    def from_dict(cls, a_dict):
        return BivariateDiscreteDistribution(a_dict['population_X'], a_dict['population_Y'], a_dict['weights'])

    def add_to_index(self, index_x, index_y, weight=1):
        self.weights[index_y][index_x] += weight

    def add(self, value_x, value_y, weight=1):
        index_x = self.population_X.index(value_x)
        index_y = self.population_Y.index(value_y)
        self.add_to_index(index_x, index_y, weight)


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


class BivariateDiscreteDistributionSerializer(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'population_X': o.population_X,
                'population_Y': o.population_Y,
                'weights': o.weights
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
