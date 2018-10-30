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

    @property
    def cumulative_weights(self):
        cumulative_weights = [list(accumulate(weights_)) for weights_ in self.weights]
        for j in range(1, len(cumulative_weights)):
            for i in range(len(cumulative_weights[j])):
                cumulative_weights[j][i] += cumulative_weights[j-1][i]

        return cumulative_weights

    @property
    def probability_distribution(self):
        sum_weights = sum([sum(weights_) for weights_ in self.weights])
        return [[weight/sum_weights for weight in weights_] for weights_ in self.weights]

    @property
    def cumulative_distribution(self):
        sum_weights = sum([sum(weights_) for weights_ in self.weights])
        return [
            [cumulative_weight/sum_weights for cumulative_weight in cumulative_weight_]
            for cumulative_weight_ in self.cumulative_weights
        ]

    @property
    def marginal_distribution_X(self):
        sum_weights = sum([sum(weights_) for weights_ in self.weights])
        weights = self.weights
        weights_X = [
            sum([weights[j][i] for j, _ in enumerate(self.population_Y)])
            for i, _ in enumerate(self.population_X)
        ]
        return [weight_X/sum_weights for weight_X in weights_X]

    @property
    def marginal_distribution_Y(self):
        sum_weights = sum([sum(weights_) for weights_ in self.weights])
        weights_Y = [sum(weights_) for weights_ in self.weights]
        return [weight_Y/sum_weights for weight_Y in weights_Y]

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
