
import numpy as np
import random

import algorithm as a
import constants as c
import graph_operations as g

# Class for predator
class predator:
    # Initialise the predator position
    def __init__(self, pos):
        self.position = pos


    # Function for predator movement
    def movement(self, agent_pos):
        # Determine Behaviour (0 = Distracted movement (40% chance), 1 = Focused movement (60% chance))
        behaviour = np.random.choice([0, 1], p=[0.4, 0.6])
        
        if behaviour:
            # Dictionary to maintain distance between predator's neighbours and agent
            dist = {}
            # Loop to get shortest path to agent for all neighbours of the predator
            for neighbour in c.GRAPH[self.position]:
                dist[neighbour] = len(a.get_shortest_path(neighbour, agent_pos))

            # Get the node with minimum distance from the list
            next_node = min(dist, key=dist.get)
            poss_movement = []
            # Loop for getting all the neighbours with the shortest distance to the agent
            for i in dist:
                if dist[i] == dist[next_node]:
                    poss_movement.append(i)
            
            # Randomly move to a node with the shortest distance to the agent
            self.position = random.choice(poss_movement)
        else:
            # Randomly move to one of the neighbours of the predator
            self.position = random.choice(c.GRAPH[self.position])
            
        return g.check_if_alive()


    def __str__(self):
        return "Predator position: " + str(self.position)

    
    __repr__ = __str__