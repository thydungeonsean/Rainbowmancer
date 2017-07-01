from stat_component import StatComponent


class PlayerStatComponent(StatComponent):

    def __init__(self, owner, **kwargs):

        StatComponent.__init__(self, owner, **kwargs)

    def take_damage(self, damage):
        if self.state == StatComponent.encode['weak']:
            self.die()
        self.health -= damage
        if self.health <= 0:
            self.die()

        self.update_panel()

    def heal(self, amnt):

        self.health += amnt
        if self.health > self.max_health:
            self.health = self.max_health

        self.update_panel()

    def update_panel(self):

        self.owner.map.game.ui.panels['character'].change()
