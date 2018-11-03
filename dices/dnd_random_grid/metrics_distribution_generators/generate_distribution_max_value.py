from random import choices
from pathlib import Path
import json

from dices.utils.discrete_distribution import DiscreteDistribution, DiscreteDistributionSerializer
from dices.dnd_random_grid.metrics import max_value


def generate_distribution(roll_distribution, metrics, k=1000):
    # initialization
    min_score = roll_distribution.population[0]
    max_score = roll_distribution.population[-1]
    score_distribution = DiscreteDistribution([score for score in range(min_score, max_score+1)])

    # roll grids
    rolls = choices(
        roll_distribution.population,
        cum_weights=roll_distribution.cumulative_weights,
        k=9*k
    )

    for i in range(k):
        grid_values = rolls[i*9:(i+1)*9]
        score = metrics(grid_values)
        score_distribution.add_to_index(score - min_score)

    return score_distribution


if __name__ == '__main__':
    roll_path = Path('../../../data/roll_distributions')
    score_path = Path('../../../data/dnd_random_grid/metrics_distributions')

    for roll in ('2d6p6', '3d6', '4d6dl'):
        print(f'Generating distribution for roll {roll}.')

        with Path(roll_path, f'{roll}.json').open('r') as fi:
            roll_distribution = json.load(fi, object_hook=DiscreteDistribution.from_dict)

        score_distribution = generate_distribution(roll_distribution, max_value, 10000000)

        with Path(score_path, f'max_value_{roll}.json').open('w') as fo:
            json.dump(score_distribution, fo, cls=DiscreteDistributionSerializer)
