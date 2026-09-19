class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.cost = 0

    def __eq__(self, other):
        return self.position == other.position

def move(current_node, movement):
    return (current_node.position[0] + movement[0], current_node.position[1] + movement[1])

def check(current, neighbor, row, col, maze):
    r, c = neighbor
    if r < 0 or r >= row or c < 0 or c >= col:
        return False
    if maze[r][c] == 'x':
        return False
    if current.parent and neighbor == current.parent.position:
        return False
    return True

def print_path(maze, start, goal, solution_path):
    output = [row[:] for row in maze]
    output[start[0]][start[1]] = 'S'  # Start
    output[goal[0]][goal[1]] = 'G'    # Goal

    for r in range(len(output)):
        for c in range(len(output[r])):
            if output[r][c] == '0':
                output[r][c] = ' '

    for position in solution_path:
        r, c = position
        if output[r][c] not in ['S', 'G']:
            output[r][c] = '*'

    for row in output:
        print(' '.join(row))

def dfs(maze,row, col, start, goal, open_list):
    close_list = []
    solution_path = []
    current_node = Node(start)
    open_list.append(current_node)

    while open_list:
        current_node = open_list.pop(0)
        close_list.append(current_node)

        if current_node.position == goal:
            solution_path.append(current_node.position)
            while current_node.parent:
                current_node = current_node.parent
                solution_path.append(current_node.position)
            solution_path.reverse()
            return solution_path

        for movement in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = move(current_node, movement)
            if check(current_node, neighbor, row, col, maze):
                neighbor_node = Node(neighbor, current_node)
                open_list.append(neighbor_node)

def bfs(maze,row, col, start, goal, open_list):
    close_list = []
    solution_path = []
    current_node = Node(start)
    open_list.append(current_node)
    close_list.append(current_node)

    while open_list:
        current_node = open_list.pop(0)

        # If we reached the end
        if current_node.position == goal:
            solution_path.append(current_node.position)
            while current_node.parent:
                current_node = current_node.parent
                solution_path.append(current_node.position)
            solution_path.reverse()
            return solution_path

        # Explore neighbors
        for movement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            neighbor = move(current_node, movement)

            # Check if neighbor is valid
            if check(current_node, neighbor, row, col, maze):
                neighbor_node = Node(neighbor, current_node)
                open_list.append(neighbor_node)
                close_list.append(neighbor_node)


def main():
    maze = []
    with open('maze1.txt', 'r') as f:
        for line in f:
            processed_line = line.strip()
            maze.append(list(processed_line))

    row = len(maze)
    col = len(maze[0])
    open_list = []
    solution_path_m1 = [
        (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (2, 5),
        (2, 6), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (6, 8), (6, 9),
        (7, 9), (8, 9), (9, 9)
    ]

    start = (0, 0)
    goal = (9, 9)

    print("DFS Solution Path:")
    solution_path = dfs(maze,row, col, start, goal, open_list)
    print_path(maze, start, goal, solution_path)
    
    print("\nBFS Solution Path:")
    solution_path = bfs(maze,row, col, start, goal, open_list)
    print_path(maze, start, goal, solution_path)

if __name__ == "__main__":
    main()