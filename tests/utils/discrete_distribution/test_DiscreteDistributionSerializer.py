import json

from dices.utils import discrete_distribution


def test_serializes_correctly():
    # Arrange
    dist = discrete_distribution.DiscreteDistribution([1, 2, 3], [4, 5, 6])
    expected_json = """
{
"population": [1, 2, 3],
"weights": [4, 5, 6]
}
"""

    # Act
    dist_json = json.dumps(dist, cls=discrete_distribution.DiscreteDistributionSerializer)

    # Assert
    json.loads(dist_json) == json.loads(expected_json)