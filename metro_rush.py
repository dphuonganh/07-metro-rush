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

class find_all_path(Metro):
    def find_index(self, line, position):
        for x, y in enumerate(self.metro[line]):
            if y.name == self.metro[position[0]][position[1]].name:
                return x
        raise ValueError()

    def check_node_anoline(self, cur_node, open_list):
        try:
            if self.metro[cur_node.position[0]][cur_node.position[1]].line:
                ano_line = self.metro[cur_node.position[0]][cur_node.position[1]].line
                if ano_line in self.clo_line and ano_line != self.end[0]:
                    return
                self.clo_line.append(ano_line)
                index = self.find_index(ano_line, cur_node.position)
                open_list.append(node([ano_line, index], 'a', cur_node))
        except Exception:
            return False
    
    def check_node_left(self, current_node, open_list):
        try:
            if current_node.position[1] > 0 and current_node.run in ['a', 'l']:
                new_position = current_node.position.copy()
                new_position[1] -= 1
                open_list.append(node(new_position, 'l', current_node))
        except TypeError:
            pass
    
    def check_node_right(self, current_node, open_list):
        try:
            if current_node.position[1] < len(self.metro[current_node.position[0]]) - 1\
               and current_node.run in ['a', 'r']:
                new_position = current_node.position.copy()
                new_position[1] += 1
                open_list.append(node(new_position, 'r', current_node))
        except TypeError:
            pass

    def bfs(self):
        open_list = [node(self.start, 'a', None)]
        output = []
        self.clo_line = [self.start[0]]
        while open_list:
            current_node = open_list.pop(0)

            if current_node.position == self.end:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                output.append(path[::-1])

            self.check_node_anoline(current_node, open_list)
            self.check_node_left(current_node, open_list)
            self.check_node_right(current_node, open_list)
        return output


def main():
    for x in find_all_path('delhi-metro-stations').bfs():
        print(*x, sep=' -> ')
        print()
    # print(find_all_path('delhi-metro-stations').bfs())


if __name__ == '__main__':
    main()