import random

class RandomAgent:
    def __init__(self):
        pass
    
    
    def decide_move(self, grid):
        #  RandomAgent plays randomly
        rand_number = random.randint(0, 4)

        #  convert number to direction string
        decided_move = ""
        if (rand_number == 0):
            decided_move = "R"
        elif (rand_number == 1):
            decided_move = "U"
        elif (rand_number == 2):
            decided_move = "L"
        elif (rand_number == 3):
            decided_move = "D"
        elif (rand_number == 4):
            decided_move = "PASS"
        else:
            print("not today")
            exit(0)

        #print("RandomAgent decided ", decided_move)
        return decided_move

    def train(self):
        #  RandomAgent does not need any training
        pass