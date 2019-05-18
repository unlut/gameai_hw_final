def direction_to_rowcol(direction, old_facing_index=0):
    facing_index = 0
    if direction == "L":
        i = 0
        j = -1
        facing_index = 2
    elif direction == "R":
        i = 0
        j = 1
        facing_index = 0
    elif direction == "U":
        i = -1
        j = 0
        facing_index = 1
    elif direction == "D":
        i = 1
        j = 0
        facing_index = 3
    elif direction == "PASS":
        i = 0
        j = 0
        facing_index = old_facing_index
    drow = i
    dcol = j
    return (drow, dcol, facing_index)


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0
