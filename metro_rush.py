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

    def add_train(self, train):
        if len(self.trains) < self.capacity:
            self.trains.insert(0, train)
            return True
        return False

    def remove_train(self):
        try:
            self.trains.pop(-1)
        except IndexError:
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
        self.num_turns = 0

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
            trains.append('T{}'.format(index))
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


class Node:
    def __init__(self, pos, parent, status=0, action=None, flag=False):
        self.pos = pos
        self.parent = parent
        self.status = status
        self.action = action
        self.flag = flag


###############################################################################


class BFS(Graph):
    def get_station_id(self, line_name, station_name):
        for index, station in enumerate(self.lines[line_name]):
            if station.name == station_name:
                return index + 1

    def check_another_lines(self, current_node, open_list):
        try:
            station_name = self.get_station(*current_node.pos).name
            lines = self.get_station(*current_node.pos).lines.copy()
            lines.remove(current_node.pos[0])
            while lines:
                another_line = lines.pop()
                if another_line not in self.lines:
                    continue
                station_id = self.get_station_id(another_line, station_name)
                open_list.append(Node([another_line, station_id], current_node,
                                      0, 'switch'))
        except TypeError:
            pass

    @staticmethod
    def check_left_node(current_node, open_list):
        try:
            if current_node.pos[1] > 1 and current_node.status != 1:
                next_pos = current_node.pos.copy()
                next_pos[1] -= 1
                open_list.append(Node(next_pos, current_node, -1, 'move'))
        except TypeError:
            pass

    def check_right_node(self, current_node, open_list):
        try:
            if current_node.pos[1] < len(self.lines[current_node.pos[0]]) \
                    and current_node.status != -1:
                next_pos = current_node.pos.copy()
                next_pos[1] += 1
                open_list.append(Node(next_pos, current_node, 1, 'move'))
        except TypeError:
            pass

    def check_neighbor_node(self, current_node, open_list):
        self.check_another_lines(current_node, open_list)
        self.check_left_node(current_node, open_list)
        self.check_right_node(current_node, open_list)

    @staticmethod
    def get_route(node):
        result = []
        while node.parent:
            result.append(node)
            node = node.parent
        result.append(node)
        return result[::-1]

    def find_all_path(self):
        open_list = [Node(self.start, None)]
        close_list = []
        while open_list:
            current_node = open_list.pop(0)
            if current_node.pos in close_list:
                continue
            if current_node.pos == self.end:
                self.paths.append(self.get_route(current_node))
                continue
            close_list.append(current_node.pos)
            self.check_neighbor_node(current_node, open_list)

    def print_trains_1(self):
        print('___Turn {}___'.format(self.num_turns))
        result = []
        for node in self.paths[0]:
            if node.action == 'switch':
                continue
            station = self.get_station(*node.pos)
            if not len(station.trains):
                continue
            result.append('{}({}:{})-{}'.format(station.name,
                                                node.pos[0],
                                                node.pos[1],
                                                ','.join(station.trains)))
        print('|'.join(result))

    def print_trains_2(self):
        print('___Turn {}___'.format(self.num_turns))
        result = [[], []]
        for index, path in enumerate(self.paths[:2]):
            for node in path:
                if node.action == 'switch':
                    continue
                station = self.get_station(*node.pos)
                if not len(station.trains):
                    continue
                result[index].append('{}({}:{})-{}'.format(
                    station.name, node.pos[0], node.pos[1],
                    ','.join(station.trains)))
            print('\t* Path {}:'.format(index + 1))
            print('|'.join(result[index]))

    @staticmethod
    def run_one_train(current_station, parent_station):
        if parent_station.trains:
            if current_station.add_train(parent_station.trains[-1]):
                parent_station.remove_train()

    def update_trains_1(self, index):
        for node in self.paths[index][:0:-1]:
            current_station = self.get_station(*node.pos)
            parent_station = self.get_station(*node.parent.pos)
            if node.action != 'move' or not parent_station.trains:
                continue
            if node.parent.action in [None, 'move']:
                self.run_one_train(current_station, parent_station)
            else:
                if node.parent.flag:
                    self.run_one_train(current_station, parent_station)
                node.parent.flag = not node.parent.flag

    def update_trains_2(self):
        for index in range(2):
            self.update_trains_1(index)

    def run_all_trains(self):
        self.print_trains_2()
        while len(self.get_station(*self.end).trains) < self.num_trains:
            self.update_trains_2()
            self.num_turns += 1
            self.print_trains_2()


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
    delhi.find_all_path()
    delhi.run_all_trains()
    print(len(delhi.paths[1]))


if __name__ == '__main__':
    start = time()
    main()
    print('Runtime: {}s'.format(round(time() - start, 5)))
