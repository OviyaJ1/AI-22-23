# Oviya Jeyaprakash, 4/24/2023 
# Decision Trees
# l820

import sys
import math

file_name = "mushroom.csv"
information_gain_dict = {}
entropy_dict = {}
frequency_dict = {}
final_dict = {}
       
#tree and node class
class Tree():
    def __init__(self,root):
        self.root = root
        self.data = root
        self.children = []
        self.Nodes = []
    def addNode(self,obj):
        self.children.append(obj)
    def checkChildren(self,obj):
        for i in self.children:
            if obj in i.data:
                return (self.children).index(i)
        else:
            return -1
    def getAllNodes(self):
        self.Nodes.append(self.root)
        for child in self.children:
            self.Nodes.append(child.data)
        for child in self.children:
            if child.getChildNodes(self.Nodes) != None:
                child.getChildNodes(self.Nodes)
        print(*self.Nodes, sep = "\n")
        print('Tree Size:' + str(len(self.Nodes)))

class Node():
    def __init__(self, data):
        self.data = data
        self.children = []
    def addNode(self,obj):
        self.children.append(obj)
    def checkChildren(self, obj):
        for i in self.children:
            if obj in i.data:
                return (self.children).index(i)
        else:
            return -1
    def getChildNodes(self,Tree):
        for child in self.children:
            if child.children:
                child.getChildNodes(Tree)
                Tree.append(child.data)
            else:
                Tree.append(child.data)

def printTree(location, num):
    if len(location.children) == 0:
        pass
    else:
        ending = ""
        if len(location.children[0].children) == 0:
            ending = "--> " + str(location.children[0].data)

        indents = ""
        for i in range(num):
            indents += "  "
        
        if str(location.data) in num_to_variable_dict.values():
            print(indents + "*", str(location.data) + "?", ending)
        else:
            print(indents + "*", str(location.data), ending)

        for j in location.children:
            printTree(j, num + 1)
        
def createTree(root_name, is_subset, subset_name, file_name):
    num_to_variable_dict = {}
    tree_root = Tree(root_name)
    count = 0
    with open(file_name) as f:
        for line in f:
            if count == 0:
                line = line.strip()
                variables = line.split(",")
                for num in range(len(variables)):
                    num_to_variable_dict[num] = variables[num]
                    if num != (len(variables) - 1):
                        tree_root.addNode(Node(variables[num]))
            if count != 0:
                line = line.strip()
                data = line.split(",") 
                if not is_subset or subset_name in data:
                    for key in range(len(num_to_variable_dict)):
                        if key != (len(num_to_variable_dict) - 1):
                            if (s_child_key := tree_root.children[key].checkChildren(data[key])) == -1:
                                tree_root.children[key].addNode(Node(data[key]))
                                s_child_key = tree_root.children[key].checkChildren(data[key])
                                tree_root.children[key].children[s_child_key].addNode(Node(data[len(num_to_variable_dict) - 1]))
                            
                            s_child_key = tree_root.children[key].checkChildren(data[key])
                            if (s_s_child_key := tree_root.children[key].children[s_child_key].checkChildren(data[len(num_to_variable_dict) - 1])) == -1:
                                tree_root.children[key].children[s_child_key].addNode(Node(data[len(num_to_variable_dict) - 1]))
                                s_s_child_key = tree_root.children[key].children[s_child_key].checkChildren(data[len(num_to_variable_dict) - 1])
                                tree_root.children[key].children[s_child_key].children[s_s_child_key].addNode(Node(1))
                            else:
                                if len(tree_root.children[key].children[s_child_key].children[s_s_child_key].children) == 0:
                                    tree_root.children[key].children[s_child_key].children[s_s_child_key].addNode(Node(1))
                                else:        
                                    tree_root.children[key].children[s_child_key].children[s_s_child_key].children[0].data += 1
                        else:
                            if data[key] in final_dict:
                                final_dict[data[key]] += 1
                            else:
                                final_dict[data[key]] = 1
            count += 1
    return tree_root, num_to_variable_dict

