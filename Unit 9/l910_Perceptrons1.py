# Oviya Jeyaprakash, 5/3/2023 
# Perceptrons 1
# l910

import sys
import ast

def pretty_print_tt(table):
    header_done = False
    for key in table.keys():
        if header_done == False:
            header = ""
            header_below = ""
            for i in range(len(key)):
                header += "v" + str(i) + " "
                header_below += "---"
            header += "| Output"
            header_below += "---"
            print(header)
            print(header_below)
            header_done = True

        k_string = ""
        for k in key:
            k_string += str(k) +"  "
        k_string += "| " + str(table[key])
        print(k_string)

def convert_to_binary(bits, n):
    result_string = ""
    count = pow(2, bits)
    num = pow(2, count)/2

    while count != 0:
        if num > n or n == 0:
            result_string += "0"
            num = num/2
            count -= 1
        else:
            result_string += "1"
            n -= num
            num = num/2
            count -= 1
    
    return result_string

def truth_table(bits, n):
    binary_n = convert_to_binary(bits, n)
    table_dict = {}

    for index in range((p := pow(2, bits))):
        #table_dict[tuple(int(i) for i in convert_to_binary(bits - 1, p - index - 1))] = int(binary_n[index])
        temp_list = []
        for i in range(len((c := convert_to_binary(bits - 1, p - index - 1)))):
            if i in range(len(c) - bits, len(c)):
                temp_list.append(int(c[i]))
        table_dict[tuple(temp_list)] = int(binary_n[index])
    return table_dict

def dot_product(w, x):
    result_sum = 0
    for i in range(len(w)):
        result_sum += w[i] * x[i]
    return result_sum

def step(num):
    if num > 0:
        return 1
    else: 
        return 0

def perceptron(A, w, b, x):
    return A(dot_product(w, x) + b)

def check(n, w, b):
    #pretty_print_tt((t := truth_table(len(w), n)))
    #print(t)
    #print()

    t = truth_table(len(w), n)
    right = 0
    wrong = 0
    for key in t.keys():
        if perceptron(step, w, b, key) == t[key]:
            right += 1
        else:
            wrong += 1
    
    #print(right, wrong)
    return right/(right + wrong)

print(check(float(sys.argv[1]), ast.literal_eval(sys.argv[2]), float(sys.argv[3])))
# print(convert_to_binary(1, 2))
# pretty_print_tt(truth_table(2, 8))

