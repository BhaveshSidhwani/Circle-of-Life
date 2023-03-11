
import random
import numpy as np

import algorithm as a
import constants as c
import graph_operations as g


def agent_9():
    is_alive = True
    is_win = False

    # List to maintain the probabilities of prey of all the nodes
    prey_new_belief = prey_init_belief()
    prey_old_belief = prey_new_belief.copy()

    # List to maintain the probabilities of predator of all the nodes
    pred_new_belief = pred_init_belief()
    pred_old_belief = pred_new_belief.copy()

    # Loop until Agent CATCHES Prey or DIES or TIMES OUT
    while c.STEPS != c.TIME_OUT_STEPS and is_alive and not is_win:
        # Get all the nodes with max possibility of prey being there
        prey_max_poss = [i for i, x in enumerate(prey_new_belief) if x == max(prey_new_belief)]
        # Randomly choose a node with max possibility
        max_poss_of_prey = random.choice(prey_max_poss)
        
        # Get the closest node to agent with highest probability of predator being there
        max_poss_of_pred = get_node_with_max_poss(pred_new_belief)

        # Survey for predator when we don't know the precise position of the predator
        if pred_new_belief[max_poss_of_pred] != 1:
            # If predator if found at surveyed node then change the probability of that node to 1 and rest all to 0
            if survey(0, max_poss_of_pred):
                pred_new_belief = [0 for _ in range(c.SIZE)]
                pred_new_belief[max_poss_of_pred] = 1
                c.PRED_CAUGHT_NUM += 1
            # Else change the probability of surveyed node to 0 and redistribute the probability
            else:
                pred_new_belief = update_belief(pred_new_belief, max_poss_of_pred)
            pred_old_belief = pred_new_belief.copy()
        # Else survey for prey
        else:
            # Survey the chosen node
            # If prey if found at surveyed node then change the probability of that node to 1 and rest all to 0
            if survey(1, max_poss_of_prey):
                prey_new_belief = [0 for _ in range(c.SIZE)]
                prey_new_belief[max_poss_of_prey] = 1
                c.PREY_CAUGHT_NUM += 1
            # Else change the probability of surveyed node to 0 and redistribute the probability
            else:
                prey_new_belief = update_belief(prey_new_belief, max_poss_of_prey)
            prey_old_belief = prey_new_belief.copy()

        # Get all the nodes with max possibility of prey being there
        prey_max_poss = [i for i, x in enumerate(prey_new_belief) if x==max(prey_new_belief)]
        # Randomly choose a node with max possibility
        max_poss_of_prey = random.choice(prey_max_poss)
        
        # Get the closest node to agent with highest probability
        max_poss_of_pred = get_node_with_max_poss(pred_new_belief)

        # Function call for agent movement
        c.AGENT_POS = movement(c.AGENT_POS, max_poss_of_pred, max_poss_of_prey)
        is_alive = g.check_if_alive()       # Function call to check if the agent is alive
        is_win = g.check_if_win()           # Function call to check if the agent won
        if not is_alive:                    # If agent dies then break loop and return False
            print("You walked into a trap!!!")
            return False
        elif is_alive and is_win:           # If agent is alive and catches the prey
            print("You win!!!")             # then break loop and return True
            return True
        elif c.STEPS == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
            print("Too slow to catch")
            return False
        
        # If prey is not found at the agent's new location
        # then change the probability of the node to 0 and redistribute the probability
        prey_new_belief = update_belief(prey_new_belief, c.AGENT_POS)
        prey_old_belief = prey_new_belief.copy()

        # If predator is not found at the agent's new location
        # then change the probability of the node to 0 and redistribute the probability
        pred_new_belief = update_belief(pred_new_belief, c.AGENT_POS)
        pred_old_belief = pred_new_belief.copy()

        is_win = c.PREY_POS.movement()      # Function call for prey movement
        if is_win and is_alive:             # If agent is alive and catches the prey
            print("Lucky win!!!")           # then break loop and return True
            return True

        # Redistribute the belief based on the prey's movement
        prey_new_belief = prey_redistribute_belief(prey_new_belief, prey_old_belief)
        prey_old_belief = prey_new_belief.copy()
        
        is_alive = c.PREDATOR_POS.movement() # Function call for predator movement
        if not is_alive:                     # If agent dies then break loop and return False
            print("You are dead now!!!")
            return False        

        # Redistribute the belief based on the predator's movement
        pred_new_belief = predator_move_belief_update(pred_old_belief)
        pred_old_belief = pred_new_belief.copy()
        
    return False


# Function to initialize the initial probability to 1/49 for all nodes except the agent's position
def prey_init_belief():
    belief = [( 1 / (c.SIZE-1) ) for _ in range(c.SIZE)]
    belief[c.AGENT_POS] = 0
    return belief

