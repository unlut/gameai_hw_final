import numpy as np
import random
from tolNet import TolNet
from copy import deepcopy

class Individual():
    def __init__(self, input_size, output_size, use_crafted_features=True):
        self.input_size = input_size
        self.output_size = output_size

        #  create neural network
        self.network = TolNet()

        if (use_crafted_features):
            #  use a small network
            self.network.addLayer(in_size=input_size, out_size=9)
            self.network.addLayer(in_size=9, out_size=15)
            self.network.addLayer(in_size=15, out_size=output_size)
        else:
            self.network.addLayer(in_size=input_size, out_size=128)
            self.network.addLayer(in_size=128, out_size=256)
            self.network.addLayer(in_size=256, out_size=output_size)

        #  each Individual has a fitness value
        self.fitness_value = 0

        #  grid values to real numbers
        self.mapping = {'W': 0, 
                    'A': 0.2, 
                    'F': 0.4, 
                    'G': 0.6, 
                    'P': 0.8, 
                    'R': 1.0}

        self.max_ascii_value = max([ord(c) for c in self.mapping.keys()])
        self.min_ascii_value = min([ord(c) for c in self.mapping.keys()])
        self.ascii_difference = self.max_ascii_value - self.min_ascii_value
        #self.mapping = 

    def grid_to_network_input(self, grid):
        #  row count and column count of the grid
        rc = len(grid)
        cc = len(grid[0])
        #network_input = np.zeros((rc, cc))

    
        network_input = (np.array(grid).view(np.uint32)).astype(np.float32)
        network_input = (network_input - self.min_ascii_value)/ self.ascii_difference

        """
        #  convert letters to real numbers by using our predefined mapping
        for r in range(0, rc):
            for c in range(0, cc):
                network_input[r][c] = self.mapping[grid[r][c]]
        """

        #  flatten 2d array to 1d array
        network_input = network_input.flatten()


        return network_input

    def decide_move(self, network_input):
        #  ask network what it thinks about values of actions for given game state
        network_output = self.network.run(network_input)

        #  select action with largest value
        decided_move_index = np.argmax(network_output)

        #  convert number to direction string
        decided_move = ""
        if (decided_move_index == 0):
            decided_move = "R"
        elif (decided_move_index == 1):
            decided_move = "U"
        elif (decided_move_index == 2):
            decided_move = "L"
        elif (decided_move_index == 3):
            decided_move = "D"
        elif (decided_move_index == 4):
            decided_move = "PASS"
        else:
            print("not today")
            exit(0)

        #print("GeneticIndividual decided ", decided_move)
        return decided_move
    

    def save(self, filename):
        self.network.save(filename)
    
    def load(self, filename):
        self.network.load(filename)


class GeneticAgent():
    def __init__(self, population_size=30, selection_size=10, 
                       crossover_size=10, mutation_size=10, 
                       input_size=15*15, output_size=5,  #  input and output sizes of neural network
                       mutation_chance=0.05, 
                       mutation_max_magnitude=1e0,
                       mutation_min_magnitude=1e-3,
                       use_crafted_features=True):  
        self.population_size = population_size
        self.selection_size = selection_size
        self.crossover_size = crossover_size
        self.mutation_size = mutation_size

        if ((self.selection_size + self.crossover_size + self.mutation_size) != self.population_size):
            print("INVALID HYPERPARAMETERS !")
            print("Population size {} must be equal to sum of selection, crossover and mutation sizes")
            exit(0)

        self.input_size = input_size
        self.output_size = output_size
        self.use_crafted_features = use_crafted_features


        self.mutation_chance = mutation_chance
        self.mutation_max_magnitude = np.abs(mutation_max_magnitude)
        self.mutation_min_magnitude = np.abs(mutation_min_magnitude)
        
        #  initialize individuals
        self.individuals = [0] * self.population_size
        for i in range(self.population_size):
            self.individuals[i] = Individual(self.input_size, self.output_size, self.use_crafted_features)
        

        #  placeholder list, may be used in update
        self.next_individuals = []

        self.individuals_sorted = False

        self.current_replace_index = 0

        
    
    #  sorts individuals from largest fitness to smallest fitness
    def sort_individuals(self):
        self.individuals.sort(key=lambda b: b.fitness_value, reverse=True)
        self.individuals_sorted = True

    
    """
    Performs operations in below order:
    1- Selection
    2- Crossover
    3- Mutation
    """
    def update(self):
        #  sort individuals if they are not sorted
        if (not self.individuals_sorted):
            self.sort_individuals()


        #  THESE METHODS SHOULD ONLY BE CALLED WITHIN UPDATE !
        #DO NOT CALL EXPLICITY FROM ANYWHERE ELSE
        selected_individuals = self.selection()
        crossed_individuals = self.crossover()
        mutated_individuals = self.mutation(crossed_individuals)


        #  next generation is formed by selecteds + crosseds + mutateds
        self.individuals = selected_individuals + crossed_individuals + mutated_individuals
        

        if (len(self.individuals) != self.population_size):
            print("NUMBER OF INDIVIDUALS({}) MUST BE EQUAL TO POPULATION SIZE({}) !".format(len(self.individuals), self.population_size))
            exit(0)


        #  reset fitness values for next update cycle
        for individual in self.individuals:
            individual.fitness_value = 0

        #  mark individuals as not sorted for next iteration
        self.individuals_sorted = False




    """
        select self.selection_size amount of individuals for next generation
    next_individuals[0:self.selection_size] will be selected by this function
    
        Select N best individuals of the generation
    """
    def selection(self):
        selected_individuals = [0] * self.selection_size

        """
        Fill the list selected_individuals 
        """

        return selected_individuals





    """
        next_individuals[self.selection_size : self.selection_size+self.crossover_size] 
    will be selected by this function
    """
    def crossover(self):
        crossed_individuals = [0] * self.crossover_size
        
        """
        Fill the list crossed individuals
        """
        for i in range(self.crossover_size):
            pass


        return crossed_individuals





    """
        next_individuals[self.selection_size+self.crossover_size : self.population_size] 
    will be selected by this function

    You do not have to use crossed_individuals parameter if you don't want to
    """
    def mutation(self, crossed_individuals):
        mutated_individuals = [0] * self.mutation_size
        
        """
        Fill the list mutated_individuals
        
        
        Here is a step by step example
        
        #  create a new individual
        new_individual = Individual(self.input_size, self.output_size, self.use_crafted_features)
        
        #  get parameters of this new individual's neural network into a variable
        new_individual_params = new_individual.network.parameters()
        
        
        #  new_individual_params is a list of numpy array
        #it is a python list, and each element in the list is a numpy array
        #numbers in the ith element of the list are parameters of the network in ith layer
        
        
        #  this is how you iterate layers
        for layer_params in new_individual_params:
            num_layer_param = layer_params.shape[0]  #  number of parameters in current layer
        
        
        #  PERFORM MUTATION SOMEHOW 
        
        
        #  set parameters of newly created individual
        new_individual.network.update(new_individual_params)
        
        
        #  add newly created individual to list of mutated individuals
        mutated_individuals[i] = new_individual
        """
        
        
        for i in range(self.mutation_size):
            pass

        return mutated_individuals
        


    


    

