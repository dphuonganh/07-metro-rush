from sys import stderr
from math import inf
from station import Station


def parse_station_info(args):
    station_name, other_line_name = None, None
    if len(args) == 2:
        _, station_name = args
    elif len(args) == 4:
        _, station_name, _, other_line_name = args
    return [station_name, other_line_name]


class Graph:
    def __init__(self):
        self.stations = {}
        self.lines = {}
        self.circular_lines = set()
        self.start, self.end = [None, None], [None, None]
        self.num_trains = 0

    def get_station(self, line_name, station_id):
        try:
            return self.lines[line_name][station_id - 1]
        except KeyError:
            return None

    def create_line(self, arg):
        if arg not in self.lines:
            self.lines[arg] = []
        return arg

    def check_circular_line(self, line_name, station_name):
        try:
            if station_name == self.lines[line_name][0].name:
                self.circular_lines.add(line_name)
        except IndexError:
            pass

    def setup_station(self, line_name, station_name, another_line_name):
        if station_name not in self.stations:
            self.stations[station_name] = Station(station_name, line_name)
        else:
            self.stations[station_name].add_line(line_name)
            self.stations[station_name].add_line(another_line_name)
        if another_line_name:
            self.stations[station_name].add_line(another_line_name)
        return self.stations[station_name]

    def create_station(self, line_name, args):
        station_name, other_line_name = parse_station_info(args)
        self.check_circular_line(line_name, station_name)
        self.lines[line_name].append(
            self.setup_station(line_name, station_name, other_line_name))

    def setup_start_end_point(self, line_name, station_id):
        self.get_station(line_name, station_id).capacity = inf
        return [line_name, station_id]

    def setup_trains(self, arg):
        self.num_trains = arg
        trains = []
        for index in range(arg, 0, -1):
            trains.append('T{}'.format(index))
        self.get_station(*self.start).trains = trains

    def analyze_and_store_data(self, input_data):
        line_name = None
        for row in input_data:
            row = row.strip()
            if row.startswith('#'):
                line_name = self.create_line(row[1:])
            elif row.startswith('START'):
                sep_pos = row.find(':')
                self.start = self.setup_start_end_point(
                    row[6:sep_pos], int(row[sep_pos + 1:]))
            elif row.startswith('END'):
                sep_pos = row.find(':')
                self.end = self.setup_start_end_point(
                    row[4:sep_pos], int(row[sep_pos + 1:]))
            elif row.startswith('TRAINS'):
                self.setup_trains(int(row[7:]))
            elif row:
                self.create_station(
                    line_name, [arg.strip() for arg in row.split(':')])

    def create_graph(self, input_data):
        try:
            self.analyze_and_store_data(input_data)
        except (NameError, ValueError):
            stderr.write('Invalid file\n')
            exit(1)
