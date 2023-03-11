
import ast

import algorithm as a
import constants as c
import graph_operations as g


def U_star():
    states = []
    Ustar_old = {}

    infinity = 100000000

    # Generate graph
    c.GRAPH = g.generate_graph()
    g.pre_load_dist()
    with open("Graph.txt", 'w') as f:
        for key, value in c.GRAPH.items():
            f.write('%s: %s\n' % (key, value))

    # Initialize U* with distance from agent to prey
    for agent_p in range(0, c.SIZE):
        for prey_p in range(0, c.SIZE):
            for pred_p in range(0, c.SIZE):
                states.append((agent_p, prey_p, pred_p))

                if agent_p == pred_p and agent_p != prey_p:
                    Ustar_old[states[-1]] = infinity
                elif agent_p == prey_p:
                    Ustar_old[states[-1]] = 0
                else:
                    Ustar_old[states[-1]] = c.FULL_DIST[agent_p][prey_p]

    print(Ustar_old)
    with open("Ustar_old.txt", 'w') as f:
        for key, value in Ustar_old.items():
            f.write('%s: %s\n' % (key, value))

    # Cost of moving is 1
    reward = 1
    Ustar_new = Ustar_old.copy()

    err = 0
    # Convergence condition
    while True:
        err = 0

        # For every state in states
        for state in states:
            # print("state: ", state)
            # Unpack tuple
            agent_state, prey_state, pred_state = state

            # Prey Probability
            prey_prob = 1 / ( len(c.GRAPH[prey_state]) + 1 )

            Ustar_temp = infinity

            for agent in c.GRAPH[agent_state] + [agent_state]:
                dist = {}
                # Loop to get shortest path to agent for all neighbours of the predator
                for neighbour in c.GRAPH[pred_state]:
                    dist[neighbour] = c.FULL_DIST[neighbour][agent]
                # Get the node with minimum distance from the list
                min_dist_node = min(dist, key=dist.get)
                min_dist = []
                # Loop for getting all the neighbours with the shortest distance to the agent
                for i in dist:
                    if dist[i] == dist[min_dist_node]:
                        min_dist.append(i)
                sum = reward

                for pr in c.GRAPH[prey_state] + [prey_state]:

                    for pd in c.GRAPH[pred_state]:
                        pred_prob = 0
                        if pd in min_dist:
                            pred_prob = ( 0.6 * ( 1 / len(min_dist) ) )

                        pred_prob += ( 0.4 * (1 / len(c.GRAPH[pd])) )

                        transition_prob = prey_prob * pred_prob
                        sum += (Ustar_old[(agent, pr, pd)] * transition_prob)

                Ustar_temp = min(Ustar_temp, sum)
            
            if agent_state == prey_state:
                Ustar_temp = 0
            elif agent_state == pred_state or abs(agent - pred_state) == 1:
                Ustar_temp = infinity

            Ustar_new[state] = Ustar_temp

            err = max(err, abs(Ustar_new[state] - Ustar_old[state]))

            Ustar_old = Ustar_new.copy()
        print(err)
        if err < 0.005:
            break

    with open("Ustar_new.txt", 'w') as f:
        for key, value in Ustar_new.items():
            f.write('%s: %s\n' % (key, value))


def to_dict():
    with open('Ustar.txt') as f:
        lines = f.readlines()

        d = {}
        for line in lines:
            key, value = line.split(':')
            d[ast.literal_eval(key)] = float(value)

    c.U_star = d




# U_star()
