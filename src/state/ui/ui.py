from crystal_panel import CrystalPanel
from character_panel import CharacterPanel
from ability_panel import AbilityPanel


class UI(object):

    def __init__(self, game):

        self.game = game

        self.ui_objects = []
        self.panels = {}

        self.initialize()

    def initialize(self):

        crystal = CrystalPanel(self)
        self.add_ui_object(crystal)
        self.panels['crystal'] = crystal

        character = CharacterPanel(self)
        self.add_ui_object(character)
        self.panels['character'] = character

        ability = AbilityPanel(self)
        self.add_ui_object(ability)
        self.panels['ability'] = ability

    def add_ui_object(self, obj):
        self.ui_objects.append(obj)

    def remove_ui_object(self, obj):
        self.ui_objects.remove(obj)

    def draw(self, surface, tick):

        for obj in self.ui_objects:
            obj.draw(surface, tick)

    def run(self):
        pass

    def click(self, point):

        for panel in self.ui_objects:
            clicked = panel.click(point)
            if clicked:
                return True
        return False

    def right_click(self, point):

        for panel in self.ui_objects:
            right_clicked = panel.right_click(point)
            if right_clicked:
                return True
        return False
