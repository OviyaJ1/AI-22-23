#Oviya Jeyaprakash 09/20/2022
#Word Ladders
#130

import sys
from collections import deque
from time import perf_counter
dict_start = perf_counter()
#file = sys.argv[1]
dictionary, file_pairs = "words_06_letters.txt", "puzzles_normal.txt"
#dictionary, file_pairs = sys.argv[1], sys.argv[2]
line_list = set()
dict_count = 0
word_pairs = []

with open(dictionary) as f:
    line_list = ({line.strip() for line in f})
    dict_count = len(line_list)

with open(file_pairs) as f:
    word_pairs = ([line.strip() for line in f])

def create_dict(line_list):
    word_dict = {}
    for word in line_list:
        value_list = []
        for i in range(len(word)):
            initial_char = word[i]
            for j in "abcdefghijklmnopqrstuvwxyz":
                if j != initial_char:
                    child = word[:i] + j + word[i+1:]
                    if child in line_list:
                        value_list.append(child)
        word_dict[word] = value_list 
    
    dict_end = perf_counter()
    print("Time to create the data structure was:", dict_end - dict_start, "seconds")
    print("There are", dict_count, "words in this dict.")
    return word_dict

def find_goal(line):
    intial_state, goal_state = line.split()
    return intial_state, goal_state

def get_children(word_dict, word):
    return word_dict[word]

def reverseBFS(temp_dict, goal, state):
    word = goal
    solution_path = [goal]
    while word != state:
        solution_path.append(temp_dict[word])
        word = temp_dict[word]
    return solution_path

def reverseBiBFS(s_temp_dict, e_temp_dict, goal, state, overlap):
    word = overlap
    solution_path1 = []
    while word != state:
        solution_path1.append(s_temp_dict[word])
        word = s_temp_dict[word]

    word = overlap
    solution_path2 = [overlap]
    while word != goal:
        solution_path2.append(e_temp_dict[word])
        word = e_temp_dict[word]

    solution_path = []
    for i in reversed(solution_path2):
        solution_path.append(i)
    for i in solution_path1:
        solution_path.append(i)
    
    return solution_path

def BFS(line):
    state, goal = find_goal(line)
    temp_dict = {}

    fringe = deque()
    visited = set()
    path = [state]
    fringe.append((state, path))
    visited.add(state)

    while fringe:
        v = fringe.popleft()
        if v[0] == goal:
            #print("Moves: %s" % v[1])
            solution_path = reverseBFS(temp_dict, goal, state)
            return solution_path
        for child in get_children(word_dict, v[0]):
            if child not in visited:
                temp_dict[child] = v[0]
                fringe.append((child, path))
                visited.add(child)
    print("No Solution!")

def BiBFS(line):
    state, goal = find_goal(line)
    path_start = [state]
    path_end = [goal]
    s_temp_dict = {}
    e_temp_dict = {}
    
    fringe_start = deque()
    visited_start = set()
    fringe_end = deque()
    visited_end = set()

    fringe_start.append((state, path_start))
    visited_start.add(state)
    fringe_end.append((goal, path_end))
    visited_end.add(goal)

    while fringe_start and fringe_end:
        v1 = fringe_start.popleft()
        v2 = fringe_end.popleft()

        if v1[0] in visited_end or v2[0] in visited_start:
            solution_path = reverseBiBFS(s_temp_dict, e_temp_dict, goal, state, v1[0])
            return solution_path #goal, v1[1] + temp_dict_end[v1[0]]
        for child in get_children(word_dict, v1[0]):
            if child not in visited_start:
                s_temp_dict[child] = v1[0]
                fringe_start.append((child, path_start))
                visited_start.add(child)
        for child in get_children(word_dict, v2[0]):
            if child not in visited_end:
                e_temp_dict[child] = v2[0]
                fringe_end.append((child, path_end))
                visited_end.add(child)
    print("Unsolvable")

count = 0
word_dict = create_dict(line_list)
print("\n")

#print(BFS("parked yonder"))

start = perf_counter()
print(BFS("foiled cooper"))
end = perf_counter()
print("Time:", end - start)

start = perf_counter()
print(BiBFS("foiled cooper"))
end = perf_counter()
print("Time:", end - start)

# for line in word_pairs:
    
#     print("Line:", count)
#     puzzle_start = perf_counter()

#     start = perf_counter()
#     print(BFS(line))
#     end = perf_counter()
#     print("Time:", end - start)

#     start = perf_counter()
#     print(BiBFS(line))
#     end = perf_counter()
#     print("Time:", end - start)

#     print("\n")
#     count += 1

   

#puzzle_end = perf_counter()

#print("Time to solve all of these puzzles was:", puzzle_end - puzzle_start, "seconds")