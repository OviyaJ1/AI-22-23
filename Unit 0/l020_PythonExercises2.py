#Oviya Jeyaprakash 08/25/2022
#Python Exercises 2
#020

import sys
s = sys.argv[1]

print("#1:", s[2])

print("#2:", s[4])

print("#3:", len(s))

print("#4:", s[0])

print("#5:", s[len(s) - 1])

print("#6:", s[len(s) - 2])

print("#7:", s[3:8])

print("#8:", s[len(s) - 5:])

print("#9:", s[2:])

print("#10:", s[::2])

print("#11:", s[1::3])

print("#12:", s[::-1])

print("#13:", s.find(" "))

print("#14:", s[:len(s) - 1])

print("#15:", s[1:])

print("#16:", s.lower())

print("#17:", (x := s.split()))

print("#18:", len(x))

print("#19:", list(s))

print("#20:", ''.join(sorted(s)))

print("#21:", s[:s.find(" ")])

print("#22:", True if s == s[::-1] else False)
