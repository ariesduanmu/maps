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

# -*- coding: utf-8 -*-
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import squareform, pdist, cdist
from numpy.linalg import norm
from pprint import pprint

'''
hmm haha not so interested in this birddddd now, so I just copy code,
I think I will idk haha
ok things news for me:

matplotlib has animation!!! and even react to button even!!!

the pdist and squareform is really anamzing, scipy is amazing
'''

class Birds():
    def __init__(self, n, width, height):
        self.pos = [width/2, height/2] + 10 * np.random.rand(2*n).reshape(n, 2)
        angles = 2*math.pi*np.random.rand(n)
        self.vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.n = n
        self.minDist = 25.0
        self.maxRuleVel = 0.03
        self.maxVel = 2.0
        self.width = width
        self.height = height

    def tick(self, frameNum, pts, beak):
        distMatrix_x = squareform(pdist(self.pos, lambda u, v: abs(u-v)[0]))
        distMatrix_y = squareform(pdist(self.pos, lambda u, v: abs(u-v)[1]))
        self.distMatrix = np.vstack((distMatrix_x.reshape(1,self.n*self.n),\
                                     distMatrix_y.reshape(1,self.n*self.n))).T\
                                    .reshape(self.n, self.n, 2)
        self.vel += self.applyRules()
        self.limit(self.vel, self.maxVel)
        self.pos += self.vel
        # self.applyBC()

        # self.vel = self.vel*0.9
        pts.set_data(self.pos.reshape(2*self.n)[::2],
                     self.pos.reshape(2*self.n)[1::2])
        vec = self.pos + 10*self.vel/self.maxVel
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
        for coord in self.pos:
            if coord[0] > self.width:
                self.stop = True
                coord[0] = self.width
            if coord[0] < 0:
                self.stop = True
                coord[0] = 0
            if coord[1] > self.height:
                self.stop = True
                coord[1] = self.height
            if coord[1] < 0:
                self.stop = True
                coord[1] = 0

    def applyRules(self):
        D = self.distMatrix < 2.0
        D = D.prod(axis=2)
        vel = self.pos*D.sum(axis=1).reshape(self.n, 1) - D.dot(self.pos)
        self.limit(vel, self.maxRuleVel)

        return vel

    def buttonPress(self, event):
        # left click - add a bird
        if event.button == 1:
            self.pos = np.concatenate((self.pos, np.array([[event.xdata, event.ydata]])), axis=0)
            angles = 2*math.pi*np.random.rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel = np.concatenate((self.vel, v), axis=0)
            self.n += 1
        # right click - scatter
        elif event.button == 3:
            self.vel += 0.1*(self.pos - np.array([[event.xdata, event.ydata]]))


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
    birds = Birds(args.num_birds, args.width, args.height)
    fig = plt.figure()
    ax = plt.axes(xlim=(0, args.width), ylim=(0, args.height))

    pts, = ax.plot([], [], markersize=10, color='b', marker='o', ls='None')
    beak, = ax.plot([], [], markersize=4, color='c', marker='o', ls='None')
    anim = animation.FuncAnimation(fig, func=tick, fargs=(pts, beak, birds), interval=50)

    cid = fig.canvas.mpl_connect('button_press_event', birds.buttonPress)
    plt.show()


if __name__ == "__main__":
    main()