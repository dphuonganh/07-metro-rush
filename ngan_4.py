#!/usr/bin/env python3
from abc import ABC, abstractmethod
from sys import stderr
from time import time
from math import inf


class Station:
    def __init__(self, station_name, line_name, capacity=1):
        self.name = station_name
        self.lines = {line_name}
        self.capacity = capacity
        self.trains = []

    def add_line(self, line_name):
        self.lines.add(line_name)

    def add_train(self, train_label):
        if len(self.trains) < self.capacity:
            self.trains.insert(0, train_label)
            return True
        return False

    def remove_train(self):
        return self.trains.pop(-1)


class Metro(ABC):
    def __init__(self):
        self.stations = {}
        self.lines = {}
        self.start = None
        self.end = None
        self.num_trains = 0
        self.route = []

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
            self.stations[station_name].add_line(line_name)
        if other_line_name:
            self.stations[station_name].add_line(other_line_name)
        self.lines[line_name].append(self.stations[station_name])

    def create_start_point(self, line_name, station_id):
        self.start = [line_name, station_id]
        self.get_station(*self.start).capacity = inf

    def create_end_point(self, line_name, station_id):
        self.end = [line_name, station_id]
        self.get_station(*self.end).capacity = inf

    def setup_trains(self):
        self.get_station(*self.start).trains = \
            ['T{}'.format(index) for index in range(self.num_trains, 0, -1)]

    def get_station(self, line_name, station_id):
        return self.lines[line_name][station_id - 1]

    def build_metro(self, data):
        try:
            line_name = None
            for row in data:
                row = row.strip()
                if row.startswith('#'):
                    line_name = row[1:]
                    self.create_line(line_name)
                elif row.startswith('START'):
                    sep_pos = row.find(':')
                    self.create_start_point(row[6:sep_pos],
                                            int(row[sep_pos + 1:]))
                elif row.startswith('END'):
                    sep_pos = row.find(':')
                    self.create_end_point(row[4:sep_pos],
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
    def find_shortest_path(self):
        pass

    def move_trains_1(self):
        for index in range(len(self.route) - 1, 0, -1):
            cur_station = self.get_station(*self.route[index])
            pre_station = self.get_station(*self.route[index - 1])
            if pre_station.trains:
                if cur_station.add_train(pre_station.trains[-1]):
                    pre_station.remove_train()

    def display_turn(self, turn):
        print('Turn', turn)
        result = []
        for pos in self.route:
            station = self.get_station(*pos)
            if len(station.trains):
                result.append('{}({}:{})-{}'.format(
                    station.name, pos[0], pos[1], ','.join(station.trains)))
        print('|'.join(result))

    def update_turn(self):
        turn = 1
        self.display_turn(turn)
        while len(self.get_station(*self.end).trains) != self.num_trains:
            self.move_trains_1()
            turn += 1
            self.display_turn(turn)


class BFS(Metro):
    def find_shortest_path(self):
        self.route = [['Blue Line', 17],
                      ['Blue Line', 18],
                      ['Blue Line', 19],
                      ['Blue Line', 20],
                      ['Blue Line', 21]]


def exit_program():
    stderr.write('Invalid file\n')
    exit(1)


def read_data_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        exit_program()


def main():
    delhi = BFS()
    delhi.build_metro(read_data_file('delhi-metro-stations'))
    delhi.find_shortest_path()
    delhi.update_turn()


if __name__ == '__main__':
    start = time()
    main()
    print('Runtime: {}s'.format(round(time() - start, 5)))
