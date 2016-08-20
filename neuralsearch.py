from __future__ import division
from Queue import PriorityQueue
from searchnode import SearchNode
import neural_network

def heuristic(node, n):
	steps = neural_network.predict(node.get_cube(), n)
	return steps

def search(initial_state):
	#load network from file:
	n = neural_network.read_network_from_file(neural_network.network_file)
	initial_node = SearchNode(initial_state, None, '')
	#initialize the frontier using the initial state of problem
	frontier = PriorityQueue()
	h = heuristic(initial_node, n)
	print "Search:", initial_state.data_as_string(), h
	frontier.put((h, initial_node))
	#initialize the explored set to be empty
	explored = set()
	#count loop iterations:
	visits = 0
	while True:
		visits += 1
		#if the frontier is empty then return failure
		if frontier.empty():
			return False
		#choose a leaf node and remove it from the frontier
		(f, node) = frontier.get()
		explored.add(node.state_to_string())
		if (visits % 500 == 0):
			print visits, node.get_path(), f, frontier.qsize(), node.state_to_string()
		#if the node contains a goal state
		if (node.is_goal()):
			#then return the corresponding solution
			print 'visits:', visits
			return node
		#add the node to the explored set
		#expand the chosen node and add the resulting nodes to the frontier only if not in the frontier or explored set
		for child in node.expand():
			if (child.state_to_string() not in explored):
				hc = heuristic(child, n)
				gc = len(node.get_path())
				frontier.put((gc+hc, child))
