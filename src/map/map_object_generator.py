from src.map_objects.actor import Actor
from src.map_objects.player import Player
from src.map_objects.crystal import Crystal
from src.map_objects.door import Door
from src.map_objects.brazier import Brazier


class MapObjectGen(object):

    def __init__(self, map):
        self.map = map

    def add_map_object(self, obj):

        self.map.game.objects.append(obj)

    def create_monster(self, name, coord):
        m = Actor(self.map, coord, name)
        self.add_map_object(m)

    def add_player(self, player_key, coord):

        player = Player(coord, player_key)

        player.initialize(self.map)
        self.map.game.objects.insert(0, player)

        return player

    def add_crystal(self, point, color):

        c = Crystal(self.map, point, color)
        self.add_map_object(c)

    def add_brazier(self, point):
        b = Brazier(self.map, point)
        self.add_map_object(b)

    def add_door(self, point):

        d = Door(self.map, point)
        self.add_map_object(d)

    def add_random_monster(self, point):

        monster = Actor(self.map, point, 'gnome')

        self.add_map_object(monster)
