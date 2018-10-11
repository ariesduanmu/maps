# -*- coding: utf-8 -*-


# @dataclass
# class Room():
#     center: (int, int)
#     size: (int, int)

#     @property
#     def boundary(self):
#         i, j = self.center
#         w, h = self.size
#         return i-w//2, j-h//2, i+w//2, j+h//2

'''

compare the center distance

width distance
>>> squareform(pdist(a, lambda u, v: abs(u-v)[0]))
array([[0., 1., 0.],
       [1., 0., 1.],
       [0., 1., 0.]])

height distance
>>> squareform(pdist(a, lambda u, v: abs(u-v)[1]))
array([[0., 1., 0.],
       [1., 0., 1.],
       [0., 1., 0.]])

if the distance larger than the sum of two half square


'''

import argparse
import math
import random

n = 10
width = 100
height = 100

# position of center (40-60, 40-60)
centers = [(random.random()*10+50, random.random()*10+50) for i in range(10)]

# width/height (10-20)
size = [(int(random.random()*10+10), int(random.random()*10+10)) for i in range(10)]


angle = [random.random() for i in range(10)]
vec = [(math.sin(angle), math.cos(angle)) for i in range(10)]

# calculate the distance of each room, if it is too small update vel

# stop while vel is zero