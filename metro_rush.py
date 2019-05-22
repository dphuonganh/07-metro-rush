#!/usr/bin/env python3
from argparse import ArgumentParser
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


class Graph:
    def __init__(self):
        self.stations = {}
        self.lines = {}
        self.start = None
        self.end = None
        self.num_trains = 0
        self.paths = []
        self.trains_start = [0, 0]
        self.num_turns = 0
        self.circular_lines = set()
        self.output = []

    def get_station(self, line_name, station_id):
        try:
            return self.lines[line_name][station_id - 1]
        except KeyError:
            return None

    def create_line(self, line_name):
        if line_name not in self.lines:
            self.lines[line_name] = []

    def check_circular_line(self, line_name, station_name):
        try:
            if station_name == self.lines[line_name][0].name:
                self.circular_lines.add(line_name)
        except IndexError:
            pass

    def create_station(self, args, line_name):
        station_name, other_line_name = None, None
        if len(args) == 2:
            _, station_name = args
        elif len(args) == 4:
            _, station_name, _, other_line_name = args
        self.check_circular_line(line_name, station_name)
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
            return self.lines
        except (NameError, ValueError):
            exit_program()


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

    def check_left_node(self, current_node, open_list):
        try:
            n = len(self.lines[current_node.pos[0]])
            if current_node.pos[1] > 1 and current_node.status != 1:
                next_pos = current_node.pos.copy()
                next_pos[1] -= 1
                open_list.append(Node(next_pos, current_node, -1, 'move'))
            elif current_node.pos[0] in self.circular_lines \
                    and current_node.pos[1] == 1:
                next_pos = current_node.pos.copy()
                next_pos[1] = n - 1
                open_list.append(Node(next_pos, current_node, -1, 'move'))
        except TypeError:
            pass

    def check_right_node(self, current_node, open_list):
        try:
            n = len(self.lines[current_node.pos[0]])
            if current_node.pos[1] < n and current_node.status != -1:
                next_pos = current_node.pos.copy()
                next_pos[1] += 1
                open_list.append(Node(next_pos, current_node, 1, 'move'))
            elif current_node.pos[0] in self.circular_lines \
                    and current_node.pos[1] == n:
                next_pos = current_node.pos.copy()
                next_pos[1] = 2
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

    def get_constant(self):
        const = [1, 1]
        for i in range(2):
            for node in self.paths[i]:
                if node.action == 'switch':
                    const[i] = 2
                    break
        return const

    def get_cost_two_paths(self):
        c1, c2 = self.get_constant()
        cost1 = len(self.paths[0]) - 1 + self.trains_start[0] * c1
        cost2 = len(self.paths[1]) - 1 + self.trains_start[1] * c2
        return cost1, cost2

    def calculate_trains_start(self, algo):
        if len(self.paths) == 1 or algo == 0:
            self.trains_start[0] = self.num_trains
        elif len(self.paths) > 1:
            cost1, cost2 = self.get_cost_two_paths()
            for index in range(1, self.num_trains + 1):
                print(cost1, cost2)
                if cost1 <= cost2:
                    self.trains_start[0] += 1
                    cost1 += 2
                    continue
                self.trains_start[1] += 1
                cost2 += 2

    def print_trains_0(self):
        print('___Turn {}___'.format(self.num_turns))
        result = []
        temp = []
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
            temp.append(node.pos)
        self.output.append(temp.copy())
        print('\n'.join(result))

    def print_trains_1(self):
        print('___Turn {}___'.format(self.num_turns))
        result = [[], []]
        for index, path in enumerate(self.paths[:2]):
            temporary = []
            for node in path:
                if node.action == 'switch':
                    continue
                station = self.get_station(*node.pos)
                if not len(station.trains):
                    continue
                result[index].append('{}({}:{})-{}'.format(
                    station.name, node.pos[0], node.pos[1],
                    ','.join(station.trains)))
            self.output.append(temporary)
            print('\t* Path {}:'.format(index + 1))
            print('\n'.join(result[index]))

    def print_trains(self, algo):
        if algo == 0:
            self.print_trains_0()
        elif algo == 1:
            self.print_trains_1()

    @staticmethod
    def run_one_train(current_station, parent_station):
        if parent_station.trains:
            if current_station.add_train(parent_station.trains[-1]):
                parent_station.remove_train()
                return True
        return False

    def check_out_train(self, index):
        if self.trains_start[index] > 0:
            return True
        return False

    def update_trains_0(self, index=0):
        for node in self.paths[index][:0:-1]:
            current_station = self.get_station(*node.pos)
            parent_station = self.get_station(*node.parent.pos)
            if node.action != 'move' or not parent_station.trains:
                continue
            if node.parent.action == 'move':
                self.run_one_train(current_station, parent_station)
            elif not node.parent.action:
                if self.check_out_train(index):
                    if self.run_one_train(current_station, parent_station):
                        self.trains_start[index] -= 1
            else:
                if node.parent.flag:
                    self.run_one_train(current_station, parent_station)
                node.parent.flag = not node.parent.flag

    def update_trains_1(self):
        for index in range(2):
            self.update_trains_0(index)

    def update_trains(self, algo):
        try:
            if algo == 0:
                self.update_trains_0()
            elif algo == 1:
                self.update_trains_1()
        except IndexError:
            pass

    def run_all_trains(self, algo):
        self.print_trains(algo)
        while len(self.get_station(*self.end).trains) < self.num_trains:
            self.update_trains(algo)
            self.num_turns += 1
            self.print_trains(algo)


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


def get_arguments():
    parser = ArgumentParser(prog='Metro Network',
                            usage='[filename] --algo [ALGO] --gui')
    parser.add_argument('filename', help='A metro stations file')
    parser.add_argument('--algo', nargs='?', metavar='ALGO', default=0,
                        choices=[0, 1], type=int,
                        help='specify which algorithm to use for finding '
                             'the smallest number of turns')
    parser.add_argument('--gui', action='store_true',
                        help='visualize the Metro Network with Pyglet')
    return parser.parse_args()


###############################################################################


def main():
    args = get_arguments()
    delhi = BFS()
    delhi.create_graph(read_data_file(args.filename))
    delhi.find_all_path()
    delhi.calculate_trains_start(args.algo)
    delhi.run_all_trains(args.algo)
    # for i, y in enumerate(delhi.paths):
    #     print('\n__Path__', i + 1)
    #     for node in delhi.paths[i]:
    #         print(delhi.get_station(*node.pos).name)
    for x in delhi.output:
        print(x)
    if args.gui:
        from graphic import GUI
        GUI(delhi)


if __name__ == '__main__':
    start = time()
    main()
    print('Runtime: {}s'.format(round(time() - start, 5)))
