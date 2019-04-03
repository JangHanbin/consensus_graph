import matplotlib.pyplot as plt
import math
import operator as op
from decimal import *
from multiprocessing import Pool
import matplotlib.patches as mpatches

from functools import reduce
from xls_saver import ExcelSaver

COUNT = 0

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    global COUNT
    return int(numer // denom)

def confirm(q, z):

    p = Decimal(1.0) - q
    lam = z * (q / p)
    sum = Decimal(1.0)
    for k in range(0, z+1):
        poisson = Decimal(math.exp(-lam))
        for i in range(1, k+1):
            poisson *= Decimal(lam / i)
        sum -= poisson * Decimal(1 - math.pow(q / p, z - k))

    return (1 - sum) * 100


def safety_of_consensus(a, max_of_validator, num_of_nodes):
    results = list()
    x_values = dict()
    y_values = dict()
    z_values = dict()

    for m in max_of_validator:
        sum = 0
        for i in range(math.ceil(m / 4), int(min(m, num_of_nodes * a / 100)) + 1):

            # if there is a pre value then use that nor calculate
            x = x_values.get(i) if x_values.get(i) else ncr(int(num_of_nodes * a / 100), i)
            y = y_values.get(m - i) if y_values.get(m - i) else ncr(int(num_of_nodes * (1 - (a / 100))), m - i)
            z = z_values.get(m) if z_values.get(m) else ncr(num_of_nodes, m)
            x_values.update({i: x})
            y_values.update({m - i: y})
            z_values.update({m: z})

            result = x * y / z
            sum += result

        # insert by percentage of safety

        results.append((1 - sum) * 100)

    return results

def possibility_of_propagation(p, max_of_validator, num_of_nodes):

    results = list()
    x_values = dict()
    y_values = dict()
    z_values = dict()

    for m in max_of_validator:
        sum = 0
        print('{0} of {1} processing in Propagation[{2}] \r'.format(m, max(max_of_validator),p),end='')

        for i in range(math.ceil(m / 4), int(min(m, num_of_nodes * (1 - (p / 100))))+1):
            x = x_values.get(m - i) if x_values.get(m - i) else ncr(int(num_of_nodes * p / 100), m - i)
            y = y_values.get(i) if y_values.get(i) else ncr(int(num_of_nodes * (1 - (p / 100))), i)
            z = z_values.get(m) if z_values.get(m) else ncr(num_of_nodes, m)
            x_values.update({m-i: x})
            y_values.update({i: y})
            z_values.update({m: z})
            getcontext().prec = 8

            result = Decimal(x) * Decimal(y) / Decimal(z)


            sum += result

        # insert by percentage of possibility
        results.append((1 - sum) * 100)
        # print('Possiblilty of propagation x = {0} y = {1}'.format(m, (1 - sum) * 100))

    return results


if __name__=='__main__':

    n = 8954
    # rate of attacker
    a = 10
    # rate of propagation
    p_list = [32, 60, 74, 80]

    # p_list = [75]
    max_of_validator = range(1, n + 1)
    plt.grid(True)
    colors = ['#C80000', '#001EFF', '#FFE600', '#00C800']


    # Safety
    safety = safety_of_consensus(a, max_of_validator, n)
    plt.ylabel('Safety [%]')
    plt.xlabel('Number of miners')

    # draw main line
    # plt.plot(max_of_validator, safety, c='k')
    # print('Safety of consensus')
    # for idx, i in enumerate(p_list):
    #     i= i/100
    #     x = int(i*max(max_of_validator))
    #     y = int(safety[int(i*max(max_of_validator))])
    #     plt.plot(x, y ,linestyle=None, ms=15, c=colors[idx], marker='*')
        # plt.annotate('({0}, {1})'.format(x,y), xy=(x,y), xytext=(x-700, y-(2*idx)))





    # propagation
    possibilities=list()
    # plt.ylabel('Safety [%]')
    # plt.xlabel('Number of miners')
    for idx, p in enumerate(p_list):
        possibility=possibility_of_propagation(p, max_of_validator, n)
        possibilities.append(possibility)
    #     # draw propagation
    #     plt.plot(max_of_validator, possibility, c=colors[idx], label='{0}%'.format(p))

    # for idx, possibility in enumerate(possibilities) :
    #     plt.plot(max_of_validator, possibility, c=colors[idx], )



    # plt.plot(int(0.8*max(max_of_validator)),possibility[int(0.8*max(max_of_validator))],ms=15, c='#ffe600', marker='*')


    # Total result
    results = list()
    # results.append([(a/100*b/100)*100 for a, b in zip(safety,possibility)] for possibility in possibilities)
    for possibility in possibilities:
        results.append([(Decimal(a) / 100 * Decimal(b) / 100) * 100 for a, b in zip(safety, possibility)])

    plt.ylabel('Safety [%]')
    plt.xlabel('Number of miners')

    # draw each graph
    for result, color, p in zip(results, colors, p_list) :
        # draw main graph as each color
        excelSaver = ExcelSaver('Total_value_node_{0}_propagation_{1}.xlsx'.format(max(max_of_validator),p))
        excelSaver.save_to_file(max_of_validator, result)
        plt.plot(max_of_validator,result, c=color)
        p = p /100
        # draw star at each p
        plt.plot(int(p*max(max_of_validator)), result[int(p*max(max_of_validator))], linestyle=None, ms=15, c=color, marker='*')
        # point of star
        print('{2} : x = {0}, y = {1}'.format(p, int(p*max(max_of_validator)),result[int(p*max(max_of_validator))] ))
        # To find 99.97 safety by confirm
        q = 1 - (result[int(p*max(max_of_validator))] / 100)
        for z in range(0,100):
            if 99.97 < confirm(q=q, z=z):
                print('Z : {0} value = {1}'.format(z,confirm(q=q, z=z)))
                break

    # plt.title('Confirm')
    # plt.ylabel('Value [%]')
    # plt.xlabel('Number of Confirms')
    # plt.plot(max_of_vali
    # dator, results)

    # confirms = list()


    propa_result = list()





    # plt.ylabel('Safety [%]')
    # plt.xlabel('Number of confirms')
    # plt.plot(range(0,10+1), confirms, c='#C80000',ls='--',marker='o')
    # plt.plot(1, confirms[1],ms=15, c='#ffe600', marker='*')
    # plt.plot(6, confirms[6], ms=15, c='#ffe600', marker='*')

    # paches = list()
    # for color, p in zip(colors, p_list):
    #     paches.append(mpatches.Patch(color=color, label='{0}%'.format(p)))
    # plt.legend(loc=4, handles=paches)
    # plt.legend(handles=[red_patch])
    plt.show()









