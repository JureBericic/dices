import json
from random import choices

from dices.utils.discrete_distribution import DiscreteDistribution, DiscreteDistributionSerializer
from dices.roll_distribution_generators import generate_distribution_4d6dl


def metrics_sum_all(grid_values):
    """
    Calculates the sum of all grid values.
    Results in scores from
    :param grid_values: values of grid
    :return: metrics score
    """
    score = sum(grid_values)
    return score


def metrics_max_value(grid_values):
    """
    Calculates the maximal value of the grid.
    :param grid_values: values of grid
    :return: metrics score
    """
    score = max(grid_values)
    return score


def metrics_sum_max_three(grid_values):
    """
    Calculates the sum of the maximal three values of the grid.
    :param grid_values: values of the grid
    :return: metrics score
    """
    score = sum(sorted(grid_values, reverse=True)[:3])
    return score


def metrics_sum_max_selectable(grid_values):
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


if __name__ == '__main__':
    # initialize distributions
    distribution_sum_all = DiscreteDistribution([val for val in range(9*3, 9*18+1)])
    distribution_max_value = DiscreteDistribution([val for val in range(3, 18+1)])
    distribution_sum_max_three_weights = DiscreteDistribution([val for val in range(3*3, 3*18+1)])

    # roll grids
    roll_dist = generate_distribution_4d6dl.generate_distribution()
    num_grids = 10000000
    rolls = choices(roll_dist.population, cum_weights=roll_dist.cumulative_weights, k=9*num_grids)

    # generate distributions
    for i in range(num_grids):
        grid_values = rolls[i*9:(i+1)*9]

        distribution_sum_all.add_to_index(metrics_sum_all(grid_values) - 27)
        distribution_max_value.add_to_index(metrics_max_value(grid_values) - 3)
        distribution_sum_max_three_weights.add_to_index(metrics_sum_max_three(grid_values) - 9)

    # write distributions
    with open('data/distribution_sum_all.json', 'w') as fo:
        json.dump(distribution_sum_all, fo, cls=DiscreteDistributionSerializer, indent=4)

    with open('data/distribution_max_value.json', 'w') as fo:
        json.dump(distribution_max_value, fo, cls=DiscreteDistributionSerializer, indent=4)

    with open('data/distribution_sum_max_three_weights.json', 'w') as fo:
        json.dump(distribution_sum_max_three_weights, fo, cls=DiscreteDistributionSerializer, indent=4)

    print('end')
