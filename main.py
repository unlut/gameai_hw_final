import time
import sys
import os


#  import constant definitions
from macros import *

#  import agent classes
from random_agent import RandomAgent
from genetic_agent import GeneticAgent, Individual

#  for mathematical operations
import numpy as np

#  for saving our agents
import pickle

#  import game class
from hamham import Game




""" 
YOU ARE NOT ALLOWED TO CHANGE THESE TWO PARAMETERS 
"""
REQUIRED_INDIVIDUAL_COUNT = 3
REQUIRED_SCORE_THRESHOLD = 60











#  Initialize game
hamham = Game()



#First command line argument is player_string
player_string = ""
if (len(sys.argv) >= 2):
    player_string = sys.argv[1]
else:
    #  no argument is provided, assign player_string hardcodedly

    #player_string = "HUMAN"
    #player_string = "RANDOM"
    player_string = "GENETIC"
    #player_string = "GENETIC_TEST"



#Second command line argument is played level
PLAYED_LEVEL = 1
if (len(sys.argv) >= 3):
    PLAYED_LEVEL = int(sys.argv[2])
else:
    PLAYED_LEVEL = 1



#  display player and played level
print("Player {} will be playing level {}".format(player_string, PLAYED_LEVEL))















""" 

GENETIC ALGORITHM HYPERPARAMETERS START

"""
#  number of individuals in population
POPULATION_SIZE = 60

#  number of individuals we will obtain in individual phases
#!!! sum of them must be equal to POPULATION_SIZE !!!
SELECTION_SIZE = 12
CROSSOVER_SIZE = 24
MUTATION_SIZE = 24


MUTATION_CHANCE = 1.0 #0.05
MUTATION_MAX_MAGNITUDE = 1e-1
MUTATION_MIN_MAGNITUDE = 1e-3


MAX_EPISODE_LENGTH = 300

""" 

GENETIC ALGORITHM HYPERPARAMETERS END

"""



USE_CRAFTED_FEATURES = True  #  keep it True for your sanity

input_size, output_size = 0, 0
if (USE_CRAFTED_FEATURES):
    #  number of crafted features
    input_size = 10

    #  output_size = Number of possible actions
    output_size = 4
else:
    #  input_size = (width of game area)*(height of game area)
    input_size = 15*15

    #  output_size = Number of possible actions
    output_size = 4




if (player_string == "HUMAN"):
    (collected_apple_count, apple_distance_rewards, wall_crash_penalties, elapsed_time_step, robot_death_penalty) = hamham.start_level_human(PLAYED_LEVEL)
    printed_str = "--- Player Statistics ---\n"
    printed_str += "collected apple count:{}\n".format(collected_apple_count)
    printed_str += "total apple distance reward:{}\n".format(np.sum(apple_distance_rewards))
    printed_str += "total wall crash penalty:{}\n".format(np.sum(wall_crash_penalties))
    printed_str += "robot death penalty:{}\n".format(robot_death_penalty)
    printed_str += "total reward:{}\n".format(collected_apple_count*COLLECT_APPLE_REWARD + np.sum(apple_distance_rewards) + np.sum(wall_crash_penalties) + robot_death_penalty)
    printed_str += "elapsed time step:{}\n".format(elapsed_time_step)
    print(printed_str)

elif (player_string == "RANDOM"):
    agent = RandomAgent()
    (collected_apple_count, apple_distance_rewards, wall_crash_penalties, elapsed_time_step, robot_death_penalty) = hamham.start_level_computer(PLAYED_LEVEL, agent, render=False)
    print("Collected apple count:", collected_apple_count)
    print("Elapsed time step:", elapsed_time_step)	

