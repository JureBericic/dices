import pytest

from dices.utils.discrete_distribution import BivariateDiscreteDistribution


def test_initialized_correctly_without_weights():
    # Arrange
    population_X = [1, 2]
    population_Y = [10, 20, 30]

    # Act
    dist = BivariateDiscreteDistribution(population_X, population_Y)

    # Assert
    assert dist.population_X == population_X
    assert dist.population_Y == population_Y
    assert dist.weights == [[0, 0], [0, 0], [0, 0]]


def test_initialized_correctly_with_weights():
    # Arrange
    population_X = [1, 2]
    population_Y = [10, 20, 30]
    weights = [
        [11, 12],
        [21, 22],
        [31, 32]
    ]

    # Act
    dist = BivariateDiscreteDistribution(population_X, population_Y, weights)

    # Assert
    assert dist.population_X == population_X
    assert dist.population_Y == population_Y
    assert dist.weights == weights


@pytest.mark.parametrize("weights", [
    [[11, 12], [21, 22]],
    [[11, 12], [21, 22], [31, 32, 33]]
])
def test_raises_when_incorrect_shape_of_weights(weights):
    # Arrange
    population_X = [1, 2]
    population_Y = [10, 20, 30]

    # Assert
    with pytest.raises(ValueError):
        BivariateDiscreteDistribution(population_X, population_Y, weights)


def test_from_dict_constructs_properly():
    # Arrange
    a_dict = {
        'population_X': [1, 2],
        'population_Y': [10, 20, 30],
        'weights': [[11, 12], [21, 22], [31, 32]]
    }

    # Act
    dist = BivariateDiscreteDistribution.from_dict(a_dict)

    # Arrange
    assert dist.population_X == a_dict['population_X']
    assert dist.population_Y == a_dict['population_Y']
    assert dist.weights == a_dict['weights']


@pytest.mark.parametrize("index_x,index_y,weight,expected_weights", [
    (1, 0, None, [[0, 1], [0, 0], [0, 0]]),
    (0, 2, 3, [[0, 0], [0, 0], [3, 0]])
])
def test_add_to_index_adds_correctly(index_x, index_y, weight, expected_weights):
    # Arrange
    dist = BivariateDiscreteDistribution([1, 2], [10, 20, 30])

    # Act
    if weight is None:
        dist.add_to_index(index_x, index_y)
    else:
        dist.add_to_index(index_x, index_y, weight)

    # Assert
    assert dist.weights == expected_weights


@pytest.mark.parametrize("population_X,population_Y,weights,expected_cumulative_weights", [
    ([1, 2], [10, 20, 30], [[11, 12], [21, 22], [31, 32]], [[11, 23], [32, 66], [63, 129]]),
    ([1], [10, 20], [[11], [21]], [[11], [32]]),
    ([1, 2], [10], [[11, 12]], [[11, 23]]),
    ([1], [10], [[11]], [[11]])
])
def test_cumulative_weights_are_calculated_correctly(population_X, population_Y, weights, expected_cumulative_weights):
    # Arrange
    dist = BivariateDiscreteDistribution(population_X, population_Y, weights)

    # Act
    cumulative_weights = dist.cumulative_weights

    # Assert
    assert cumulative_weights == expected_cumulative_weights


def test_probability_distribution_is_calculated_correctly():
    # Arrange
    dist = BivariateDiscreteDistribution([1, 2], [10, 20, 30], [[20, 30], [40, 50], [24, 36]])

    # Act
    probability_distribution = dist.probability_distribution

    # Assert
    assert probability_distribution == [[0.10, 0.15], [0.20, 0.25], [0.12, 0.18]]


def test_cumulative_distribution_is_calculated_correctly():
    # Arrange
    dist = BivariateDiscreteDistribution([1, 2], [10, 20, 30], [[20, 30], [40, 50], [24, 36]])

    # Act
    cumulative_distribution = dist.cumulative_distribution

    # Assert
    assert cumulative_distribution == [[0.10, 0.25], [0.30, 0.70], [0.42, 1.00]]


def test_marginal_distribution_X_is_calculated_correctly():
    # Arrange
    dist = BivariateDiscreteDistribution([1, 2], [10, 20, 30], [[20, 30], [40, 50], [24, 36]])

    # Act
    marginal_distribution_X = dist.marginal_distribution_X

    # Assert
    assert marginal_distribution_X == [0.42, 0.58]


def test_marginal_distribution_Y_is_calculated_correctly():
    # Arrange
    dist = BivariateDiscreteDistribution([1, 2], [10, 20, 30], [[20, 30], [40, 50], [24, 36]])

    # Act
    marginal_distribution_Y = dist.marginal_distribution_Y

    # Assert
    assert marginal_distribution_Y == [0.25, 0.45, 0.30]


@pytest.mark.parametrize("value_x,value_y,weight,expected_weights", [
    (2, 10, None, [[0, 1], [0, 0], [0, 0]]),
    (1, 30, 3, [[0, 0], [0, 0], [3, 0]])
])
def test_add_adds_correctly(value_x, value_y, weight, expected_weights):
    # Arrange
    dist = BivariateDiscreteDistribution([1, 2], [10, 20, 30])

    # Act
    if weight is None:
        dist.add(value_x, value_y)
    else:
        dist.add(value_x, value_y, weight)

    # Assert
    assert dist.weights == expected_weights


