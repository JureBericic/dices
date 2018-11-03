def sum_all(grid_values):
    """
    Calculates the sum of all grid values.
    Results in scores from
    :param grid_values: values of grid
    :return: metrics score
    """
    score = sum(grid_values)
    return score


def max_value(grid_values):
    """
    Calculates the maximal value of the grid.
    :param grid_values: values of grid
    :return: metrics score
    """
    score = max(grid_values)
    return score


def sum_max_three(grid_values):
    """
    Calculates the sum of the maximal three values of the grid.
    :param grid_values: values of the grid
    :return: metrics score
    """
    score = sum(sorted(grid_values, reverse=True)[:3])
    return score


def sum_max_selectable(grid_values):
    """
    Calculated the sum of maximal selectable values of the grid.
    :param grid_values: values of the grid
    :return: metrics score
    """
    grid = [(value, i//3, i%3) for i, value in enumerate(grid_values)]
    sorted_grid = sorted(grid, key=lambda e: e[0], reverse=True)
    rows = set(element[1] for element in sorted_grid[:6])
    columns = set(element[2] for element in sorted_grid[:6])

    if len(rows) is len(columns) is 3:
        score = sum(element[0] for element in sorted_grid[:6])
    else:
        score = sum(element[0] for element in sorted_grid[:5]) + sorted_grid[7-1][0]
    return score
