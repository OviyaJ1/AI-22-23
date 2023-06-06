# Oviya Jeyaprakash, 2/7/2023 
# Practical RegEx (Colorama and Re Implementation)
# l530

import sys
import re
from colorama import init, Back, Fore

init()
initial_input = sys.argv[1]
input = (initial_input.split("/"))[1]
flags = (initial_input.split("/"))[2]

#s = "While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?"
s = "commercialistic"
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

result_acc = ""
last_index = 0
beBlue = False

for result in exp.finditer(s):
    if result.start() == last_index and last_index != 0 and beBlue == True:
        result_acc += s[last_index:result.start()] + Back.LIGHTCYAN_EX + Fore.BLACK + s[result.start():result.end()] + Back.RESET + Fore.RESET
        last_index = result.end() 
        beBlue = False
    else:
        result_acc += s[last_index:result.start()] + Back.LIGHTYELLOW_EX + Fore.BLACK + s[result.start():result.end()] + Back.RESET + Fore.RESET
        last_index = result.end()
        beBlue = True

print(result_acc + s[last_index:])

if exp.fullmatch(s):
    print("bruh")
    
    for result in exp.finditer(s):
        print(result.start(), result.end())