
import random

import algorithm as a
import constants as c
import prey
import predator as pred


agent_u_path = []
agent_3_path = []
agent_4_path = []

pred_u_path = []
pred_3_path = []
pred_4_path = []

prey_u_path = []
prey_3_path = []
prey_4_path = []


def agent_compare():
    agent_u_pos, prey_pos, pred_pos = init_characters()
    agent_4_pos = agent_3_pos = agent_u_pos

    agent_u_path.append(agent_u_pos)
    agent_3_path.append(agent_3_pos)
    agent_4_path.append(agent_4_pos)

    pred_u = pred.predator(pred_pos)
    pred_3 = pred.predator(pred_pos)
    pred_4 = pred.predator(pred_pos)

    pred_u_path.append(pred_u.position)
    pred_3_path.append(pred_3.position)
    pred_4_path.append(pred_4.position)

    c.PREY_POS = prey.prey(prey_pos)
    prey_u_path.append(c.PREY_POS.position)
    prey_3_path.append(c.PREY_POS.position)
    prey_4_path.append(c.PREY_POS.position)

    output = {}

    is_win_U = False
    is_alive_U = True
    steps_U = 0

    is_win_3 = False
    is_alive_3 = True
    steps_3 = 0

    is_win_4 = False
    is_alive_4 = True
    steps_4 = 0

    new_belief_U = init_belief()
    old_belief_U = new_belief_U.copy()

    new_belief_3 = init_belief()
    old_belief_3 = new_belief_3.copy()

    new_belief_4 = init_belief()
    old_belief_4 = new_belief_4.copy()
    # Loop until Agent CATCHES Prey or DIES or TIMES OUT
    while ((steps_U != c.TIME_OUT_STEPS and is_alive_U and not is_win_U)\
            or (steps_3 != c.TIME_OUT_STEPS and is_alive_3 and not is_win_3)\
            or (steps_4 != c.TIME_OUT_STEPS and is_alive_4 and not is_win_4)):
        
        
        # Function call for agent movement
        if not is_win_U and is_alive_U:
            # Get all the nodes with max possibility of prey being there
            max_poss = [i for i, x in enumerate(new_belief_U) if x == max(new_belief_U)]
            # Randomly choose a node with max possibility
            max_poss_of_prey = random.choice(max_poss)
            # Survey the chosen node
            # If prey if found at surveyed node then change the probability of that node to 1 and rest all to 0
            if survey(max_poss_of_prey):
                new_belief_U = [0 for _ in range(c.SIZE)]
                new_belief_U[max_poss_of_prey] = 1
                c.PREY_CAUGHT_NUM += 1
            # Else change the probability of surveyed node to 0 and redistribute the probability
            else:
                new_belief_U = update_belief(new_belief_U, max_poss_of_prey)
            old_belief_U = new_belief_U.copy()

            agent_u_pos = movement_U(agent_u_pos, new_belief_U, pred_u.position)
            agent_u_path.append(agent_u_pos)
            steps_U += 1

            is_win_U = check_if_win(agent_u_pos, c.PREY_POS.position)            # Function call to check if the agent won
            is_alive_U = check_if_alive(agent_u_pos, pred_u.position)   # Function call to check if the agent is alive
            
            if is_win_U:                      # If agent dies then break loop and return False
                print("U Success!!!")
                output["U_star"] = (1, steps_U)
            elif not is_alive_U:              # If agent is alive and catches the prey
                print("U Fail!!!")            # then break loop and return True
                output["U_star"] = (0, steps_U)
            elif steps_U == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
                print("U Fail!!!")
                is_alive_U = False
                output["U_star"] = (0, steps_U)
            
            # If prey is not found at the agent's new location
            # then change the probability of the node to 0 and redistribute the probability
            new_belief_U = update_belief(new_belief_U, agent_u_pos)
            old_belief_U = new_belief_U.copy()
        
        if not is_win_3 and is_alive_3:
            # Get all the nodes with max possibility of prey being there
            max_poss = [i for i, x in enumerate(new_belief_3) if x == max(new_belief_3)]
            # Randomly choose a node with max possibility
            max_poss_of_prey = random.choice(max_poss)
            # Survey the chosen node
            # If prey if found at surveyed node then change the probability of that node to 1 and rest all to 0
            if survey(max_poss_of_prey):
                new_belief_3 = [0 for _ in range(c.SIZE)]
                new_belief_3[max_poss_of_prey] = 1
                c.PREY_CAUGHT_NUM += 1
            # Else change the probability of surveyed node to 0 and redistribute the probability
            else:
                new_belief_3 = update_belief(new_belief_3, max_poss_of_prey)
            old_belief_3 = new_belief_3.copy()

            # Get all the nodes with max possibility of prey being there
            max_poss = [i for i, x in enumerate(new_belief_3) if x==max(new_belief_3)]
            # Randomly choose a node with max possibility
            max_poss_of_prey = random.choice(max_poss)

            agent_3_pos = movement(agent_3_pos, max_poss_of_prey, pred_3.position)
            agent_3_path.append(agent_3_pos)
            steps_3 += 1

            is_win_3 = check_if_win(agent_3_pos, c.PREY_POS.position)            # Function call to check if the agent won
            is_alive_3 = check_if_alive(agent_3_pos, pred_3.position)   # Function call to check if the agent is alive
            
            if is_win_3:                      # If agent dies then break loop and return False
                print("3 Success!!!")
                output["3_star"] = (1, steps_3)
            elif not is_alive_3:              # If agent is alive and catches the prey
                print("3 Fail!!!")            # then break loop and return True
                output["3_star"] = (0, steps_3)
            elif steps_3 == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
                print("3 Fail!!!")
                is_alive_3 = False
                output["3_star"] = (0, steps_3)
            
            # If prey is not found at the agent's new location
            # then change the probability of the node to 0 and redistribute the probability
            new_belief_3 = update_belief(new_belief_3, agent_u_pos)
            old_belief_3 = new_belief_3.copy()
        
        if not is_win_4 and is_alive_4:
            # Get all the nodes with max possibility of prey being there
            max_poss = [i for i, x in enumerate(new_belief_4) if x == max(new_belief_4)]
            # Randomly choose a node with max possibility
            max_poss_of_prey = random.choice(max_poss)
            # Survey the chosen node
            # If prey if found at surveyed node then change the probability of that node to 1 and rest all to 0
            if survey(max_poss_of_prey):
                new_belief_4 = [0 for _ in range(c.SIZE)]
                new_belief_4[max_poss_of_prey] = 1
                c.PREY_CAUGHT_NUM += 1
            # Else change the probability of surveyed node to 0 and redistribute the probability
            else:
                new_belief_4 = update_belief(new_belief_4, max_poss_of_prey)
            old_belief_4 = new_belief_4.copy()

            # Get all the nodes with max possibility of prey being there
            max_poss = [i for i, x in enumerate(new_belief_4) if x==max(new_belief_4)]
            # Randomly choose a node with max possibility
            max_poss_of_prey = random.choice(max_poss)

            agent_4_pos = movement_even(agent_4_pos, max_poss_of_prey, pred_4.position)
            agent_4_path.append(agent_4_pos)
            steps_4 += 1

            is_win_4 = check_if_win(agent_4_pos, c.PREY_POS.position)            # Function call to check if the agent won
            is_alive_4 = check_if_alive(agent_4_pos, pred_4.position)   # Function call to check if the agent is alive
            
            if is_win_4:                      # If agent dies then break loop and return False
                print("4 Success!!!")
                output["4_star"] = (1, steps_4)
            elif not is_alive_4:              # If agent is alive and catches the prey
                print("4 Fail!!!")            # then break loop and return True
                output["4_star"] = (0, steps_4)
            elif steps_4 == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
                print("4 Fail!!!")
                is_alive_4 = False
                output["4_star"] = (0, steps_4)
            
            # If prey is not found at the agent's new location
            # then change the probability of the node to 0 and redistribute the probability
            new_belief_4 = update_belief(new_belief_4, agent_u_pos)
            old_belief_4 = new_belief_4.copy()

        c.PREY_POS.movement()             # Function call for prey movement
        if not is_win_U and is_alive_U:
            is_win_U = check_if_win(agent_u_pos, c.PREY_POS.position)            # Function call to check if the agent won
            prey_u_path.append(c.PREY_POS.position)
            if is_win_U:                      # If agent dies then break loop and return False
                print("U Success!!!")
                output["U_star"] = (1, steps_U)
            
            new_belief_U = redistribute_belief(new_belief_U, old_belief_U)
            old_belief_U = new_belief_U.copy()
        
        if not is_win_3 and is_alive_3:
            is_win_3 = check_if_win(agent_3_pos, c.PREY_POS.position)            # Function call to check if the agent won
            prey_3_path.append(c.PREY_POS.position)
            if is_win_3:                      # If agent dies then break loop and return False
                print("3 Success!!!")
                output["3_star"] = (1, steps_3)
            
            new_belief_3 = redistribute_belief(new_belief_3, old_belief_3)
            old_belief_3 = new_belief_3.copy()
        
        if not is_win_4 and is_alive_4:
            is_win_4 = check_if_win(agent_4_pos, c.PREY_POS.position)            # Function call to check if the agent won
            prey_4_path.append(c.PREY_POS.position)
            if is_win_4:                      # If agent dies then break loop and return False
                print("4 Sucess!!!")
                output["4_star"] = (1, steps_4)
            
            new_belief_4 = redistribute_belief(new_belief_4, old_belief_4)
            old_belief_4 = new_belief_4.copy()
        

        if not is_win_U and is_alive_U:
            pred_u.movement(agent_u_pos)                    # Function call for predator movement
            pred_u_path.append(pred_u.position)
            is_alive_U = check_if_alive(agent_u_pos, pred_u.position)   # Function call to check if the agent is alive
            if not is_alive_U:              # If agent is alive and catches the prey
                print("U Fail!!!")            # then break loop and return True
                output["U_star"] = (0, steps_U)

        if not is_win_3 and is_alive_3:
            pred_3.movement(agent_3_pos)                    # Function call for predator movement
            pred_3_path.append(pred_3.position)
            is_alive_3 = check_if_alive(agent_3_pos, pred_3.position)   # Function call to check if the agent is alive
            if not is_alive_3:              # If agent is alive and catches the prey
                print("1 Fail!!!")            # then break loop and return True
                output["1_star"] = (0, steps_3)
        
        if not is_win_4 and is_alive_4:
            pred_4.movement(agent_4_pos)                    # Function call for predator movement
            pred_4_path.append(pred_4.position)
            is_alive_4 = check_if_alive(agent_4_pos, pred_4.position)   # Function call to check if the agent is alive
            if not is_alive_4:              # If agent is alive and catches the prey
                print("2 Fail!!!")            # then break loop and return True
                output["2_star"] = (0, steps_4)
        
    return output

