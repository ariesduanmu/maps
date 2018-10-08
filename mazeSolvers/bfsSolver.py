# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from collections import deque
from mazeGenerator.maze import Maze
from helper.helper import generate_image

def bfs_solver(board, start, end):
    n, m = len(board), len(board[0])
    open_points = deque()
    meta = {}
    close_points = set()

    open_points.append(start)

    while open_points:
        point = open_points.popleft()
        if point == end:
            return construct_path(end, meta)
        
        r, c = point
        directions = ((0,1),(0,-1),(1,0),(-1,0))
        for i, j in directions:
            if 0 <= r+i < n and 0 <= c+j < m:
                if board[r+i][c+j] == 2 and (r+i, c+j) not in close_points:
                    open_points.append((r+i,c+j))
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
    maze = Maze((9,9))
    maze()
    print(maze.board)
    print(maze.start_point)
    print(maze.end_point)
    board = [b[:] for b in maze.board]
    route = bfs_solver(maze.board, maze.start_point, maze.end_point)
    for i, j in route:
        board[i][j] = 1
    generate_image(board, (990,990))


