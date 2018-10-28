import json

import dices.utils.discrete_distribution as dd


def test_serializes_correctly():
    # Arrange
    dist = dd.BivariateDiscreteDistribution([1, 2], [10, 20, 30], [[11, 12], [21, 22], [31, 32]])
    expected_json = """
{
    "population_X": [1, 2],
    "population_Y": [10, 20, 30],
    "weights": [[11, 12], [21, 22], [31, 32]]
}
"""

    # Act
    dist_json = json.dumps(dist, cls=dd.BivariateDiscreteDistributionSerializer)

    # Assert
    json.loads(dist_json) == json.loads(expected_json)
