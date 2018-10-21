# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from helper.helper import generate_colorful_image
from dungeon.random_room import random_rooms
from random import choice

'''
Randomized Kruskal's algorithm and bird random room
'''
def corridor(board, step=2):
    row, column = len(board), len(board[0])
    moves = [(i,j) for i in range(row) for j in range(column) if (i-1)%step==0 and (j-1)%step==0 and board[i][j] == 0]
    if len(moves) > 0:
        r, c = choice(moves)
        board[r][c] = 1
        history = [(r,c)]
        while len(history)>0:
            r, c = choice(history)
            check = []
            if r + step < row and board[r+step][c] == 0:
                check.append((step,0))

            if c + step < column and board[r][c+step] == 0:
                check.append((0,step))

            if r - step >= 0 and board[r-step][c] == 0:
                check.append((-1*step,0))

            if c - step >= 0 and board[r][c-step] == 0:
                check.append((0,-1*step))

            if len(check) > 0:
                i, j = choice(check)
                x, y = i//step, j//step
                for k in range(1,step+1):
                    board[r+x*k][c+y*k] = max(1, board[r+x*k][c+y*k])
                history.append((r+i,c+j))
            else:
                history.remove((r,c))

            if len(history) == 0:
                moves = [(i,j) for i in range(row) for j in range(column) if (i-1)%step==0 and (j-1)%step==0 and board[i][j] == 0]
                if len(moves) > 0:
                    r, c = choice(moves)
                    board[r][c] = 1
                    history = [(r,c)]
    return board




if __name__ == "__main__":
    r = c = 99
    num_rooms = 30
    board = random_rooms(num_rooms, (r,c))
    board = corridor(board, 5)
    generate_colorful_image(board, (990,990))
