#!/usr/bin/python3
from Helpers.graph import GWGrid

# TODO: set up path to files to bo be passed as cmd args


def main():
    x = GWGrid()
    x.readdata("TestData")
    return 0


if __name__ == "__main__":
    main()
