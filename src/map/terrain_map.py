from _map import _Map


class TerrainMap(_Map):

    key = {
    0: 'floor',
    1: 'wall',
    2: 'door',
    3: 'crystal',
    4: 'brazier',
    5: 'stalagtite'
    }

    def __init__(self, w, h):
        
        _Map.__init__(self, w, h)
        
    
        