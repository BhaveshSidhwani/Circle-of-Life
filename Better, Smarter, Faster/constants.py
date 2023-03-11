
import predator as pred
import prey


# Constants for graph
START = 0
SIZE = 50
GRAPH = {
    0: [49, 1, 5],\
    1: [0, 2, 46],\
    2: [1, 3, 47],\
    3: [2, 4, 48],\
    4: [3, 5, 7],\
    5: [4, 6, 0],\
    6: [5, 7, 9],\
    7: [6, 8, 4],\
    8: [7, 9, 13],\
    9: [8, 10, 6],\
    10: [9, 11, 12],\
    11: [10, 12, 14],\
    12: [11, 13, 10],\
    13: [12, 14, 8],\
    14: [13, 15, 11],\
    15: [14, 16, 19],\
    16: [15, 17],\
    17: [16, 18],\
    18: [17, 19, 20],\
    19: [18, 20, 15],\
    20: [19, 21, 18],\
    21: [20, 22, 24],\
    22: [21, 23, 26],\
    23: [22, 24, 27],\
    24: [23, 25, 21],\
    25: [24, 26, 30],\
    26: [25, 27, 22],\
    27: [26, 28, 23],\
    28: [27, 29, 31],\
    29: [28, 30, 33],\
    30: [29, 31, 25],\
    31: [30, 32, 28],\
    32: [31, 33, 37],\
    33: [32, 34, 29],\
    34: [33, 35, 38],\
    35: [34, 36, 39],\
    36: [35, 37, 40],\
    37: [36, 38, 32],\
    38: [37, 39, 34],\
    39: [38, 40, 35],\
    40: [39, 41, 36],\
    41: [40, 42, 43],\
    42: [41, 43, 44],\
    43: [42, 44, 41],\
    44: [43, 45, 42],\
    45: [44, 46, 49],\
    46: [45, 47, 1],\
    47: [46, 48, 2],\
    48: [47, 49, 3],\
    49: [48, 0, 45]\
}

# Pre Computed distance between nodes
FULL_DIST = []

# Constants for game characters
AGENT_POS = 0
PREDATOR_POS: pred.predator = None
PREY_POS: prey.prey = None

# Constants for data extraction
PREY_CAUGHT_NUM = 0
PRED_CAUGHT_NUM = 0
STEPS = 0
TIME_OUT_STEPS = 5000

U_star = {}
