from os import listdir
import flopy.utils.binaryfile as bf
from Helpers.ADJlist import Edge, ADJlist


# helper to fix negative zeros
def zero_fix(val):
    return round(val, 4) + 0


# helper function for formatting values for printing
def output_formatting(val):
    if val is None:
        return "N"
    return str(round(val, 4))


# getdepth: parses all files and returns the highest depth value of text files
def get_depth(files):
    depthvals = []
    for file in files:
        if file.endswith(".txt"):
            depthvals.append(int(file.split('.')[0][1:]))
    depthvals.sort(reverse=True)
    return depthvals[0]


# function to dynamically open files with specified direction for weights
def open_side(depth, direction, path):
    weights = []
    for layer in range(0, depth + 1):
        print("Opening file: " + str(direction) + str(layer) + ".txt")
        file = path + "/" + str(direction) + str(layer) + ".txt"
        f = open(file)
        temp_weights = []
        for line in f:
            temp_weights.append(  # Append the list of numbers to the result array
                [int(item)  # Convert each number to an integer
                 for item in line.split()  # Split each line of whitespace
                 ])
        weights.append(temp_weights)
    return weights


class Node:
    def __init__(self, x, y, z, name):
        # initiates a node to be placed in grid
        # x y z values reprasent right, down, and foreward values respectively
        self.name = name
        self.node_frac_through = 0
        self.x = x  # right weight follows x axis
        self.y = y  # down weight follows y axis
        self.z = z  # forward weight follows z axis


