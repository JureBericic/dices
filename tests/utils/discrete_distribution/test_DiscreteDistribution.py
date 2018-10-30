import pytest

from dices.utils.discrete_distribution import DiscreteDistribution


def test_initialized_correctly_without_weights():
    # Arrange
    population = [1, 2, 3]

    # Act
    dist = DiscreteDistribution(population)

    # Assert
    assert dist.population == population
    assert dist.weights == [0, 0, 0]


def test_initialized_correctly_with_weights():
    # Arrange
    population = [1, 2, 3]
    weights = [4, 5, 6]

    # Act
    dist = DiscreteDistribution(population, weights)

    # Assert
    assert dist.population == population
    assert dist.weights == weights


def test_raises_when_incorrect_length_of_weights():
    # Arrange
    population = [1, 2, 3]
    weights = [4, 5]

    # Assert
    with pytest.raises(ValueError):
        DiscreteDistribution(population, weights)


def test_from_dict_constructs_properly():
    # Arrange
    a_dict = {
        'population': [1, 2, 3],
        'weights': [4, 5, 6]
    }

    # Act
    dist = DiscreteDistribution.from_dict(a_dict)

    # Arrange
    assert dist.population == a_dict['population']
    assert dist.weights == a_dict['weights']


def test_cumulative_weights_are_calculated_correctly():
    # Arrange
    dist = DiscreteDistribution([1, 2, 3], [4, 5, 6])

    # Act
    cumulative_weights = dist.cumulative_weights

    # Assert
    assert cumulative_weights == [4, 9, 15]


def test_probability_distribution_is_calculated_correctly():
    # Arrange
    dist = DiscreteDistribution([1, 2, 3], [1, 5, 4])

    # Act
    probability_distribution = dist.probability_distribution

    # Assert
    assert probability_distribution == [0.1, 0.5, 0.4]


def test_cumulative_distribution_is_calculated_correctly():
    # Arrange
    dist = DiscreteDistribution([1, 2, 3], [1, 5, 4])

    # Act
    cumulative_distribution = dist.cumulative_distribution

    # Assert
    assert cumulative_distribution == [0.1, 0.6, 1.0]


def test_complementary_cumulative_distribution_is_calculated_correctly():
    # Arrange
    dist = DiscreteDistribution([1, 2, 3], [1, 5, 4])

    # Act
    complementary_cumulative_distribution = dist.complementary_cumulative_distribution

    # Assert
    assert complementary_cumulative_distribution == [0.9, 0.4, 0.0]


@pytest.mark.parametrize("test_input,expected_weights", [
    ({'value': 2}, [0, 1, 0]),
    ({'value': 2, 'weight': 3}, [0, 3, 0]),
])
def test_add_adds_correctly(test_input, expected_weights):
    # Arrange
    dist = DiscreteDistribution([1, 2, 3])

    # Act
    dist.add(**test_input)

    # Assert
    assert dist.weights == expected_weights


@pytest.mark.parametrize("test_input,expected_weights", [
    ({'index': 2}, [0, 0, 1]),
    ({'index': 2, 'weight': 3}, [0, 0, 3]),
])
def test_add_to_index_adds_correctly(test_input, expected_weights):
    # Arrange
    dist = DiscreteDistribution([1, 2, 3])

    # Act
    dist.add_to_index(**test_input)

    # Assert
    assert dist.weights == expected_weights


