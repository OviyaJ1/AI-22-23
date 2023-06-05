import sys
from collections import deque
from time import perf_counter
from heapq import heappush, heappop, heapify
from math import pi, acos , sin , cos
import tkinter as tk
import time

start_graph = perf_counter()

coor_dict = {}
junctions_dict = {}
city_id_dict = {}
line_dict_draw = {}
line_dict_acc = {}

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

def dijkstra(city_start, city_end, r, c):
    city_start_id = city_id_dict[city_start]
    city_end_id = city_id_dict[city_end]

    closed_acc = set()
    closed = {city_start_id: (0, [city_start_id])}
    start = (0, city_start_id) #(depth, state)
    fringe = []
    heappush(fringe, start)

    count_update = 0
    while fringe:
        v = heappop(fringe)
        if v[1] == city_end_id:
            count = 0
            while count <= (len(closed[v[1]][1]) - 2):
                c.itemconfig(line_dict_acc[(closed[v[1]][1][count], closed[v[1]][1][count + 1])], fill="green", width = 2)
                if count % 100:
                    r.update()
                count += 1
            return v[0]
        if v[1] not in closed_acc:
            closed_acc.add(v[1])
            for child in junctions_dict[v[1]]:
                if child[0] not in closed_acc:
                    temp = (v[0] + child[1], child[0]) #
                    closed[child[0]] = (v[0] + child[1], closed[v[1]][1] + [child[0]])
                    heappush(fringe, temp)
                    c.itemconfig(line_dict_acc[(v[1], child[0])], tag = "grid_line", fill="red", width = 2)

                    # if v[1] > child[0]:
                    #     c.itemconfig(line_dict_acc[(v[1], child[0])], tag = "grid_line", fill="red", width = 2)
                    # else:
                    #     c.itemconfig(line_dict_acc[(child[0], v[1])], tag = "grid_line", fill="red", width = 2)

            count_update += 1
            if count_update % 2500 == 0:
                r.update()
    return None

def heuristic(city_start_id, city_end_id): ##
    return calcd(coor_dict[city_start_id], coor_dict[city_end_id])

def a_star(city_start, city_end, r, c):
    city_start_id = city_id_dict[city_start]
    city_end_id = city_id_dict[city_end]

    closed_acc = set()
    closed = {city_start_id: (0, [city_start_id])}
    start = (heuristic(city_start_id, city_end_id), 0, city_start_id)
    fringe = []
    heappush(fringe, start)

    count_update = 0
    while fringe:
        v = heappop(fringe)
        if v[2] == city_end_id:
            count = 0
            while count <= (len(closed[v[2]][1]) - 2):
                c.itemconfig(line_dict_acc[(closed[v[2]][1][count], closed[v[2]][1][count + 1])], fill="green", width = 2)
                if count % 100:
                    r.update()
                count += 1
            return v[1]
        if v[2] not in closed_acc:
            closed_acc.add(v[2])
            for child in junctions_dict[v[2]]:
                if child[0] not in closed_acc:
                    temp = ((p := heuristic(child[0], city_end_id) + v[1] + child[1]), v[1] + child[1], child[0])
                    heappush(fringe, temp)
                    closed[child[0]] = (p, closed[v[2]][1] + [child[0]])
                    c.itemconfig(line_dict_acc[(v[2], child[0])], tag = "grid_line", fill="blue", width = 2)

                    # if v[2] > child[0]:
                    #     c.itemconfig(line_dict_acc[(v[2], child[0])], tag = "grid_line", fill="red", width = 2)
                    # else:
                    #     c.itemconfig(line_dict_acc[(child[0], v[2])], tag = "grid_line", fill="red", width = 2)
                    
            count_update += 1
            if count_update % 1000 == 0:
                r.update()
    return None

def draw_connect(c):
    for id1, id2_eh in junctions_dict.items():
        for value in id2_eh:
            id2 = value[0]

            coor_pair1 = coor_dict[id1]
            coor_pair2 = coor_dict[id2]
            xy_pair1 = (750* ((coor_pair1[1] + 130)/70) + 30, 750 - (750*((coor_pair1[0] - 10)/60)) - 30)
            xy_pair2 = (750* ((coor_pair2[1] + 130)/70) + 30, 750 - (750*((coor_pair2[0] - 10)/60)) - 30)
            line = c.create_line([xy_pair1, xy_pair2], tag='grid_line')

            # if id1 < id2:
            #     line_dict_acc[(id2, id1)] = line
            # if id1 > id2:
            #     line_dict_acc[(id1, id2)] = line

            #line_dict_draw[(id1, id2)] = line
            line_dict_acc[(id1, id2)] = line
            line_dict_acc[(id2, id1)] = line

root = tk.Tk() #creates the frame
canvas = tk.Canvas(root, height=800, width=800, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
draw_connect(canvas)
canvas.pack(expand=True) #packing widgets places them on the board
#draw(root, canvas)
#print("Map done")

print("Time to create data structure:", (end_graph - start_graph))
start1 = perf_counter()
d_dis = dijkstra(sys.argv[1], sys.argv[2], root, canvas)
end1 = perf_counter()
print(sys.argv[1], "to", sys.argv[2], "with Dijkstra:", d_dis, "in", end1 - start1, "seconds")
root.mainloop()

root = tk.Tk() #creates the frame
canvas = tk.Canvas(root, height=800, width=800, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
draw_connect(canvas)
canvas.pack(expand=True) #packing widgets places them on the board

start2 = perf_counter()
a_dis = a_star(sys.argv[1], sys.argv[2], root, canvas)
end2 = perf_counter()
print(sys.argv[1], "to", sys.argv[2], "with A*:", a_dis, "in", end2 - start2, "seconds")
root.mainloop()
