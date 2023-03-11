
import pandas as pd
import os.path

import constants as c
import graph_operations as g
import Ustar as u

import agent as a
import agent_u_partial as ap

import v_agent as v
import v_partial_agent as vp

# Columns for data
agent_data = pd.DataFrame(columns = ["Graph No.", "Output", "Agent Pos", "Prey Pos", "Predator Pos", "Steps"])  # DataFrame for data collection

u.to_dict()
g.pre_load_dist()
true_count = 0
false_count = 0
output = False

for i in range(1, 3001):

    # Reseting constants for every experiment
    c.STEPS = 0

    # New positions for characters in every experiment
    g.init_characters()
    agent = c.AGENT_POS
    prey = c.PREY_POS.position
    pred = c.PREDATOR_POS.position
    
    # output = a.agent()
    # output = ap.agent_u_partial()
    
    # output = v.agent()
    # output = vp.agent()
    
    print(i)

    if output:
        true_count+=1
    else:
        false_count+=1
    row = pd.DataFrame([{"Graph No.": i, "Output": str(output), "Agent Pos": agent, "Prey Pos": prey, "Predator Pos": pred, "Steps": c.STEPS}])
    agent_data = pd.concat([agent_data, row], ignore_index=True)

print("Wins: ", true_count)
print("Fails: ", false_count)
# agent_data.to_csv(os.path.join("data", "Ustar_agent.csv"))
# agent_data.to_csv(os.path.join("data", "Ustar_partial_agent.csv"))

# agent_data.to_csv(os.path.join("data", "V_agent.csv"))
# agent_data.to_csv(os.path.join("data", "V_partial_agent.csv"))
