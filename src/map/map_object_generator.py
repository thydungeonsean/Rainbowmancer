from src.map_objects.actor import Actor
from src.map_objects.player import Player

from src.map_objects.light_component import LightComponent


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
        #l = LightComponent(player, self.map, 'blue', 5)
        #player.set_light(l)

        player.set_map(self.map)
        self.map.game.objects.insert(0, player)

        return player
