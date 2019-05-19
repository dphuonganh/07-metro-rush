#!/usr/bin/env python3
from time import time
from sys import stderr
from math import inf


class Station:
    def __init__(self, station_name, line_instance, capacity=1):
        self.station_name = station_name
        self.lines = {line_instance}
        self.capacity = capacity
        self.trains = set()

    def add_line(self, line):
        self.lines.add(line)

    def add_train(self, train):
        if len(self.trains) < self.capacity:
            self.trains.add(train)


class Line:
    def __init__(self, line_name):
        self.line_name = line_name
        self.instance_to_id = {}
        self.id_to_instance = {}

    def add_station(self, station):
        station_id = len(self.instance_to_id) + 1
        self.instance_to_id[station] = station_id
        self.id_to_instance[station_id] = station


class Train:
    def __init__(self, train_id, line_instance, station_id):
        self.train_label = 'T{}'.format(train_id)
        self.line = line_instance
        self.station = self.line.id_to_instance[station_id]


class Metro:
    def __init__(self):
        self.station_dict = {}
        self.line_dict = {}
        self.train_dict = {}
        self.start_station = None
        self.end_station = None

    def create_new_line(self, line_name):
        if line_name not in self.line_dict:
            self.line_dict[line_name] = Line(line_name)
        return self.line_dict[line_name]

    def create_new_station(self, args, current_line):
        if len(args) == 2:
            _, station_name = args
        elif len(args) == 4:
            _, station_name, _, other_line_name = args
            if other_line_name not in self.line_dict:
                self.line_dict[other_line_name] = Line(other_line_name)
        if station_name not in self.station_dict:
            self.station_dict[station_name] = \
                Station(station_name, current_line)
        if len(args) == 4:
            self.station_dict[station_name].add_line(
                self.line_dict[other_line_name])
        current_line.add_station(self.station_dict[station_name])

    def create_start_or_end_station(self, line_name, station_id, mode=False):
        if not mode:
            self.start_station = \
                self.line_dict[line_name].id_to_instance[station_id]
            self.start_station.capacity = inf
        else:
            self.end_station = \
                self.line_dict[line_name].id_to_instance[station_id]
            self.end_station.capacity = inf

    def setup_trains(self, num_trains, line_name, station_id):
        for train_id in range(1, num_trains + 1):
            self.train_dict[train_id] = Train(train_id,
                                              self.line_dict[line_name],
                                              station_id)
            self.start_station.add_train(self.train_dict[train_id])

    def build_metro(self, data):
        try:
            for row in data:
                row = row.strip()
                if row.startswith('#'):
                    current_line = self.create_new_line(row[1:])
                elif row.startswith('START'):
                    sep_pos = row.find(':')
                    line_name = row[6:sep_pos]
                    station_id = int(row[sep_pos + 1:])
                    self.create_start_or_end_station(line_name, station_id)
                elif row.startswith('END'):
                    sep_pos = row.find(':')
                    self.create_start_or_end_station(row[4:sep_pos],
                                                     int(row[sep_pos + 1:]),
                                                     True)
                elif row.startswith('TRAINS'):
                    self.setup_trains(int(row[7:]), line_name, station_id)
                elif row:
                    args = [arg.strip() for arg in row.split(':')]
                    self.create_new_station(args, current_line)
        except (NameError, ValueError):
            exit_program()

    def display_metro_info(self):
        print('Stations:')
        print(len(self.station_dict))
        print('Lines:')
        print(len(self.line_dict))
        print('Train:')
        print(len(self.train_dict))
        print('Start station:', self.start_station)
        print('End station:', self.end_station)


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
    delhi = Metro()
    delhi.build_metro(read_data_file('delhi-metro-stations'))
    delhi.display_metro_info()


if __name__ == '__main__':
    start = time()
    main()
    print('Runtime: {}s'.format(round(time() - start, 5)))