def movement_U(agent_pos, prey_belief, pred_pos):
    poss_moves = {}
    for m in c.GRAPH[agent_pos] + [agent_pos]:
        for n in c.GRAPH[pred_pos]:
            sum = 0
            for p in range(c.SIZE):
                sum += (prey_belief[p] * c.U_star[(m, p, n)])
            poss_moves[(m, n)] = sum
    best_move = min(poss_moves, key=poss_moves.get)
    c.STEPS += 1
    return best_move[0]


# Function for agent movement
def movement(agent_pos, prey_pos, pred_pos):
    # Dictionary to store distance of agent's neighbours' position to prey
    dist_from_prey = {}
    # Distance from agent's current position to prey
    dist_prey = c.FULL_DIST[agent_pos][prey_pos]
    # Dictionary to store distance of agent's neighbours' position to predator
    dist_from_pred = {}
    # Distance from agent's current position to predator
    dist_pred = c.FULL_DIST[pred_pos][agent_pos]

    # Loop to get distance from agent's neighbours to prey and predator
    for neighbour in c.GRAPH[agent_pos]+[agent_pos]:
        dist_from_prey[neighbour] = c.FULL_DIST[neighbour][prey_pos]
        dist_from_pred[neighbour] = c.FULL_DIST[pred_pos][neighbour]

    return movement_rules(agent_pos, dist_prey, dist_pred, dist_from_prey, dist_from_pred)


