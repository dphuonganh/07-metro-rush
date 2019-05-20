#!/usr/bin/env python3
from abc import ABC, abstractmethod
from sys import stderr
from time import time


###############################################################################


class Node:
    def __init__(self):
        pass


###############################################################################


class Train:
    def __init__(self, label, line_name, station_id):
        self.label = label
        self.line_name = line_name
        self.station_id = station_id

    def switch_line(self, line_name):
        self.line_name = line_name

    def move_station(self, station_id):
        self.station_id = station_id


###############################################################################


class Graph(ABC):
    def __init__(self):
        self.map = {}
        self.trains = []
        self.start = None
        self.end = None
        self.paths = []

    def create_graph(self, data):
        pass

    @abstractmethod
    def find_all_path(self):
        pass


###############################################################################


class BFS(Graph):
    def find_all_path(self):
        pass


###############################################################################


def exit_program():
    stderr.write('Invalid file\n')
    exit(1)


def read_data_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        exit_program()


###############################################################################


def main():
    delhi = BFS()
    delhi.create_graph(read_data_file('delhi-metro-stations'))


if __name__ == '__main__':
    start = time()
    main()
    print('Runtime: {}s'.format(round(time() - start, 5)))
