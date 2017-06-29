from crystal_panel import CrystalPanel


class UI(object):

    def __init__(self, game):

        self.game = game

        self.ui_objects = []

        self.initialize()

    def initialize(self):

        self.add_ui_object(CrystalPanel(self))

    def add_ui_object(self, obj):
        self.ui_objects.append(obj)

    def remove_ui_object(self, obj):
        self.ui_objects.remove(obj)

    def draw(self, surface, tick):

        for obj in self.ui_objects:
            obj.draw(surface)

    def run(self):
        pass

