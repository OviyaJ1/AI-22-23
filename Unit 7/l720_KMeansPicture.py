# Oviya Jeyaprakash, 3/30/2023 
# k-Means Picture
# l720

from PIL import Image
import sys
import random
from time import perf_counter
img = Image.open(sys.argv[1]) 
#img.show() 
#print(img.size) 

time_start = perf_counter()

K = int(sys.argv[2])

pix = img.load() 
initial_pix_location_dict = {}
#new_pix_location_dict = {}
initial_pix_num = {}

def color_naive_27(value):
    if value < 255//3:
        return 0
    elif value > 255 * 2 // 3:
        return 255
    else:
        return 127

def color_naive_8(value):
    if value < 128:
        return 0
    else:
        return 255

for col in range(img.size[0]):
    for row in range(img.size[1]):
        # new_pix_27 = (color_naive_27(pix[col, row][0]), color_naive_27(pix[col, row][1]), color_naive_27(pix[col, row][2]))
        # new_pix_8 = (color_naive_8(pix[col, row][0]), color_naive_8(pix[col, row][1]), color_naive_8(pix[col, row][2]))
        # new_pix_location_dict[(col, row)] = new_pix_27

        if (p := pix[col, row]) in initial_pix_location_dict:
            initial_pix_location_dict[p].append((col, row))
        else:
            initial_pix_location_dict[p] = [(col, row)]
        if (p := pix[col, row]) in initial_pix_num:
            initial_pix_num[p] = initial_pix_num[p] + 1
        else:
            initial_pix_num[p] = 1
#print(initial_pix_num)
#input()    

def distance_formula(value1, value2):
    return (((value1[0]-value2[0]) ** 2) + ((value1[1]-value2[1]) ** 2) + ((value1[2]-value2[2]) ** 2)) ** 0.5

def k_value_closest(color, k_elements):
    result_k = k_elements[0]
    min_dist = distance_formula(color, k_elements[0])
    for k in k_elements:
        if (d := distance_formula(color, k)) < min_dist:
            min_dist = d
            result_k = k
    return result_k

def recalculate_means(k_mean_dict, k_elements): #never gonna work on the first iteration
    new_k_elements = []
    for key, value in k_mean_dict.items():
        sum = [0, 0, 0]
        num = 0
        for color in value:
            sum[0] += color[0]
            sum[1] += color[1]
            sum[2] += color[2]
            num += 1
            #num += initial_pix_num[color]
        #print(value)
        #print(sum, num)
        new_mean = (sum[0]/num, sum[1]/num, sum[2]/num)
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
    for color in initial_pix_num.keys():
        closest_k = k_value_closest(color, k_elements)
        k_mean_dict[closest_k].append(color)
    return k_mean_dict

k_mean_dict = {}
k_elements = random.sample(initial_pix_num.keys(), K)
should_recalculate = True
iteration = 0

while should_recalculate:
    k_mean_dict = k_means(K, k_elements)
    #for k in k_mean_dict.keys():
    #    print(k, len(k_mean_dict[k]))
    #input()
    should_recalculate, new_k_elements = recalculate_means(k_mean_dict, k_elements)
    k_elements = new_k_elements
    iteration += 1

for k in k_elements:
    k_round = (round(k[0]), round(k[1]), round(k[2]))
    for color in k_mean_dict[k]:
        for loc in initial_pix_location_dict[color]:
            pix[loc[0], loc[1]] = k_round

#for key, value in new_pix_location_dict.items():
#    pix[key[0], key[1]] = value

time_end = perf_counter()

img.show() 
img.save("kmeansout.png") 
print((time_end - time_start))