# Function for agent movement
def movement_even(agent_pos, prey_pos, pred_pos):
    # Dictionary to store distance of agent's neighbours' position to prey
    dist_from_prey = {}
    # Distance from agent's current position to prey while avoiding predator
    dist_prey = len(a.get_shortest_path_avoiding_predator(agent_pos, prey_pos, pred_pos))
    # Dictionary to store distance of agent's neighbours' position to predator
    dist_from_pred = {}
    # Distance from agent's current position to predator
    dist_pred = len(a.get_shortest_path(pred_pos, agent_pos))

    # Loop to get distance from agent's neighbours to predator and prey while avoiding predator
    for neighbour in c.GRAPH[agent_pos]+[agent_pos]:
        dist_from_prey[neighbour] = len(a.get_shortest_path_avoiding_predator(neighbour, prey_pos, pred_pos))
        dist_from_pred[neighbour] = len(a.get_shortest_path(pred_pos, neighbour))

    return movement_rules(agent_pos, dist_prey, dist_pred, dist_from_prey, dist_from_pred)


# Function to determine next_node of agent based on the movement rules
def movement_rules(agent_pos, dist_prey, dist_pred, dist_from_prey, dist_from_pred):
    # List to maintain the priority of agent's neighbour based on the rules
    # Lowest number is the highest priority
    priority = []

    # Loop to iterate over dictionary
    for i in dist_from_prey:
        # Assign priority 1 to neighbors that are closer to the Prey and farther from the Predator
        if dist_from_prey[i] < dist_prey and dist_from_pred[i] > dist_pred:
            priority.append((1, i))

        # Assign priority 2 to neighbors that are closer to the Prey and not closer to the Predator
        elif dist_from_prey[i] < dist_prey and dist_from_pred[i] == dist_pred:
            priority.append((2, i))

        # Assign priority 3 to neighbors that are not farther from the Prey and farther from the Predator
        elif dist_from_prey[i] == dist_prey and dist_from_pred[i] > dist_pred:
            priority.append((3, i))

        # Assign priority 4 to neighbors that are not farther from the Prey and not closer to the Predator
        elif dist_from_prey[i] == dist_prey and dist_from_pred[i] == dist_pred:
            priority.append((4, i))

        # Assign priority 5 to neighbors that are farther from the Predator
        elif dist_from_pred[i] > dist_pred:
            priority.append((5, i))

        # Assign priority 6 to neighbors that are not closer to the Predator
        elif dist_from_pred[i] == dist_pred:
            priority.append((6, i))

        # Assign priority 7 if the agent sits still and prays
        else:
            priority.append((7, agent_pos))

    # Get the neighbour with lowest number (highest priority)
    next_node = min(priority)

    # List to store all the neighbours with the highest priority
    poss_movement = []
    for i in priority:
        if i[0] == next_node[0]:
            poss_movement.append(i[1])

    # Return random among neighbours with highest priority
    return random.choice(poss_movement)


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


def survey(survey_node):
    return survey_node == c.PREY_POS.position


def init_characters():
    return random.sample(range(c.START, c.SIZE), 3)


def check_if_win(agent_pos, prey_pos):
    return agent_pos == prey_pos


def check_if_alive(agent_pos, pred_pos):
    return agent_pos != pred_pos
