#Oviya Jeyaprakash 08/30/2022
#Data Structures Challenge
#020

import sys
from heapq import heappush, heappop, heapify
from time import perf_counter
start = perf_counter()

f1, f2, f3 = "1mfile1.txt", "1mfile2.txt", "1mfile3.txt"
l1, l2, l3 = [], [], []

with open(f1) as f:
    l1 = [int(line.strip()) for line in f]

with open(f2) as f:
    l2 = [int(line.strip()) for line in f]

with open(f3) as f:
    l3 = [int(line.strip()) for line in f]


#1
s1 = set(l1)
s2 = set(l2)
s3 = set(l3)
count = 0

for i in s1:
    if i in s2:
        count += 1
print(count)

#2
dict1 = {}
count = sum = 0
for i in l1:
    if i in dict1:
        dict1[i] += 1
    else:
        dict1[i] = 1
        count += 1
        if count % 100 == 0:
            sum += i
print(sum)

#3 #use a dictionary
dict2 = {}
for i in l2:
    if i in dict2:
        dict2[i] += 1
    else:
        dict2[i] = 1

count = 0
for i in s3:
    if i in dict1:
        count += dict1[i]
    if i in dict2:
        count += dict2[i]

print(count)

#4
s4 = set(l1)
result = []
for k in range(10):
    result.append(s4.pop())
print(result)

#5
result = []
newS2 = set()
for key, value in dict2.items():
    if value >= 2:
        newS2.add(key)
newS2 = sorted(newS2)
#print(newS2)

for k in range(10):
    result.append(newS2.pop())


# sortL1 = sorted(l1)
# #print(sortS1)
# result = []

# for index, value in enumerate(sortL1):
#     if(value == sortL1[index + 1]):
#         result.append(value)
#     if len(result) >= 10:
#         break

print(result)

#6
sum = 0
heap_list = []
printL = []
#print(s1)
for i in l1:
    heappush(heap_list, i)
    if i % 53 == 0:
        k = heappop(heap_list)
        while k in printL:
            k = heappop(heap_list)
        sum += k
        printL.append(k)
print(sum)
#print(printL)

end = perf_counter()
print("Total time:", end - start)