example = [3, 7, 5, 3, 0]

#Java-esque
for i in range(len(example)):
    print(i, example[i])

#Pythonic
for index, value in enumerate(example):
    print(index, value)

#DO NOT USE OBJECTS IN PYTHON
def example_tuple_return():
    board_state = "...............X"
    num_of_moves = 1
    return board_state, num_of_moves

new_board_state, new_num_of_moves = example_tuple_return()
print(new_board_state)
print(new_num_of_moves)
a, b, c = 1, 2, 3

#Bad
if len(example) < 10:
    print(len(example))

#Better
x = len(example)
if x < 10:
    print(x)

#Pythonic
if (x := len(example)) < 10:
    print(x)

# Cute boolean use
if example:
    print("Hello")

other_example = []
if other_example:
    print("Hello again")

#Comprehensions

#Java-esque
new_list = []
for value in example:
    new_list.append(value * 2)

#Pythonic
new_list = [value * 2 for value in example]
new_list_2 = [a + b for a in example for b in new_list if a + b % 2 == 0]