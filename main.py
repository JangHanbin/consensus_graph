import matplotlib.pyplot as plt
import math
import operator as op
from decimal import *
from multiprocessing import Process, Manager, current_process
from functools import reduce
from xls_saver import ExcelSaver


getcontext().prec = 8

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)

    return Decimal(numer) / Decimal(denom)

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


def safety_of_consensus(a, max_of_validator, num_of_nodes, safeties):
    results = list()
    x_values = dict()
    y_values = dict()
    z_values = dict()
    print('Process {0}, A : {a}'.format(current_process(), p))
    for m in max_of_validator:
        sum = Decimal(0)
        print('{0} of {1} processing in Safety[{2}] \r'.format(m, max(max_of_validator), a), end='')
        for i in range(max(math.ceil(m / 4), round(m-(1-a/100)*n)), round(min(m, num_of_nodes * a / 100)) + 1):
            # if there is a pre value then use that nor calculate
            x = x_values.get(i) if x_values.get(i) else ncr(round(num_of_nodes * a / 100), i)
            y = y_values.get(m - i) if y_values.get(m - i) else ncr(round(num_of_nodes * (1 - (a / 100))), m - i)
            z = z_values.get(m) if z_values.get(m) else ncr(num_of_nodes, m)
            x_values.update({i: x})
            y_values.update({m - i: y})
            z_values.update({m: z})

            result = Decimal(x) * Decimal(y) / Decimal(z)
            # if a==68:
            #     print('M : {0} I : {1}'.format(m,i))
            #     print(int(m-(1-a/100)*n))
            #     print(m - (1 - a / 100) * n)
            #     print('{0} ncr {1} = {2}'.format(int(num_of_nodes * a / 100),i,x))
            #     print('{0} ncr {1} = {2}'.format(int(num_of_nodes * (1 - (a / 100))), m-i, y))
            #     print('{0} ncr {1} = {2}'.format(num_of_nodes, m, z))

            sum += result
            # if a == 68:
            #     print(sum)
            #     print()



        # insert by percentage of safety
        results.append((1- sum) * 100)
        # print(sum)
        # print(int((Decimal(1) - sum)))
        # print((1 - sum) * 100)
        # print('m[{0}] = {1},'.format(m,float((1- sum) * 100)))
    print()
    safeties[a] = results.copy()
    return results


def possibility_of_propagation(p, max_of_validator, num_of_nodes, idx, possibilities):

    print('Process {0}, P : {1}'.format(current_process(), p))
    results = list()
    x_values = dict()
    y_values = dict()
    z_values = dict()

    for m in max_of_validator:
        sum = 0
        print('{0} of {1} processing in Propagation[{2}] \r'.format(m, max(max_of_validator),p),end='')

        for i in range(max(math.ceil(m / 4), m-p*n), round(min(m, num_of_nodes * (1 - (p / 100))))+1):
            x = x_values.get(m - i) if x_values.get(m - i) else ncr(round(num_of_nodes * p / 100), m - i)
            y = y_values.get(i) if y_values.get(i) else ncr(round(num_of_nodes * (1 - (p / 100))), i)
            z = z_values.get(m) if z_values.get(m) else ncr(num_of_nodes, m)
            x_values.update({m-i: x})
            y_values.update({i: y})
            z_values.update({m: z})

            result = Decimal(x) * Decimal(y) / Decimal(z)
            sum += result

        # insert by percentage of possibility
        results.append((1 - sum) * 100)
        # print('Possiblilty of propagation x = {0} y = {1}'.format(m, (1 - sum) * 100))
    print()
    possibilities[idx] = results.copy()
    # ret_dict.append(results.copy())
    return results



def compute_attacker_range(p_list, a):
    a_list=list()

    for p in p_list:
        tmp = list()
        for i in range(100-p, min(100-p+a+1,100)):
            tmp.append(i)
        a_list.append(tmp)

    return a_list.copy()


def compute_safeties_by_list(a_list, max_of_validator, n):

    safeties = Manager().dict()

    for a_ in a_list:
        procs = list()
        for a in a_:
            proc = Process(target=safety_of_consensus, args=(a, max_of_validator, n, safeties))
            procs.append(proc)
            proc.start()

        # wating for proc
        for proc in procs:
            proc.join()

    return safeties.copy()


