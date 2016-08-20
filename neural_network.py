from __future__ import division
import random
import json
import math
from cube import Cube
import matplotlib.pyplot as plt

#network definitions:
input_size = 324 # =9*6*6, a whole lot of input states (0/1 per each cell-color combination)
num_hidden = 60 # num of neurons in hidden layer, big enough for our needs
output_size = 1
network_file = "network_dump_single1.json"
#training definitions:
num_runs = 400000
max_moves = 10

#math functions:
def sigmoid(t):
	return 1/(1+math.exp(-t))

def dot(v,w):
	return sum(v_i * w_i for v_i, w_i in zip(v,w))

def neuron_output(weights, inputs):
	return sigmoid(dot(weights, inputs))

#input/output manipulation:
def create_input(cube_data):
	return [1 if c==i else 0 for c in cube_data for i in range(6)]

def create_output(moves_length):
	output = [min(1,moves_length / max_moves)]
	return output

def parse_output(output):
	return output[0] * max_moves

#neural functions:
def feed_forward(neural_network, input_vector):
	outputs = []
	for layer in neural_network:
		input_with_bias = input_vector + [1]
		output = [neuron_output(neuron, input_with_bias) for neuron in layer]
		outputs.append(output)
		input_vector = output
	return outputs

def backpropagate(network, input_vector, targets):
	hidden_outputs, outputs = feed_forward(network, input_vector)
	
	#adjust weights for output layer:
	output_deltas = [output * (1-output) * (output-target) for output, target in zip(outputs, targets)]
	for i, output_neuron in enumerate(network[-1]):
		for j, hidden_output in enumerate(hidden_outputs + [1]):
			output_neuron[j] -= output_deltas[i] * hidden_output

	#backprop to hidden layer:
	hidden_deltas = [hidden_output * (1-hidden_output) * dot(output_deltas, [n[i] for n in network[-1]])
		for i, hidden_output in enumerate(hidden_outputs)]
	for i, hidden_neuron in enumerate(network[0]):
		for j, inp in enumerate(input_vector + [1]):
			hidden_neuron[j] -= hidden_deltas[i] * inp

# input/output state functions
def dump_network_to_file(network_file_name, network):
	file = open(network_file_name, "w")
	file.write("%s" % json.dumps(network))
	file.close()

def read_network_from_file(network_file_name):
	with open(network_file_name) as data_file:
		n = json.load(data_file)
	return n

def train_network(net_file = None):
	if net_file is not None:
		network = read_network_from_file(net_file)
	else:
		hidden_layer = [[random.uniform(-1,1) for _ in range(input_size+1)] for _ in range(num_hidden)]
		output_layer = [[random.uniform(-1,1) for _ in range(num_hidden+1)] for _ in range(output_size)]
		network = [hidden_layer, output_layer]

	for r in range(num_runs):
		# create a random cube:
		moves_length = random.randrange(max_moves+1)
		moves = ''.join([random.choice(Cube.moves) for _ in range(moves_length)])
		c = Cube(None, moves)

		# get the starting cube data
		cube_data = c.data_as_list()

		# input, target vectors:
		input_vector = create_input(cube_data)
		target_vector = create_output(moves_length)

		if (r % 500 == 0):
			res_before = predict(c,network)

		backpropagate(network, input_vector, target_vector)

		if (r % 500 == 0):
			res_after = predict(c,network)
			print r, c.data_as_string(), moves_length, "%.2f %.2f" % (res_before, res_after)

	return network

def predict(cube, network):
	input_vector = create_input(cube.data_as_list())
	return parse_output(feed_forward(network, input_vector)[-1])

#for training:
#n = train_network(network_file)
#dump_network_to_file(network_file, n)

#for solving:
#n = read_network_from_file(network_file)
#c = Cube()
#c.move('rLfDbUEsB')
#print predict(c, n)