def recur(initial_location, location, initial_entropy):
    if len(location.children[0].children[0].children) == 0:
        e = entropy(location)
        
        if initial_location.data not in entropy_dict:
            entropy_dict[initial_location.data] = {}
            entropy_dict[initial_location.data][location.data] = e[0]
        else:
            entropy_dict[initial_location.data][location.data] = e[0]
        
        if initial_location.data not in information_gain_dict:
            information_gain_dict[initial_location.data] = {}
            information_gain_dict[initial_location.data][location.data] = (initial_entropy - e[0])
        else:
            information_gain_dict[initial_location.data][location.data] = (initial_entropy - e[0])
        
        if initial_location.data not in frequency_dict:
            frequency_dict[initial_location.data] = {}
            frequency_dict[initial_location.data][location.data] = e[1]
        else:
            frequency_dict[initial_location.data][location.data] = e[1]

        return e
    else:
        total_entropy_vals = []
        for i in range(len(location.children)):
            recur(location, location.children[i], initial_entropy)
            total_entropy_vals.append(location.children[i])
        
        total = 0.0
        for j in total_entropy_vals:
            total += frequency_dict[location.data][j.data]
        
        total_entropy = 0.0
        for k in total_entropy_vals:
            total_entropy += (frequency_dict[location.data][k.data]/total) * entropy_dict[location.data][k.data]
        
        if initial_location.data not in entropy_dict:
            entropy_dict[initial_location.data] = {}
            entropy_dict[initial_location.data][location.data] = total_entropy
        else:
            entropy_dict[initial_location.data][location.data] = total_entropy
        
        if initial_location.data not in information_gain_dict:
            information_gain_dict[initial_location.data] = {}
            information_gain_dict[initial_location.data][location.data] = initial_entropy - total_entropy
        else:
            information_gain_dict[initial_location.data][location.data] = initial_entropy - total_entropy
        
        if initial_location.data not in frequency_dict:
            frequency_dict[initial_location.data] = {}
            frequency_dict[initial_location.data][location.data] = total
        else:
            frequency_dict[initial_location.data][location.data] = total

        return total_entropy

def entropy(location):
    entropy_vals = []
    for i in range(len(location.children)):
        entropy_vals.append(location.children[i].children[0].data)
    return entropy_helper(entropy_vals)

def entropy_helper(nums):
    total = 0.0
    for num in nums:
        total += num
    
    result = 0.0
    for num in nums:
        result += (num/total) * math.log2(num/total)
    
    return ((-1 * result), total)

def recur_big(initial_location, location, child_dict, max_var, sub_tree, file_name):
    initial_location = location
    location.addNode(Node(max_var))
    location = location.children[len(location.children) - 1]
    for child_var in child_dict[(m := max_var)]:
        if entropy_dict[m][child_var] == 0:
            #printTree(sub_tree, 0)
            #print(entropy_dict)
            s_child_key = sub_tree.checkChildren(m)
            s_s_child_key = sub_tree.children[s_child_key].checkChildren(child_var)
            leaf = sub_tree.children[s_child_key].children[s_s_child_key].children[0].data
            location.addNode(Node(child_var))
            location.children[len(location.children) - 1].addNode(Node(leaf))
        else:
            sub_tree, new_num_to_variable_dict = createTree("sub_tree", True, child_var, file_name)
            location.addNode(Node(child_var))
            key = len(location.children) - 1
            new_location = location.children[key]

            new_entropy_vals = []
            for i in final_dict.keys():
                new_entropy_vals.append(final_dict[i])

            new_entropy = entropy_helper(new_entropy_vals)[0]
            recur(sub_tree, sub_tree, new_entropy)

            new_child_dict = {}
            for j in range(len(new_num_to_variable_dict) - 1):
                for k in sub_tree.children[j].children:
                    if sub_tree.children[j].data in new_child_dict:
                        new_child_dict[sub_tree.children[j].data].append(k.data)
                    else:
                        new_child_dict[sub_tree.children[j].data] = [k.data]

            max_var = ""
            max_info_gain = 0
            for initial_var in new_child_dict.keys():
                if max_info_gain < information_gain_dict[sub_tree.data][initial_var]:
                    max_info_gain = information_gain_dict[sub_tree.data][initial_var]
                    max_var = initial_var

            #printTree(sub_tree, 0)
            #print(entropy_dict)
            #print(information_gain_dict)
            #printTree(result_tree, 0)
            recur_big(initial_location, new_location, new_child_dict, max_var, sub_tree, file_name)

children_dict = {}
num_to_variable_dict = {}

tree_root, num_to_variable_dict = createTree("start", False, "idk", file_name)

initial_entropy_vals = []
for i in final_dict.keys():
    initial_entropy_vals.append(final_dict[i])

initial_entropy = entropy_helper(initial_entropy_vals)[0]
recur(tree_root, tree_root, initial_entropy)

for j in range(len(num_to_variable_dict) - 1):
    for k in tree_root.children[j].children:
        if tree_root.children[j].data in children_dict:
            children_dict[tree_root.children[j].data].append(k.data)
        else:
            children_dict[tree_root.children[j].data] = [k.data]

max_var = ""
max_info_gain = 0
for initial_var in children_dict.keys():
    if max_info_gain < information_gain_dict[tree_root.data][initial_var]:
        max_info_gain = information_gain_dict[tree_root.data][initial_var]
        max_var = initial_var

result_tree = Tree(max_var)
recur_big(result_tree, result_tree, children_dict, max_var, tree_root, file_name)
printTree(result_tree.children[0], 0)

stout = sys.stdout
with open("treeout.txt", "w") as f:
    sys.stdout = f
    printTree(result_tree.children[0], 0)
    sys.stdout = stout

#printTree(tree_root, 0)
# print(max_var)
#print(initial_entropy)
# print()
#print(entropy_dict)
# print(children_dict)
#print(information_gain_dict)
#print(frequency_dict)
