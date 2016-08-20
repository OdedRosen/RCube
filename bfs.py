from searchnode import SearchNode

def search(initial_state):
	initial_node = SearchNode(initial_state, None, '')
	#initialize the frontier using the initial state of problem
	frontier = [initial_node]
	#initialize the explored set to be empty
	explored = set()
	#count loop iterations:
	visits = 0
	while True:
		visits += 1
		#if the frontier is empty then return failure
		if not frontier:
			return False
		#choose a leaf node and remove it from the frontier
		node = frontier.pop(0)
		if (visits % 10000 == 0):
			print visits, node.get_path()
		#if the node contains a goal state
		if (node.is_goal()):
			#then return the corresponding solution
			print 'visits:', visits
			return node
		#add the node to the explored set
		explored.add(node.state_to_string())
		#expand the chosen node and add the resulting nodes to the frontier only if not in the frontier or explored set
		for child in node.expand():
			if (child.state_to_string() not in explored):
				frontier.append(child)
