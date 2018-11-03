import pytest

from analyze_grid import metrics_sum_all


@pytest.mark.parametrize("grid_values,expected_score", [
    ([3, 5, 10, 18, 12, 6, 5, 14, 18], 91),
    ([6, 12, 13, 8, 14, 18, 12, 5, 6], 94)
])
def test_calculates_score_correctly(grid_values, expected_score):
    # Act
    score = metrics_sum_all(grid_values)

    # Assert
    assert score == expected_score
