# -*- coding: utf-8 -*-
from random import choice


class Maze():
    def __init__(self, size):
        width, height = size
        self.width = width - 1 + width%2
        self.height = height - 1 + height%2
        self.directions = [(2,0),(-2,0),(0,2),(0,-2)]
        self._board = None
        self._start_point = None
        self._end_point = None

    @property
    def board(self):
        return self._board

    @property
    def start_point(self):
        return self._start_point

    @property
    def end_point(self):
        return self._end_point

    def generate(self):
        board = self._init_board()
        current_position = choice(self._start_options())
        self._start_point = current_position
        i, j = current_position
        board[i][j] = 2
        route = []
        end_options = []
        while True:
            available_direction = self._avaliable_directions(board, current_position)
            if len(available_direction) > 0:
                i, j = choice(available_direction)
                r, c = current_position
                board[r + i//2][c + j//2] = 2
                board[r + i][c + j] = 2
                current_position = (r + i, c + j)
                route += [current_position]
            else:
                r, c = current_position
                eage_point = r == 1 or r == self.height-2 or c == 1 or c == self.width-2
                if self._valid_end(board,(r,c)) and eage_point:
                    end_options += [current_position]
                route.pop()
                if len(route) == 0:
                    break
                current_position = route[-1]
        self._end_point = choice(end_options)
        self._board = board

    def _init_board(self):
        return [[1 if i%2 and j%2 else 0 
                 for j in range(self.width)] 
                 for i in range(self.height)]

    def _start_options(self):
        starts = [(1,i) for i in range(self.width) if i%2] 
        starts += [(self.height-2,i) for i in range(self.width) if i%2]
        starts += [(i,1) for i in range(self.height) if i%2]
        starts += [(i,self.width-2) for i in range(self.height) if i%2]
        return starts

    def _avaliable_directions(self, board, position):
        available_directions = []
        for i, j in self.directions:
            r = position[0] + i
            c = position[1] + j
            if 0 <= r < self.height and 0 <= c < self.width and board[r][c] == 1:
                available_directions += [(i, j)]
        return available_directions

    def _valid_end(self, board, point):
        r, c = point
        s = 0
        directions = ((1,0),(-1,0),(0,-1),(0,1))
        for i, j in directions:
            if 0 <= i+r < self.height and 0 <= j+c < self.width and board[i+r][j+c] == 0:
                s += 1
        return s >= 3

    def __str__(self):
        if self.board is None:
            return "Haven't generate maze yet"
        return "\n".join("".join("." if i == 2 else " " for i in b) for b in self.board)

    def __call__(self):
        return self.generate()



