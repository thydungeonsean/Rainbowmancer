from map_object import MapObject


class Door(MapObject):

    def __init__(self, map, coord):

        MapObject.__init__(self)

        self.set_map(map)
        self.set_coord(coord)

        self.state = 0  # closed
        self.block_sight = True

    def on_bump(self):
        if self.state == 0:
            self.open_door()

    def open_door(self):
        self.state = 1  # open
        self.block_sight = False
        self.blocks = False
        self.change_tile()

    def close_door(self):
        self.state = 0
        self.block_sight = True
        self.blocks = True
        self.change_tile()

    def change_tile(self):

        tile_key = {0: 16, 1: 17}  # open and closed door images

        self.map.tile_map.set_tile(tile_key[self.state], self.coord)
        self.map.map_image.add_to_redraw(self.coord)
        self.map.map_image.redraw_tiles()

        self.map.fov_map.update_point(self.coord)  # change fov for tile
        self.map.fov_map.recompute_fov()
        # self.map.redraw_manager.run()

