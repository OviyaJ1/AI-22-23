# Oviya Jeyaprakash, 3/1/2023 
# Deterministic Finite Automaton (DFA)
# l550

import sys

num1 = "ab\n4\n3\n\n0\na 1\n\n1\na 2\n\n2\nb 3\n\n3"
num2 = "012\n3\n2\n\n0\n0 1\n1 2\n2 1\n\n1\n0 1\n1 2\n2 1\n\n2\n0 1\n1 2\n2 1"
num3 = "abc\n3\n2\n\n0\na 1\nb 2\nc 1\n\n1\na 1\nb 2\nc 1\n\n2\na 2\nb 2\nc 2"
num4 = "01\n5\n0 4\n\n0\n0 2\n1 1\n\n1\n0 2\n1 1\n\n2\n0 4\n1 3\n\n3\n0 4\n1 3\n\n4\n0 2\n1 4"
num5 = "01\n4\n0\n\n0\n0 2\n1 1\n\n1\n0 3\n1 0\n\n2\n0 0\n1 3\n\n3\n0 1\n1 2"
num6 = "abc\n4\n0 1 2\n\n0\na 1\nb 0\nc 0\n\n1\na 1\nb 2\nc 0\n\n2\na 1\nb 0\nc 3\n\n3\na 3\nb 3\nc 3"
num7 = "01\n8\n7\n\n0\n0 1\n1 2\n\n1\n0 1\n1 2\n\n2\n0 3\n1 2\n\n3\n0 4\n1 5\n\n4\n0 4\n1 5\n\n5\n0 6\n1 7\n\n6\n0 4\n1 5\n\n7\n0 7\n1 7"

#input = "dfa_ex_spec.txt"
#input2 = "dfa_ex_tests.txt"
input2 = sys.argv[2]
spec = ""

#f = open(input)
#spec = f.read()

try:
    spec2 = int(sys.argv[1])
except:
    f = open(sys.argv[1])
    spec = f.read()

if sys.argv[1] == "1":
    spec = num1
elif sys.argv[1] == "2":
    spec = num2
elif sys.argv[1] == "3":
    spec = num3
elif sys.argv[1] == "4":
    spec = num4
elif sys.argv[1] == "5":
    spec = num5
elif sys.argv[1] == "6":
    spec = num6
elif sys.argv[1] == "7":
    spec = num7

split = spec.split("\n\n")

spec_info = split[0]
state_dfa = {} #
for i in range(1, len(split)):
    line = split[i]

    key_state_dfa = line[0]
    state_dfa[key_state_dfa] = {}
    state_dfa_split = line.split("\n")
    #print(state_dfa_split)

    for j in range(1, len(state_dfa_split)):
        key_small, value_small = state_dfa_split[j].split(" ")
        state_dfa[key_state_dfa][key_small] = value_small

spec_info_split = spec_info.split("\n")
final_states = spec_info_split[2].split(" ")

letter_to_space_dict = {}
temp_list = ["*"]
for c in range(len((char := spec_info_split[0]))):
    temp_list.append(char[c])
    letter_to_space_dict[char[c]] = c + 1

print("         ".join(temp_list))

for d in range(int(spec_info_split[1])):
    temp_list = []
    temp_list.append(str(d))
    for i in letter_to_space_dict.keys():
        if i not in state_dfa[str(d)].keys():
            temp_list.append("_")
        else:
            temp_list.append(state_dfa[str(d)][i])
    print("         ".join(temp_list))

print("Final Nodes:", final_states)


with open(input2) as f:
    for line in f:
        line = line.strip()
        current_node = 0
        flag = True
        for char_num in range(len(line)):
            current_char = line[char_num]
                
            if current_char in state_dfa[str(current_node)] and flag == True:
                new_node = state_dfa[str(current_node)][current_char]
                current_node = new_node
            else: 
                flag = False

        if flag and current_node in final_states:
            print(True, line)
        else:
            print(False, line)
