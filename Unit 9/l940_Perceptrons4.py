# Oviya Jeyaprakash, 5/14/2023 
# Perceptrons 4
# l940

from operator import truth
import numpy as np
import random
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

def A(x): return 1 if x > 0 else 0 

def A_vec(x): 
    new_f = np.vectorize(A)
    return new_f(x)

def sigmoid(x): return 1 / (1 + np.e**(-1 * x))

def accuracy_check(x, y, result):
    temp = (pow(x, 2) + pow(y, 2)) ** 0.5
    if (temp < 1 and result == 1) or (temp > 1 and result == 0):
        return 1
    else:
        return 0

def p_net(A_vec, weights, biases, input):
    a = list()
    a.append(input)
    n = len(weights)
    for i in range(1, n):
        #print(weights[i], a[i - 1], biases[i])
        c = (a[i - 1] @ weights[i]) + biases[i]
        a.append(A_vec(c))
    return a[n - 1]

def circle_accuracy(x, y):
    r = ((x ** 2) + (y ** 2)) ** 0.5
    if r < 1:
        return 1
    else:
        return 0

# weights = [np.array([[None, None]]), np.array([[-1, 1], [1, -1]]), np.array([[1, 1]])]
# biases = [np.array([[None]]), np.array([[0], [0]]), np.array([[0]])]
#input = np.array([[ast.literal_eval(sys.argv[1])[0], ast.literal_eval(sys.argv[1])[1]]])
input = np.array([[1, 1]])

def XOR(input):
    weights = [None, np.array([[-1, 1], [1, -1]]), np.array([[1],[1]])]
    biases = [None, np.array([[0, 0]]), np.array([[0]])]

    #XOR HAPPENS HERE
    output = p_net(A_vec, weights, biases, input)
    print(output)

def diamond(input):
    weights2 = [np.array([[None, None]]), np.array([[1, -1, 1, -1], [1, 1, -1, -1]]), np.array([[1], [1], [1], [1]])]
    biases2 = [np.array([[None]]), np.array([[1, 1, 1, 1]]), np.array([[-3]])]

    #DIAMOND HAPPENS HERE
    output = p_net(A_vec, weights2, biases2, input)[0][0]
    if output == 0:
        print("outside")
    else:
        print("inside")

    #print(output)

def circle():
    weights3 = [np.array([[None, None]]), np.array([[1, -1, 1, -1], [1, 1, -1, -1]]), np.array([[1], [1], [1], [1]])]
    biases3 = [np.array([[None]]), np.array([[1, 1, 1, 1]]), np.array([[-3]])]

    #CIRCLE HAPPENS HERE

    """for b in np.arange(0, 2, 0.2):
        accuracy = 0
        total = 0
        for i in range(500):
            x = random.uniform(-1.0, 1.0)
            y = random.uniform(-1.0, 1.0)
            output = p_net(sigmoid, weights3, [np.array([[None]]), np.array([[b, b, b, b]]), np.array([[-3]])], np.array([[x, y]]))
            output_rounded = round(output[0][0], 0)
            #print(output, output_rounded)
            
            if output_rounded == circle_accuracy(x, y):
                accuracy += 1
            total += 1
        print(b, accuracy/total)"""

    b = 1.35
    weights3 = [None, np.array([[1, -1, 1, -1], [1, 1, -1, -1]]), np.array([[1], [1], [1], [1]])]
    biases3 = [None, np.array([[b, b, b, b]]), np.array([[-3]])]

    accuracy = 0
    for i in range(500):
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        output = p_net(sigmoid, weights3, biases3, np.array([[x, y]]))
        output_rounded = round(output[0][0], 0)
        #print(output, output_rounded)
            
        if output_rounded == circle_accuracy(x, y):
            accuracy += 1
        else:
            print("(" + str(x) + ", " + str(y) +")")
    print("Accuracy:", (accuracy * 100)/500)

input = sys.argv[1:]

if len(input) == 1:
    XOR(np.array([[ast.literal_eval(sys.argv[1])[0], ast.literal_eval(sys.argv[1])[1]]]))
elif len(input) == 2:
    diamond([[float(input[0]), float(input[1])]])
elif len(input) == 0:
    circle()

#print(output)

