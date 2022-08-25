import sys
s = sys.argv[1]

print(s[2]) #1

print(s[4]) #2

print(len(s)) #3

print(s[0]) #4

print(s[len(s) - 1]) #5

print(s[len(s) - 2]) #6

print(s[3:8]) #7

print(s[len(s) - 5:]) #8

print(s[3:]) #9

print(value for index, value in enumerate(s) if index%2 == 1) #10!