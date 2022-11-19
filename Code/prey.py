
import random

import constants as c
import graph_operations as g

# Class for prey
class prey:
    # Initialise the prey position
    def __init__(self, pos):
        self.position = pos


    # Function for prey movement
    def movement(self):
        # Possible nodes include its neighbours and its current node
        poss_movement = c.GRAPH[self.position] + [self.position]
        # Randomly choose from the possible nodes
        move_to_node = random.choice(poss_movement)
        # Move to the chosen node
        self.position = move_to_node

        return g.check_if_win()

    
    def __str__(self):
        return "Prey position: " + str(self.position)


    __repr__ = __str__
