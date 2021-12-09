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
        # add edges to the graph
        for edge in edges:
            self.adjList[edge.source].append(edge)

    # Prints an adjacency list of the graph
    def print_adjlist(self):
        for src in range(len(self.adjList)):
            if len(self.adjList[src]) != 0:
                for edge in self.adjList[src]:
                    print(f"[{src} —> {edge.dest}]", end='')
                print()

    # Perform DFS on the graph
    def dfs(self, v, discovered, departure, time):
        discovered[v] = True
        for edge in self.adjList[v]:
            u = edge.dest
            # if `u` is not yet discovered
            if not discovered[u]:
                time = self.dfs(u, discovered, departure, time)

        departure[time] = v
        time = time + 1
        return time

    # The function performs the topological sort on a given graph of flows
    def topological_sort(self):
        departure = [-1] * self.totalNodes
        discovered = [False] * self.totalNodes
        time = 0

        for i in range(self.totalNodes):
            if not discovered[i]:
                time = self.dfs(i, discovered, departure, time)

        return departure

    # Perform DFS on a reversed graph to find upstream nodes from target node
    def dfs_target(self, revadglist, v, discovered):
        # mark the current node as discovered
        discovered[v] = True
        # set arrival time – not needed
        # time = time + 1
        # do for every edge `v —> u`
        for edge in revadglist[v]:
            u = edge.dest
            # if `u` is not yet discovered
            if not discovered[u]:
                discovered = self.dfs_target(revadglist, u, discovered)
        return discovered

    # Perform DFS on the graph and set the departure time of all
    # vertices of the graph
    def upstream_target(self, target):
        rev_adj_list = [[] for _ in range(self.totalNodes)]
        discovered = [False] * self.totalNodes
        # reversing adjacency list to find all upstream nodes
        for src in range(len(self.adjList)):
            if len(self.adjList[src]) != 0:
                for edge in self.adjList[src]:
                    temp_edge = Edge(edge.dest, src, edge.weight)
                    rev_adj_list[edge.dest].append(temp_edge)

        return self.dfs_target(rev_adj_list, target, discovered)
