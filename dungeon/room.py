# -*- coding: utf-8 -*-
from queue import Queue
from random import randint, choice, choices
from collections import namedtuple

Position = namedtuple("Position", ["lx","ly","rx","ry"])

class Room():
    '''
    Sperate by space
    '''
    def __init__(self, size, room_number=20, min_room_space=(5,5)):
        width, height = size
        self.width = width - 1 + width%2
        self.height = height - 1 + height%2
        self.min_room_space = min_room_space
        self.room_number = room_number
        self._board = None

    @property
    def board(self):
        return self._board

    @property
    def rooms(self):
        return choices(self._generate_rooms(), k=self.room_number)
    
    def generate(self):
        board = [[0]*self.width for _ in range(self.height)]
        # room type
        for room in self.rooms:
            for i in range(room.lx, room.rx+1):
                board[room.ly][i] = 1
                board[room.ry][i] = 1
            for i in range(room.ly, room.ry+1):
                board[i][room.lx] = 1
                board[i][room.rx] = 1
            for i in range(room.ly+1, room.ry):
                for j in range(room.lx+1, room.rx):
                    board[i][j] = 2
        self._board = board

    def _generate_rooms(self):
        splitable = Queue()
        splitable.put(Position(1,1,self.width-2,self.height-2))
        unsplitable = Queue()
        while splitable.qsize() > 0:
            room = splitable.get()
            room_a, room_b = self._split_room(room)
            if room_a is None:
                unsplitable.put(room)
            else:
                splitable.put(room_a)
                splitable.put(room_b)
        return list(splitable.queue) + list(unsplitable.queue)

    def _split_room(self, room):
        
        room_h_a, room_h_b = self._split_room_horizon(room)
        room_v_a, room_v_b = self._split_room_vertical(room)

        if room_h_a is None and room_v_a is None:
            return None, None
        if room_h_a is None:
            return room_v_a, room_v_b
        if room_v_a is None:
            return room_h_a, room_h_b
        return choice([(room_h_a,room_h_b), (room_v_a,room_v_b)])

    def _split_room_horizon(self, room):
        m_x, m_y = self.min_room_space
        if room.ry - room.ly < 2 * m_y:
            return None, None
        sepline_y = randint(room.ly+m_y, room.ry-m_y)
        room_a = Position(room.lx, room.ly, room.rx, sepline_y)
        room_b = Position(room.lx, sepline_y, room.rx, room.ry)

        return room_a, room_b


    def _split_room_vertical(self, room):
        m_x, m_y = self.min_room_space
        if room.rx - room.lx < 2 * m_x:
            return None, None

        sepline_x = randint(room.lx+m_x, room.rx-m_x)
        room_a = Position(room.lx, room.ly, sepline_x, room.ry)
        room_b = Position(sepline_x, room.ly, room.rx, room.ry)
        return room_a, room_b

    def __str__(self):
        if self.board is None:
            return "Haven't generate room yet"
        return "\n".join("".join("." if i == 2 else " " for i in b) for b in self.board)

if __name__ == "__main__":
    room = Room((9,9))
    room.generate()
    print(room)

