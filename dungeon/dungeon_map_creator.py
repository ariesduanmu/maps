# -*- coding: utf-8 -*-

from helper.helper import generate_image
from mazeGenerator.maze import Maze
from dungeon.room import Room


if __name__ == "__main__":
    map_size = (9,9)
    maze = Maze(map_size)
    maze.generate()
    room = Room(map_size)
    room.generate()
    r, c = map_size
    board = [[0]*c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            if maze.board[i][j] == 2 or room.board[i][j] == 2:
                board[i][j] = 2
            if room.board[i][j] == 1:
                board[i][j] = 1
    print(board)

    generate_image(board, (90,90))




