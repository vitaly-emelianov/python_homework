class Nonliving(object):
    pass


class Obstacle(Nonliving):
    def __str__(self):
        return "*"


class Emptiness(Nonliving):
    def __str__(self):
        return " "
