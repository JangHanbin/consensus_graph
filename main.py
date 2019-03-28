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

    start_time = time()
    for m in max_of_validator:
        sum = 0
        for i in range(math.ceil(m / 4), int(min(m, num_of_nodes * a / 100)) + 1):
            # Before
            # x = ncr(int(num_of_nodes * a / 100), i)
            # y = ncr(int(num_of_nodes * (1 - (a / 100))), m - i)
            # z = ncr(num_of_nodes, m)

            # After
            # if there is a pre value then use that nor calculate
            x = x_values.get(i) if x_values.get(i) else ncr(int(num_of_nodes * a / 100), i)
            y = y_values.get(m - i) if y_values.get(m - i) else ncr(int(num_of_nodes * (1 - (a / 100))), m - i)
            z = z_values.get(m) if z_values.get(m) else ncr(num_of_nodes, m)

            x_values.update({i: x})
            y_values.update({m - i: y})
            z_values.update({m: z})

            #calculate
            result = x * y / z
            sum += result
        # insert by percentage of safety
        results.append((1 - sum) * 100)

    end_time = time()
    print('processing time : {0}'.format(end_time-start_time))

    return results


def possibility_of_propagation(p, max_of_validator, num_of_nodes):

    results = list()
    x_values = dict()
    y_values = dict()
    z_values = dict()
    for m in max_of_validator:
        sum = 0
        # print((1 - (p / 100)))
        # exit(9)
        for j in range(math.ceil(m / 3), int(min(m, num_of_nodes * (1 - (p / 100))))+1):
            x = x_values.get(m - j) if x_values.get(m - j-1) else ncr(int(num_of_nodes * p / 100), m - j)
            y = y_values.get(j) if y_values.get(j-1) else ncr(int(num_of_nodes * (1 - (p / 100))), j)
            z = z_values.get(m)if z_values.get(m-1) else ncr(num_of_nodes, m)
            result = x * y / z
            sum += result

        # insert by percentage of possibility
        results.append((sum) * 100)

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
    #looping different nodes case
    for idx, n in enumerate(n_list):
        max_of_validator = range(3, n+1)
        # extend value of safety
        # plt.subplot(half_of_nodes_list, half_of_nodes_list, idx+1)
        plt.title('Safety of consensus [node : {0}]'.format(n))
        plt.ylabel('Percentage of Safety [result]')
        plt.xlabel('Number of validator [m]')
        safety = safety_of_consensus(a, max_of_validator, n)
        plt.plot(max_of_validator, safety)

    # for idx, n in enumerate(n_list):
    #     # m must be smaller than 0.99 * n
    #     max_of_validator = range(1, int(0.75 * n)+1)
    #     # extend value of safety
    #     # plt.subplot(half_of_nodes_list, half_of_nodes_list, idx+1)
    #     # plt.title('Possibility of Propagation [node : {0}]'.format(n))
    #     # plt.ylabel('Percentage of Safety [result]')
    #     # plt.xlabel('Number of validator [m]')
    #     possibility=possibility_of_propagation(p, max_of_validator, n)
    #     # plt.plot(max_of_validator,possibility_of_propagation())
    #
    # plt.title('Total [node : {0}]'.format(n))
    # plt.ylabel('Total Safety [result]')
    # plt.xlabel('Number of validator [m]')
    # plt.plot(max_of_validator, [a*b for a,b in zip(safety,possibility)])
    #

    plt.show()









