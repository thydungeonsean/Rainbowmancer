

class Color(object):

    def __init__(self, *args):
    
        if isinstance(args[0], tuple) and len(args[0]) == 3:
            r, g, b = args[0]
        else:
            r, g, b = args
    
        self.r = r
        self.g = g
        self.b = b
        
    def add(self, other_col):
        
        new_r = (self.r + other_col.r) / 2
        new_g = (self.g + other_col.g) / 2
        new_b = (self.b + other_col.b) / 2
        
        self.set_color_rgb(new_r, new_g, new_b)
        
    def set_color_rgb(self, r, g, b):
        new = []
        for c in (r, g, b):
            if c > 255:
                new.append(255)
            elif c < 0:
                new.append(0)
            else:
                new.append(c)
        self.r = new[0]
        self.g = new[1]
        self.b = new[2]

    def get(self):
        return self.r, self.g, self.b


def add_colors((ar, ag, ab), (br, bg, bb)):

    r = (ar + br) / 2
    g = (ag + bg) / 2
    b = (ab + bb) / 2
    return r, g, b


def boost_color((r, g, b), boost):

    r = min((r + boost, 255))
    g = min((g + boost, 255))
    b = min((b + boost, 255))
    return r, g, b


def drain_color((r, g, b), drain):

    r = max((r - drain, 10))
    g = max((g - drain, 10))
    b = max((b - drain, 10))
    return r, g, b
