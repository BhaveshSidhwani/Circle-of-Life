
import random

import algorithm as a
import constants as c
import graph_operations as g


def agent_5():
    is_alive = True
    is_win = False

    # List to maintain the probabilities of all the nodes
    new_belief = init_belief()
    old_belief = new_belief.copy()

    # Loop until Agent CATCHES Prey or DIES or TIMES OUT
    while c.STEPS != c.TIME_OUT_STEPS and is_alive and not is_win:
        # Get the closest node to agent with highest probability
        max_poss_of_pred = get_node_with_max_poss(new_belief)

        # Survey only when we don't know the precise position of the predator
        if new_belief[max_poss_of_pred] != 1:
            # If predator if found at surveyed node then change the probability of that node to 1 and rest all to 0
            if survey(max_poss_of_pred):
                new_belief = [0 for _ in range(c.SIZE)]
                new_belief[max_poss_of_pred] = 1
                c.PRED_CAUGHT_NUM += 1
            # Else change the probability of surveyed node to 0 and redistribute the probability
            else:
                new_belief = update_belief(new_belief, max_poss_of_pred)
        old_belief = new_belief.copy()

        # Get the closest node to agent with highest probability
        max_poss_of_pred = get_node_with_max_poss(new_belief)

        # Function call for agent movement
        c.AGENT_POS = g.movement(c.AGENT_POS, c.PREY_POS.position, max_poss_of_pred) #       agent move
        is_alive = g.check_if_alive()       # Function call to check if the agent is alive
        is_win = g.check_if_win()           # Function call to check if the agent won
        if not is_alive:                    # If agent dies then break loop and return False
            print("Fail!!!")
            return False
        elif is_alive and is_win:           # If agent is alive and catches the prey
            print("Success!!!")             # then break loop and return True
            return True
        elif c.STEPS == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
            print("Fail!!!")
            return False

        # If predator is not found at the agent's new location
        # then change the probability of the node to 0 and redistribute the probability
        new_belief = update_belief(new_belief, c.AGENT_POS)
        old_belief = new_belief.copy()

        is_win = c.PREY_POS.movement()      # Function call for prey movement
        if is_win and is_alive:             # If agent is alive and catches the prey
            print("Success!!!")           # then break loop and return True
            return True

        is_alive = c.PREDATOR_POS.movement() # Function call for predator movement
        if not is_alive:                     # If agent dies then break loop and return False
            print("Fail!!!")
            return False
        
        # Redistribute the belief based on the predator's movement
        new_belief = predator_move_belief_update(old_belief)
        old_belief = new_belief.copy()
    
    return False


# Function to get the closest node to agent with highest probability
def get_node_with_max_poss(new_belief):
    # List to store all the nodes with maximum probability
    max_poss = [i for i, x in enumerate(new_belief) if x == max(new_belief)]
    # Dictionary to store the distance to agent from each of the node with maximum probability
    dist_to_agent = {}
    # Loop for all the nodes in the list
    for n in max_poss:
        dist_to_agent[n] = len(a.get_shortest_path(n, c.AGENT_POS))
    # Get the minimum distance in the dictionary
    minimum = min(dist_to_agent, key=dist_to_agent.get)
    # Get all the agents closest to the agent
    closest_to_agent = [k for k, v in dist_to_agent.items() if v == dist_to_agent[minimum]]
    # Randomly select the node with highest probability and closest to the agent
    return random.choice(closest_to_agent)


# Function to initialize the initial probability to 1 at predator's position
# and 0 for all other nodes
def init_belief():
    belief = [0 for _ in range(c.SIZE)]
    belief[c.PREDATOR_POS.position] = 1
    return belief


# Set the probability of the node to 0 and redistribute it
def update_belief(new_belief, node):
    temp = 1 - new_belief[node]
    new_belief[node] = 0
    for i in range(c.SIZE):
        new_belief[i] = new_belief[i] / temp
    return new_belief


# Function to update the probabilites based on the predator's behaviour
def predator_move_belief_update(old_belief):
    # Initialised the distracted, focused and final probabilities list to 0
    distracted_new_belief = [0 for _ in range(c.SIZE)]
    focused_new_belief = [0 for _ in range(c.SIZE)]
    final_new_belief = [0 for _ in range(c.SIZE)]

    # Probability distribution for distracted behaviour
    for i in range(c.SIZE):
        for neighbour in c.GRAPH[i]:
            distracted_new_belief[i] = distracted_new_belief[i] + (old_belief[neighbour] / len(c.GRAPH[neighbour]))

        distracted_new_belief[i] = distracted_new_belief[i] * 0.4

    # Probability distribution for focused behaviour
    for i in range(c.SIZE):
        poss_movement = predator_move_sim(i)
        for j in poss_movement:
            focused_new_belief[j] = focused_new_belief[j] + old_belief[i]/len(poss_movement)

    # Final probability = (distracted behaviour * 0.4) + (focused behaviour * 0.6)
    for i in range(c.SIZE):
        focused_new_belief[i] = focused_new_belief[i] * 0.6
        final_new_belief[i] = focused_new_belief[i] + distracted_new_belief[i]
    return update_belief(final_new_belief, c.AGENT_POS)

# Function to simulate the predator's focused movement behaviour
def predator_move_sim(node):
    dist = {}
    for neighbour in c.GRAPH[node]:
        dist[neighbour] = len(a.get_shortest_path(node, c.AGENT_POS))

    next_node = min(dist, key=dist.get)
    poss_movement = []
    for i in dist:
        if dist[i] == dist[next_node]:
            poss_movement.append(i)
            
    return poss_movement


# Function to survey a node and return whether the predator is in that location or not
def survey(survey_node):
    return survey_node == c.PREDATOR_POS.position
