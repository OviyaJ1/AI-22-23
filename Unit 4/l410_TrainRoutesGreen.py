import sys
from collections import deque
from time import perf_counter
from heapq import heappush, heappop, heapify
from math import pi , acos , sin , cos

start_graph = perf_counter()

coor_dict = {}
junctions_dict = {}
city_id_dict = {}

def calcd(node1, node2):

    if node1 == node2:
        return 0

    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees
    y1, x1 = node1
    y2, x2 = node2

    R   = 3958.76 # miles = 6371 km
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0

    # approximate great circle distance with law of cosines
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

with open("rrNodeCity.txt") as f:
    for line in f:
        space = line.split()
        id = space[0]
        
        if len(space) == 2:
            city_name = space[1]
        else:
            city_name = space[1] + " " + space[2]

        city_id_dict[city_name] = id

with open("rrNodes.txt") as f:
    for line in f:
        space = line.split()
        id = space[0]
        coor = (float(space[1]), float(space[2]))
        coor_dict[id] = coor

with open("rrEdges.txt") as f:
    for line in f:
        space = line.split()
        j1 = space[0]
        j2 = space[1]
        distance = calcd(coor_dict[j1], coor_dict[j2])

        if not (j1 in junctions_dict):
            junctions_dict[j1] = {(j2, distance)}
        else:
            junctions_dict[j1].add((j2, distance))

        if not (j2 in junctions_dict):
            junctions_dict[j2] = {(j1, distance)}
        else:
            junctions_dict[j2].add((j1, distance))

end_graph = perf_counter()

def dijkstra(city_start, city_end):
    city_start_id = city_id_dict[city_start]
    city_end_id = city_id_dict[city_end]

    closed = set()
    start = (0, city_start_id) #(depth, state)
    fringe = []
    heappush(fringe, start)

    while fringe:
        v = heappop(fringe)
        if v[1] == city_end_id:
            return v[0]
        if v[1] not in closed:
            closed.add(v[1])
            for child in junctions_dict[v[1]]:
                if child[0] not in closed:
                    temp = (v[0] + child[1], child[0]) #
                    heappush(fringe, temp)
    return None

def heuristic(city_start_id, city_end_id): ##
    return calcd(coor_dict[city_start_id], coor_dict[city_end_id])

def a_star(city_start, city_end):
    city_start_id = city_id_dict[city_start]
    city_end_id = city_id_dict[city_end]

    closed = set()
    start = (heuristic(city_start_id, city_end_id), 0, city_start_id)
    fringe = []
    heappush(fringe, start)

    while fringe:
        v = heappop(fringe)
        if v[2] == city_end_id:
            return v[1]
        if v[2] not in closed:
            closed.add(v[2])
            for child in junctions_dict[v[2]]:
                if child not in closed:
                    temp = (heuristic(child[0], city_end_id) + v[1] + child[1], v[1] + child[1], child[0])
                    heappush(fringe, temp)
    return None

print("Time to create data structure:", (end_graph - start_graph))
start1 = perf_counter()
d_dis = dijkstra(sys.argv[1], sys.argv[2])
end1 = perf_counter()
print(sys.argv[1], "to", sys.argv[2], "with Dijkstra:", d_dis, "in", end1 - start1, "seconds")

start2 = perf_counter()
a_dis = a_star(sys.argv[1], sys.argv[2])
end2 = perf_counter()
print(sys.argv[1], "to", sys.argv[2], "with A*:", a_dis, "in", end2 - start2, "seconds")
