from src.color.color_palette import hue_codes


class BoostSlot(object):

    def __init__(self, ability):

        self.ability = ability

        self.state = 0

        self.boost_color = None

    def crystal_click(self, color):

        if self.state == 0:
            self.load_color(color)
        elif self.state == 1:
            self.switch_color(color)
        print self.boost_color

    def load_color(self, color):

        self.boost_color = color
        self.state = 1
        self.ability.set_hue(hue_codes[color])

    def clear_color(self):
        self.boost_color = None
        self.state = 0
        self.ability.set_hue_to_inventory_hue()

    def switch_color(self, color):

        if color == self.boost_color:
            self.clear_color()
        else:
            self.load_color(color)
