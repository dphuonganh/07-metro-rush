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
                    self.start[1] = int(self.start[1]) - 1
                elif line.startswith('END'):
                    self.end = line.split('=')[1].split(':')
                    self.end[1] = int(self.end[1]) - 1
                elif line.startswith('TRAINS'):
                    self.trains = int(line.split('=')[1])
                    output[self.start[0]][self.start[1]].capacity = self.trains
                    output[self.end[0]][self.end[1]].capacity = self.trains
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


class node:
    def __init__(self, position, run, parent):
        self.position = position
        self.run = run
        self.parent = parent
    
    def __eq__(self, other):
        return self.position == other.position


def find_index(metro, line, position):
    for x, y in enumerate(metro[line]):
        if y.name == metro[position[0]][position[1]].name:
            return x


def check_node_anoline(metro, cur_node, open_list):
    try:
        print(cur_node.position)
        if metro[cur_node.position[0]][cur_node.position[1]].line:
            ano_line = metro[cur_node.position[0]][cur_node.position[1]].line
            # print(ano_line)
            index = find_index(metro, ano_line, cur_node.position)
            # print(index)
            # print(cur_node.position)
            # quit()
            open_list.append(node([ano_line, index], 'a', cur_node))
            return True
    except Exception:
        return False


def bfs(metro, start, end):
    open_list = [node(start, 'a', None)]
    while open_list:
        current_node = open_list.pop(0)
        if current_node.position == end:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        check_node_anoline(metro, current_node, open_list)
        try:
            if current_node.position[1] > 0 and current_node.run in ['a', 'l']:
                new_position = current_node.position.copy()
                new_position[1] -= 1
                open_list.append(node(new_position, 'l', current_node))
        except TypeError:
            pass
        
        try:
            if current_node.position[1] < len(metro[current_node.position[0]]) - 1 and current_node.run in ['a', 'r']:
                new_position = current_node.position.copy()
                new_position[1] += 1
                open_list.append(node(new_position, 'r', current_node))
        except TypeError:
            pass


def main():
    graph = Metro('delhi-metro-stations')
    # for x in graph.metro.values():
    #     for y in x:
    #         print(y.name, 234, y.line, 123)
    # print(graph.start)
    # print(graph.end)
    # print(graph.trains)
    print(bfs(graph.metro, graph.start, graph.end))

if __name__ == '__main__':
    main()