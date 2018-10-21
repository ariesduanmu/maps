# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import squareform, pdist, cdist
from numpy.linalg import norm
from pprint import pprint
from helper.helper import generate_image


class Rooms():
    
    def __init__(self, n, width, height, length_min, length_max):
        self._pos = [width/2, height/2] + 10 * np.random.rand(2*n).reshape(n, 2)
        # half width/height
        self._size = ([length_min, length_min] + (length_max-length_min) * np.random.rand(2*n).reshape(n, 2))*2
        self._size = self._size.astype(int)
        self._minDistanceMatrix = squareform(pdist(self._size, lambda u, v: sum(np.hypot([u[0],v[0]],[u[1],v[1]]))))
        self._distMatrix = squareform(pdist(self._pos))
        angles = 2*math.pi*np.random.rand(n)
        self._vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self._n = n
        self._maxRuleVel = 0.03
        self._maxVel = 0.5
        self._width = width
        self._height = height

    @property
    def centers(self):
        return self._pos

    @property
    def sizes(self):
        return self._size
    
    @property
    def distance(self):
        return self._distMatrix < self._minDistanceMatrix


    def tick(self):
        self._distMatrix = squareform(pdist(self._pos))
        self._vel += self.applyRules()
        self.limit(self._vel, self._maxVel)
        self._pos += self._vel

    def limitVec(self, vec, maxVel):
        mag = norm(vec)
        if mag > maxVel:
            vec[0], vec[1] = vec[0]*maxVel/mag, vec[1]*maxVel/mag

    def limit(self, x, maxVel):
        for vec in x:
            self.limitVec(vec, maxVel)

    def applyRules(self):
        vel = self._pos*self.distance.sum(axis=1).reshape(self._n, 1) - self.distance.dot(self._pos)
        self.limit(vel, self._maxRuleVel)
        return vel

def random_rooms(num_rooms, size):
    width, height = size
    birds = Rooms(num_rooms, width, height, 1, 3)
    while True:
        if birds.distance.sum() == 0:
            break
        birds.tick()

    board = [[0 for _ in range(width)] for _ in range(height)]
    for i in range(num_rooms):
        r, c = birds.centers[i]
        r = int(r)
        c = int(c)
        h, w = birds.sizes[i]
        if r-h >= 0 and r+h < width and c-w >= 0 and c+w < height:
            for x in range(r-h, r+h+1):
                for y in range(c-w, c+w+1):
                    board[x][y] = 2
    return board

def parse_arguments():
    parser = argparse.ArgumentParser(description="Implementing Craig Reynold's Boids...")
    parser.add_argument('-n','--num_rooms', type=int, default=30, required=False, help="birds number")
    parser.add_argument('-w','--width', type=int, default=99, required=False, help="plot screen width")
    parser.add_argument('-e','--height', type=int, default=99, required=False, help="plot screen height")

    args = parser.parse_args()
    return args
    


if __name__ == "__main__":
    args = parse_arguments()
    board = random_rooms(args.num_rooms, (args.width, args.height))
    generate_image(board, (990,990))