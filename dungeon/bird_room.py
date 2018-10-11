# -*- coding: utf-8 -*-
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import squareform, pdist, cdist
from numpy.linalg import norm
from dataclasses import dataclass

# @dataclass
# class Room():
#     center: (int, int)
#     size: (int, int)

#     @property
#     def boundary(self):
#         i, j = self.center
#         w, h = self.size
#         return i-w//2, j-h//2, i+w//2, j+h//2

class Rooms():
    def __init__(self, n, width, height):
        self.center = [width/2, height/2] + 10 * np.random.rand(2*n).reshape(n, 2)
        #width/height, room size range from 10-20
        self.size = [10, 10] + 10 * np.random.rand(2*n).reshape(n, 2)

        #spead outside
        angles = 2*math.pi*np.random.rand(n)
        self.vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.width = width
        self.height = height
        self.n = n
        self.minDist = 25.0
        self.maxRuleVel = 0.03
        self.maxVel = 2.0

    def tick(self, frameNum, pts, beak):
        self.distMatrix = squareform(pdist(self.center))
        self.vel += self.applyRules()
        self.limit(self.vel, self.maxVel)
        self.center += self.vel
        self.applyBC()

        pts.set_data(self.center.reshape(2*self.n)[::2],
                     self.center.reshape(2*self.n)[1::2])
        vec = self.center + 10*self.vel/self.maxVel
        beak.set_data(vec.reshape(2*self.n)[::2],
                      vec.reshape(2*self.n)[1::2])

    def limitVec(self, vec, maxVel):
        mag = norm(vec)
        if mag > maxVel:
            vec[0], vec[1] = vec[0]*maxVel/mag, vec[1]*maxVel/mag

    def limit(self, x, maxVel):
        for vec in x:
            self.limitVec(vec, maxVel)

    def applyBC(self):
        for k in range(self.n):
            i, j = self.center[k]
            w, h = self.size[k]
            if i+w//2 > self.width:
                self.center[k][0] = self.width - w//2
            if i-w//2 < 0:
                self.center[k][0] = w//2
            if j+h//2 > self.height:
                self.center[k][1] = self.height - h//2
            if j-h//2 < 0:
                self.center[k][1] = h//2

    def applyRules(self):
        D = self.distMatrix < 50.0
        vel = self.center*D.sum(axis=1).reshape(self.n, 1) - D.dot(self.center)
        #self.limit(vel, self.maxRuleVel)

        # different distance threshold
        D = self.distMatrix < 100.0

        # apply rule #2 - Alignment
        vel2 = D.dot(self.vel)
        #self.limit(vel2, self.maxRuleVel)
        vel += vel2

        # # apply rule #1 - Cohesion
        vel3 = D.dot(self.center) - self.center
        self.limit(vel3, self.maxRuleVel)
        vel += vel3

        return vel

def tick(frameNum, pts, beak, birds):
    birds.tick(frameNum, pts, beak)
    return pts, beak

def parse_arguments():
    parser = argparse.ArgumentParser(description="Implementing Craig Reynold's Boids...")
    parser.add_argument('-n','--num_birds', type=int, default=100, required=False, help="birds number")
    parser.add_argument('-w','--width', type=int, default=640, required=False, help="plot screen width")
    parser.add_argument('-e','--height', type=int, default=480, required=False, help="plot screen height")

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    birds = Rooms(args.num_birds, args.width, args.height)
    fig = plt.figure()
    ax = plt.axes(xlim=(0, args.width), ylim=(0, args.height))

    pts, = ax.plot([], [], markersize=10, color='b', marker='o', ls='None')
    beak, = ax.plot([], [], markersize=4, color='c', marker='o', ls='None')
    anim = animation.FuncAnimation(fig, func=tick, fargs=(pts, beak, birds), interval=50)

    plt.show()


if __name__ == "__main__":
    main()