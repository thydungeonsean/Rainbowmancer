

class StatComponent(object):

    defaults = {
        'attack': 1,
        'health': 3
    }

    states = {
        0: 'normal',
        1: 'boosted',
        2: 'weak',
        3: 'dead'
    }

    encode = {v: k for (k, v) in states.iteritems()}

    def __init__(self, owner, **kwargs):

        self.owner = owner

        cls = StatComponent
        self.atk = kwargs.get('attack', cls.defaults['attack'])
        self.max_health = kwargs.get('health', cls.defaults['health'])
        self.health = self.max_health

        self.state = 0

    def attack(self, target):

        attack_value = self.get_attack_value(target)
        target.take_damage(attack_value)

    def get_attack_value(self, target):
        if self.get_hue_interation(target) == 'strong_against':
            print 'boooste attackk'
            return self.atk + 1
        return self.atk

    def get_bolt_attack(self, target):
        return 1

    def get_hue_interation(self, target):
        return self.owner.color_component.hue_interaction(target)

    def take_damage(self, damage):
        if self.state == StatComponent.encode['weak']:
            self.die()
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.state = 3
        self.owner.die()

    def heal(self, amnt):

        self.health += amnt
        if self.health > self.max_health:
            self.health = self.max_health

    def fire_bolt(self, target):
        attack_value = self.get_bolt_attack(target)
        target.take_damage(attack_value)

    def state_update(self):

        color = self.owner.color_component
        if color.mode == 'generate':
            affinity = color.get_affinity()
            if affinity == 'boosted' and self.health == self.max_health:
                self.state = 1
            elif affinity == 'weak_against' or self.health == 1:
                self.state = 2
        elif color.mode == 'reflect':
            if self.health == 1:
                self.state = 2

