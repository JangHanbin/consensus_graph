import matplotlib.pyplot as plt
import math
import operator as op
from functools import reduce
from itertools import combinations


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)

    return int(numer // denom)


def safety_of_consensus(a, max_of_validator, num_of_nodes):
    results = list()
    # m must be smaller than 0.99 * n
    for m in max_of_validator:
        sum = 0
        for i in range(math.ceil(m / 3), int(min(m, num_of_nodes * a / 100)) + 1):
            result = (ncr(int(num_of_nodes * a / 100), i) * ncr(int(num_of_nodes * (1 - (a / 100))), m - i)) / ncr(num_of_nodes, m)

            sum += result
        print('processing {0} of {1}'.format(m, max(max_of_validator)))

        # print('Node : {0}, Validator : {1} = {2}'.format(num_of_nodes, m, (1- sum) * 100))
        # insert by percentage of safety
        results.append((1 - sum) * 100)

    return results


def probally_of_propagation(p, max_of_validator, num_of_nodes):
    results = list()
    # m must be smaller than 0.99 * n
    for m in max_of_validator:
        sum = 0
        for j in range(math.ceil(m / 3), int(min(m, num_of_nodes * (1 - (p / 100)) + 1))):
            result = ncr(int(num_of_nodes * p / 100), j) * ncr(int(num_of_nodes * 1 - (p / 100)), j) / ncr(num_of_nodes, m)
            sum += result
        print('Node : {0}, Validator : {1} = {2}'.format(num_of_nodes, m, (1- sum) * 100))
        # insert by percentage of safety
        results.append((1 - sum) * 100)

    return results


if __name__=='__main__':

    n_list = [10000]
    # rate of attacker
    a = 33
    # rate of propagation per second
    p = 75
    # half value for grid
    half_of_nodes_list = int(len(n_list) / 2)
    # looping different nodes case
    print(half_of_nodes_list)
    for idx, n in enumerate(n_list):
        max_of_validator = range(1, int(0.99 * n))
        # extend value of safety
        # plt.subplot(half_of_nodes_list, half_of_nodes_list, idx+1)
        plt.title('Vulnerable of consensus [node : {0}]'.format(n))
        plt.ylabel('Percentage of Safety [result]')
        plt.xlabel('Number of validator [m]')
        plt.plot(max_of_validator, safety_of_consensus(a, max_of_validator, n))

    # for idx, n in enumerate(n_list):
    #     max_of_validator = range(1, (p / 100) * n)
    # display by graph
    plt.show()









