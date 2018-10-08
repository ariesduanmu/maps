# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from mazeGenerator.maze import Maze
from helper.helper import generate_image

def dfs_solver(board, start, end):
    n, m = len(board), len(board[0])
    open_point = [start]
    meta = {}
    visited_points = set()
    visited_points.add(start)

    while len(open_point) > 0:
        point = open_point[-1]
        if point == end:
            return construct_path(point, meta)
        r, c = point
        directions = ((0,1),(0,-1),(1,0),(-1,0))
        for i, j in directions:
            if 0 <= r+i < n and 0 <= c+j < m:
                if board[r+i][c+j] == 2 and (r+i, c+j) not in visited_points:
                    open_point.append((r+i, c+j))
                    visited_points.add((r+i, c+j))
                    meta[(r+i,c+j)] = (r,c)
                    break
        else:
            open_point.pop()
            

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
    print(f"[*] Start Point: {maze.start_point}")
    print(f"[*] End Point: {maze.end_point}")
    print("[*] Searching solution..")
    route = dfs_solver(maze.board, maze.start_point, maze.end_point)
    for i, j in route:
        board[i][j] = 1
    generate_image(board, (990,990))
    print("[*] Done")