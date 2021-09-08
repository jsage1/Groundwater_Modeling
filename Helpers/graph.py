from os import listdir


# getdepth: parses all files and returns the highest depth value of text files
def getdepth(files):
    depthvals = []
    for file in files:
        if file.endswith(".txt"):
            depthvals.append(int(file.split('.')[0][1:]))
    depthvals.sort(reverse=True)
    return depthvals[0]


# function to dynamically open files with specified direction for weights
def openside(depth, direction, path):
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
    def __init__(self):
        # initiates a node to be placed in grid
        # x y z values reprasent right, down, and foreward values respectively
        self.x = 0
        self.y = 0
        self.z = 0


class GWGrid:
    def __init__(self):
        # initiating empty graph prior to insertion
        # this graph should contain a 3d array of Nodes representing
        # water flow from a section of a 3d plot of land
        self.graph = []
        # read in the
        self.RightWeightString = []
        self.DownWeightString = []
        self.ForwardWeightString = []

    # readdata: takes in path to files
    # expects
    def readdata(self, path):
        print("reading in data from:")
        files = listdir(path)
        highest_depth = getdepth(files)
        print("Reading in files with expected depth of: " + str(highest_depth))
        print("Reading in right edge values")
        self.RightWeightString = openside(highest_depth, "r", path)
        print(self.RightWeightString)
        print("Reading in down edge values")
        self.DownWeightString = openside(highest_depth, "d", path)
        print(self.DownWeightString)
        print("Reading in forward edge values")
        self.ForwardWeightString = openside(highest_depth, "f", path)
        print(self.ForwardWeightString)

        # TODO: COMPARE LEVELS TO ENSURE SAME L,W,H THROUGHOUT
        # TODO: BUILD GRAPH FROM NODES