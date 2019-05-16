#!/usr/bin/env python3
from time import time
from math import inf


class Station:
    def __init__(self, name, line, capacity=1):
        self.name = name
        self.lines = {line}
        self.capacity = capacity
        self.trains = set()

    def __str__(self):
        return '{}|{}|{}|{}'.format(self.name,
                                    self.lines,
                                    self.capacity,
                                    self.trains)

    def __hash__(self):
        return hash(self.name)

    # def __eq__(self, other):
    #     return self.name == other.name

    def add_line(self, line):
        self.lines.add(line)

    def add_train(self, train):
        if len(self.trains) < self.capacity:
            self.trains.add(train)

    def remove_train(self, train):
        try:
            self.trains.remove(train)
        except KeyError:
            pass

    def find_neighbor_stations(self):
        return


class Line:
    def __init__(self, name):
        self.name = name
        self.stations = {}
        self.ids = {}

    def __str__(self):
        stations_str = ['{}:{}'.format(key, value)
                        for key, value in self.stations.items()]
        ids_str = ['{}:{}'.format(key, value)
                   for key, value in self.ids.items()]
        return '{}:\n\t{}\n\t{}'.format(self.name,
                                        ', '.join(stations_str),
                                        ', '.join(ids_str))

    def __hash__(self):
        return hash(self.name)

    # def __getitem__(self, station_id):
    #     return self.ids[station_id]

    # def __contains__(self, station):
    #     return station in self.stations

    # def __iter__(self):
    #     return self.stations

    # def __eq__(self, other):
    #     return self.name == other.name

    def add_station(self, station):
        if station not in self.stations:
            new_id = len(self.stations) + 1
            self.stations[station] = new_id
            self.ids[new_id] = station


class Train:
    def __init__(self, train_id, line, station_id):
        self.id = train_id
        self.line = line
        self.station = line.ids[station_id]

    def __str__(self):
        return 'No.{} - {} - {}:{}'.format(self.id,
                                           self.line.name,
                                           self.line.stations[self.station],
                                           self.station.name)

    def move_station(self, next_station):
        if next_station in self.line:
            self.station = next_station

    def switch_line(self, new_line):
        if new_line in self.station.lines:
            self.line = new_line


class Metro:
    def __init__(self):
        self.stations = {}
        self.lines = {}
        self.trains = {}
        self.transfer_points = {}
        self.start_point = None
        self.end_point = None
        self.turns = 0

    def create_graph(self, filename):
        try:
            with open(filename, 'r') as file:
                for row in file:
                    row = row.strip()
                    if row.startswith('#'):
                        line_name = row[1:]
                        current_line = Line(line_name)
                        self.lines[line_name] = current_line
                    elif row.startswith('START'):
                        sep_pos = row.find(':')
                        start_name = row[6:sep_pos]
                        start_id = int(row[sep_pos + 1:])
                        self.start_point = self.lines[start_name].ids[start_id]
                        self.start_point.capacity = inf
                    elif row.startswith('END'):
                        sep_pos = row.find(':')
                        end_name = row[4:sep_pos]
                        end_id = int(row[sep_pos + 1:])
                        self.end_point = self.lines[end_name].ids[end_id]
                        self.end_point.capacity = inf
                    elif row.startswith('TRAINS'):
                        num_trains = int(row[7:])
                        for index in range(1, num_trains + 1):
                            train = Train(index,
                                          self.lines[start_name],
                                          start_id)
                            self.trains[index] = train
                            self.start_point.add_train(train)
                    elif row:
                        args = [arg.strip() for arg in row.split(':')]
                        if len(args) == 2:
                            station_id, station_name = args
                            station = Station(station_name, current_line)
                            current_line.add_station(station)
                            self.stations[station_name] = station
                        elif len(args) == 4:
                            station_id, station_name, _, other_line = args
                            if station_name in self.stations:
                                station = self.stations[station_name]
                            else:
                                station = Station(station_name, current_line)
                                self.stations[station_name] = station
                            current_line.add_station(station)
                            self.transfer_points[station_name] = station
                            if other_line not in self.lines:
                                self.lines[other_line] = Line(other_line)
                            station.add_line(self.lines[other_line])

        except (FileNotFoundError,
                PermissionError,
                IsADirectoryError,
                NameError,
                ValueError):
            pass


def main():
    delhi = Metro()
    delhi.create_graph('delhi-metro-stations')


if __name__ == '__main__':
    start = time()
    main()
    print('Runtime: {}s'.format(round(time() - start, 3)))
