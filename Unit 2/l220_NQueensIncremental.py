#Oviya Jeyaprakash 09/16/2022
#NQueens Backtracking
#210

from operator import truediv
import sys
from heapq import heappush, heappop, heapify
from collections import deque
from time import perf_counter
import random
total_start = perf_counter()

def slay(size): 
    return backtrack(make_flaws(size), size)

def find_goal(size):
    return [0 for i in range(size)]

def make_flaws(size):
    result = []
    
    for r in range(size):
        temp = []
        for col in range(size):
            collisions = 0
            count = 1
            if col in result:
                collisions += 1
            while (row := r - count) >= 0:
                if result[row] == col - count or result[row] == col + count:
                    collisions += 1
                count += 1
            temp.append(collisions)

        min = temp[0]
        index_list = []
        for index, val in enumerate(temp):
            if val == min:
                index_list.append(index)
            if val < min:
                min = val
                index_list.clear()
                index_list.append(index)            

        result.append(index_list[random.randint(0, len(index_list) - 1)])  
    print(result)
    return result

def check_row_flaws(result, size):
    acc_result = []
    for index, col in enumerate(result):
        count = 1
        collisions = 0
        while (row := index - count) >= 0:
            if result[row] == col - count or result[row] == col + count or result[row] == col:
                collisions += 1
            count += 1
        count = 1
        while (row := index + count) < size:
            if result[row] == col - count or result[row] == col + count or result[row] == col:
                collisions += 1
            count += 1
        acc_result.append(collisions)
    
    max = acc_result[0]
    index_list = []
    for index, val in enumerate(acc_result):
        if val == max:
            index_list.append(index)
        if val > max:
            max = val
            index_list.clear()
            index_list.append(index)        

    print("check:", acc_result)
    return acc_result, index_list
        

def backtrack(result, size):
    check = check_row_flaws(result, size)
    if check[0] == find_goal(size):
        return result
    else:
        var = check[1][random.randint(0, len(check[1]) - 1)]
        #print("var", var)
        val = get_sorted_values(result, var, len(result))
        print(val)
        return backtrack(val, size)
    


def get_sorted_values(result, var, size):
    acc_result = []
    for col in range(size):
        count = 1
        collisions = 0
        while (row := var - count) >= 0:
            if result[row] != None and (result[row] == col - count or result[row] == col + count or result[row] == col):
                collisions += 1
            count += 1
        count = 1
        while (row := var + count) < size:
            if result[row] != None and (result[row] == col - count or result[row] == col + count or result[row] == col):
                collisions += 1
            count += 1
        acc_result.append(collisions)

    min = acc_result[0]
    index_list = []
    for index, val in enumerate(acc_result):
        if val == min:
            index_list.append(index)
        if val < min:
            min = val
            index_list.clear()
            index_list.append(index)
    
    #print(acc_result, index_list)
    result[var] = index_list[random.randint(0, len(index_list) - 1)]
    return result

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True

print(test_solution(slay(31)))
print(test_solution(slay(32)))

#print(slay(35))
#print(test_solution(slay(35)))

total_end = perf_counter()
print(total_end - total_start)