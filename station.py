class Station:
    def __init__(self, station_name, line_name, capacity=1):
        self.name = station_name
        self.lines = {line_name}
        self.capacity = capacity
        self.trains = []

    def add_line(self, line_name):
        self.lines.add(line_name)

    def push_train(self, train_label):
        if len(self.trains) < self.capacity:
            self.trains.insert(0, train_label)
            return True
        return False

    def pop_train(self):
        try:
            self.trains.pop(-1)
        except IndexError:
            pass
