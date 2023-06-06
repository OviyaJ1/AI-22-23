# Oviya Jeyaprakash, 2/7/2023 
# Practical RegEx (Dict Search)
# l535

import sys
import re

dict_input = sys.argv[1]

'''def minLengthFunc(result_extra):
    min = len(result_extra[0])
    result = []
    count = 0

    for i in result_extra:
        if len(i) < min:
            min = len(i)
            count = 0
            count += 1
            result = []
            result.append(i)
        elif len(i) == min:
            count += 1
            if count <= 5:
                result.append(i)

    return (result, count)

def maxLengthFunc(result_extra):
    max = len(result_extra[0])
    result = []
    count = 0

    for i in result_extra:
        if len(i) > max:
            max = len(i)
            count = 0
            count += 1
            result = []
            result.append(i)
        elif len(i) == max:
            count += 1
            if count <= 5:
                result.append(i)

    return (result, count)

def func(initial_input, question, extra):
    input = (initial_input.split("/"))[1]
    flags = (initial_input.split("/"))[2]
    count = 0
    result_extra = []
    result_acc = []

    with open(dict_input) as f:        
        exp = None
        if len(flags) != 0:
            if "i" in flags and "m" in flags and "s" in flags:
                exp = re.compile(r"{}".format(input), re.I | re.S | re.M)
            elif "i" in flags and "m" in flags:
                exp = re.compile(r"{}".format(input), re.I | re.M)
            elif "i" in flags and "s" in flags:
                exp = re.compile(r"{}".format(input), re.I | re.S)
            elif "s" in flags and "m" in flags:
                exp = re.compile(r"{}".format(input), re.M | re.S)
            elif "i" in flags:
                exp = re.compile(r"{}".format(input), re.I)
            elif "m" in flags:
                exp = re.compile(r"{}".format(input), re.M)
            elif "s" in flags:
                exp = re.compile(r"{}".format(input), re.S)
        else:
            exp = re.compile(r"{}".format(input))

        for line in f:
            s = line.strip()
            s = s.lower()
            #s = "abaaba"
            #print(exp.findall(s))
            #if exp.fullmatch(s):
            for result in exp.finditer(s):
                if result.start() == 0 and result.end() == (len(s)):
                    count += 1
                    if(count <= 5):
                        result_acc.append(s)
                    result_extra.append(s)

    if extra == 1:
        result_acc, count = minLengthFunc(result_extra)
    if extra == 2:
        result_acc, count = maxLengthFunc(result_extra)

    print(question, initial_input)
    print(count, "total matches")
    for i in result_acc:
        print(i)
    print()

#question 1
#func("/\w*/i", "#1:")
#func("/\w*?([aeiou])(?!\w*\1)\w*?([aeiou])(?!\w*\2)\w*?([aeiou])(?!\w*\3)\w*?([aeiou])(?!\w*\4)\w*?([aeiou])(?!\w*\5)/i", "#1:", 1)
#func("/\w*([aeiou])\w*(?!\w*\1)([aeiou])\w*(?!\w*\2)([aeiou])\w*(?!\w*\3)([aeiou])\w*(?!\w*\4)([aeiou])\w*(?!\w*\5)/i", "#2:", 2)
#func("/(?=\w*((\w)(\w)(\w))\b)\w*\4\3\2\b/i", "#4:", 0)
#func("/\b(?=(\w)(\w)(\w))\w*\3\2\1\b/i", "#4:", 0)
func("/(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)\w*/i", "#1:", 1)
func("/([^aeiou]*?[aeiou]){5}[^aeiou]*/i", "#2:", 2)

#func("/^(\w)(?!\w*?\1)\w*\1$/i", "#3:", 1)
#func("/^(\w)\w*?\1/i", "#3:", 1)

reg = r"^(\w)\w*?\1"
reg_bruh = re.compile(reg, re.I)
r = []
r_extra = []
count = 0

with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                count += 1
                if(count <= 5):
                    r.append(s)
                r_extra.append(s)

r_acc, c = maxLengthFunc(r_extra)

print("#3:", "/^(\w)\w*?\1/i")
print(c, "total matches")
for i in r_acc:
    print(i)
print()


reg = r"^(\w)(\w)(\w)\w*$(?<=\3\2\1)"
reg_bruh = re.compile(reg, re.I)
r = []
r_extra = []
count = 0

with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        if reg_bruh.fullmatch(s):
            count += 1
            if(count <= 5):
                r.append(s)
            r_extra.append(s)

print("#4:", "/^(\w)(\w)(\w)\w*$(?<=\3\2\1)/i")
print(count, "total matches")
for i in r:
    print(i)
print()

#func("/^(\w)(\w)(\w)\w*$(?<=\3\2\1)/i", "#4:", 0)
func("/[^tb]*?(tb|bt)(?!\w*(t|b))\w*/i", "#5:", 0)'''

reg = r"\w*(\w)\1+\w*"
reg_bruh = re.compile(reg, re.I)
r = []
r_extra = []
count = 0
temp_list = []
max_length = 0

