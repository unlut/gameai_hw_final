import pygame,sys,os
from level import Level
from utils import direction_to_rowcol

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.prev_pos = [self.row, self.col]
        self.current_pos = [self.row, self.col]
        #self.next_pos = [self.row, self.col]

        
        self.possible_facings = ["R", "U", "L", "D"]
        self.current_facing_index = 0

    def get_pos(self):
        return self.current_pos

    def get_row(self):
        return self.get_pos()[0]

    def get_col(self):
        return self.get_pos()[1]
    
    def get_prev_pos(self):
        return self.prev_pos
    
    def get_prev_row(self):
        return self.get_prev_pos()[0]
    
    def get_prev_col(self):
        return self.get_prev_pos()[1]

    def move(self, direction):
        if (direction == "PASS"):
            i, j, self.current_facing_index = 0, 0, self.current_facing_index
        else:
            i, j, self.current_facing_index = direction_to_rowcol(direction)
        
        self.prev_pos = self.current_pos
        self.current_pos = [self.current_pos[0]+i, self.current_pos[1]+j]
        return self.current_pos
