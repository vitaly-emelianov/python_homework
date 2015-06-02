from nonliving import Emptiness


class Creature(object):
    def __init__(self):
        self.without_reproduction = 0
        self.available_cell_types = [Emptiness]
        self.age = 0


class Predator(Creature):
    def __init__(self, satiety):
        super(Predator, self).__init__()
        self.without_food = 0
        self.satiety = satiety
        self.available_cell_types.append(Victim)

    def __str__(self):
        return "p"


class Victim(Creature):
    def __str__(self):
        return "v"