if __name__=='__main__':

    n = 8954
    # n = 100
    # rate of attacker
    a = 10
    # rate of propagation
    p_list = [32, 60, 74, 80]
    # p_list = [i for i in range(1,11)]

    max_of_validator = range(1, n + 1)
    plt.grid(True)
    colors = ['#C80000', '#001EFF', '#FFE600', '#00C800']


    # Safety
    a_list = compute_attacker_range(p_list, a)
    safeties = compute_safeties_by_list(a_list, max_of_validator, n)

    # SAVE AND DRAW VALUES
    for a, safety in safeties.items():
        plt.plot(max_of_validator, safety)
        excelSaver = ExcelSaver('safety_node[{0}]_attacker[{1}].xlsx'.format(max(max_of_validator), a))
        excelSaver.save_to_file(max_of_validator, safety)

    plt.ylabel('Safety [%]')
    plt.xlabel('Number of miners')
    plt.show()

    exit(0)

    # ######################### Dont necessary anymore #########################
    # # propagation
    # possibilities=Manager().dict()
    # # plt.ylabel('Safety [%]')
    # # plt.xlabel('Number of miners')
    # procs = list()
    #
    # # for multiprocessing
    # for idx, p in enumerate(p_list):
    #     proc = Process(target=possibility_of_propagation, args=(p, max_of_validator, n, idx, possibilities))
    #     procs.append(proc)
    #     proc.start()
    #
    #     # possibility=possibility_of_propagation(p, max_of_validator, n)
    #     # possibilities.append(possibility)
    #
    # # wating for proc
    # for proc in procs:
    #     proc.join()    # Dont necessary anymore
    #     # # propagation
    #     # possibilities=Manager().dict()
    #     # # plt.ylabel('Safety [%]')
    #     # # plt.xlabel('Number of miners')
    #     # procs = list()
    #     #
    #     # # for multiprocessing
    #     # for idx, p in enumerate(p_list):
    #     #     proc = Process(target=possibility_of_propagation, args=(p, max_of_validator, n, idx, possibilities))
    #     #     procs.append(proc)
    #     #     proc.start()
    #     #
    #     #     # possibility=possibility_of_propagation(p, max_of_validator, n)
    #     #     # possibilities.append(possibility)
    #     #
    #     # # wating for proc
    #     # for proc in procs:
    #     #     proc.join()
    #
    #
    #
    #
    # #     # draw propagation
    # #     plt.plot(max_of_validator, possibility, c=colors[idx], label='{0}%'.format(p))
    #
    # # for idx, possibility in enumerate(possibilities) :
    # #     plt.plot(max_of_validator, possibility, c=colors[idx], )
    #
    # # plt.plot(int(0.8*max(max_of_validator)),possibility[int(0.8*max(max_of_validator))],ms=15, c='#ffe600', marker='*')
    #
    #
    # # Total result
    # results = list()
    # for idx in range(0,len(p_list)):
    #     results.append([(Decimal(a) / 100 * Decimal(b) / 100) * 100 for a, b in zip(safety, possibilities[idx])])
    # # results.append([(a/100*b/100)*100 for a, b in zip(safety,possibility)] for possibility in possibilities)
    # # possibilities results order can be changed by process so that reorder by seq
    #
    #
    # # for possibility in possibilities:
    # #     results.append([(Decimal(a) / 100 * Decimal(b) / 100) * 100 for a, b in zip(safety, possibility)])
    #
    # plt.ylabel('Safety [%]')
    # plt.xlabel('Number of miners')
    #
    # # draw each graph
    # for result, color, p in zip(results, colors, p_list) :
    #     # draw main graph as each color
    #     excelSaver = ExcelSaver('Total_value_node_{0}_propagation_{1}.xlsx'.format(max(max_of_validator),p))
    #     excelSaver.save_to_file(max_of_validator, result)
    #     plt.plot(max_of_validator,result, c=color)
    #     p = p /100
    #     # draw star at each p
    #     plt.plot(int(p*max(max_of_validator)), result[int(p*max(max_of_validator))-1], linestyle=None, ms=15, c=color, marker='*')
    #     # point of star
    #     # print('{2}% : x = {0}, y = {1}'.format( int(p*max(max_of_validator)),result[int(p*max(max_of_validator))-1], p*100 ))
    #     # # To find 99.97 safety by confirm
    #     # q = 1 - (result[int(p*max(max_of_validator))-1] / 100)
    #     # for z in range(0,100):
    #     #     if 99.97 < confirm(q=q, z=z):
    #     #         print('Z : {0} value = {1}'.format(z,confirm(q=q, z=z)))
    #     #         break
    # ######################### Dont necessary anymore #########################
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









