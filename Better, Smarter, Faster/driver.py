
import constants as c
import graph_operations as g
import Ustar as u

import agent as a
import agent_u_partial as ap

import agent_compare as ac
import agent_compare_partial as acp

import v_agent as v
import v_partial_agent as vp


# Initialise the character's starting location
g.init_characters()

u.to_dict()
g.pre_load_dist()

# Print the graph and character's position
print("GRAPH", c.GRAPH)
print("Character position:")
print("Agent position: ", c.AGENT_POS)
print(c.PREDATOR_POS)
print(c.PREY_POS)


# a.agent()
# ap.agent_u_partial()

# v.agent()
# vp.agent()

# ac.agent_compare()
# acp.agent_compare()
