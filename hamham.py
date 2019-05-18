import time
import sys
import os


import pygame

#  import game object classes
from level import Level
from player import Player
from robot import Robot
from apple import Apple

#  import constant definitions
from macros import *


#  for mathematical operations
import numpy as np


class Game:
    def __init__(self, game_window_name="Hamham"):
        #  initialize pygame stuff
        pygame.display.init()
        pygame.mixer.init()
        pygame.display.set_caption(game_window_name)
        self.screen = pygame.display.set_mode(game_window_size)
        self.clock = pygame.time.Clock()
        
        #wall_width = self.wall.get_width()
        wall_width = 36

		# Load images
        self.wall = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/wall.png').convert(), (wall_width, wall_width))
        
        self.apple = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/apple_bg.png').convert(), (wall_width, wall_width))
        self.floor = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/floor.png').convert(), (wall_width, wall_width))
        self.grass = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/grass.png').convert(), (wall_width, wall_width))
        
        self.player_right = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/pacman_bg.png').convert(), (wall_width, wall_width))
        self.player_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/pacman_bg.png').convert(), (wall_width, wall_width)), 90.0)
        self.player_left = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/pacman_bg.png').convert(), (wall_width, wall_width)), True, False)
        self.player_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/pacman_bg.png').convert(), (wall_width, wall_width)), -90.0)
        self.player_image = self.player_right
        self.player_images = [self.player_right, self.player_up, self.player_left, self.player_down]

        self.robot = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/robot_bg.png').convert(), (wall_width, wall_width))


        #  load sounds
        self.win_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '/sounds/tada.wav')
        self.lose_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '/sounds/fail_trombone_4s.wav')

		# Dictionary to map images to characters in level matrix
        self.images = {'W': self.wall, 
                    'A': self.apple, 
                    'F': self.floor, 
                    'G': self.grass, 
                    'P': self.player_image, 
                    'R': self.robot}

        self.current_level = None
        self.current_level_number = 0

		#  player object
        self.player = None

		#  robots
        self.robots = []

        self.game_finished = False
        self.player_alive = True

        """
        Current level statistics
        """
        #  number of apples player collected so far in curret level
        self.collected_apple_count = 0

        #  number of all apples in the initial level configuration
        self.total_apple_count = 0

        #  number of time steps elapsed in a level
        self.elapsed_time_step = 0

        #  
        self.distance_to_closest_apple = 0

        self.crashed_into_wall = False

    def draw_level(self, level_matrix):
        # Get image size to print on screen
        box_size = self.wall.get_width()

        # Print images for matrix
        for i in range(0, len(level_matrix)):
            for c in range(0, len(level_matrix[i])):
                self.screen.blit(self.images[level_matrix[i][c]], (c * box_size, i * box_size))
        pygame.display.update()

    def init_level(self, level):
        self.current_level = Level(level)
        #self.draw_level(self.current_level.get_matrix())

        #  mark game as not finished
        self.game_finished = False
        self.player_alive = True

        #  number of time steps elapsed in a level
        self.elapsed_time_step = 0

        #  initialize number of apples player collected so far in curret level
        self.collected_apple_count = 0
		

        #  create player object
        player_pos = self.current_level.get_player_pos()
        player_current_row = player_pos[0]
        player_current_col = player_pos[1]
        self.player = Player(player_current_row, player_current_col)

        #  create robots
        self.robots = []
        robot_positions = self.current_level.get_robot_positions()
        for pos in robot_positions:
            r = pos[0]
            c = pos[1]
            self.robots.append(Robot(r, c, self.current_level.get_matrix()))

        #  create apples
        self.apples = []
        apple_positions = self.current_level.get_apple_positions()
        for pos in apple_positions:
            r = pos[0]
            c = pos[1]
            self.apples.append(Apple(r, c))
        
        #  count number of apples
        self.total_apple_count = len(self.apples)
        #print("Number of apples in the level ", self.total_apple_count)


        #  whether played tried to move into wall at last step
        self.crashed_into_wall = False
        


    

    """
    Calculates distance between player and the closest apple to player
    """
    def get_closest_apple_to_player(self):
        player_pos = self.player.get_pos()
        pr = player_pos[0]
        pc = player_pos[1]

        minDist = 1000
        closestApple = None
        for apple in self.apples:
            apple_pos = apple.get_pos()
            rr = apple_pos[0]
            rc = apple_pos[1]
            dist = np.abs(pr - rr) + np.abs(pc - rc)
            if (dist < minDist):
                minDist = dist
                closestApple = apple
        
        return (closestApple, minDist)


    def step(self, player_direction, render=True):
        matrix = self.current_level.get_matrix()
        self.current_level.save_history(matrix)

        #Print apples
        #print(self.current_level.get_apple_positions())

        #  robots movement
        for robot in self.robots:
            #robot_old_pos = robot.get_pos()
            #robot_old_row = robot_old_pos[0]
            #robot_old_col = robot_old_pos[1]

            robot_dir = robot.choose_dir()
            robot_new_pos = robot.move(robot_dir)
            robot_next_row = robot_new_pos[0]
            robot_next_col = robot_new_pos[1]
       

		#  save old position of the player
        player_current_pos = self.player.get_pos()
        player_current_row = player_current_pos[0]
        player_current_col = player_current_pos[1]

		#  calculate new position of the player
        player_next_pos = self.player.move(player_direction)
        player_next_row = player_next_pos[0]
        player_next_col = player_next_pos[1]


        #  resolve static collision for robots
        for robot in self.robots:
            robot_prev_pos = robot.get_prev_pos()
            robot_prev_row = robot_prev_pos[0]
            robot_prev_col = robot_prev_pos[1]

            robot_next_pos = robot.get_pos()
            robot_next_row = robot_next_pos[0]
            robot_next_col = robot_next_pos[1]

            next_cell = matrix[robot_next_row][robot_next_col]
            if next_cell == "F":
                #  next cell is floor
                pass
            elif ((next_cell == "G")
                  or (next_cell == "W")
                  or (next_cell == "A")):
                #  next cell is grass or wall or apple
                #robot cant pass here
                robot.current_pos = robot_prev_pos
            elif (next_cell == "R"):
                #  go into another robot
                pass
            elif (next_cell == "P"):
                #  will resolve later
                pass
        
        

        #  resolve static collisions for player
        next_cell = matrix[player_next_row][player_next_col]
        if (next_cell == "F"):
            #  next cell is floor
            pass
        elif (next_cell == "W"):
            #  next cell is wall
            #player cant pass here
            self.player.current_pos = self.player.prev_pos
            self.crashed_into_wall = True
        elif (next_cell == "G"):
            #  next cell is grass
            #player removes grass
            matrix[player_next_row][player_next_col] = "P"
        elif (next_cell == 'A'):
            #  next cell is apple
            #player removes apple
            matrix[player_next_row][player_next_col] = "P"
        elif (next_cell == "R"):
            #  next square is robot
            #will resolve later
            pass
        
        #  check if player collected an apple
        #  TO DO: create a 2d apple grid for faster check
        new_apples = []
        for apple in self.apples:
            apple_pos = apple.get_pos()
            apple_row = apple_pos[0]
            apple_col = apple_pos[1]
            if (player_next_row == apple_row and player_next_col == apple_col):
                #player removes apple
                #  check if game is finished
                self.collected_apple_count += 1
                if (self.collected_apple_count == self.total_apple_count):
                    self.game_finished = True
            else:
                new_apples.append(apple)
        self.apples = new_apples

            

        player_next_row = self.player.current_pos[0]
        player_next_col = self.player.current_pos[1]


        #  resolve dynamic player-robot collisions
        for robot in self.robots:
            robot_prev_pos = robot.get_prev_pos()
            robot_prev_row = robot_prev_pos[0]
            robot_prev_col = robot_prev_pos[1]

            robot_next_pos = robot.get_pos()
            robot_next_row = robot_next_pos[0]
            robot_next_col = robot_next_pos[1]

            #  CASE 1
            #player and robot moves into same cell
            if (robot_next_row == player_next_row and robot_next_col == player_next_col):
                #print("CASE 1: Player and robot {} moved into same cell!".format(robot.get_id()))
                self.player_alive = False
                self.game_finished = True
            
            #  CASE 2
            #player in cell C1, robot in cell C2
            #player moves from C1 to C2
            #robot moves from C3 to C4
            #C1 == C4 AND C2 == C3
            if (player_current_pos == robot_next_pos and player_next_pos == robot_prev_pos):
                #print("CASE 2: Player and robot {} passed by!".format(robot.get_id()))
                self.player_alive = False
                self.game_finished = True


        #  update game matrix
        level_matrix = self.current_level.get_matrix()
        for robot in self.robots:
            robot_old_pos = robot.get_prev_pos()
            robot_old_row = robot_old_pos[0]
            robot_old_col = robot_old_pos[1]
            robot_new_pos = robot.get_pos()
            robot_next_row = robot_new_pos[0]
            robot_next_col = robot_new_pos[1]

            level_matrix[robot_old_row][robot_old_col] = "F"
            level_matrix[robot_next_row][robot_next_col] = "R"
        player_prev_row = self.player.get_prev_row()
        player_prev_col = self.player.get_prev_col()
        player_next_row = self.player.get_row()
        player_next_col = self.player.get_col()

        #  if there is not a robot in the previous cell of player, clear it
        if (level_matrix[player_prev_row][player_prev_col] != "R"):
            level_matrix[player_prev_row][player_prev_col] = "F"
        level_matrix[player_next_row][player_next_col] = "P"

        #  draw
        if (render):
            self.images["P"] = self.player_images[self.player.current_facing_index]
            self.draw_level(matrix)


        self.elapsed_time_step += 1

        #remaining_apple_count = len(self.current_level.get_apple_positions())
        #print("Number of remaining apples: ", remaining_apple_count)

        #  check if game is finished
        if (self.game_finished):
            if (self.player_alive):
                #  player collected all apples
                #print("Level completed!")
                return RESULT_PLAYER_WON
            else:
                #  player is dead
                #print("Player is killed by the robot!")
                return RESULT_PLAYER_DEAD
        else:
            return RESULT_GAME_CONTINUE


    #  function when a human player plays the game
    def start_level_human(self, level_index):
        self.init_level(level_index)
        self.draw_level(self.current_level.get_matrix())


		#  number of all apples in the initial level configuration
        self.total_apple_count = len(self.apples)
        
        #  at each time step, distance of player to the closest apple
        apple_distance_rewards = []
        
        #  negative reward if crash into wall
        wall_crash_penalties = []

        self.distance_to_closest_apple = self.get_closest_apple_to_player()[1]

        #  game loop
        while True:
            result = 0

            #  manual input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #self.craft_features()

                    if event.key == pygame.K_RIGHT:
                        result = self.step("R", render=True)
                    elif event.key == pygame.K_UP:
                        result = self.step("U", render=True)
                    elif event.key == pygame.K_LEFT:
                        result = self.step("L", render=True)
                    elif event.key == pygame.K_DOWN:
                        result = self.step("D", render=True)
                    elif event.key == pygame.K_SPACE:
                        result = self.step("PASS", render=True)
                    #elif event.key == pygame.K_u:
                    #    self.draw_level(self.current_level.undo())
                    elif event.key == pygame.K_r:
                        self.init_level(self.current_level_number)
                        result = RESULT_GAME_CONTINUE
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    
                    
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if (result == RESULT_PLAYER_WON or result == RESULT_PLAYER_DEAD):
                sound_channel = None
                if (result == RESULT_PLAYER_WON):
                    #print("WON")
                    sound_channel = self.win_sound.play()
                else:
                    #print("LOSE")
                    sound_channel = self.lose_sound.play()

                #  wait for sound to end
                while sound_channel.get_busy() == True:
                    continue
                break
            else:
                #  
                new_closest_apple_dist = self.get_closest_apple_to_player()[1]
                if (new_closest_apple_dist > self.distance_to_closest_apple):
                    apple_distance_rewards.append(MOVING_AWAY_FROM_APPLE)
                elif (new_closest_apple_dist < self.distance_to_closest_apple):
                    apple_distance_rewards.append(GETTING_CLOSER_TO_APPLE_REWARD)
                self.distance_to_closest_apple = new_closest_apple_dist
            
                if (self.crashed_into_wall):
                    self.crashed_into_wall = False
                    wall_crash_penalties.append(WALL_CRASH_PENALTY)
    

        #  if killed by robot, give penalty
        robot_death_penalty = 0
        if (result == RESULT_PLAYER_DEAD):
            robot_death_penalty = ROBOT_DEATH_PENALTY

        #  return a tuple of
        #(number of collected apples, elapsed time step)
        return (self.collected_apple_count, apple_distance_rewards, wall_crash_penalties,
                self.elapsed_time_step, robot_death_penalty)



    """
    R T L U blocked (4)
    R T L U contains a robot or is adjacent to a robot (4)
    closest apple vector components (2)

    returns a feature vector containing above 10 features
    """
    def craft_features(self):
        player_pos = self.player.get_pos()
        pr = player_pos[0]
        pc = player_pos[1]
        matrix = self.current_level.get_matrix()

        #  features showing whether 4 cardinal direction cells blocked or not 
        checked_cell = matrix[pr][pc+1]
        right_blocked = int( (checked_cell == "W") )
        checked_cell = matrix[pr-1][pc]
        up_blocked = int( (checked_cell == "W") )
        checked_cell = matrix[pr][pc-1]
        left_blocked = int( (checked_cell == "W") )
        checked_cell = matrix[pr+1][pc]
        down_blocked = int( (checked_cell == "W") )
        

        #  features showing whether 4 cardinal direction cells contains robot danger or not
        drs = [0, -1, 0, 1]
        dcs = [1, 0, -1, 0]
        matrix_height = len(matrix)
        matrix_width = len(matrix[0])
        robot_vector = np.zeros(4)
        for c in range(4):
            #  calculate cth adjacent cell
            adj_cell_row = pr + drs[c]
            adj_cell_col = pc + dcs[c]

            #  check if there is a robot in the cell
            if (matrix[adj_cell_row][adj_cell_col] == "R"):
                robot_vector[c] = 1.0
                continue
            
            #  check if there is a robot danger in the cell
            for dr in drs:
                for dc in dcs:
                    if (adj_cell_row + dr >= 0 and adj_cell_row + dr < matrix_height
                        and adj_cell_col + dc >= 0 and adj_cell_col + dc < matrix_width
                        and matrix[adj_cell_row + dr][adj_cell_col + dc] == "R"):
                        robot_vector[c] = 1.0
                        break


        #right_robot = int( (checked_cell == "R") )
        #up_robot = int( (checked_cell == "R") )
        #left_robot = int( (checked_cell == "R") )
        #down_robot = int( (checked_cell == "R") )


        #  
        blocked_vector = np.array([right_blocked, up_blocked, left_blocked, down_blocked])
        #robot_vector = np.array([right_robot, up_robot, left_robot, down_robot])

        #  calculate vector that shows the apple direction
        closest_apple = self.get_closest_apple_to_player()[0]
        closest_apple_pos = closest_apple.get_pos()
        closest_apple_row = closest_apple_pos[0]
        closest_apple_col = closest_apple_pos[1]
        closest_apple_vector = np.array([closest_apple_row - pr, closest_apple_col - pc])

        #  normalize direction vector
        closest_apple_vector_norm = np.linalg.norm(closest_apple_vector)
        if (closest_apple_vector_norm == 0):
            closest_apple_vector_norm = len(matrix)
        closest_apple_vector = closest_apple_vector / closest_apple_vector_norm

        #  obtain feature vector by merging blocked and direction vectors
        feature_vector = np.concatenate([blocked_vector, robot_vector, closest_apple_vector])

        #print("--- MATRIX ---")
        #print(matrix)
        #print("--- FEATURES ---")
        #print(feature_vector)

        #  return feature vector
        return feature_vector

    def start_level_computer(self, level_index, agent, 
                             render=False, play_sound=False,
                             max_episode_length=150,
                             use_crafted_features=True,
                             test=False):
        self.init_level(level_index)

        if (render):
            self.draw_level(self.current_level.get_matrix())


		#  number of all apples in the initial level configuration
        self.total_apple_count = len(self.apples)
        
        #  at each time step, distance of player to the closest apple
        apple_distance_rewards = []
        
        #  negative reward if crash into wall
        wall_crash_penalties = []

        self.distance_to_closest_apple = self.get_closest_apple_to_player()[1]
    
        while True:
            result = 0

            #  input source will use matrix to decide
            matrix = self.current_level.get_matrix()

            network_input = None
            if (use_crafted_features):
                network_input = self.craft_features()
            else:
                #  convert grid to network input
                network_input = agent.grid_to_network_input(matrix)
            chosen_action = agent.decide_move(network_input)

            #  apply decided action
            result = self.step(chosen_action, render=render)

            #  if we want to render our agent, wait some time 
            if (render):
                self.clock.tick(FPS)

            #  check if game finished
            if (result == RESULT_PLAYER_WON or result == RESULT_PLAYER_DEAD):
                if (play_sound):
                    sound_channel = None
                    if (result == RESULT_PLAYER_WON):
                        sound_channel = self.win_sound.play()
                    else:
                        sound_channel = self.lose_sound.play()

                    #  wait for sound to end
                    while sound_channel.get_busy() == True:
                        continue
                break
            else:
                #  
                new_closest_apple_dist = self.get_closest_apple_to_player()[1]
                if (new_closest_apple_dist > self.distance_to_closest_apple):
                    apple_distance_rewards.append(MOVING_AWAY_FROM_APPLE)
                elif (new_closest_apple_dist < self.distance_to_closest_apple):
                    apple_distance_rewards.append(GETTING_CLOSER_TO_APPLE_REWARD)
                self.distance_to_closest_apple = new_closest_apple_dist
            
                if (self.crashed_into_wall):
                    self.crashed_into_wall = False
                    wall_crash_penalties.append(WALL_CRASH_PENALTY)
            
            #  check if we reached episode length
            if (self.elapsed_time_step >= max_episode_length):
                break
        

        #  if killed by robot, give penalty
        robot_death_penalty = 0
        if (result == RESULT_PLAYER_DEAD):
            robot_death_penalty = ROBOT_DEATH_PENALTY

        #  return a tuple of
        #(number of collected apples, elapsed time step)
        return (self.collected_apple_count, apple_distance_rewards, wall_crash_penalties,
                self.elapsed_time_step, robot_death_penalty)
    
