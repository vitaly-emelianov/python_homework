import random
from creatures import Predator, Victim
from nonliving import Obstacle, Emptiness


class Ocean(object):

    def __init__(self, **kwargs):
        """Initiate ocean state."""
        self.x_size = kwargs['x_size']
        self.y_size = kwargs['y_size']
        self.seed = kwargs['seed']
        self.probabilities = {
            Victim: kwargs['victim_probability'],
            Predator: kwargs['predator_probability'],
            Obstacle: kwargs['obstacle_probability'],
            Emptiness: kwargs['emptiness_probability']
        }
        self.reproduction_interval = {
            Victim: kwargs['victim_reproduction_interval'],
            Predator: kwargs['predator_reproduction_interval']
        }
        self.satiety = kwargs['satiety']

        self.step = dict()
        self.steps_number = 0
        self.counter = {Victim: 0, Predator: 0}

        random.seed(self.seed)
        self.area = [[self.generate_cell(self.probabilities)
                     for y in xrange(self.y_size)]
                     for x in xrange(self.x_size)]

    def generate_cell(self, probabilities):
        """Return cell on given probabilities."""
        totals = []
        cell_types = []
        running_total = 0
        for cell_type, probability in probabilities.items():
            cell_types.append(cell_type)
            running_total += probability
            totals.append(running_total)
        rnd = random.random()
        for i, total in enumerate(totals):
            if rnd < total:
                if cell_types[i] == Predator:
                    cell = cell_types[i](self.satiety)
                else:
                    cell = cell_types[i]()
                if type(cell) in {Victim, Predator}:
                    creature = cell
                    self.step[creature] = 0
                    self.counter[type(creature)] += 1
                return cell

    def __str__(self):
        ocean = [' '.join([' ']+[str(y) for y in xrange(self.y_size)])]
        line_counter = 0
        for line in self.area:
            row = [str(line_counter)]
            for cell in line:
                row.append(str(cell))
            ocean.append(' '.join(row))
            line_counter += 1
        return '\n'.join(ocean)

    def process_step(self):
        """Process next step of life."""
        for x in xrange(self.x_size):
            for y in xrange(self.y_size):
                self.process_cell(x, y)
        self.steps_number += 1

    def process_cell(self, x, y):
        """Process cell given coordinates."""
        if type(self.area[x][y]) in {Emptiness, Obstacle}:
            return
        else:
            creature = self.area[x][y]
            if self.step[creature] == self.steps_number:
                self.step[creature] += 1
                actions = self.possible_actions(x, y)
                rnd = random.random()
                # new creature born with 70% probability
                if (creature.without_reproduction >= self.reproduction_interval[type(creature)]
                        and rnd < 0.7):
                    try:
                        (new_x, new_y) = random.choice(actions[Emptiness])
                        if type(creature) == Predator:
                            new_creature = type(creature)(self.satiety)
                        else:
                            new_creature = type(creature)()
                        self.counter[type(new_creature)] += 1
                        self.step[new_creature] = self.steps_number+1
                        creature.without_reproduction = 0
                        self.area[new_x][new_y] = new_creature
                    except IndexError:
                        creature.without_reproduction += 1
                        if type(creature) is Victim:
                            self.process_victim(creature, x, y, actions)
                        elif type(creature) is Predator:
                            self.process_predator(creature, x, y, actions)
                else:
                    creature.without_reproduction += 1
                    if type(creature) is Victim:
                        self.process_victim(creature, x, y, actions)
                    elif type(creature) is Predator:
                        self.process_predator(creature, x, y, actions)
            else:
                return

    def process_victim(self, victim, x, y, actions):
        """Process cell with victim inside it."""
        try:
            (new_x, new_y) = random.choice(actions[Emptiness])
            self.area[new_x][new_y] = victim
            self.area[x][y] = Emptiness()
        except IndexError:
            return

    def process_predator(self, predator, x, y, actions):
        """Process cell with predator inside it."""
        try:
            (new_x, new_y) = random.choice(actions[Victim])
            del self.step[self.area[new_x][new_y]]
            self.counter[Victim] -= 1
            self.area[new_x][new_y] = Emptiness()
            predator.satiety += 1
        except IndexError:
            if predator.satiety == 0:
                rnd = random.random()
                # predator dies with probability of 60 % if it didn't eat one step
                if rnd < 0.6:
                    del self.step[predator]
                    self.counter[Predator] -= 1
                    self.area[x][y] = Emptiness()
            else:
                predator.satiety -= 1
                try:
                    (new_x, new_y) = random.choice(actions[Emptiness])
                    self.area[new_x][new_y] = predator
                    self.area[x][y] = Emptiness()
                except IndexError:
                    return

    def possible_actions(self, x, y):
        """Get creature's possible actions given cell coordinates."""
        creature = self.area[x][y]
        possibilities = {cell_type: [] for cell_type in creature.available_cell_types}
        for cell_type in creature.available_cell_types:
            if x < self.x_size-1:
                if type(self.area[x+1][y]) == cell_type:
                    possibilities[cell_type].append((x+1, y))
            if x > 0:
                if type(self.area[x-1][y]) == cell_type:
                    possibilities[cell_type].append((x-1, y))
            if y < self.y_size-1:
                if type(self.area[x][y+1]) == cell_type:
                    possibilities[cell_type].append((x, y+1))
            if y > 0:
                if type(self.area[x][y-1]) == cell_type:
                    possibilities[cell_type].append((x, y-1))
        return possibilities
