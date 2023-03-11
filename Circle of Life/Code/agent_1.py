
import random

import algorithm as a
import constants as c
import graph_operations as g

def agent_1():
    is_alive = True
    is_win = False
    # Loop until Agent CATCHES Prey or DIES or TIMES OUT
    while c.STEPS != c.TIME_OUT_STEPS and is_alive and not is_win:
        
        # Function call for agent movement
        c.AGENT_POS = g.movement(c.AGENT_POS, c.PREY_POS.position, c.PREDATOR_POS.position)
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

        is_win = c.PREY_POS.movement()       # Function call for prey movement
        if is_win and is_alive:              # If agent is alive and catches the prey
            print("Success!!!")            # then break loop and return True
            return True

        is_alive = c.PREDATOR_POS.movement() # Function call for predator movement
        if not is_alive:                     # If agent dies then break loop and return False
            print("Fail!!!")
            return False
        
    return False
