
import random
import numpy as np

import algorithm as a
import constants as c
import predator as pred
import prey


def pre_load_dist():
    c.FULL_DIST = np.zeros([50, 50]).tolist()
    for i in range(c.SIZE):
        for j in range(c.SIZE):
            c.FULL_DIST[i][j] = len(a.get_shortest_path(i, j))


# Remove element(n) from list(l) if (n) exists in (l)
def safe_remove(l, n):
    if n in l:
        l.remove(n)


# Functions to initialize nodes and connect them with their previous and next node
def init_nodes(n):
    # Declare neighbours as list
    neighbours = []

    # Link to previous node
    if n == c.START:
        neighbours.append(c.SIZE-1)
    else:
        neighbours.append(n-1)
        
    # Link to next node
    if n == c.SIZE-1:
        neighbours.append(c.START)
    else:
        neighbours.append(n+1)
    
    return neighbours


# Function to initialise the starting position of agent, prey and predator
def init_characters():
    c.AGENT_POS, pred_pos, prey_pos = random.sample(range(c.START, c.SIZE), 3)
    c.PREDATOR_POS = pred.predator(pred_pos)
    c.PREY_POS = prey.prey(prey_pos)


# Function to generate random graph
def generate_graph():
    graph = {}
    temp_graph = []

    # Create nodes
    for i in range(c.START, c.SIZE):
        graph[i] = init_nodes(i)
        temp_graph.append(i)

    # Loop until list is not empty
    while temp_graph:
        
        # Select a random node between 0 and n
        rand_node = random.randint(c.START, c.SIZE-1)

        # Check if the random node's degree is less than 3
        if len(graph[rand_node]) < 3:

            # Generate the possible connections
            poss_conn = []
            # Loop for 5 nodes before and 5 nodes after current node
            for i in range(rand_node-5, rand_node+6):
                if i < 0:
                    poss_conn.append(i + c.SIZE)
                elif i >= c.SIZE:
                    poss_conn.append(i % c.SIZE)
                else:
                    poss_conn.append(i)

            # Remove the random node, and the node 1 step ahead and 1 step backward from it
            safe_remove(poss_conn, rand_node)
            if rand_node == c.START:
                safe_remove(poss_conn, c.SIZE)
            else:
                safe_remove(poss_conn, rand_node+1)
            if rand_node == c.SIZE:
                safe_remove(poss_conn, c.START)
            else:
                safe_remove(poss_conn, rand_node-1)

            # Loop until there are no possible connections with less than degree 3
            while poss_conn:

                # Randomly select a node from the possible connections
                selection = random.choice(poss_conn)
                safe_remove(poss_conn, selection)

                # Check if the possible connection's degree is less than 3
                # print("graph[selection]: ", selection, " graph[rand_node]: ", rand_node)
                if len(graph[selection]) < 3:
                    # Add the random node and possible connection to each others neighbours sets
                    graph[selection].append(rand_node)
                    graph[rand_node].append(selection)
                    # print("graph[selection]: ", graph[selection], " graph[rand_node]: ", graph[rand_node])
                    # Break when the random node's degree goes to 3
                    break

        # Remove the random node and possible connection from the graph's copy so it doesn't come up again
        safe_remove(temp_graph, selection)
        safe_remove(temp_graph, rand_node)

    return graph


# Function for agent movement
def movement(agent_pos, prey_pos, pred_pos):
    # Dictionary to store distance of agent's neighbours' position to prey
    dist_from_prey = {}
    # Distance from agent's current position to prey
    dist_prey = len(a.get_shortest_path(agent_pos, prey_pos))
    # Dictionary to store distance of agent's neighbours' position to predator
    dist_from_pred = {}
    # Distance from agent's current position to predator
    dist_pred = len(a.get_shortest_path(pred_pos, agent_pos))

    # Loop to get distance from agent's neighbours to prey and predator
    for neighbour in c.GRAPH[c.AGENT_POS]:
        dist_from_prey[neighbour] = len(a.get_shortest_path(neighbour, prey_pos))
        dist_from_pred[neighbour] = len(a.get_shortest_path(pred_pos, neighbour))

    # Number of steps taken till now
    c.STEPS += 1

    return movement_rules(dist_prey, dist_pred, dist_from_prey, dist_from_pred)


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
            priority.append((7, c.AGENT_POS))

    # Get the neighbour with lowest number (highest priority)
    next_node = min(priority)

    # List to store all the neighbours with the highest priority
    poss_movement = []
    for i in priority:
        if i[0] == next_node[0]:
            poss_movement.append(i[1])

    # Return random among neighbours with highest priority
    return random.choice(poss_movement)


# Function to check if the agent is alive
def check_if_alive():
    if c.AGENT_POS == None:
        return False
    return c.AGENT_POS != c.PREDATOR_POS.position


# Function to check if agent won
def check_if_win():
    if c.AGENT_POS == None:
        return False
    return c.AGENT_POS == c.PREY_POS.position
