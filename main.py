import matplotlib.pyplot as plt
import math
import operator as op
from functools import reduce
from time import time


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)

    return int(numer // denom)


def safety_of_consensus(a, max_of_validator, num_of_nodes):
    results = list()
    x_values = dict()
    y_values = dict()
    z_values = dict()
    # m must be smaller than 0.99 * n
    start_time = time()
    for m in max_of_validator:
        sum = 0
        for i in range(math.ceil(m / 3), int(min(m, num_of_nodes * a / 100)) + 1):
            # Before
            # x = ncr(int(num_of_nodes * a / 100), i)
            # y = ncr(int(num_of_nodes * (1 - (a / 100))), m - i)
            # z = ncr(num_of_nodes, m)

            # After
            # if there is a pre value then use that nor calculate
            x = x_values.get(i) if x_values.get(i) else ncr(int(num_of_nodes * a / 100), i)
            y = y_values.get(m-i) if y_values.get(m-i) else ncr(int(num_of_nodes * (1 - (a / 100))), m - i)
            z = z_values.get(m) if z_values.get(m) else ncr(num_of_nodes, m)
            # update for reference pre values
            x_values.update({i: x})
            y_values.update({m - i: y})
            z_values.update({m:z})

            result = x * y / z

            sum += result
        print('processing {0} of {1}'.format(m, max(max_of_validator)))
        # print(sum)
        # print('Node : {0}, Validator : {1} = {2}'.format(num_of_nodes, m, (1- sum) * 100))
        # insert by percentage of safety
        results.append((1 - sum) * 100)
    end_time = time()
    print('processing time : {0}'.format(end_time-start_time))

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

    # n_list = [1000]

    n_list = [int(input('Enter entire nodes number : '))]
    # rate of attacker
    a = 10
    # rate of propagation per second
    p = 75
    # half value for grid


    # half_of_nodes_list = int(len(n_list) / 2)
    # looping different nodes case
    for idx, n in enumerate(n_list):
        max_of_validator = range(1, int(0.99 * n))
        # extend value of safety
        # plt.subplot(half_of_nodes_list, half_of_nodes_list, idx+1)
        plt.title('Safety of consensus [node : {0}]'.format(n))
        plt.ylabel('Percentage of Safety [result]')
        plt.xlabel('Number of validator [m]')
        plt.plot(max_of_validator, safety_of_consensus(a, max_of_validator, n))

    # for idx, n in enumerate(n_list):
    #     max_of_validator = range(1, (p / 100) * n)
    # display by graph
    plt.show()









