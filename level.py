import os,copy


class Level:
    matrix = []
    hist_matrix = []

    def __init__(self, level_num):

        del self.matrix[:]
        del self.hist_matrix[:]

        # Create level
        with open(os.path.dirname(os.path.abspath(__file__)) + '/Levels/level' + str(level_num), 'r') as dosya:
            for row in dosya.read().splitlines():
                letters = row.strip().split("\t")
                self.matrix.append(list(letters))

    def get_matrix(self):
        return self.matrix

    def save_history(self, matrix):
        pass#self.hist_matrix.append(copy.deepcopy(matrix))

    def undo(self):
        if len(self.hist_matrix) > 0:
            last_matrix = self.hist_matrix.pop()
            self.matrix = last_matrix
            return last_matrix
        else:
            return self.matrix

    def get_player_pos(self):
        # Iterate all Rows
        for r in range(0, len(self.matrix)):
            # Iterate all columns
            for c in range(0, len(self.matrix[r])):
                if self.matrix[r][c] == "P":
                    return [r, c]

    def get_apple_positions(self):
        apples = []
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.matrix[r])):
                if self.matrix[r][c] == "A":
                    apples.append([r, c])
        return apples
    
    def get_robot_positions(self):
        robots = []
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.matrix[r])):
                if self.matrix[r][c] == "R":
                    robots.append([r, c])
        return robots


    def get_size(self):
        max_row_length = 0
        for i in range(0, len(self.matrix)):
            row_length = len(self.matrix[i])
            if row_length > max_row_length:
                max_row_length = row_length
        return [len(self.matrix), max_row_length]
