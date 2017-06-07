

class _Map(object):

    def __init__(self, w, h):
        
        self.map = [[ 0 for my in range(w)] for mx in range(h)]
        self.w = w
        self.h = h
        
    def get_tile(self, *args):
        if isinstance(args[0], tuple):
            x = args[0][0]
            y = args[0][1]
        else:
            x = args[0]
            y = args[1]
        return self.map[x][y]
        
    def set_tile(self, value, *args):
        if isinstance(args[0], tuple):
            x = args[0][0]
            y = args[0][1]
        else:
            x = args[0]
            y = args[1]
        self.map[x][y] = value
         
    @property
    def all_points(self):

        points = []
        for y in range(self.h):
            for x in range(self.w):
                points.append((x, y))
        return points

    def point_in_bounds(self, (x, y)):

        return 0 <= x < self.w and 0 <= y < self.h

    def get_adj(self, (x, y)):

        adj = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        return list(filter(self.point_in_bounds, adj))
        