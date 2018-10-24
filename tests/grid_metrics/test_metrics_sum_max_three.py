import pytest

from analyze_grid import metrics_sum_max_three


@pytest.mark.parametrize("test_input,expected_score", [
    ([3, 5, 10, 18, 12, 6, 5, 14, 18], 50),
    ([6, 12, 13, 8, 14, 16, 12, 5, 6], 43)
])
def test_calculates_score_correctly(test_input, expected_score):
    # Act
    score = metrics_sum_max_three(test_input)

    # Assert
    assert score == expected_score
