# Oviya Jeyaprakash, 5/29/2023 
# MNIST
# l960

from operator import truth
import numpy as np
import random
import sys
import ast
import math

def sigmoid(x): return 1 / (1 + np.e**(-1 * x))

def sigmoid_prime(x): return (np.e**(-1 * x))/((1 + np.e**(-1 * x)) ** 2)

training_set = []
with open("mnist_train.csv") as f:
    for line in f:
        line = line.strip()
        s = line.split(",")

        output = []
        for i in range(10):
            if i == int(s[0]):
                output.append(1)
            else:
                output.append(0)

        output = np.array(output)
        input = np.array([int(j)/255.0 for j in s[1:]])
        training_set.append((input, output))

        #print(output)

testing_set = []
with open("mnist_test.csv") as f:
    for line in f:
        line = line.strip()
        s = line.split(",")

        output = []
        for i in range(10):
            if i == int(s[0]):
                output.append(1)
            else:
                output.append(0)

        output = np.array(output)
        input = np.array([int(j)/255.0 for j in s[1:]])
        testing_set.append((input, output))

        #print(output)

def create_random_matrices(parameter_list):
    weights = [None]
    biases = [None]
    for l in range(len(parameter_list) - 1):
        weights.append(np.random.rand(parameter_list[l], parameter_list[l+1]))
        biases.append(np.random.rand(1, parameter_list[l+1]))
    return weights, biases

def back_prop(epoch, training_set, num_layers, w, b, lamb, a_input, dot_input, delta_input):
    training_weights_output_file = open("mnist_training_weights.pkl", "w")
    training_biases_output_file = open("mnist_training_biases.pkl", "w")
    biases = b
    weights = w

    for e in range(epoch):
        count = 0
        for s in training_set:
            x = s[0] #matrix of input [#, #]
            y = s[1] #matrix of expected output [#, #]

            a = a_input
            dot = dot_input   
            a[0] = np.array([x])

            for l in range(1, num_layers):
                dot[l] = ((d := (a[l-1] @ weights[l]) + biases[l])) #weights & biases of certain layer l
                a[l] = sigmoid(d)
            #print(error(a, y))

            delta = delta_input
            n = num_layers - 1
            delta_n = sigmoid_prime(dot[n]) * (y - a[n])
            delta[n] = (delta_n)

            for l in range(num_layers - 2, -1, -1): #counting down from n - 1 !!
                d = sigmoid_prime(dot[l]) * (delta[l+1] @ weights[l+1].T)
                delta[l] = (d)
            
            for l in range(len(delta) - 1, 0, -1):
                biases[l] = (biases[l] + (lamb * delta[l]))
                # print(a[l-1])
                # print()
                # print(a[l-1].T)
                # print()
                # print(delta[l])
                weights[l] = (weights[l] + ((a[l - 1].T) @ (lamb * delta[l])))

            count += 1
        
        print(e)
        training_weights_output_file.write(str(e) + "\n" + str(weights))
        print(biases)
        training_biases_output_file.write(str(e) + "\n" + str(biases))

    training_weights_output_file.close()
    training_biases_output_file.close()

    return biases, weights

def testing(t_set, a_input, dot_input, num_layers, b, w):
    biases = b
    weights = w

    mis_classified = 0
    total = 0
    for s in t_set:
        x = s[0] #matrix of input [#, #]
        y = list(s[1]) #matrix of expected output [#, #]

        acc_num = y.index(max(y))

        a = a_input
        dot = dot_input   
        a[0] = np.array([x])
        n = num_layers - 1

        for l in range(1, num_layers):
            dot[l] = ((d := (a[l-1] @ weights[l]) + biases[l])) #weights & biases of certain layer l
            a[l] = sigmoid(d)

        check_list = list(a[n][0])
        check_num = check_list.index(max(check_list))

        if check_num != acc_num:
            mis_classified += 1
        total += 1

    print("# Misclassified:", mis_classified)
    print("Percentage Misclassified:", (mis_classified/total) * 100)
    print("Accuracy:", (1 - ((mis_classified/total) * 100)))

epoch = 50
lamb = 0.3
network_arc = [784, 300, 100, 10]
weights, biases = create_random_matrices(network_arc)
a = [np.array([[0]]) for i in range(len(weights))]
dot = [np.array([[0]]) for i in range(len(weights))]
delta = [np.array([[0]]) for i in range(len(weights))]

updated_biases, updated_weights = back_prop(epoch, training_set, len(weights), weights, biases, lamb, a, dot, delta)

"""updated_weights = None
updated_biases = None
training_weights_output_file = open("mnist_training_weights.pkl")
training_biases_output_file = open("mnist_training_biases.pkl")

for line in training_weights_output_file:
    updated_weights = line

for line in training_biases_output_file:
    updated_biases = line"""

print("Network Architecture:", network_arc)
print()
print("# of epochs:", epoch)
print()
print("Training Set:")
testing(training_set, a, dot, len(updated_weights), updated_biases, updated_weights)
print()
print("Testing Set:")
testing(testing_set, a, dot, len(updated_weights), updated_biases, updated_weights)
print()





    