# Function to initialize the initial probability to 1 at predator's position
# and 0 for all other nodes
def pred_init_belief():
    belief = [0 for _ in range(c.SIZE)]
    belief[c.PREDATOR_POS.position] = 1
    return belief


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
    closest_to_agent = [i for i in dist_to_agent if i == minimum]
    # Randomly select the node with highest probability and closest to the agent
    return random.choice(closest_to_agent)


# Set the probability of the node to (0.1 * probability of the node) and redistribute the remaining
def update_belief(new_belief, node):
    temp = 1 - (new_belief[node]*0.9)
    new_belief[node] = new_belief[node] * 0.1
    for i in range(c.SIZE):
        new_belief[i] = new_belief[i] / temp
    return new_belief


# Redistribute the probabilities after prey's movement
def prey_redistribute_belief(new_belief, old_belief):
    for i in range(c.SIZE):
        new_belief[i] = old_belief[i] / (len(c.GRAPH[i]) + 1)
        for neighbour in c.GRAPH[i]:
            new_belief[i] = new_belief[i] + (old_belief[neighbour] / (len(c.GRAPH[neighbour]) + 1))
    return update_belief(new_belief, c.AGENT_POS)


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


# Survey a node for prey if mode = 1 and for predator if mode = 0
def survey(mode, survey_node):
    if mode == 0:
        result = survey_node == c.PREDATOR_POS.position
    else:
        result = survey_node == c.PREY_POS.position
    
    # If prey or predator is in the surveyed location
    # then it will return false negative with a 10% probability
    if result:
        fault = np.random.choice([0, 1], p=[0.9, 0.1])
        if fault:
            return False
    return result


# Function for agent movement
def movement(agent_pos, prey_pos, pred_pos):
    # Dictionary to store distance of agent's neighbours' position to prey
    dist_from_prey = {}
    # Distance from agent's current position to prey while avoiding predator
    dist_prey = len(a.get_shortest_path_avoiding_predator(agent_pos, prey_pos, pred_pos))
    # Dictionary to store distance of agent's neighbours' position to predator
    dist_from_pred = {}
    # Distance from agent's current position to predator
    dist_pred = len(a.get_shortest_path(pred_pos, agent_pos))

    # Loop to get distance from agent's neighbours to predator and prey while avoiding predator
    for neighbour in c.GRAPH[c.AGENT_POS]:
        dist_from_prey[neighbour] = len(a.get_shortest_path_avoiding_predator(neighbour, prey_pos, pred_pos))
        dist_from_pred[neighbour] = len(a.get_shortest_path(pred_pos, neighbour))

    # Number of steps taken till now
    c.STEPS += 1

    return movement_rules(dist_prey, dist_pred, dist_from_prey, dist_from_pred)


# Function to determine next_node of agent based on the movement rules
def movement_rules(dist_prey, dist_pred, dist_from_prey, dist_from_pred):
    # List to maintain the priority of agent's neighbour based on the rules
    # Lowest number is the highest priority
    priority = []

    # Loop to iterate over dictionary
    for i in dist_from_prey:
        # Assign priority 1 to neighbors that are farther from Predator if the current distance is less than 3
        if dist_pred <= 3 and dist_from_pred[i] > dist_pred:
            priority.append((1, i))
        
        elif dist_from_prey[i] < dist_prey and dist_from_pred[i] > dist_pred:
            priority.append((2, i))

        # Assign priority 2 to neighbors that are closer to the Prey and not closer to the Predator
        elif dist_from_prey[i] < dist_prey and dist_from_pred[i] == dist_pred:
            priority.append((3, i))

        # Assign priority 3 to neighbors that are not farther from the Prey and farther from the Predator
        elif dist_from_prey[i] == dist_prey and dist_from_pred[i] > dist_pred:
            priority.append((4, i))

        # Assign priority 4 to neighbors that are not farther from the Prey and not closer to the Predator
        elif dist_from_prey[i] == dist_prey and dist_from_pred[i] == dist_pred:
            priority.append((5, i))

        # Assign priority 5 to neighbors that are farther from the Predator
        elif dist_from_pred[i] > dist_pred:
            priority.append((6, i))

        # Assign priority 6 to neighbors that are not closer to the Predator
        elif dist_from_pred[i] == dist_pred:
            priority.append((7, i))

        # Assign priority 7 if the agent sits still and prays
        else:
            priority.append((8, c.AGENT_POS))

    # Get the neighbour with lowest number (highest priority)
    next_node = min(priority)

    # List to store all the neighbours with the highest priority
    poss_movement = []
    for i in priority:
        if i[0] == next_node[0]:
            poss_movement.append(i[1])

    # Return random among neighbours with highest priority
    return random.choice(poss_movement)
