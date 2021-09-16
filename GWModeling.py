#!/usr/bin/python3
from Helpers.GWGrid import GWGrid

# OPTION: set up path to files to bo be passed as cmd args


def main():
    # initialize class for graph
    x = GWGrid()
    # reading in data files from specified folders
    x.read_data("TestData/original")
    x.print_graph()
    return 0


if __name__ == "__main__":
    main()
