from os import listdir


class Node:
    def __init__(self):
        # initiates a node to be placed in grid
        self.x = 0


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

    # readdata:
    def readdata(self, path):
        print("reading in data from:")
        files = listdir(path)
        files.sort()
        for filename in files:
            print(path+"\\"+filename)
            infile = open(path + "\\" + filename)

