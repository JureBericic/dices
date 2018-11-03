import dices.utils.discrete_distribution as dd


def generate_distribution():
    # initialization
    population = list(range(8, 18+1))
    distribution = dd.DiscreteDistribution(population)

    # loop over all possibilities
    for d0 in range(1, 6+1):
        for d1 in range(1, 6+1):
            roll = d0 + d1
            distribution.add_to_index(roll+6-8)

    return distribution


if __name__ == '__main__':
    import json

    print('Generating distribution for 2D6 + 6 rolls.')
    dist = generate_distribution()

    with open('../../data/roll_distributions/2d6p6.json', 'w') as fo:
        json.dump(dist, fo, cls=dd.DiscreteDistributionSerializer)
