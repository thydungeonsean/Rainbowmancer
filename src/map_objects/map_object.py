from components.components import ImageComponent, ColorComponent


class MapObject(object):

    def __init__(self):

        self.map = None
        self.coord = None

        self.move_component = None
        self.image_component = None
        self.color_component = None
        self.light_component = None
        self.ai_component = None
        self.stat_component = None

        self.team = None
        self.object_type = None

        self.blocks = True
        self.block_sight = False

    def set_map(self, map):
        self.map = map

    def set_coord(self, coord):
        self.coord = coord

    def set_move(self, move):
        self.move_component = move

    def set_image(self, name):
        self.image_component = ImageComponent(self, name)

    def set_color(self, color):
        self.color_component = ColorComponent(self, color)

    def set_light(self, light):
        self.light_component = light

    def set_ai(self, ai):
        self.ai_component = ai

    def move(self, new):
        self.coord = new
        if self.light_component is not None:
            self.light_component.move(new)

    def draw(self, surface, tick):

        if self.image_component is not None and self.map.fov_map.point_is_visible(self.coord):

            self.image_component.draw(surface, tick)

    def remove(self):
        self.map.game.objects.remove(self)
        if self.light_component is not None:
            self.light_component.kill()

    def on_bump(self):
        pass
