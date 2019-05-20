#!/usr/bin/env python3
from abc import ABC, abstractmethod
from sys import stderr
from time import time
from math import inf


###############################################################################


class Station:
    def __init__(self, station_name, line_name):
        self.name = station_name
        self.lines = {line_name}
        self.capacity = 1
        self.trains = []

    def add_line(self, line_name):
        self.lines.add(line_name)


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

    def switch_line(self):
        pass

    def move_station(self):
        pass


###############################################################################


class Graph(ABC):
    def __init__(self):
        self.stations = {}
        self.lines = {}
        self.start = None
        self.end = None
        self.num_trains = 0
        self.paths = []

    def get_station(self, line_name, station_id):
        try:
            return self.lines[line_name][station_id - 1]
        except KeyError:
            return None

    def create_line(self, line_name):
        if line_name not in self.lines:
            self.lines[line_name] = []

    def create_station(self, args, line_name):
        station_name, other_line_name = None, None
        if len(args) == 2:
            _, station_name = args
        elif len(args) == 4:
            _, station_name, _, other_line_name = args
        if station_name not in self.stations:
            self.stations[station_name] = Station(station_name, line_name)
        else:
            self.stations[station_name].add_line(other_line_name)
        if other_line_name:
            self.stations[station_name].add_line(other_line_name)
        self.lines[line_name].append(self.stations[station_name])

    def create_start_end(self, line_name, station_id):
        self.get_station(line_name, station_id).capacity = inf
        return [line_name, station_id]

    def setup_trains(self):
        trains = []
        for index in range(self.num_trains, 0, -1):
            trains.append(Train(index, self.start[0], self.start[1]))
        self.get_station(*self.start).trains = trains

    def create_graph(self, data):
        try:
            line_name = None
            for row in data:
                row = row.strip()
                if row.startswith('#'):
                    line_name = row[1:]
                    self.create_line(line_name)
                elif row.startswith('START'):
                    sep_pos = row.find(':')
                    self.start = self.create_start_end(row[6:sep_pos],
                                                       int(row[sep_pos + 1:]))
                elif row.startswith('END'):
                    sep_pos = row.find(':')
                    self.end = self.create_start_end(row[4:sep_pos],
                                                     int(row[sep_pos + 1:]))
                elif row.startswith('TRAINS'):
                    self.num_trains = int(row[7:])
                    self.setup_trains()
                elif row:
                    args = [arg.strip() for arg in row.split(':')]
                    self.create_station(args, line_name)
        except (NameError, ValueError):
            exit_program()

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