elif (player_string == "GENETIC"):
    

    #  initialize our GeneticAgent with specified hyperparameters
    genetic_agent = GeneticAgent(population_size=POPULATION_SIZE,
                            selection_size=SELECTION_SIZE,
                            crossover_size=CROSSOVER_SIZE,
                            mutation_size=MUTATION_SIZE, 
                            input_size=input_size, 
                            output_size=output_size,
                            mutation_chance=MUTATION_CHANCE,
                            mutation_max_magnitude=MUTATION_MAX_MAGNITUDE,
                            mutation_min_magnitude=MUTATION_MIN_MAGNITUDE,
                            use_crafted_features=USE_CRAFTED_FEATURES)
    
    #  we will play until we collect all apples
    finished = False
    iteration_counter = 0
    
    while (not finished):
        #  save collected apple counts for statistics
        collected_apple_counts = np.zeros(POPULATION_SIZE)

        #  make each individual play a game
        for (index, individual) in enumerate(genetic_agent.individuals):
            (collected_apple_count, apple_distance_rewards, wall_crash_penalties, elapsed_time_step, robot_death_penalty) = hamham.start_level_computer(PLAYED_LEVEL, individual, 
                                                                                    render=False, play_sound=False,
                                                                                    max_episode_length=MAX_EPISODE_LENGTH,
                                                                                    use_crafted_features=USE_CRAFTED_FEATURES)

            #  use collected apple count and robot penalty as fitness value
            individual.fitness_value = collected_apple_count * COLLECT_APPLE_REWARD
            individual.fitness_value += robot_death_penalty

            #  add distance rewards
            individual.fitness_value += np.sum(apple_distance_rewards)

            #  add wall crashes
            individual.fitness_value += np.sum(wall_crash_penalties)



           
        #  sort individuals by fitness values
        genetic_agent.sort_individuals()
        
        #  check if enough individuals with best fitness played good enough
        best_individuals = [genetic_agent.individuals[i] for i in range(REQUIRED_INDIVIDUAL_COUNT)]
        best_fitness_values = [individual.fitness_value for individual in best_individuals]
        print("Iteration {} - Best fitness values {}".format(iteration_counter, best_fitness_values))
        
            
        
        #  watch best individual
        (collected_apple_count, apple_distance_rewards, wall_crash_penalties, elapsed_time_step, robot_death_penalty) = hamham.start_level_computer(PLAYED_LEVEL, genetic_agent.individuals[0], 
                                                                                render=False, play_sound=False,
                                                                                max_episode_length=MAX_EPISODE_LENGTH,
                                                                                use_crafted_features=USE_CRAFTED_FEATURES,
                                                                                test=True)
        test_total_reward = collected_apple_count*COLLECT_APPLE_REWARD + np.sum(apple_distance_rewards) + np.sum(wall_crash_penalties) + robot_death_penalty
        print("Testing best agent of iteration {}, elapsed time step:{}, reward:{}".format(iteration_counter, elapsed_time_step, test_total_reward))


        #  check if the training is finished
        if np.sum(best_fitness_values) >= REQUIRED_SCORE_THRESHOLD*REQUIRED_INDIVIDUAL_COUNT:
            print("DONE!")
            finished = True

            #  save best REQUIRED_INDIVIDUAL_COUNT agents
            for (j, best_individual) in enumerate(best_individuals):
                best_individual.save("level_{}_best_individual_{}.weights".format(PLAYED_LEVEL, j))
        else:
            #  not finished, update individuals
            genetic_agent.update()

        iteration_counter += 1
elif (player_string == "GENETIC_TEST"):
    best_individuals = [0] * REQUIRED_INDIVIDUAL_COUNT
    for j in range(REQUIRED_INDIVIDUAL_COUNT):
        best_individuals[j] = Individual(input_size, output_size, USE_CRAFTED_FEATURES)
        best_individuals[j].load("level_{}_best_individual_{}.weights".format(PLAYED_LEVEL, j))
        print("Watching individual {}".format(j))
        (collected_apple_count, apple_distance_rewards, wall_crash_penalties, elapsed_time_step, robot_death_penalty) = hamham.start_level_computer(PLAYED_LEVEL, best_individuals[j], 
                                                                                render=True, play_sound=False,
                                                                                max_episode_length=MAX_EPISODE_LENGTH,
                                                                                use_crafted_features=USE_CRAFTED_FEATURES,
                                                                                test=True)
        printed_str = "--- Tested Agent {} Statistics ---\n".format(j)
        printed_str += "collected apple count:{}\n".format(collected_apple_count)
        printed_str += "total apple distance reward:{}\n".format(np.sum(apple_distance_rewards))
        printed_str += "total wall crash penalty:{}\n".format(np.sum(wall_crash_penalties))
        printed_str += "robot death penalty:{}\n".format(robot_death_penalty)
        printed_str += "total reward:{}\n".format(collected_apple_count*COLLECT_APPLE_REWARD + np.sum(apple_distance_rewards) + np.sum(wall_crash_penalties) + robot_death_penalty)
        printed_str += "elapsed time step:{}\n".format(elapsed_time_step)
        print(printed_str)

