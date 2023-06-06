# Oviya Jeyaprakash, 5/10/2023 
# Perceptrons 3
# l920

from operator import truth
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

def adding_vectors(w, x, coefficient):
    new_w = []
    for i in range(len(w)):
        new_w.append(w[i] + (coefficient * x[i]))
    return tuple(new_w)

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

def training_helper(x, y, w, b):
    if (p := perceptron(step, w, b, x)) == y:
        return w, b
    else:
        w = adding_vectors(w, x, (y - p))
        b = b + (y - p)
        return w, b

def training(n, w, b, truth_table, epoch):
    if (c := check(n, w, b)) == 1 or epoch >= 100:
        if c == 1:
            return (1, w, b, c)
        else:
            return (0, w, b, c)
    else:
        for key in truth_table:
            w, b = training_helper(key, truth_table[key], w, b)
        return training(n, w, b, truth_table, epoch + 1)
        
def model(bits):
    poss_func_num = pow(2, len(convert_to_binary(bits, 0)))
    actual_func_num = 0
    truth_table_list = []
    
    for i in range(poss_func_num):
        truth_table_list.append((i, truth_table(bits, i)))

    w = []
    for j in range(bits):
        w.append(0)
    w = tuple(w)
    b = 0

    for k in truth_table_list:
        actual_func_num += training(k[0], w, b, k[1], 0)[0]

    print("bits = " + str(bits) + ":", poss_func_num, "possible functions;", actual_func_num, "can be correctly modeled.")    

#XOR HAPPENS HERE
def XOR(A, w3, w4, w5, b3, b4, b5, in1, in2):
    perceptron3 = perceptron(A, w3, b3, (in1, in2))
    perceptron4 = perceptron(A, w4, b4, (in1, in2))
    perceptron5 = perceptron(A, w5, b5, (perceptron3, perceptron4))
    print(perceptron5)

XOR(step, (-1, 1), (1, -1), (1, 1), 0, 0, 0, ast.literal_eval(sys.argv[1])[0], ast.literal_eval(sys.argv[1])[1])

# print(check(float(sys.argv[1]), ast.literal_eval(sys.argv[2]), float(sys.argv[3])))
# print(convert_to_binary(1, 2))
# pretty_print_tt(truth_table(2, 8))
# print(truth_table(2, 8))
# model(4)

# bits = int(sys.argv[1])
# n = int(sys.argv[2])

# w = []
# for j in range(bits):
#     w.append(0)
# w = tuple(w)
# b = 0

# result = training(n, w, b, truth_table(bits, n), 0)
# print("Final weight vector:", result[1])
# print("Final bias value:", result[2])
# print("Accuracy:", result[3])
