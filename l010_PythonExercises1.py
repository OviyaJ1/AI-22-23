#Oviya Jeyaprakash 08/24/2022
#Python Exercises 1
#010
import sys

if(sys.argv[1] == "A"):
    print(int(sys.argv[2]) + int(sys.argv[3]) + int(sys.argv[4]))

elif(sys.argv[1] == "B"):
    x = 0
    for index, value in enumerate(sys.argv):
        if(index > 1):
            x += int(value)
    print(x)

elif(sys.argv[1] == "C"):
    l = []
    for index, value in enumerate(sys.argv):
        if(index > 1 and int(value) % 3 == 0):
            l.append(value)
    print(l)

elif(sys.argv[1] == "D"):
    a = b = 1
    l = []
    for i in range(x := int(sys.argv[2])):
        if(i == 0):
            l.append(1)
        if(i == 1):
            l.append(1)
        elif(i >= 2):
            c = a + b
            a = b 
            b = c
            l.append(c)
    print(l)

elif(sys.argv[1] == "E"):
    l = []
    a, b = int(sys.argv[2]), int(sys.argv[3])
    for i in range(a, b + 1):
        l.append(pow(i, 2) - 3 * i + 2)
    print(l)

elif(sys.argv[1] == "F"):
    a, b, c = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])

    if((a + b) <= c or (a + c) <= b or (b + c) <= a):
        print("Invalid")
    else:
        p = (a + b + c)/2
        print(pow(p * (p-a) * (p-b) * (p-c), 0.5))

elif(sys.argv[1] == "G"):
    l = [0, 0, 0, 0, 0] #order a,e,i,o,u
    for index, s in enumerate(sys.argv[2]):
        if(s == "a" or s == "A"):
            l[0] += 1
        elif(s == "e" or s == "E"):
            l[1] += 1
        elif(s == "i" or s == "I"):
            l[2] += 1
        elif(s == "o" or s == "O"):
            l[3] += 1
        elif(s == "u" or s == "U"):
            l[4] += 1
    print("A:" + str(l[0]) + " E:" + str(l[1]) + " I:" + str(l[2]) + " O:" + str(l[3]) + " U:" + str(l[4]))

    
    
    
