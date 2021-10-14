#!/usr/bin/python3
from Helpers.GWGrid import GWGrid

def main():
    # initialize class for graph
    x = GWGrid()
    # reading in data files from specified folders
    x.read_data_bin("TestData/binfiles/Test01", "Test01")
    #x.read_data("TestData/txtfiles/original")
    x.print_graph()
    x.create_adjlist2()
    x.print_adjlist()
    x.topsort()

    return 0


if __name__ == "__main__":
    main()
