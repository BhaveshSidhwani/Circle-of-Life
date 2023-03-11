import numpy as np

import constants as c
import graph_operations as g
import Ustar as u


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

infinity = 100000000
lookup_table = []

weight1 = 1 * np.random.randn(3, 4)
weight12 = 1 * np.random.randn(4, 4)
weight23 = 1 * np.random.randn(4, 4)
weight34 = 1 * np.random.randn(4, 4)
weight4 = 1 * np.random.randn(4, 1)

train_outputs = np.array([c.U_star.values()]).T

train_input = []
train_outputs = []
for state, util in c.U_star.items():
    agent, prey, predator = state

    inputs_temp = [c.FULL_DIST[agent][prey], c.FULL_DIST[agent][predator], c.FULL_DIST[prey][predator]]
    if inputs_temp not in train_input:
        if c.U_star[state] < infinity:
            train_input.append(inputs_temp)
            train_outputs.append([c.U_star[state] / 3])
        else:
            lookup_table.append(state)

train_outputs = np.array(train_outputs)
train_inputs = np.array(train_input)

err = 100
while err > 0.02:
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
    
    l2_err = output_delta.dot(weight4.T)
    l2_delta = l2_err * derived_activation_function(l2)
    
    l4_err = l2_delta.dot(weight12.T)
    l4_delta = l4_err * derived_activation_function(l4)

    l6_err = l4_delta.dot(weight23.T)
    l6_delta = l6_err * derived_activation_function(l2)

    l8_err = l6_delta.dot(weight34.T)
    l8_delta = l8_err * derived_activation_function(l2)
    
    weight1 += 0.01 * train_inputs.T.dot(l4_delta)
    weight12 += 0.01 * l2.T.dot(l2_delta)
    weight23 += 0.01 * l4.T.dot(output_delta)
    weight34 += 0.01 * l6.T.dot(output_delta)
    weight4 += 0.01 * l8.T.dot(output_delta)

    err = np.mean(np.square(train_outputs - output))
    print("Loss: " + str(err))


to_file(str(weight1), "weight1")
to_file(str(weight12), "weight12")
to_file(str(weight23), "weight23")
to_file(str(weight34), "weight34")
to_file(str(weight4), "weight4")
to_file(str(lookup_table), "lookup_table")

print("\nweight1: ", weight1)
print("\nweight12: ", weight12)
print("\nweight23: ", weight23)
print("\nweight34: ", weight34)
print("\nweight4: ", weight4)
