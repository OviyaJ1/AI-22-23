# Oviya Jeyaprakash, 5/25/2023 
# Back Propagation
# l950

from operator import truth
import numpy as np
import random
import sys
import ast
import math

def sigmoid(x): return 1 / (1 + np.e**(-1 * x))

def sigmoid_prime(x): return (np.e**(-1 * x))/((1 + np.e**(-1 * x)) ** 2)

def A(x): return 1 if x > 0.5 else 0 

def A_vec(x): 
    new_f = np.vectorize(A)
    return new_f(x)

def back_prop(epoch, training_set, num_layers, w, b, lamb, user_input, a_input, dot_input):
    biases = b
    weights = w

    output = []
    for i in range(len(training_set)):
        if user_input == "S":
            output.append((0,0))
    
    for e in range(epoch):
        count = 0
        for s in training_set:
            x = s[0] #matrix of input [#, #]
            y = s[1] #matrix of expected output [#, #]

            a = a_input
            dot = dot_input   
            a[0] = x

            for l in range(1, num_layers):
                dot[l] = ((d := (a[l-1] @ weights[l]) + biases[l])) #weights & biases of certain layer l
                a[l] = (sigmoid(d))
            #print(error(a, y))

            delta = [np.array([0, 0]), np.array([0, 0]), np.array([0, 0])]
            n = num_layers - 1
            delta_n = sigmoid_prime(dot[n]) * (y - a[n])
            delta[n] = (delta_n)

            if user_input == "S":
                print(a[n])
                output[count] = (a[n][0][0], a[n][0][1])

            for l in range(num_layers - 2, -1, -1): #counting down from n - 1 !!
                d = sigmoid_prime(dot[l]) * (delta[l+1] @ weights[l+1].T)
                delta[l] = (d)
            
            for l in range(len(delta) - 1, 0, -1):
                biases[l] = (biases[l] + (lamb * delta[l]))
                weights[l] = (weights[l] + (lamb * delta[l]) @ (a[l - 1].T))

            count += 1

        if user_input == "C":
            misclassified = 0
            for s in training_set:
                x = s[0] 
                y = s[1] 
                
                a[0] = x           
                for l in range(1, num_layers):
                    dot[l] = ((d := (a[l-1] @ weights[l]) + biases[l])) 
                    a[l] = (sigmoid(d))
                
                if round(a[n][0][0]) != y[0]:
                    misclassified += 1

            print("Misclassified points", str(e) + ":", misclassified)
    
    if user_input == "S":
        print()
        for j in range(len(training_set)):
            print(training_set[j][0], "-->", (round(output[j][0]),round(output[j][1])))

def error(a, y):
    a_acc = a[len(a) - 1][0]
    y_acc = y[0]
    return 0.5 * ((y_acc[0] - a_acc[0]) ** 2 + (y_acc[1] - a_acc[1]) ** 2)

def circle_accuracy(x, y):
    r = ((x ** 2) + (y ** 2)) ** 0.5
    if r < 1:
        return 1
    else:
        return 0

user_input = sys.argv[1]

if user_input == "S":
    epoch = 1000
    lamb = 3
    training_set = []
    #training_set.append((np.array([[2, 3]]), np.array([[0.8, 1]])))
    training_set.append((np.array([[0, 0]]), np.array([[0, 0]])))
    training_set.append((np.array([[1, 0]]), np.array([[0, 1]])))
    training_set.append((np.array([[0, 1]]), np.array([[0, 1]])))
    training_set.append((np.array([[1, 1]]), np.array([[1, 0]])))
    #weights = (np.array([[1, -0.5], [1, 0.5]]), np.array([[1, 2], [-1, -2]]))
    weights = [None, np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]]), np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]])]
    biases = [None, np.array([[random.uniform(-1, 1), random.uniform(-1, 1)]]), np.array([[random.uniform(-1, 1), random.uniform(-1, 1)]])]

    a = [0] * 3
    dot = [0] * 3

    #a = [np.array([0, 0]), np.array([0, 0]), np.array([0, 0])]
    #dot = [np.array([0, 0]), np.array([0, 0]), np.array([0, 0])]

    back_prop(epoch, training_set, len(weights), weights, biases, lamb, user_input, a, dot)
elif user_input == "C":
    epoch = 100
    lamb = .3

    training_set = []
    with open("10000_pairs.txt") as f:
        for line in f:
            line = line.strip()
            s = line.split()
            training_set.append((np.array([[float(s[0]), float(s[1])]]), [circle_accuracy(float(s[0]), float(s[1]))]))

    FACT = math.sqrt(2) / 2

    #weights = (np.array([[1, -0.5], [1, 0.5]]), np.array([[1, 2], [-1, -2]]))
    weights = [None, np.array([[1, -1, 1, -1], [1, 1, -1, -1]]), np.array([[1], [1], [1], [1]])]
    biases = [None, np.array([[FACT, FACT * 3, FACT, -FACT]]), np.array([[-3]])]

    a = [0] * 3
    dot = [0] * 3

    #a = [np.array([0, 0]), np.array([0, 0]), np.array([0, 0])]
    #dot = [np.array([0, 0]), np.array([0, 0]), np.array([0, 0])]

    back_prop(epoch, training_set, len(weights), weights, biases, lamb, user_input, a, dot)