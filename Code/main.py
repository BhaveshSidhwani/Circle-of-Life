
import pandas as pd
import os.path

import constants as c
import graph_operations as g

import agent_1 as a1
import agent_2 as a2
import agent_3 as a3
import agent_4 as a4
import agent_5 as a5
import agent_6 as a6
import agent_7 as a7
import agent_8 as a8
import agent_7a as a7a
import agent_8a as a8a
import agent_7b as a7b
import agent_8b as a8b

# Columns for data
agent_data = pd.DataFrame(columns = ["Graph No.", "Wins", "Losses", "Prey Found", "Predator Found"])  # DataFrame for data collection

# 30 Trials
for i in range(1,31):
    # win and loss count
    true_count = 0
    false_count = 0
    
    # Generate new graph for each trial
    c.GRAPH = g.generate_graph()

    # 100 experiments for each trial
    for j in range(100):
        # Reseting constants for every experiment
        c.PREY_CAUGHT_NUM = 0
        c.PRED_CAUGHT_NUM = 0
        c.STEPS = 0

        # New positions for characters in every experiment
        g.init_characters()
        output = False
        
        # Uncomment agent according to your need
        # output = a1.agent_1()
        # output = a2.agent_2()
        # output = a3.agent_3()
        # output = a4.agent_4()
        # output = a5.agent_5()
        # output = a6.agent_6()
        # output = a7.agent_7()
        # output = a7a.agent_7a()
        # output = a7b.agent_7b()
        # output = a8.agent_8()
        # output = a8a.agent_8a()
        # output = a8b.agent_8b()

        if output:
            true_count+=1
        else:
            false_count+=1
        row = pd.DataFrame([{"Graph No.": i, "Wins": true_count, "Losses": false_count, "Prey Found": c.PREY_CAUGHT_NUM, "Predator Found": c.PRED_CAUGHT_NUM}])
        agent_data = pd.concat([agent_data, row], ignore_index=True)

agent_data.to_csv(os.path.join("data", "Agent8-Raw.csv"))