class Person:
    def __init__(self, name, position, time):
        self.name = name
        self.position = position
        self.time = time 

    def duplicate(self):
        return Person(self.name, self.position, self.time)

    def __str__(self):
        return f"{self.name}({self.position})"

class Main:
    def __init__(self, persons, umbrella, total_time=0, path=None):
        self.persons = persons 
        self.umbrella = umbrella
        self.total_time = total_time
        self.path = path if path else []

    def goalTest(self):
        for p in self.persons:
            if p.position == 'L':
                return False 
        return self.total_time <60

    def moveGen(self):
        children = []
        current_side = self.umbrella
        opposite_side = 'R' if current_side == 'L' else 'L'
        people = [p for p in self.persons if p.position == current_side]

        if current_side == 'L':
            for i in range(len(people)):
                for j in range(i+1, len(people)):
                    p1, p2 = people[i], people[j]
                    crossing_time = max(p1.time, p2.time)
                    if self.total_time + crossing_time < 60:
                        new_persons = [p.duplicate() for p in self.persons]
                        for p in new_persons:
                            if p.name == p1.name or p.name == p2.name:
                                p.position = opposite_side
                        new_path = self.path + [f"{p1.name} & {p2.name} cross --> {crossing_time}"]
                        child = Main(new_persons, opposite_side, self.total_time + crossing_time, new_path)
                        children.append(child)

        else:
            for p in people:
                return_time = p.time
                if self.total_time + return_time <60:
                    new_persons = [x.duplicate() for x in self.persons]
                    for x in new_persons:
                        if x.name == p.name:
                            x.position = opposite_side
                    new_path = self.path + [f"{p.name} returns <-- {return_time}"]
                    child = Main(new_persons, opposite_side, self.total_time + return_time, new_path)
                    children.append(child)

        return children

    def __str__(self):
        left = [p.name for p in self.persons if p.position == 'L']
        right = [p.name for p in self.persons if p.position == 'R']
        return f"Left: {left} | Right: {right} | Umbrella: {self.umbrella} | Time: {self.total_time}"

    def __eq__(self, other):
        if not isinstance(other, Main):
            return False
        return self.persons_state() == other.persons_state() and self.umbrella == other.umbrella

    def __hash__(self):
        return hash((tuple(self.persons_state()), self.umbrella))

    def persons_state(self):
        return tuple(sorted((p.name, p.position) for p in self.persons))

def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, parent in OPEN]
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
    path.reverse()
    print("\n--- Solution Path ---")
    for state in path:
        print(state)
    print("\n--- Movements ---")
    for move in path[-1].path:
        print(move)
    print(f"Total Time Taken: {path[-1].total_time}")
    return path

def bfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair
        if N.goalTest():
            print("Goal is found!\n")
            reconstructPath(node_pair, CLOSED)
            return
        else:
            CLOSED.append(node_pair)
            children = N.moveGen()
            new_nodes = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(node, N) for node in new_nodes]
            OPEN = OPEN + new_pairs
    print("No solution found.")
    return []

# Initial Setup
amol = Person("amol", "L", 5)
ameya = Person("ameya", "L", 10)
grandfather = Person("grandfather", "L", 25)
grandmother = Person("grandmother", "L", 20)

start_state = Main([amol, ameya, grandfather, grandmother], umbrella='L', total_time=0, path=[])
bfs(start_state)