class GWGrid:
    def __init__(self):
        # initiating empty graph prior to insertion
        # this graph should contain a 3d array of Nodes representing
        # water flow from a section of a 3d plot of land
        self.GWGraph = []

        # object for adjlist
        self.adjlist = None
        self.topsortList = []
        # keys.
        # read in the
        self.depth = 0
        self.length = 0
        self.width = 0
        self.totalNodes = 0

    # readdata: takes in path to files
    # expects
    def read_data(self, path):
        files = listdir(path)
        highest_depth = get_depth(files)
        print("Reading in files with expected depth of: " + str(highest_depth))
        print("Reading in right edge values")
        right_weight_string = open_side(highest_depth, "r", path)
        # print(right_weight_string)
        print("Reading in down edge values")
        down_weight_string = open_side(highest_depth, "d", path)
        # print(down_weight_string)
        print("Reading in forward edge values")
        forward_weight_string = open_side(highest_depth, "f", path)
        # print(forward_weight_string)

        # COMPARE LEVELS TO ENSURE SAME L,W,H THROUGHOUT
        # throws error if any dimension is out of place
        try:
            self.depth = len(forward_weight_string)
            self.width = len(forward_weight_string[0])
            self.length = len(forward_weight_string[0][0])
        except Exception:
            raise Exception("Error in Front Weights level 0")
        finally:
            # ensuring that down weights match expected graph dimensions
            # width should be 1 less
            for layer in down_weight_string:
                if len(layer) != self.width :
                    raise Exception(
                        "Error: Improper Length of Down weights(expected: " + str(self.length) + ", got " +
                        str(len(layer)) + ".")
                for row in layer:
                    if len(row) != self.length:
                        raise Exception(
                            "Error: Improper Length of Down weights(expected: " + str(self.length) + ", got " +
                            str(len(layer)) + ".")
            # ensuring that right weights match expected graph dimensions
            # length should be 1 less
            for layer in right_weight_string:
                if len(layer) != self.width:
                    raise Exception("Error: Improper Width of Right weights")
                for row in layer:
                    if len(row) != self.length:
                        raise Exception("Error: Improper Length of Right weights")
        # end of finally

        print("Creating 3d array with " + str(self.depth) + " Layers with dimensions: " +
              str(self.width) + " width, " + str(self.length) + " length.")

        for z in range(0, self.depth):
            temp_level = []
            for y in range(0, self.width):
                temp_row = []
                for x in range(0, self.length):
                    forward = forward_weight_string[z][y][x]
                    right = right_weight_string[z][y][x]
                    down = down_weight_string[z][y][x]
                    temp_row.append(Node(right, down, forward, self.totalNodes))
                    self.totalNodes += 1
                temp_level.append(temp_row)
            self.GWGraph.append(temp_level)
        print("Graph creation successful!")

    def print_graph(self):
        cstr = "Printing GWGraph"
        counter = 0
        print(cstr.center(40, '#'))
        print("Total Nodes: " + str(self.totalNodes))
        for level in self.GWGraph:
            cstr = "Printing Level: " + str(counter)
            print(cstr.center(40, '-'))

            print("Right weights:")
            lines = []
            for row in level:
                lines.append(' '.join(output_formatting(val.x) for val in row))
            print('\n'.join(lines))

            print("Down weights:")
            lines = []
            for row in level:
                lines.append(' '.join(output_formatting(val.y) for val in row))
            print('\n'.join(lines))

            print("Forward weights:")
            lines = []
            for row in level:
                lines.append(' '.join(output_formatting(val.z) for val in row))
            print('\n'.join(lines))
            counter = counter + 1

    def create_adjlist(self):  # includes inner 0s
        edges = []
        for level in range(len(self.GWGraph)):
            for row in range(len(self.GWGraph[level])):
                for item in range(len(self.GWGraph[level][row])):
                    if self.GWGraph[level][row][item].x is not None:
                        edges.append(Edge(self.GWGraph[level][row][item].name,
                                          self.GWGraph[level][row][item + 1].name,
                                          self.GWGraph[level][row][item].x))
                    if self.GWGraph[level][row][item].y is not None:
                        edges.append(Edge(self.GWGraph[level][row][item].name,
                                          self.GWGraph[level][row + 1][item].name,
                                          self.GWGraph[level][row][item].y))
                    if self.GWGraph[level][row][item].z is not None:
                        edges.append(Edge(self.GWGraph[level][row][item].name,
                                          self.GWGraph[level + 1][row][item].name,
                                          self.GWGraph[level][row][item].z))
        self.adjlist = ADJlist(self.totalNodes, edges)

    def create_adjlist2(self):  # includes inner 0s
        edges = []
        for level in range(len(self.GWGraph)):
            for row in range(len(self.GWGraph[level])):
                for item in range(len(self.GWGraph[level][row])):
                    if self.GWGraph[level][row][item].x is not None and self.GWGraph[level][row][item].x != 0:
                        edges.append(Edge(self.GWGraph[level][row][item].name,
                                          self.GWGraph[level][row][item + 1].name,
                                          self.GWGraph[level][row][item].x))
                    if self.GWGraph[level][row][item].y is not None and self.GWGraph[level][row][item].y != 0:
                        edges.append(Edge(self.GWGraph[level][row][item].name,
                                          self.GWGraph[level][row + 1][item].name,
                                          self.GWGraph[level][row][item].y))
                    if self.GWGraph[level][row][item].z is not None and self.GWGraph[level][row][item].z != 0:
                        edges.append(Edge(self.GWGraph[level][row][item].name,
                                          self.GWGraph[level + 1][row][item].name,
                                          self.GWGraph[level][row][item].z))
        self.adjlist = ADJlist(self.totalNodes, edges)

    def print_adjlist(self):
        cstr = "Printing ADJlist"
        print(cstr.center(40, '#'))
        self.adjlist.print_adjlist()
        print()

    def topsort(self):
        cstr = "Printing Topological Sort"
        print(cstr.center(40, '#'))
        self.topsortList = self.adjlist.topological_sort()
        print()

    # binary data operations
    def read_data_bin(self, directory, modelname):
        print(f"reading in binary files from {directory}, with expected model name: {modelname}")
        # headobj = bf.HeadFile(f"{directory}/{modelname}.hds")
        # times = headobj.get_times()
        mytimes = [1.0, 101.0, 201.0]  # leaving in for now, eventually observing all times
        cbb = bf.CellBudgetFile(f"{directory}/{modelname}.cbc")
        frf = cbb.get_data(text='FLOW RIGHT FACE', totim=mytimes[1])[0]  # [1] is dtype, no other elements
        fff = cbb.get_data(text='FLOW FRONT FACE', totim=mytimes[1])[0]
        fbf = cbb.get_data(text='FLOW LOWER FACE', totim=mytimes[1])[0]
        # print(cbb.get_data(text='FLOW RIGHT FACE', totim=mytimes[1]))
        self.depth = len(frf)
        self.width = len(fff[0])
        self.length = len(fbf[0][0])
        # appending empty row at bottom
        self.totalNodes = 0
        print("Creating 3d array with " + str(self.depth) + " Layers with dimensions: " +
              str(self.width) + " width, " + str(self.length) + " length.")

        for z in range(0, self.depth):
            temp_level = []
            for y in range(0, self.width):
                temp_row = []
                for x in range(0, self.length):
                    right = None
                    down = None
                    forward = None
                    if x != self.length - 1:  # not at right edge of container
                        right = zero_fix(frf[z][y][x].item())
                    if y != self.width - 1:  # not at bottom edge of container
                        down = zero_fix(fbf[z][y][x].item())
                    if z != self.depth - 1:  # not at front edge of container
                        forward = zero_fix(fff[z][y][x].item())
                    temp_row.append(Node(right, down, forward, self.totalNodes))
                    self.totalNodes += 1
                temp_level.append(temp_row)
            self.GWGraph.append(temp_level)
        print("Graph creation successful!")

    # helper function for fraction through,
    # used to get from graph back to top sort
    def coords_from_name(self, name):
        nodes_per_level = (self.width * self.length)
        z = int(name / nodes_per_level)
        y = int((name - (nodes_per_level * z)) / self.length)
        x = int(name - ((nodes_per_level * z) + (self.length * y)))
        return z, y, x

    def fraction_through(self, target_node):
        # we check to see all the nodes that are upstream from the target node
        visited = self.adjlist.upstream_target(target_node)

        # get only nodes connected to target node and reverse to go upstream from target
        filt_top_order = [x for x in self.topsortList if visited[x]][::-1]

        # we are going to visit each node going upstream from target and calculate
        # fraction through.
        while filt_top_order:
            # derive coordinates from name
            z, y, x = self.coords_from_name(filt_top_order.pop())

            # check if current is start
            if self.GWGraph[z][y][x].name == target_node:
                # target node has 100% going through itself
                self.GWGraph[z][y][x].node_frac_through = 1.0
            else:
                # now checking other nodes
                # check x, y and z and do calculations for each
                # setting values to calculate flow
                x_downstream = 0
                y_downstream = 0
                z_downstream = 0
                x_downstream_mod = 0.0
                y_downstream_mod = 0.0
                z_downstream_mod = 0.0
                if self.GWGraph[z][y][x].x is not None and self.GWGraph[z][y][x].x != 0:
                    x_downstream = self.GWGraph[z][y][x].x
                    x_downstream_mod = float(x_downstream) * self.GWGraph[z][y][x+1].node_frac_through
                if self.GWGraph[z][y][x].x is not None and self.GWGraph[z][y][x].y != 0:
                    y_downstream = self.GWGraph[z][y][x].y
                    y_downstream_mod = float(y_downstream) * self.GWGraph[z][y+1][x].node_frac_through
                if self.GWGraph[z][y][x].x is not None and self.GWGraph[z][y][x].z != 0:
                    z_downstream = self.GWGraph[z][y][x].z
                    z_downstream_mod = float(z_downstream) * self.GWGraph[z+1][y][x].node_frac_through
                self.GWGraph[z][y][x].node_frac_through = \
                    (x_downstream_mod + y_downstream_mod + z_downstream_mod) / \
                    (x_downstream + y_downstream + z_downstream)

    def print_frac_through(self):
        cstr = "Printing fraction through"
        counter = 0
        print(cstr.center(40, '#'))
        print("Total Nodes: " + str(self.totalNodes))
        for level in self.GWGraph:
            cstr = "Printing Level: " + str(counter)
            print(cstr.center(40, '-'))
            lines = []
            for row in level:
                lines.append(' '.join(output_formatting(val.node_frac_through) for val in row))
            print('\n'.join(lines))
            counter = counter + 1
