import numpy as np

import constants as c
import graph_operations as g
import Ustar as u
import pandas as pd
import ast
upartial_load = pd.read_csv("data/upartial_df.csv")

def to_file(o, file_name):
    with open((file_name + ".txt"), 'w') as f:
        print("\no: ", o)
        for value in o:
            f.write('%s\n' % (value))


def activation_function(x):
    return 1 / (1 + np.exp(-x))


def derived_activation_function(x):
    return x * (1 - x)


u.to_dict()
g.pre_load_dist()


infinity = 100000
lookup_table = []

train_outputs = np.array([c.U_star.values()]).T

train_input = []
train_outputs = []
for i in range(len(upartial_load)):
    state = ast.literal_eval(upartial_load["agent_pred"][i])
    util = float(upartial_load["utility"][i])
    belief = ast.literal_eval(upartial_load["beliefs"][i])

    agent, predator = state

    inputs_temp = [agent, predator] +[c.FULL_DIST[agent][predator]] + belief
    if inputs_temp not in train_input:
        if util < infinity:
            train_input.append(inputs_temp)
            train_outputs.append([util / 3])
        else:
            lookup_table.append(state)

train_outputs = np.array(train_outputs)
train_inputs = np.array(train_input)

weight1 = 1 * np.random.randn(53, 4)
weight12 = 1 * np.random.randn(4, 4)
weight23 = 1 * np.random.randn(4, 4)
weight34 = 1 * np.random.randn(4, 4)
weight4 = 1 * np.random.randn(4, 1)

err_mean = 100
while err_mean > 0.02:
    input_layer = np.dot(train_inputs, weight1)
    l2 = activation_function(input_layer)
    l3 = np.dot(l2, weight12)
    l4 = activation_function(l3)
    l5 = np.dot(l4, weight23)
    l6 = activation_function(l5)
    l7 = np.dot(l6, weight34)
    l8 = activation_function(l7)
    l9 = np.dot(l8, weight4)
    output = activation_function(l9)

    output_error = train_outputs - output
    output_delta = output_error * derived_activation_function(output)
    
    l2_error = output_delta.dot(weight4.T)
    l2_delta = l2_error * derived_activation_function(l2)
    
    l4_error = l2_delta.dot(weight12.T)
    l4_delta = l4_error * derived_activation_function(l4)

    l6_error = l4_delta.dot(weight23.T)
    l6_delta = l6_error * derived_activation_function(l2)

    l8_error = l6_delta.dot(weight34.T)
    l8_delta = l8_error * derived_activation_function(l2)
    
    weight1 += 0.01 * train_inputs.T.dot(l4_delta)
    weight12 += 0.01 * l2.T.dot(l2_delta)
    weight23 += 0.01 * l4.T.dot(output_delta)
    weight34 += 0.01 * l6.T.dot(output_delta)
    weight4 += 0.01 * l8.T.dot(output_delta)

    err_mean = np.mean(np.square(train_outputs - output))
    print("Loss: " + str(err_mean))

op = {}
to_file(str(weight1), "weight1_vp")
to_file(str(weight12), "weight12_vp")
to_file(str(weight23), "weight23_vp")
to_file(str(weight34), "weight34_vp")
to_file(str(weight4), "weight4_vp")
to_file(str(lookup_table), "lookup_table_vp")
op["weight12"] = weight12
op["weight23"] = weight23
op["weight34"] = weight34
op["weight4"] = weight4
op["lookup_table"] = lookup_table

print("\nweight1: ", weight1)
print("\nweight12: ", weight12)
print("\nweight23: ", weight23)
print("\nweight34: ", weight34)
print("\nweight4: ", weight4)

# to_file(op)
