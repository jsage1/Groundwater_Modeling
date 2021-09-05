# A class to store a graph edge
class Edge:
    def __init__(self, source, dest, weight):
        self.source = source
        self.dest = dest
        self.weight = weight
 
# A class to represent a graph object
class Graph:
    # Constructor
    def __init__(self, edges, N):
 
        # A list of lists to represent an adjacency list
        self.adjList = [[] for _ in range(N)]
 
        # add edges to the undirected graph
        for edge in edges:
            self.adjList[edge.source].append(edge)
 
# Function to print adjacency list representation of a graph
def printGraph(graph):
    for src in range(len(graph.adjList)):
        # print current vertex and all its neighboring vertices
        for edge in graph.adjList[src]:
            print(f"({src} —> {edge.dest}, {edge.weight}) ", end='')
        print()

# Perform DFS on the graph and set the departure time of all
# vertices of the graph
def DFS(graph, v, discovered, departure, time):
 
    # mark the current node as discovered
    discovered[v] = True
 
    # set arrival time – not needed
    # time = time + 1
 
    # do for every edge `v —> u`
    for edge in graph.adjList[v]:
 
        u = edge.dest
 
        # if `u` is not yet discovered
        if not discovered[u]:
            time = DFS(graph, u, discovered, departure, time)
 
    # ready to backtrack
    # set departure time of vertex `v`
    departure[time] = v
    time = time + 1
 
    return time
 
# The function performs the topological sort on a given DAG
def Topological_Sort(graph, N):
 
    # `departure` stores the vertex number using departure time as an index
    departure = [-1] * N
 
    # to keep track of whether a vertex is discovered or not
    discovered = [False] * N
    time = 0
 
    # perform DFS on all undiscovered vertices
    for i in range(N):
        if not discovered[i]:
            time = DFS(graph, i, discovered, departure, time)
 
    # Process the vertices in topological order, i.e., in order
    # of their decreasing departure time in DFS
    for i in reversed(range(N)):
 
        # for each vertex in topological order,
        # relax the cost of its adjacent vertices
        v = departure[i]
        print(v, end = " ")

# The function reads edge weight data from text files and stores them into lists
def get_edge_weights():
    # r_weights empty list declared
    r_weights = []
    with open('right.txt') as f:
        # Iterate through each line
        for line in f:
            r_weights.extend( # Append the list of numbers to the result array
                [int(item) # Convert each number to an integer
                for item in line.split() # Split each line of whitespace
                ])
    f.close()

    # d_weights empty list declared
    d_weights = []
    with open('down.txt') as f:
        # Iterate through each line
        for line in f:
            d_weights.extend( # Append the list of numbers to the result array
                [int(item) # Convert each number to an integer
                for item in line.split() # Split each line of whitespace
                ])
    f.close()

    # f_weights empty list declared
    f_weights = []
    with open('front.txt') as f:
        # Iterate through each line
        for line in f:
            f_weights.extend( # Append the list of numbers to the result array
                [int(item) # Convert each number to an integer
                for item in line.split() # Split each line of whitespace
                ])
    f.close()

    return r_weights, d_weights, f_weights

# The function stores all the edges into a list called edges (i, o, w)
def calculate_edges(): 

    num_of_lines = 0
    with open('right.txt') as f:
        # Iterate through each line
        for line in f:
            num_of_lines += 1
    f.close()
    total_nodes = num_of_lines + 1 
    total_nodes = total_nodes * total_nodes 
    new_num_lines = num_of_lines + 1 

    r_weight_counter = 0
    d_weight_counter = 0
    f_weight_counter = 0
    edges = []
    for i in range(0,total_nodes): 
        # Every right Edge
        if (i % new_num_lines != 3):
            if (i >= total_nodes - new_num_lines):
                edges.append((i,i+1,0)) # Dummy Node fill with empty edge weight of 0
                pass
            else:
                if (r_weights[r_weight_counter] < 0):
                    edges.append((i+1,i,abs(r_weights[r_weight_counter]))) # Flip verticies flow of water if negative
                    r_weight_counter = r_weight_counter + 1
                else:
                    edges.append((i,i+1,r_weights[r_weight_counter]))
                    r_weight_counter = r_weight_counter + 1  
        # Every down Edge
        if (i < total_nodes - new_num_lines):
            if (i % new_num_lines == 3):
                edges.append((i,i+new_num_lines,0)) # Dummy Node fill with empty edge weight of 0
            else: 
                if(d_weights[d_weight_counter] < 0):
                    edges.append((i+new_num_lines,i,d_weights[d_weight_counter])) # Flip verticies flow of water if negative
                    d_weight_counter = d_weight_counter + 1   
                else:
                    edges.append((i,i+new_num_lines,d_weights[d_weight_counter]))
                    d_weight_counter = d_weight_counter + 1   
        # Every front Edge
        if (i < total_nodes):
            if (i >= total_nodes - new_num_lines):
                edges.append((i,i+total_nodes,0)) # Dummy Node fill with empty edge weight of 0
            else: 
                if (i % new_num_lines == 3):
                    edges.append((i,i+total_nodes,0)) # Dummy Node fill with empty edge weight of 0 
                else:
                    if (f_weights[f_weight_counter] < 0):
                        edges.append((i+total_nodes,i,f_weights[f_weight_counter])) # Flip verticies flow of water if negative
                        f_weight_counter = f_weight_counter + 1
                    else:
                        edges.append((i,i+total_nodes,f_weights[f_weight_counter]))
                        f_weight_counter = f_weight_counter + 1

    total_nodes = total_nodes * 2 # Total nodes is now doubles
    return total_nodes, edges

# The function loops through the list of all edges to store into class Edge
def add_edges():
    all_edges = []

    for (i, o, w) in edges: 
        all_edges.append(Edge(i, o, w))
    
    return all_edges

r_weights, d_weights, f_weights = get_edge_weights() # weights is a list with right edge values
total_nodes, edges = calculate_edges() # Calulates total nodes and calculates every edge

all_edges = add_edges() # Store the list of all edges into the class Edge 
# build a graph from the given edges
graph = Graph(all_edges, total_nodes)
    
print("Adjacency list representation of the graph")
printGraph(graph)

print("The following is in topological sort order:")
Topological_Sort(graph, total_nodes)