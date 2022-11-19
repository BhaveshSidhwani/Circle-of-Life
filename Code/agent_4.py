
import random

import algorithm as a
import constants as c
import graph_operations as g


def agent_4():
    is_alive = True
    is_win = False

    # List to maintain the probabilities of all the nodes
    new_belief = init_belief()
    old_belief = new_belief.copy()

    # Loop until Agent CATCHES Prey or DIES or TIMES OUT
    while c.STEPS != c.TIME_OUT_STEPS and is_alive and not is_win:
        # Get all the nodes with max possibility of prey being there
        max_poss = [i for i, x in enumerate(new_belief) if x == max(new_belief)]
        # Randomly choose a node with max possibility
        max_poss_of_prey = random.choice(max_poss)

        # Survey the chosen node
        # If prey if found at surveyed node then change the probability of that node to 1 and rest all to 0
        if survey(max_poss_of_prey):
            new_belief = [0 for _ in range(c.SIZE)]
            new_belief[max_poss_of_prey] = 1
            c.PREY_CAUGHT_NUM += 1
        # Else change the probability of surveyed node to 0 and redistribute the probability
        else:
            new_belief = update_belief(new_belief, max_poss_of_prey)
        old_belief = new_belief.copy()

        # Get all the nodes with max possibility of prey being there
        max_poss = [i for i, x in enumerate(new_belief) if x==max(new_belief)]
        # Randomly choose a node with max possibility
        max_poss_of_prey = random.choice(max_poss)

        # Function call for agent movement
        c.AGENT_POS = g.movement_even(c.AGENT_POS, max_poss_of_prey, c.PREDATOR_POS.position)
        is_alive = g.check_if_alive()   # Function call to check if the agent is alive
        is_win = g.check_if_win()       # Function call to check if the agent won
        
        if not is_alive:                # If agent dies then break loop and return False
            print("Fail!!!")
            return False
        elif is_alive and is_win:       # If agent is alive and catches the prey
            print("Success!!!")         # then break loop and return True
            return True
        elif c.STEPS == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
            print("Fail!!!")
            return False
        
        # If prey is not found at the agent's new location
        # then change the probability of the node to 0 and redistribute the probability
        new_belief = update_belief(new_belief, c.AGENT_POS)
        old_belief = new_belief.copy()

        is_win = c.PREY_POS.movement()      # Function call for prey movement
        if is_win and is_alive:             # If agent is alive and catches the prey
            print("Success!!!")           # then break loop and return True
            return True
        
        # Redistribute the belief based on the prey's movement
        new_belief = redistribute_belief(new_belief, old_belief)
        old_belief = new_belief.copy()
        
        is_alive = c.PREDATOR_POS.movement() # Function call for predator movement
        if not is_alive:                     # If agent dies then break loop and return False
            print("Fail!!!")
            return False    
    return False    


# Function to initialize the initial probability to 1/49 for all nodes except the agent's position
def init_belief():
    belief = [( 1 / (c.SIZE-1) ) for _ in range(c.SIZE)]
    belief[c.AGENT_POS] = 0
    return belief


# Set the probability of the node to 0 and redistribute it
def update_belief(new_belief, node):
    temp = 1 - new_belief[node]
    new_belief[node] = 0
    for i in range(c.SIZE):
        new_belief[i] = new_belief[i] / temp

    return new_belief


# Redistribute the probabilities after prey's movement
def redistribute_belief(new_belief, old_belief):
    for i in range(c.SIZE):
        new_belief[i] = old_belief[i] / (len(c.GRAPH[i]) + 1)
        for neighbour in c.GRAPH[i]:
            new_belief[i] = new_belief[i] + (old_belief[neighbour] / (len(c.GRAPH[neighbour]) + 1))
    return update_belief(new_belief, c.AGENT_POS)


# Survey a node and return whether the prey is in that location or not
def survey(survey_node):
    return survey_node == c.PREY_POS.position
