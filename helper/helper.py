# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image

def generate_image(board, size, output_filename="maze.png"):
    width, height = size
    w, h = len(board[0]), len(board)
    a = min(width // w, height // h)

    image_data = [[0]*width for _ in range(height)]
    for i in range(h):
        for j in range(w):
            if board[i][j] == 2:
                amplify_dot(image_data, i, j, a)
            if board[i][j] == 1:
                amplify_dot(image_data, i, j, a)
                
    maze_img = Image.fromarray(np.asarray(dtype=np.dtype('uint8'),a=image_data), mode='L').convert('1')
    maze_img.save(output_filename)

def generate_colorful_image(board, size, output_filename="maze.png"):
    width, height = size
    w, h = len(board[0]), len(board)
    a = min(width // w, height // h)

    image_data = [[(100,100,100)]*width for _ in range(height)]
    for i in range(h):
        for j in range(w):
            if board[i][j] == 2:
                amplify_dot(image_data, i, j, a, (255,0,0))
            if board[i][j] == 1:
                amplify_dot(image_data, i, j, a, (0,255,0))
                
    maze_img = Image.fromarray(np.asarray(dtype=np.dtype('uint8'),a=image_data))
    maze_img.save(output_filename)

def amplify_dot(board, i, j, a, color=255):
    for x in range(i*a, (i+1)*a):
        for y in range(j*a, (j+1)*a):
            board[x][y] = color