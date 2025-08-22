//Assignment -2 
class State:
    def __init__(self, row, col, grid):
        self.row = row
        self.col = col
        self.grid = grid
        self.n = len(grid)

    def goalTest(self):
        return self.row == self.n - 1 and self.col == self.n - 1

    def moveGen(self):
        children = []
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for i, j in directions:
            ni = self.row + i
            nj = self.col + j
            if 0 <= ni < self.n and 0 <= nj < self.n:
                if self.grid[ni][nj] == 0:
                    children.append(State(ni, nj, self.grid))
        return children

    def __repr__(self):
        return f"'{self.row},{self.col}'"

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

    def __lt__(self, other):
        return (self.row, self.col) < (other.row, other.col)

def manhattan(state):
    goal = state.n - 1
    return abs(state.row - goal) + abs(state.col - goal)

def reconstructPath(node_pair, CLOSED):
    parent_map = dict(CLOSED)
    N, parent = node_pair
    path = [N]
    while parent is not None:
        path.append(parent)
        parent = parent_map.get(parent)
    path.reverse()
    return path

def best_first_search(start, heuristic=manhattan):
    OPEN = [(heuristic(start), start, None)]
    CLOSED = {}
    while OPEN:
        OPEN.sort(key=lambda x: x[0])
        _, current, parent = OPEN.pop(0)
        if current in CLOSED:
            continue
        CLOSED[current] = parent
        if current.goalTest():
            return reconstructPath((current, parent), CLOSED.items())
        for child in current.moveGen():
            if child not in CLOSED:
                OPEN.append((heuristic(child), child, current))
    return "No Path Found"

def a_star(start, heuristic=manhattan):
    OPEN = [(heuristic(start), 0, start, None)]
    CLOSED = {}
    while OPEN:
        OPEN.sort(key=lambda x: x[0])
        f, g, current, parent = OPEN.pop(0)
        if current in CLOSED:
            continue
        CLOSED[current] = parent
        if current.goalTest():
            return reconstructPath((current, parent), CLOSED.items())
        for child in current.moveGen():
            if child not in CLOSED:
                new_g = g + 1
                new_f = new_g + heuristic(child)
                OPEN.append((new_f, new_g, child, current))
    return "No Path Found"

grid = [
    [0, 0, 1],
    [0, 1, 1],
    [1, 0, 0]
]

start_state = State(0, 0, grid)
print("Best First Search: ",best_first_search(start_state))
print("A* Search: ", a_star(start_state))
