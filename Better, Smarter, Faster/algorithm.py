
from queue import Queue

import constants as c


# Function to reconstruct the shortest path found
def reconstruct(start, end, came_from):
    path = []
    path.append(end)

    # Backtrack and append the nodes in the shortest path found
    current = came_from[end]
    while current != start and came_from[current] != start:
        path.append(came_from[current])
        current = came_from[current]
    return path


# Function to get shortest path while avoiding predator using BFS
def get_shortest_path_avoiding_predator(start: int, end: int, pred_pos: int):
    # If start (agent) and end (prey) are same then return end
    if start == end:
        return [end]

    # If end (prey) and predator share the same location then move according to the odd agents
    # because in such a case odd agents move away from predator
    if end == pred_pos:
        return get_shortest_path(start, end)
    
    # Boolean variable for break condition
    is_run = True
    # BFS Queue
    node_queue = Queue()
    # Start node is put in the queue
    node_queue.put(start)
    # Dictionary used for backtracking
    came_from = {}
    # List to maintain the state of nodes ( Visited(false) or Not Visited(true) )
    not_visited = [True for _ in range(c.SIZE)]
    # Mark Visited on the start node and predator postion to exclude the predator node from exploration
    not_visited[start] = False
    not_visited[pred_pos] = False
    
    # Loop until a path is created from start node till end node
    while is_run:
        # Get first element from the queue for exploration
        current = node_queue.get()
        
        # Loop for each neighbour of current node
        for neighbour in c.GRAPH[current]:
            # Exlore the node if it is not visited yet
            if not_visited[neighbour]:
                # Add neighbour in backtracking dictionary
                came_from[neighbour] = current
                
                # If end is not reached then put the neighbour of current node in the queue
                if neighbour != end:
                    node_queue.put(neighbour)
                # If end is reached then set the break condition to False
                else:
                    is_run = False
                # Set the neighbour's state to visited(false)
                not_visited[neighbour] = False
    
    # Return the reconstructed path from start node to end node
    return reconstruct(start, end, came_from)


# Function to get shortest path using BFS
def get_shortest_path(start: int, end: int):
    # If start node and end node are same then return end
    if start == end:
        return []
    
    # Boolean variable for break condition
    run = True
    # BFS Queue
    node_queue = Queue()
    # Start node is put in the queue
    node_queue.put(start)
    # Dictionary used for backtracking
    came_from = {}
    # List to maintain the state of nodes ( Visited(false) or Not Visited(true) )
    not_visited = [True for _ in range(c.SIZE)]
    # Mark Visited on the start node
    not_visited[start] = False
    
    # Loop until a path is created from start node till end node
    while run:
        # Get first element from the queue for exploration
        current = node_queue.get()
        
        # Loop for each neighbour of current node
        for neighbour in c.GRAPH[current]:
            # Exlore the node if it is not visited yet
            if not_visited[neighbour]:

                # Add neighbour in backtracking dictionary
                came_from[neighbour] = current
                
                # If end is not reached then put the neighbour of current node in the queue
                if neighbour != end:
                    node_queue.put(neighbour)
                # If end is reached then set the break condition to False
                else:
                    run = False
                # Set the neighbour's state to visited(false)
                not_visited[neighbour] = False
    
    # Return the reconstructed path from start node to end node
    return reconstruct(start, end, came_from)
