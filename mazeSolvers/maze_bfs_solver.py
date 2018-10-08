# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from queue import Queue
from mazeGenerator.maze import Maze
from helper.helper import generate_image

def bfs_solver(board, start, end):
    n, m = len(board), len(board[0])
    open_points = Queue()
    meta = {}
    close_points = set()

    open_points.put(start)

    while not open_points.empty():
        point = open_points.get()
        if point == end:
            return construct_path(end, meta)
        
        r, c = point
        directions = ((0,1),(0,-1),(1,0),(-1,0))
        for i, j in directions:
            if 0 <= r+i < n and 0 <= c+j < m:
                if board[r+i][c+j] == 2 and (r+i, c+j) not in close_points:
                    open_points.put((r+i,c+j))
                    meta[(r+i,c+j)] = (r,c)
        close_points.add(point)

def construct_path(point, meta):
    route = [point]
    while meta.get(point):
        last_point = meta.get(point)
        route.append(last_point)
        point = last_point
    return route

if __name__ == "__main__":
    maze = Maze((99,99))
    maze()
    board = [b[:] for b in maze.board]
    route = bfs_solver(maze.board, maze.start_point, maze.end_point)
    for i, j in route:
        board[i][j] = 1
    generate_image(board, (990,990))


