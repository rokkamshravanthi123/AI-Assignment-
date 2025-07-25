class State:
	def __init__(self,state):
		self.state = state
	
	def goalTest(self):
		return self.state == ['b','b','b','_','a','a','a']
		
	def moveGen(self):
		children = []
		for i in range(len(self.state)):
			current = self.state[i]
			#left to right
			if current == 'a':
				#one stone at once
				if i+1<7 and self.state[i+1] =='_':
					new_state = list(self.state)
					new_state[i],new_state[i+1] = new_state[i+1], new_state[i]
					new_child  = State(new_state)
					children.append(new_child)
				
				#2 stones at once
				if i+2 <7 and self.state[i+2] =='_' and self.state[i+1] in ['b']:
					new_state = list(self.state)
					new_state[i],new_state[i+2] = new_state[i+2], new_state[i]
					new_child  = State(new_state)
					children.append(new_child)
			#right to left	
			elif current == 'b':
				#one stone at once
				if i-1 >= 0 and self.state[i-1] =='_':
					new_state = list(self.state)
					new_state[i],new_state[i-1] = new_state[i-1], new_state[i]
					new_child  = State(new_state)
					children.append(new_child)
				
				#2 stones at once
				if i-2 >=0 and self.state[i-2] =='_' and self.state[i-1] in ['a']:
					new_state = list(self.state)
					new_state[i],new_state[i-2] = new_state[i-2], new_state[i]
					new_child  = State(new_state)
					children.append(new_child)
	
		return children
	
	
	def __eq__(self,current):
		return self.state == current.state
	
	def __hash__(self):
		return hash(tuple(self.state))
	
	def __str__(self):
		return ''.join(self.state)
	
def removeSeen(children, OPEN, CLOSED):
	open_nodes  = [node for node, parent in OPEN]
	closed_nodes = [node for node, parent in CLOSED]
	new_nodes = [node for node in children if node not in open_nodes and node not in closed_nodes]
	return new_nodes

def reconstructPath(node_pair, CLOSED):
	parent_map = {} 
	for node, parent in CLOSED:
		parent_map[node] = parent    
	N, parent = node_pair
	path = [N]
    
	while parent is not None:
		path.append(parent)
		parent = parent_map[parent]
    
    # path = path.reverse()
	print(" <- \n ".join([str(e) for e in path]))
    
	return path


def bfs(start):
	OPEN = [(start,None)]
	CLOSED = []
	while OPEN:
		node_pair = OPEN.pop(0)
		N,parent = node_pair
		if N.goalTest():
			print("Goal is found!")
			path = reconstructPath(node_pair, CLOSED)
			return 
		else:
			CLOSED.append(node_pair)
			children = N.moveGen()
			new_nodes = removeSeen(children, OPEN, CLOSED)
			new_pairs = [(node, N) for node in new_nodes]
			OPEN =OPEN + new_pairs
            		
	return []	


def dfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair
        # print(N, parent)
        if N.goalTest():
            print("Goal is found")
            path = reconstructPath(node_pair, CLOSED)
            return
        else:
            CLOSED.append(node_pair)
            children = N.moveGen()
            new_nodes = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(node, N) for node in new_nodes]
            OPEN = new_pairs + OPEN
         
    return []

start = ['a','a','a','_','b','b','b']
start_state = State(start)
print("Using BFS the traversal would be as follows:\n")
bfs(start_state)
print("Using DFS the traversal would be as follows:\n")
dfs(start_state)



