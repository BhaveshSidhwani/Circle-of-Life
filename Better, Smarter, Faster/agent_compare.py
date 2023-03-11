
import random

import algorithm as a
import constants as c
import prey
import predator as pred


agent_u_path = []
agent_1_path = []
agent_2_path = []

pred_u_path = []
pred_1_path = []
pred_2_path = []

prey_u_path = []
prey_1_path = []
prey_2_path = []

def agent_compare():
    agent_u_pos, prey_pos, pred_pos = init_characters()
    agent_2_pos = agent_1_pos = agent_u_pos

    agent_u_path.append(agent_u_pos)
    agent_1_path.append(agent_1_pos)
    agent_2_path.append(agent_2_pos)

    pred_u = pred.predator(pred_pos)
    pred_1 = pred.predator(pred_pos)
    pred_2 = pred.predator(pred_pos)

    pred_u_path.append(pred_u.position)
    pred_1_path.append(pred_1.position)
    pred_2_path.append(pred_2.position)

    c.PREY_POS = prey.prey(prey_pos)
    prey_u_path.append(c.PREY_POS.position)
    prey_1_path.append(c.PREY_POS.position)
    prey_2_path.append(c.PREY_POS.position)

    output = {}

    is_win_U = False
    is_alive_U = True
    steps_U = 0

    is_win_1 = False
    is_alive_1 = True
    steps_1 = 0

    is_win_2 = False
    is_alive_2 = True
    steps_2 = 0

    # Loop until Agent CATCHES Prey or DIES or TIMES OUT
    while ((steps_U != c.TIME_OUT_STEPS and is_alive_U and not is_win_U)\
            or (steps_1 != c.TIME_OUT_STEPS and is_alive_1 and not is_win_1)\
            or (steps_2 != c.TIME_OUT_STEPS and is_alive_2 and not is_win_2)):
        
        # Function call for agent movement
        if not is_win_U and is_alive_U:
            agent_u_pos = movement_U(agent_u_pos, c.PREY_POS.position, pred_u.position)
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
        
        if not is_win_1 and is_alive_1:
            agent_1_pos = movement(agent_1_pos, c.PREY_POS.position, pred_1.position)
            agent_1_path.append(agent_1_pos)
            steps_1 += 1

            is_win_1 = check_if_win(agent_1_pos, c.PREY_POS.position)            # Function call to check if the agent won
            is_alive_1 = check_if_alive(agent_1_pos, pred_1.position)   # Function call to check if the agent is alive
            
            if is_win_1:                      # If agent dies then break loop and return False
                print("1 Success!!!")
                output["1_star"] = (1, steps_1)
            elif not is_alive_1:              # If agent is alive and catches the prey
                print("1 Fail!!!")            # then break loop and return True
                output["1_star"] = (0, steps_1)
            elif steps_1 == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
                print("1 Fail!!!")
                is_alive_1 = False
                output["1_star"] = (0, steps_1)
        
        if not is_win_2 and is_alive_2:
            agent_2_pos = movement_even(agent_2_pos, c.PREY_POS.position, pred_2.position)
            agent_2_path.append(agent_2_pos)
            steps_2 += 1

            is_win_2 = check_if_win(agent_2_pos, c.PREY_POS.position)            # Function call to check if the agent won
            is_alive_2 = check_if_alive(agent_2_pos, pred_2.position)   # Function call to check if the agent is alive
            
            if is_win_2:                      # If agent dies then break loop and return False
                print("2 Success!!!")
                output["2_star"] = (1, steps_2)
            elif not is_alive_2:              # If agent is alive and catches the prey
                print("2 Fail!!!")            # then break loop and return True
                output["2_star"] = (0, steps_2)
            elif steps_2 == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
                print("2 Fail!!!")
                is_alive_2 = False
                output["2_star"] = (0, steps_2)

        c.PREY_POS.movement()             # Function call for prey movement
        if not is_win_U and is_alive_U:
            is_win_U = check_if_win(agent_u_pos, c.PREY_POS.position)            # Function call to check if the agent won
            prey_u_path.append(c.PREY_POS.position)
            if is_win_U:                      # If agent dies then break loop and return False
                print("U Success!!!")
                output["U_star"] = (1, steps_U)
        
        if not is_win_1 and is_alive_1:
            is_win_1 = check_if_win(agent_1_pos, c.PREY_POS.position)            # Function call to check if the agent won
            prey_1_path.append(c.PREY_POS.position)
            if is_win_1:                      # If agent dies then break loop and return False
                print("1 Success!!!")
                output["1_star"] = (1, steps_1)
        
        if not is_win_2 and is_alive_2:
            is_win_2 = check_if_win(agent_2_pos, c.PREY_POS.position)            # Function call to check if the agent won
            prey_2_path.append(c.PREY_POS.position)
            if is_win_2:                      # If agent dies then break loop and return False
                print("2 Sucess!!!")
                output["2_star"] = (1, steps_2)
        

        if not is_win_U and is_alive_U:
            pred_u.movement(agent_u_pos)                    # Function call for predator movement
            pred_u_path.append(pred_u.position)
            is_alive_U = check_if_alive(agent_u_pos, pred_u.position)   # Function call to check if the agent is alive
            if not is_alive_U:              # If agent is alive and catches the prey
                print("U Fail!!!")            # then break loop and return True
                output["U_star"] = (0, steps_U)

        if not is_win_1 and is_alive_1:
            pred_1.movement(agent_1_pos)                    # Function call for predator movement
            pred_1_path.append(pred_1.position)
            is_alive_1 = check_if_alive(agent_1_pos, pred_1.position)   # Function call to check if the agent is alive
            if not is_alive_1:              # If agent is alive and catches the prey
                print("1 Fail!!!")            # then break loop and return True
                output["1_star"] = (0, steps_1)
        
        if not is_win_2 and is_alive_2:
            pred_2.movement(agent_2_pos)                    # Function call for predator movement
            pred_2_path.append(pred_2.position)
            is_alive_2 = check_if_alive(agent_2_pos, pred_2.position)   # Function call to check if the agent is alive
            if not is_alive_2:              # If agent is alive and catches the prey
                print("2 Fail!!!")            # then break loop and return True
                output["2_star"] = (0, steps_2)
        
    return output

def movement_U(agent_pos, prey_pos, pred_pos):
    poss_moves = {}
    poss_moves[agent_pos] = c.U_star[(agent_pos, prey_pos, pred_pos)]
    for neighbour in c.GRAPH[agent_pos] + [agent_pos]:
        poss_moves[neighbour] = c.U_star[(neighbour, prey_pos, pred_pos)]
    
    best_move = min(poss_moves, key=poss_moves.get)

    return best_move


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


def init_characters():
    return random.sample(range(c.START, c.SIZE), 3)


def check_if_win(agent_pos, prey_pos):
    return agent_pos == prey_pos


def check_if_alive(agent_pos, pred_pos):
    return agent_pos != pred_pos
