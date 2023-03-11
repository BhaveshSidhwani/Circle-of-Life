
import constants as c
import graph_operations as g


def agent():
    is_alive = True
    is_win = False
    # Loop until Agent CATCHES Prey or DIES or TIMES OUT
    while c.STEPS != c.TIME_OUT_STEPS and is_alive and not is_win:
        
        # Function call for agent movement
        c.AGENT_POS = movement(c.AGENT_POS, c.PREY_POS.position, c.PREDATOR_POS.position)
        is_win = g.check_if_win()       # Function call to check if the agent won
        is_alive = g.check_if_alive()   # Function call to check if the agent is alive

        if is_win:                      # If agent dies then break loop and return False
            print("Sucess!!!")
            return True
        elif not is_alive:              # If agent is alive and catches the prey
            print("Fail!!!")            # then break loop and return True
            return False
        elif c.STEPS == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
            print("Fail!!!")
            return False

        is_win = c.PREY_POS.movement()       # Function call for prey movement
        if is_win:                           # If agent is alive and catches the prey
            print("Success!!!")              # then break loop and return True
            return True

        is_alive = c.PREDATOR_POS.movement(c.AGENT_POS) # Function call for predator movement
        if not is_alive:                     # If agent dies then break loop and return False
            print("Fail!!!")
            return False
        
    return False

def movement(agent_pos, prey_pos, pred_pos):
    poss_moves = {}
    poss_moves[agent_pos] = c.U_star[(agent_pos, prey_pos, pred_pos)]
    for neighbour in c.GRAPH[agent_pos] + [agent_pos]:
        poss_moves[neighbour] = c.U_star[(neighbour, prey_pos, pred_pos)]
    
    best_move = min(poss_moves, key=poss_moves.get)
    c.STEPS += 1
    return best_move
