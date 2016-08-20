from cube import Cube
from searchnode import SearchNode
import bfs
import neuralsearch
import random

c = Cube()
moves_length = 7
moves = ''.join([random.choice(Cube.moves) for _ in range(moves_length)])
c.move(moves)
print moves, c.data_as_string()

print 'Running'
#result = bfs.search(c)
result = neuralsearch.search(c)
if (result):
	print result.get_path()
	solved_cube = result.get_cube()
else:
	print 'No Solution'

#c.paint()
#solved_cube.paint()

# ideas:
# only one output?
# change learning pace (dynamic)
# in learning phase, start from different goal states - or 'turn' it around to have the middle-cube '0'
# limit to ~14 steps