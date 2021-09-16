# A class to store a graph edge
class Edge:
    def __init__(self, source, dest, weight):
        self.source = source
        self.dest = dest
        self.weight = weight


# A class to represent a graph object
class ADJlist:
    # Constructor
    def __init__(self, totalnodes, edges):
        # A list of lists to represent an adjacency list
        self.adjList = [[] for _ in range(totalnodes)]
        self.totalNodes = totalnodes
        # add edges to the undirected graph
        for edge in edges:
            self.adjList[edge.source].append(edge)

    # Function to print adjacency list representation of a graph
    def print_adjlist(self):
        for src in range(len(self.adjList)):
            # print current vertex and all its neighboring vertices
            if len(self.adjList[src]) != 0:
                for edge in self.adjList[src]:
                    print(f"({src} —> {edge.dest}, {edge.weight}) ", end='')
                print()

    # Perform DFS on the graph and set the departure time of all
    # vertices of the graph
    def dfs(self, v, discovered, departure, time):
        # mark the current node as discovered
        discovered[v] = True
        # set arrival time – not needed
        # time = time + 1
        # do for every edge `v —> u`
        for edge in self.adjList[v]:
            u = edge.dest
            # if `u` is not yet discovered
            if not discovered[u]:
                time = self.dfs(u, discovered, departure, time)
        # ready to backtrack
        # set departure time of vertex `v`
        departure[time] = v
        time = time + 1
        return time

    # The function performs the topological sort on a given DAG
    def topological_sort(self):
        # `departure` stores the vertex number using departure time as an index
        departure = [-1] * self.totalNodes

        # to keep track of whether a vertex is discovered or not
        discovered = [False] * self.totalNodes
        time = 0

        # perform DFS on all undiscovered vertices
        for i in range(self.totalNodes):
            if not discovered[i]:
                time = self.dfs(i, discovered, departure, time)

        # Process the vertices in topological order, i.e., in order
        # of their decreasing departure time in DFS
        for i in reversed(range(self.totalNodes)):
            # for each vertex in topological order,
            # relax the cost of its adjacent vertices
            v = departure[i]
            print(v, end=" ")
