#Oviya Jeyaprakash 09/16/2022
#NQueens
#210

from operator import truediv
import sys
from heapq import heappush, heappop, heapify
from collections import deque
from time import perf_counter
total_start = perf_counter()

def slay(size): 
    result = []
    for x in range(size):
        result.append(None)

    print(backtrack(result))  

def backtrack(result):
    if None not in result:
        return result
    var = result.index(None)
    for val in get_sorted_values(result, var, len(result)):
        new_state = result.copy()
        new_state[var] = val
        acc_result = backtrack(new_state)
        if acc_result is not None and None not in acc_result:
            return acc_result
    

def get_sorted_values(result, var, size):
    count = 1
    thing = []
    for col in range(size):
        isLegal = True
        count = 0
        if col in result:
            isLegal = False
        while (row := var - count) >= 0 and isLegal == True:
            if result[row] == col - count or result[row] == col + count:
                isLegal = False
            count += 1
        if isLegal == True:
            thing.append(col)
    return thing
   
slay(10)
total_end = perf_counter()
print(total_end - total_start)
    

