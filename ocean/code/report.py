from matplotlib import pyplot
from ConfigParser import ConfigParser
from ocean import Ocean
from creatures import Victim, Predator
from graphical_interface import Graphics
import pygame


def report(config_file, iterations_number, statistics_mode=True, display_mode=False):
    """Make a report."""

    # parsing configuration file
    config = ConfigParser()
    config.read(config_file)
    configs = dict()
    configs['x_size'] = config.getint('ocean', 'x_size')
    configs['y_size'] = config.getint('ocean', 'y_size')
    configs['seed'] = config.getfloat('ocean', 'seed')
    configs['victim_probability'] = config.getfloat('ocean', 'victim_probability')
    configs['predator_probability'] = config.getfloat('ocean', 'predator_probability')
    configs['obstacle_probability'] = config.getfloat('ocean', 'obstacle_probability')
    configs['emptiness_probability'] = config.getfloat('ocean', 'emptiness_probability')
    configs['satiety'] = config.getint('predator', 'satiety')
    configs['predator_reproduction_interval'] = config.getint('predator', 'reproduction_interval')
    configs['victim_reproduction_interval'] = config.getint('victim', 'reproduction_interval')

    ocean = Ocean(**configs)
    victim_counts = []
    predator_counts = []

    if display_mode:
        graphical_ocean = Graphics(ocean)

    for i in xrange(iterations_number):
        if ocean.counter[Victim] == 0 or ocean.counter[Predator] == 0:
            break
        ocean.process_step()
        victim_counts.append(ocean.counter[Victim])
        predator_counts.append(ocean.counter[Predator]*10)

        if display_mode:
            graphical_ocean.show(ocean)

    if statistics_mode:
        iterations = [i for i in xrange(len(victim_counts))]
        pyplot.plot(iterations, victim_counts)
        pyplot.plot(iterations, predator_counts)
        pyplot.show()
