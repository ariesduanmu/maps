# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from random import choices, randint
from pprint import pprint
import numpy as np
import math
from helper.helper import generate_image

#width/height 5 - 10
def random_center(n, width, height):
    centers = [width/2, height/2] + 10 * np.random.rand(2*n).reshape(n,2)
    size = [5,5] + 5*np.random.rand(2*n).reshape(n,2)
    angles = 2*math.pi*np.random.rand(n)
    vel = np.array(list(zip(np.sin(angles), np.cos(angles))))

    
    pprint(centers.astype(int))
    pprint(size.astype(int))


if __name__ == "__main__":
    random_center(10, 100, 100)



