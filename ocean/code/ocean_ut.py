import unittest
from ocean import Ocean
from creatures import Predator, Victim
from nonliving import Obstacle, Emptiness


class TestOcean(unittest.TestCase):

    configs = dict()
    configs['x_size'] = 5
    configs['y_size'] = 5
    configs['seed'] = 0.1
    configs['victim_probability'] = 0.4
    configs['predator_probability'] = 0.2
    configs['obstacle_probability'] = 0.1
    configs['emptiness_probability'] = 0.3
    configs['satiety'] = 10
    configs['predator_reproduction_interval'] = 3
    configs['victim_reproduction_interval'] = 3

    def test_init(self):
        ocean = Ocean(**TestOcean.configs)
        self.assertEqual(ocean.x_size, 5)
        self.assertEqual(ocean.y_size, 5)
        self.assertEqual(ocean.seed, 0.1)
        self.assertEqual(ocean.satiety, 10)
        self.assertEqual(ocean.reproduction_interval[Victim], 3)
        self.assertEqual(ocean.reproduction_interval[Predator], 3)

    def test_generate_cell(self):
        ocean = Ocean(**TestOcean.configs)
        for i in xrange(10):
            cell_type = type(ocean.generate_cell(ocean.probabilities))
            self.assertTrue(cell_type in (Victim, Predator, Obstacle, Emptiness))

    def test_possible_actions(self):
        ocean = Ocean(**TestOcean.configs)
        print "possible_actions(x, y) test:"
        print ocean

        predator_actions = ocean.possible_actions(0, 2)
        self.assertEqual({Emptiness: [(1, 2), (0, 3)], Victim: [(0, 1)]}, predator_actions)

        victim_actions = ocean.possible_actions(4, 0)
        self.assertEqual({Emptiness: [(3, 0), (4, 1)]}, victim_actions)


if __name__ == '__main__':
    unittest.main()
