from finding import BreadthFirstSearch


def move_station(current_station, parent_station):
    if parent_station.trains:
        if current_station.push_train(parent_station.trains[-1]):
            parent_station.pop_train()
            return True
    return False


class MovingTrains(BreadthFirstSearch):
    def __init__(self, input_data, algo):
        super().__init__(input_data)
        self.find_paths()
        self.algo = algo
        self.depart_rate = [0, 0]
        self.num_turns = 0
        self.output = []
        self.calculate_depart_rate()
        self.move_trains()

    def get_constant(self):
        const = [1, 1]
        for index in range(2):
            for node in self.paths[index]:
                if node.action == 'switch':
                    const[index] = 2
                    break
        return const

    def get_cost(self):
        return [len(self.paths[0]) - 1, len(self.paths[1]) - 1]

    def add_depart_rate(self, path_index, c, cost):
        self.depart_rate[path_index] += 1
        return cost + c

    def calculate_depart_rate(self):
        if len(self.paths) == 1 or self.algo == 0:
            self.depart_rate[0] = self.num_trains
        elif len(self.paths) > 1:
            c1, c2 = self.get_constant()
            cost1, cost2 = self.get_cost()
            for index in range(1, self.num_trains + 1):
                if cost1 <= cost2:
                    cost1 = self.add_depart_rate(0, c1, cost1)
                    continue
                cost2 = self.add_depart_rate(1, c2, cost2)

    def print_each_path(self):
        result = [[] for _ in range(self.algo + 1)]
        for index, path in enumerate(self.paths[:2]):
            temp = []
            for node in path:
                if node.action == 'switch':
                    continue
                station = self.get_station(node.line_name, node.station_id)
                if not len(station.trains):
                    continue
                result[index].append('{}({}:{})-{}'.format(
                    station.name, node.line_name, node.station_id,
                    ','.join(station.trains)))
                temp.append([node.line_name, node.station_id])
            self.output.append(temp.copy())
            print('\t* Path {}:'.format(index + 1))
            print('|'.join(result[index]))

    def print_trains(self):
        print('___Turn {}___'.format(self.num_turns))
        try:
            self.print_each_path()
        except IndexError:
            pass

    def check_train_depart(self, path_index):
        if self.depart_rate[path_index] > 0:
            return True
        return False

    def update_each_path(self, path_index):
        for node in self.paths[path_index][:0:-1]:
            current_station = self.get_station(node.line_name, node.station_id)
            parent_station = self.get_station(node.parent_node.line_name,
                                              node.parent_node.station_id)
            if node.action != 'move' or not parent_station.trains:
                continue
            if node.parent_node.action == 'move':
                move_station(current_station, parent_station)
            elif not node.parent_node.action:
                if self.check_train_depart(path_index):
                    if move_station(current_station, parent_station):
                        self.depart_rate[path_index] -= 1
            else:
                if node.parent_node.switched:
                    move_station(current_station, parent_station)
                node.parent_node.switched = not node.parent_node.switched

    def update_trains(self):
        try:
            for path_index in range(self.algo + 1):
                self.update_each_path(path_index)
        except IndexError:
            pass

    def move_trains(self):
        self.print_trains()
        while len(self.get_station(*self.end).trains) < self.num_trains:
            self.update_trains()
            self.num_turns += 1
            self.print_trains()
