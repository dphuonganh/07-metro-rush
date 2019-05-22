class Node:
    def __init__(self, line_name, station_id, parent_node,
                 status=0, action=None, switched=False):
        self.line_name = line_name
        self.station_id = station_id
        self.parent_node = parent_node
        self.status = status
        self.action = action
        self.switched = switched
