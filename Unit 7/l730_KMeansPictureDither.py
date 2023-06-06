# Oviya Jeyaprakash, 3/30/2023 
# k-Means Picture 2 (Dithering)
# l730

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

pix_num_list = []
for key, value in initial_pix_num.items():
    pix_num_list.append((value, key))
pix_num_list.sort(reverse = True)

def distance_formula(value1, value2):
    return ((value1[0]-value2[0]) ** 2) + ((value1[1]-value2[1]) ** 2) + ((value1[2]-value2[2]) ** 2)

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

def check_pix(pixel):
    p0 = pixel[0]
    p1 = pixel[1]
    p2 = pixel[2]

    if pixel[0] > 255:
        p0 = 255
    elif pixel[0] < 0:
        p0 = 0
    
    if pixel[1] > 255:
        p1 = 255
    elif pixel[1] < 0:
        p1 = 0
    
    if pixel[2] > 255:
        p2 = 255
    elif pixel[2] < 0:
        p2 = 0
    
    return (round(p0), round(p1), round(p2))

k_mean_dict = {}
#k_elements = random.sample(initial_pix_num.keys(), K)
k_elements = [pix_num_list[i][1] for i in range(K)]
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

# for k in k_elements:
#     k_round = (round(k[0]), round(k[1]), round(k[2]))
#     for color in k_mean_dict[k]:
#         for loc in initial_pix_location_dict[color]:
#             pix[loc[0], loc[1]] = k_round

# initial_to_new_color_dict = {}
k_elements_round = []
for k in k_elements:
    k_round = (round(k[0]), round(k[1]), round(k[2]))
    k_elements_round.append(k_round)
    # for color in k_mean_dict[k]:
    #     initial_to_new_color_dict[color] = k_round

for row in range(img.size[1]):
    for col in range(img.size[0]):
        old_pixel = pix[col, row]
        #new_pixel = initial_to_new_color_dict[old_pixel]
        new_pixel = k_value_closest(old_pixel, k_elements_round)
        pix[col, row] = new_pixel
        quant_error = (old_pixel[0] - new_pixel[0], old_pixel[1] - new_pixel[1], old_pixel[2] - new_pixel[2])

        if row + 1 < img.size[1] and col + 1 < img.size[0]:
            p = pix[col + 1, row + 1]
            p_new = (p[0] + (quant_error[0] * 0.0625), p[1] + (quant_error[1] * 0.0625), p[2] + (quant_error[2] * 0.0625))
            p = check_pix(p_new)
        if row + 1 < img.size[1]:
            p = pix[col, row + 1]
            p_new = (p[0] + (quant_error[0] * 0.3125), p[1] + (quant_error[1] * 0.3125), p[2] + (quant_error[2] * 0.3125))
            p = check_pix(p_new)
        if col + 1 < img.size[0]:
            p = pix[col + 1, row]
            p_new = (p[0] + (quant_error[0] * 0.4375), p[1] + (quant_error[1] * 0.4375), p[2] + (quant_error[2] * 0.4375))
            p = check_pix(p_new)
        if col - 1 >= 0 and row + 1 < img.size[1]:
            p = pix[col - 1, row + 1]
            p_new = (p[0] + (quant_error[0] * 0.1875), p[1] + (quant_error[1] * 0.1875), p[2] + (quant_error[2] * 0.1875)) 
            p = check_pix(p_new)

#for key, value in new_pix_location_dict.items():
#    pix[key[0], key[1]] = value

time_end = perf_counter()

img.show() 
img.save("kmeansout.png") 
print((time_end - time_start))