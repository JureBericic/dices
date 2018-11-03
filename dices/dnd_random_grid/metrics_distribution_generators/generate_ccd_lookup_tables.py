from pathlib import Path
import json

from dices.utils.discrete_distribution import DiscreteDistribution


distribution_root_path = Path('../../../data/dnd_random_grid/metrics_distributions')
metrics = ['max_value', 'sum_all', 'sum_max_selectable', 'sum_max_three']

for metric in metrics:
    # load all distributions for this metric
    files = distribution_root_path.glob(f'{metric}_*.json')
    distributions = []
    for file in sorted(files, key=lambda f: f.name):
        roll = file.name[len(metric)+1:-5]

        with file.open('r') as fi:
            distribution = json.load(fi, object_hook=DiscreteDistribution.from_dict)
            distributions.append([roll, distribution])

    # table should cover all scores
    min_score = min([distribution.population[0] for _, distribution in distributions])
    max_score = max([distribution.population[-1] for _, distribution in distributions])
    joint_population = list(range(min_score, max_score+1))

    # calculate the complementary cumulative distribution for each roll
    for dist in distributions:
        offset = joint_population.index(dist[1].population[0])

        ccd = [0.0 for _ in joint_population]
        ccd[0:offset] = [1.0]*offset
        ccd[offset:offset+len(dist[1].population)] = dist[1].complementary_cumulative_distribution

        dist.append(ccd)

    # create a csv file
    # title row
    content = 'score'
    for roll, _, _ in distributions:
        content += ',{0:>8s}'.format(roll)
    # data rows
    for i, score in enumerate(joint_population):
        content += '\n{0:>5d}'.format(score)
        for _, _, ccd in distributions:
            content += ',{0:>8.5f}'.format(ccd[i])

    # write table
    with Path(distribution_root_path, f'{metric}_ccd.csv').open('w') as fo:
        fo.write(content)
