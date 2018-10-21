# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from helper.helper import generate_image, generate_colorful_image
from dungeon.random_room import random_rooms
from pprint import pprint
from queue import Queue
from random import choice, sample

'''
Recursive division method and bird random room
'''
def corridor(board):
    row, column = len(board), len(board[0])

    for i in range(1,row-1):
        for j in range(1,column-1):
            if board[i][j] == 0:    
                board[i][j] = 1
    # print(board)

    splitable = Queue()
    splitable.put((0, 0, column-1, row-1))
    while splitable.qsize() > 0:
        room = splitable.get()
        subrooms = split_room(board,room)
        if subrooms is None:
            continue
        for subroom in subrooms:
            splitable.put(subroom)
    # pprint(board)
    return board


def split_room(board, room):
    lx, ly, rx, ry = room
    if rx - lx <= 2 or ry - ly <= 2:
        return None

    xs = [i for i in range(lx+2,rx,2) if board[ly][i] == 0 and board[ry][i] == 0]
    ys = [i for i in range(ly+2,ry,2) if board[i][lx] == 0 and board[i][rx] == 0]
     

    if len(xs) == 0 or len(ys) == 0:
        return None

    x = choice(xs)
    y = choice(ys)

    for i in range(lx+1,rx):
        if board[y][i] == 1:
            board[y][i] = 0

    for i in range(ly+1,ry):
        if board[i][x] == 1:
            board[i][x] = 0

    holes = []
    hole_1_choice = [(y,i) for i in range(lx+1,x) if board[y][i] == 0]
    if len(hole_1_choice) > 0:
        holes.append(choice(hole_1_choice))
    
    hole_2_choice = [(y,i) for i in range(x+1,rx) if board[y][i] == 0]
    if len(hole_2_choice) > 0:
        holes.append(choice(hole_2_choice))

    hole_3_choice = [(i,x) for i in range(y+1,ry) if board[i][x] == 0]
    if len(hole_3_choice) > 0:
        holes.append(choice(hole_3_choice))

    hole_4_choice = [(i,x) for i in range(ly+1,y) if board[i][x] == 0]
    if len(hole_4_choice) > 0:
        holes.append(choice(hole_4_choice))


    holes = sample(holes,k=min(3,len(holes)))

    for hole in holes:
        i, j = hole
        board[i][j] = 1

    room_a = (lx, ly, x, y)
    room_b = (x, ly, rx, y)
    room_c = (lx, y, x, ry)
    room_d = (x, y, rx, ry)
    return (room_a, room_b, room_c, room_d)


if __name__ == "__main__":
    r = c = 99
    num_rooms = 30
    board = random_rooms(num_rooms, (r,c))
    # print(board)
    board = corridor(board)
    generate_colorful_image(board, (990,990))
    