with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                temp_list.append(s)

                max_length_char = 0
                characters = {}
                for char_len in range(1, len(s)):
                    temp_count = 1
                    while s[char_len] == s[char_len - temp_count] and char_len - temp_count >= 0:
                        temp_count += 1
                    if temp_count > max_length_char:
                        max_length_char = temp_count

                if max_length_char > max_length:
                    max_length = max_length_char

reg = r"\w*(\w)\1{" + str(max_length - 1) + r"}\w*"
reg_bruh = re.compile(reg, re.I)

count = 0
r = [] 
r_extra = []  
with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                count += 1
                if(count <= 5):
                    r.append(s)
                r_extra.append(s)

print("#6:", "/\w*(\w)\1{" + str(max_length - 1) + r"}\w*/i")
print(count, "total matches")
for i in r:
    print(i)
print()

#####

'''reg = r"\w*(\w)\w*\1+\w*"
reg_bruh = re.compile(reg, re.I)
r = []
r_extra = []
count = 0
temp_list = []
max_length = 1

with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        #if reg_bruh.fullmatch(s):
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                temp_list.append(s)

                characters = {}
                for char in s:
                    if char in characters:
                        characters[char] += 1
                    else:
                        characters[char] = 1

                max_length_char = 1
                for value in characters.values():
                    if value > max_length_char:
                        max_length_char = value

                if max_length_char > max_length:
                    max_length = max_length_char

            count += 1
            if(count <= 5):
                r.append(s)
            r_extra.append(s)

#print(max_length - 1)
reg = r"\w*(\w)(\w*\1){" + str(max_length - 1) + r"}\w*"
reg_bruh = re.compile(reg, re.I)

count = 0
r = [] 
r_extra = []  
with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                count += 1
                if(count <= 5):
                    r.append(s)
                r_extra.append(s)

print("#7:", "/\w*(\w)(\w*\1){" + str(max_length - 1) + r"}\w*/i")
print(count, "total matches")
for i in r:
    print(i)
print()

reg = r"\w*((\w)(\w))\w*\1\w*"
reg_bruh = re.compile(reg, re.I)
r = []
r_extra = []
count = 0
temp_list = []
max_length = 1

with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        #if reg_bruh.fullmatch(s):
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                temp_list.append(s)

                characters = {}
                for char_len in range(len(s)-1):
                    if s[char_len:char_len+2] in characters:
                        characters[s[char_len:char_len+2]] += 1
                    else:
                        characters[s[char_len:char_len+2]] = 1

                max_length_char = 1
                for value in characters.values():
                    if value > max_length_char:
                        max_length_char = value

                if max_length_char > max_length:
                    max_length = max_length_char

            count += 1
            if(count <= 5):
                r.append(s)
            r_extra.append(s)

reg = r"\w*(\w\w)(\w*\1){" + str(max_length - 1) + r"}\w*"
reg_bruh = re.compile(reg, re.I)

count = 0
r = [] 
r_extra = []  
with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                count += 1
                if(count <= 5):
                    r.append(s)
                r_extra.append(s)

print("#8:", "/\w*(\w)(\w*\1){" + str(max_length - 1) + r"}\w*/i")
print(count, "total matches")
for i in r:
    print(i)
print()

reg = r"\w*[^aeiou]\w*"
reg_bruh = re.compile(reg, re.I)
r = []
r_extra = []
count = 0
temp_list = []
max_length = 0

with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        #if reg_bruh.fullmatch(s):
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                temp_list.append(s)

                consonants_num = 0
                for char in s:
                    if char != "a" and char != "e" and char != "i" and char != "o" and char != "u":
                        consonants_num += 1

                if consonants_num > max_length:
                    max_length = consonants_num

            count += 1
            if(count <= 5):
                r.append(s)
            r_extra.append(s)

reg = r"\w*([^aeiou]\w*){" + str(max_length) + r"}\w*"
reg_bruh = re.compile(reg, re.I)

count = 0
r = [] 
r_extra = []  
with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                count += 1
                if(count <= 5):
                    r.append(s)
                r_extra.append(s)

print("#9:", "/\w*([^aeiou]\w*){" + str(max_length) + "}\w*/i")
print(count, "total matches")
for i in r:
    print(i)
print()

reg = r"(?!\w*?(\w)(?=(\w*?\1){2})\w*)\w*"
reg_bruh = re.compile(reg, re.I)
r = []
r_extra = []
count = 0

with open(dict_input) as f: 
    for line in f:
        s = line.strip()
        s = s.lower()
        #s = "abaaba"
        #print(exp.findall(s))
        for result in reg_bruh.finditer(s):
            if result.start() == 0 and result.end() == (len(s)):
                count += 1
                if(count <= 5):
                    r.append(s)
                r_extra.append(s)

r_acc, c = maxLengthFunc(r_extra)

print("#10:", "/(?!\w*?(\w)(?=(\w*?\1){2})\w*)\w*/i")
print(c, "total matches")
for i in r_acc:
    print(i)
print()

#func("/(\w)(?!\w*\1)\w*/i", "#10:", 2)
'''