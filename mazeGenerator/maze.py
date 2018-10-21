# -*- coding: utf-8 -*-
from random import choice, sample
from pprint import pprint
from queue import Queue


class DFSMaze():
    '''
    Depth-first search
    '''
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

    def generate(self, board=None):
        if board is None:
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
                if len(route) > 0:
                    route.pop()
                if len(route) == 0:
                    break
                current_position = route[-1]
        if len(end_options):
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

    def __call__(self, *args):
        return self.generate(*args)


class RKAMaze():
    '''
    Randomized Kruskal's algorithm
    '''
    def __init__(self, size):
        self.row, self.column = size
        self._board = None

    @property
    def board(self):
        return self._board

    def generate(self):
        board = [[0]*self.column for _ in range(self.row)]
        r, c = choice([(i,j) for i in range(self.row) for j in range(self.column) if i%2 and j%2])
        board[r][c] = 1
        history = [(r,c)]
        while len(history)>0:
            r, c = choice(history)
            check = []
            if r + 2 < self.row and board[r+2][c] == 0:
                check.append((2,0))

            if c + 2 < self.column and board[r][c+2] == 0:
                check.append((0,2))

            if r - 2 >= 0 and board[r-2][c] == 0:
                check.append((-2,0))

            if c - 2 >= 0 and board[r][c-2] == 0:
                check.append((0,-2))

            if len(check) > 0:
                i, j = choice(check)
                board[r+i//2][c+j//2] = 1
                board[r+i][c+j] = 1
                history.append((r+i,c+j))
            else:
                history.remove((r,c))

        self._board = board


class RDMaze():
    '''
    Recursive division method
    '''
    def __init__(self, size):
        self.row, self.column = size
        self._board = None

    @property
    def board(self):
        return self._board

    def generate(self):
        self._board = [[0 if (i*j) == 0 or i == self.row-1 or j == self.column-1 else 1
                        for j in range(self.column)] 
                        for i in range(self.row)]
        splitable = Queue()
        splitable.put((0, 0, self.column-1, self.row-1))
        while splitable.qsize() > 0:
            room = splitable.get()
            subrooms = self._split_room(room)
            if subrooms is None:
                continue
            for subroom in subrooms:
                splitable.put(subroom)


    def _split_room(self, room):
        lx, ly, rx, ry = room
        if rx - lx <= 2 or ry - ly <= 2:
            return None

        xs = [i for i in range(lx+2,rx,2) if self._board[ly][i] == 0 and self._board[ry][i] == 0]
        ys = [i for i in range(ly+2,ry,2) if self._board[i][lx] == 0 and self._board[i][rx] == 0]
        
        if len(xs) == 0 or len(ys) == 0:
            return None

        x = choice(xs)
        y = choice(ys)

        print(x, y)

        for i in range(lx+1,rx):
            self._board[y][i] = 0

        for i in range(ly+1,ry):
            self._board[i][x] = 0

        hole_1 = choice([(y,i) for i in range(lx+1,x)])
        hole_2 = choice([(y,i) for i in range(x+1,rx)])
        hole_3 = choice([(i,x) for i in range(y+1,ry)])
        hole_4 = choice([(i,x) for i in range(ly+1,y)])


        holes = sample([hole_1,hole_2,hole_3,hole_4],k=3)

        for hole in holes:
            i, j = hole
            self._board[i][j] = 1

        room_a = (lx, ly, x, y)
        room_b = (x, ly, rx, y)
        room_c = (lx, y, x, ry)
        room_d = (x, y, rx, ry)
        return (room_a, room_b, room_c, room_d)

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    from helper.helper import generate_image
    maze = RDMaze((35,35))
    maze.generate()
    generate_image(maze.board,(350,350))




