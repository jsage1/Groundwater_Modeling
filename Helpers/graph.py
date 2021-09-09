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
        file = path + "\\" + str(direction) + str(layer) + ".txt"
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
    def __init__(self, x, y, z):
        # initiates a node to be placed in grid
        # x y z values reprasent right, down, and foreward values respectively
        self.x = x
        self.y = y
        self.z = z


class GWGrid:
    def __init__(self):
        # initiating empty graph prior to insertion
        # this graph should contain a 3d array of Nodes representing
        # water flow from a section of a 3d plot of land
        self.graph = []
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

        # TODO: BUILD GRAPH FROM NODES
        for z in range(0, self.depth):
            templevel = []
            for y in range(0, self.width):
                temprow = []
                for x in range(0, self.length):
                    temprow.append(Node(0, 0, 0))
                templevel.append(temprow)
            self.graph.append(templevel)