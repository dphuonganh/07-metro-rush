#!/usr/bin/env python3
from sys import argv


class Station:
    def __init__(self, name, line=None, capacity=1):
        self.name = name
        self.line = line
        self.capacity = capacity


class Metro:
    def __init__(self, file_name):
        self.metro = self.build_metro(file_name)
        self.start = None
        self.end = None
        self.trains = None
    
    def build_metro(self, file_name):
        output = {}
        with open(file_name, 'r') as file_metro:
            current_line = ''
            for line in file_metro.readlines():
                if line.startswith('#'):
                    current_line = line[1:].rstrip()
                    output[current_line] = []
                elif line.startswith('START'):
                    self.start = line.split('=')[1]
                elif line.startswith('END'):
                    self.end = line.split('=')[1]
                elif line.startswith('TRAINS'):
                    self.trains = line.split('=')[1]
                else:
                    try:
                        output[current_line].append(line.split(':')[1].rstrip())
                    except IndexError:
                        pass
            print(self.start)
            return output


def main():
    graph = Metro('delhi-metro-stations')
    for x, y in graph.metro.items():
        print(x)
        print(y)
    print(graph.start)
    print(graph.end)
    print(graph.trains)


if __name__ == '__main__':
    main()