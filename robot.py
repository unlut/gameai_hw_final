import pygame,sys,os
from level import Level
import random
from utils import direction_to_rowcol

class Robot:

    instance_counter = 0


    def __init__(self, row, col, level_matrix):
        self.row = row
        self.col = col

        self.prev_pos = [self.row, self.col]
        self.current_pos = [self.row, self.col]
        #self.next_pos = [self.row, self.col]

        #  direction robot choose last time
        self.last_dir = ""


        self.possible_directions = ["R", "U", "L", "D"]


        #  save matrix
        self.level_matrix = level_matrix


        self.RANDOM_WALK_EPSILON = 0#0.15

        self.robot_id = Robot.instance_counter
        Robot.instance_counter += 1


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
    
    def get_id(self):
        return self.robot_id
    
    def choose_dir(self):
        chosen_dir = ""
        if ((self.last_dir == None) or 
            (len(self.last_dir)==0)):
            #  last_dir is empty, choose a random direction
            rand_dir = random.randint(0, 3)
            chosen_dir = self.possible_directions[rand_dir]
        else:
            #  get a random number between 0 and 1
            rand_number = random.uniform(0, 1)

            if (rand_number <= self.RANDOM_WALK_EPSILON):
                #  random dir
                rand_dir = random.randint(0, 3)
                chosen_dir = self.possible_directions[rand_dir]
            else:
                #  check if wall ahead
                robot_row = self.current_pos[0]
                robot_col = self.current_pos[1]
                i, j, f = direction_to_rowcol(self.last_dir)
                cell_ahead = self.level_matrix[robot_row+i][robot_col+j]
                if ((cell_ahead == "W")
                    or (cell_ahead == "G")
                    or (cell_ahead == "A")):
                    #  wall/grass ahead, select a random direction
                    rand_dir = random.randint(0, 3)
                    chosen_dir = self.possible_directions[rand_dir]
                else:
                    #  continue in your last direction
                    chosen_dir = self.last_dir
            
        return chosen_dir


    def move(self, direction):
        i, j, facing = direction_to_rowcol(direction) 

        current_row = self.get_pos()[0]
        current_col = self.get_pos()[1]
        
        self.prev_pos = self.current_pos
        self.current_pos = [current_row+i, current_col+j]

        self.last_dir = direction
        return self.current_pos
    