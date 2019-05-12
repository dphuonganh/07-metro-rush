#!/usr/bin/env python3
from sys import argv


class Station:
    def __init__(self, name, line=None, capacity=1):
        self.name = name
        self.line = line
        self.capacity = capacity


class Metro:
    def __init__(self, file_name):
        self.start = None
        self.end = None
        self.trains = None
        self.metro = self.build_metro(file_name)
    
    def build_metro(self, file_name):
        output = {}
        with open(file_name, 'r') as file_metro:
            current_line = ''
            for line in file_metro.readlines():
                if line.startswith('#'):
                    current_line = line[1:].rstrip()
                    output[current_line] = []
                elif line.startswith('START'):
                    self.start = line.split('=')[1].split(':')
                    self.start[1] = int(self.start[1])
                elif line.startswith('END'):
                    self.end = line.split('=')[1].split(':')
                    self.end[1] = int(self.end[1])
                elif line.startswith('TRAINS'):
                    self.trains = int(line.split('=')[1])
                    output[self.start[0]][self.start[1]-1].capacity = self.trains
                    output[self.end[0]][self.end[1]-1].capacity = self.trains
                else:
                    try:
                        line = line.split(':')
                        if len(line) > 2:
                            output[current_line].append(Station(line[1].rstrip(), line=line[3].strip()))
                        else:
                            output[current_line].append(Station(line[1].rstrip()))
                    except IndexError:
                        pass
            return output


def main():
    graph = Metro('delhi-metro-stations')
    for x in graph.metro.values():
        for y in x:
            print(y.name, 234, y.line, 123)
    print(graph.start)
    print(graph.end)
    print(graph.trains)


if __name__ == '__main__':
    main()