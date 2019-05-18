import pygame,sys,os
from level import Level
import random
from utils import direction_to_rowcol


class Apple:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.current_pos = [self.row, self.col]
    

    def get_pos(self):
        return self.current_pos

    def get_row(self):
        return self.get_pos()[0]

    def get_col(self):
        return self.get_pos()[1]