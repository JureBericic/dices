import dices.utils.discrete_distribution as dd


def generate_distribution():
    # initialization
    population = list(range(3, 18+1))
    distribution = dd.DiscreteDistribution(population)

    # loop over all possibilities
    ds = [0, 0, 0, 0]
    for d0 in range(1, 6+1):
        ds[0] = d0
        for d1 in range(1, 6+1):
            ds[1] = d1
            for d2 in range(1, 6+1):
                ds[2] = d2
                for d3 in range(1, 6+1):
                    ds[3] = d3
                    roll = sum(ds) - min(ds)
                    distribution.add_to_index(roll - 3)

    return distribution


if __name__ == '__main__':
    import json

    print('Generating distribution for 4D6 drop lowest rolls.')
    dist = generate_distribution()

    with open('../../data/roll_distributions/roll_distribution_4d6dl.json', 'w') as fo:
        json.dump(dist, fo, cls=dd.DiscreteDistributionSerializer)
