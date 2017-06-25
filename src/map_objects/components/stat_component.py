

class StatComponent(object):

    defaults = {
        'attack': 1,
        'health': 3
    }

    def __init__(self, owner, **kwargs):

        self.owner = owner

        cls = StatComponent
        self.attack = kwargs.get('attack', cls.defaults['attack'])
        self.max_health = kwargs.get('health', cls.defaults['health'])
        self.health = self.max_health

