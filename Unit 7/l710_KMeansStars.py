# Oviya Jeyaprakash, 3/28/2023 
# k-Means Stars
# l710

import sys
import math
import random

star_dict = {}

count = 0
with open("star_data.csv") as f:
    for line in f:
        if count != 0:
            line.strip()
            data = line.split(",") #temp, luminosity, radius, absolute magnitude, star type
            tuple_value = (math.log(float(data[0])), math.log(float(data[1])), math.log(float(data[2])), float(data[3]))
            star_dict[tuple_value] = int(data[4])
        count += 1

def distance_formula(value1, value2):
    return (((value1[0]-value2[0]) ** 2) + ((value1[1]-value2[1]) ** 2) + ((value1[2]-value2[2]) ** 2) + ((value1[3]-value2[3]) ** 2)) ** 0.5

def k_value_closest(star, k_elements):
    result_k = k_elements[0]
    min_dist = distance_formula(star, k_elements[0])
    for k in k_elements:
        if (d := distance_formula(star, k)) < min_dist:
            min_dist = d
            result_k = k
    return result_k

def recalculate_means(k_mean_dict, k_elements): #never gonna work on the first iteration
    new_k_elements = []
    for key, value in k_mean_dict.items():
        sum = [0, 0, 0, 0]
        for star in value:
            sum[0] += star[0]
            sum[1] += star[1]
            sum[2] += star[2]
            sum[3] += star[3]
        new_mean = (sum[0]/len(value), sum[1]/len(value), sum[2]/len(value), sum[3]/len(value))
        new_k_elements.append(new_mean)
    
    should_recalculate = False
    for new_k in new_k_elements:
        if new_k not in k_elements:
            should_recalculate = True
    
    return should_recalculate, new_k_elements

def k_means(k_value, k_elements):
    k_mean_dict = {}
    for k in k_elements:
        k_mean_dict[k] = []
    for star in star_dict.keys():
        closest_k = k_value_closest(star, k_elements)
        k_mean_dict[closest_k].append(star)
    return k_mean_dict
    
k_value = 6
k_elements = random.sample(star_dict.keys(), k_value)
should_recalculate = True
iteration = 0

while should_recalculate:
    k_mean_dict = k_means(k_value, k_elements)
    should_recalculate, new_k_elements = recalculate_means(k_mean_dict, k_elements)
    k_elements = new_k_elements
    iteration += 1

for k in k_elements:
    print(str(k) + ": ")
    for stars in k_mean_dict[k]:
        print(str(stars) + ": type " + str(star_dict[stars]))
    print()
        
#print(iteration)
#print(k_elements)


