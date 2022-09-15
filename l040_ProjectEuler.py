#Oviya Jeyaprakash 08/30/2022
#Project Euler
#040

import sys
from heapq import heappush, heappop, heapify
from time import perf_counter
start = perf_counter()

def is_prime(x):
    if x > 1:
        for i in range(2, int(x ** 0.5) + 1):
            if (x % i) == 0:
                return False
        return True
    else:
        print("oops")
        return False

def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

def lcm(a, b):
    return a // gcd(a, b) * b

#1:
print("#1: %s" % sum({x for x in range(1, 1000) if x % 3 == 0 or x % 5 == 0}))

#2:
a, b, c = 1, 2, 3
s = 2

while c < 4000000:
    c = a + b
    a = b 
    b = c
    if c % 2 == 0:
        s += c
print("#2: %s" % s)

#3:
max = 0
for i in range(2, int(600851475143 ** 0.5) + 1):
    if (600851475143 % i) == 0:
        if is_prime(i) and i > max:
            max = i
print("#3: %s" % max)  

#4:
max = 0
for i in range(999, 100, -1):
    for j in range (999, 100, -1):
        if (s:= str(i * j)) and s == s[::-1] and (i * j) > max:
            max = i * j
print("#4: %s" % max)

#5:
l = 1
for i in range(2, 20):
    l = lcm(i, l)
print("#5: %s" % l)

#6:
print("#6: %s" % ((sum({x for x in range(1, 101)}) ** 2) - (sum({x ** 2 for x in range(1, 101)}))))

#7:
count, num = 1, 1
while(count < 10001):
    num += 2
    if is_prime(num):
        count += 1
print("#7: %s" % num)

#8:
num_string = "731671765313306249192251196744265747423553491949349698352031277450632623957831801698480186947885184385" +\
            "861560789112949495459501737958331952853208805511125406987471585238630507156932909632952274430435576689" +\
            "664895044524452316173185640309871112172238311362229893423380308135336276614282806444486645238749303589" +\
            "072962904915604407723907138105158593079608667017242712188399879790879227492190169972088809377665727333" +\
            "001053367881220235421809751254540594752243525849077116705560136048395864467063244157221553975369781797" +\
            "784617406495514929086256932197846862248283972241375657056057490261407972968652414535100474821663704844" +\
            "031998900088952434506585412275886668811642717147992444292823086346567481391912316282458617866458359124" +\
            "566529476545682848912883142607690042242190226710556263211111093705442175069416589604080719840385096245" +\
            "544436298123098787992724428490918884580156166097919133875499200524063689912560717606058861164671094050" +\
            "7754100225698315520005593572972571636269561882670428252483600823257530420752963450"

#8:
max_num = 0
for index in range(len(num_string) - 13):
    product = int(num_string[index])
    for i in num_string[index + 1:index + 13]:
        product *= int(i)
    if product > max_num:
        max_num = product
print("#8: %s" % max_num)

#9:
for a in range(1, 1000):
    for b in range(a + 1, 1000):
        c = (((a ** 2) + (b ** 2)) ** 0.5)
        if a + b + c == 1000:
            print("#9: %s" % (a * b * c))

#11:
data = [[8,  2, 22, 97, 38, 15,  0, 40,  0, 75,  4,  5,  7, 78, 52, 12, 50, 77, 91,  8],
       [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48,  4, 56, 62,  0],
       [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30,  3, 49, 13, 36, 65],
       [52, 70, 95, 23,  4, 60, 11, 42, 69, 24, 68, 56,  1, 32, 56, 71, 37,  2, 36, 91],
       [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
       [24, 47, 32, 60, 99,  3, 45,  2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
       [32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
       [67, 26, 20, 68,  2, 62, 12, 20, 95, 63, 94, 39, 63,  8, 40, 91, 66, 49, 94, 21],
       [24, 55, 58,  5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
       [21, 36, 23,  9, 75,  0, 76, 44, 20, 45, 35, 14,  0, 61, 33, 97, 34, 31, 33, 95],
       [78, 17, 53, 28, 22, 75, 31, 67, 15, 94,  3, 80,  4, 62, 16, 14,  9, 53, 56, 92],
       [16, 39,  5, 42, 96, 35, 31, 47, 55, 58, 88, 24,  0, 17, 54, 24, 36, 29, 85, 57],
       [86, 56,  0, 48, 35, 71, 89,  7,  5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
       [19, 80, 81, 68,  5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77,  4, 89, 55, 40],
       [ 4, 52,  8, 83, 97, 35, 99, 16,  7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
       [88, 36, 68, 87, 57, 62, 20, 72,  3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
       [ 4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18,  8, 46, 29, 32, 40, 62, 76, 36],
       [20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74,  4, 36, 16],
       [20, 73, 35, 29, 78, 31, 90,  1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57,  5, 54],
       [ 1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52,  1, 89, 19, 67, 48]]

def check(data, a, b, max):
    #check down
    if a + 4 < 20:
        if max < (p := data[a][b] * data[a + 1][b] * data[a + 2][b] * data[a + 3][b]):
            max = p

    #check right
    if b + 4 < 20:
        if max < (p := data[a][b] * data[a][b + 1] * data[a][b + 2] * data[a][b + 3]):
            max = p

    #check diagonally down and right
    if a + 4 < 20 and b + 4 < 20:
        if max < (p := data[a][b] * data[a + 1][b + 1] * data[a + 2][b + 2] * data[a + 3][b + 3]):
            max = p
    
    #check diagonally down and left
    if a + 4 < 20 and b - 4 >= 0:
        if max < (p := data[a][b] * data[a + 1][b - 1] * data[a + 2][b - 2] * data[a + 3][b - 3]):
            max = p

    return max

max = 0
for i in range(len(data)):
    for j in range(len(data[0])):
        max = check(data, i, j, max)
print("#11: %s" % max)
        

#12:
num, d = 1, 0
while d <= 250:
    d = 0
    num += 1
    triangle_num = num * (num + 1) / 2
    for i in range(1, int(triangle_num ** 0.5) + 1):
        if (triangle_num % i) == 0:
            d += 1
print("#12: %s" % triangle_num)

#14:
seq_dict = {1: 1}
max_len = 1
result = 0
for i in range(2, 1000000):
    num = i
    len_num = 0
    while i not in seq_dict:
        if num in seq_dict:
            len_num += seq_dict[num]
            seq_dict[i] = len_num
        if num % 2 == 0:
            num = num / 2
            len_num += 1
        else:
            num = (3 * num) + 1
            len_num += 1
    if max_len < seq_dict[i]:
        max_len = seq_dict[i]
        result = i
print("#14: %s" % result)

#28:
sum_num, num, count, add = 1, 1, 0, 2
while num < (1001 * 1001):
    if count == 4:
        add += 2
        count = 0
    num += add
    sum_num += num
    count += 1
print("#28: %s" % sum_num)

#29:
print("#29: %s" % len({(a ** b) for a in range(2, 101) for b in range(2,101)}))     


end = perf_counter()
print("Total time:", end - start)