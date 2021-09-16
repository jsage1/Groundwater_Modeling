from os import listdir


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
        self.x = x  # right weight follows x axis
        self.y = y  # down weight follows y axis
        self.z = z  # forward weight follows z axis


class GWGrid:
    def __init__(self):
        # initiating empty graph prior to insertion
        # this graph should contain a 3d array of Nodes representing
        # water flow from a section of a 3d plot of land
        self.GWGraph = []
        # read in the
        self.depth = 0
        self.length = 0
        self.width = 0

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
                if len(layer) != self.width - 1:
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
                    if len(row) != self.length - 1:
                        raise Exception("Error: Improper Length of Right weights")
        # end of finally

        print("Creating 3d array with " + str(self.depth) + " Layers with dimensions: " +
              str(self.width) + " width, " + str(self.length) + " length.")

        for z in range(0, self.depth):
            temp_level = []
            for y in range(0, self.width):
                temp_row = []
                for x in range(0, self.length):
                    right = None
                    down = None
                    forward = forward_weight_string[z][y][x]
                    if x != self.length - 1:  # cant get right val
                        right = right_weight_string[z][y][x]
                    if y != self.width - 1:  # cant get down val
                        down = down_weight_string[z][y][x]
                    temp_row.append(Node(right, down, forward, 0))
                temp_level.append(temp_row)
            self.GWGraph.append(temp_level)
        print("Graph creation successful!")

    def print_graph(self):
        cstr = "Printing GWGraph"
        counter = 0
        print(cstr.center(40, '#'))
        for level in self.GWGraph:
            cstr = "Printing Level: " + str(counter)
            print(cstr.center(40, '-'))
            print("Right weights:")
            out_str = ""
            for row in level:
                for item in row:
                    if item.x is not None:
                        out_str = out_str + '{:4}'.format(item.x)
                out_str = out_str + '\n'
            print(out_str)
            print("Down weights:")
            out_str = ""
            for row in level:
                for item in row:
                    if item.y is not None:
                        out_str = out_str + '{:4}'.format(item.y)
                out_str = out_str + '\n'
            print(out_str)
            print("Forward weights:")
            print('\n'.join([''.join(['{:4}'.format(item.z) for item in row])
                             for row in level]))
            counter = counter + 1
