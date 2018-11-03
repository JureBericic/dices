import pytest

from analyze_grid import metrics_sum_max_selectable


@pytest.mark.parametrize("grid_values,expected_score", [
    ([18, 17, 16, 15, 14, 12, 13, 11, 10], 93),
    ([18, 17, 12, 16, 15, 11, 14, 10, 13], 93),
    ([18, 16, 14, 17, 15, 10, 12, 11, 13], 93),
    ([18, 11, 17, 16, 15, 12, 10, 14, 13], 93),
    ([18, 17, 16, 15, 14, 13, 12, 11, 10], 92),
    ([18, 15, 12, 17, 14, 11, 16, 13, 10], 92)
])
def test_calculated_score_correctly(grid_values, expected_score):
    # Act
    score = metrics_sum_max_selectable(grid_values)

    # Assert
    assert score == expected_score
