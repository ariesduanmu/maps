# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
from maze import Maze
from room import Room

def generate_image(maze, room, size, output_filename="maze.png"):
    width, height = size
    w, h = len(maze.board[0]), len(maze.board)
    a = min(width // w, height // h)

    image_data = [[0]*width for _ in range(height)]
    for i in range(h):
        for j in range(w):
            if maze.board[i][j] == 2 or room.board[i][j] == 2:
                amplify_dot(image_data, i, j, a)
            if room.board[i][j] == 1:
                amplify_dot(image_data, i, j, a, 100)
                
    maze_img = Image.fromarray(np.asarray(dtype=np.dtype('uint8'),a=image_data), mode='L').convert('1')
    maze_img.save(output_filename)

def amplify_dot(board, i, j, a, color=255):
    for x in range(i*a, (i+1)*a):
        for y in range(j*a, (j+1)*a):
            board[x][y] = color


if __name__ == "__main__":
    map_size = (100,100)
    maze = Maze(map_size)
    maze.generate()
    room = Room(map_size)
    room.generate()

    generate_image(maze, room, (990,990))




