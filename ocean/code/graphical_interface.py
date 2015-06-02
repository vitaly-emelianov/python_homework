import pygame
from ocean import Ocean
from creatures import Victim, Predator
from nonliving import Obstacle


class Graphics(object):

    def __init__(self, ocean, pixel_size=5):

        self.pixel_size = pixel_size
        (width, height) = (ocean.x_size * pixel_size, ocean.y_size * pixel_size)
        self.screen = pygame.display.set_mode((width, height))
        self.background_color = (255, 255, 255)

    def show(self, ocean):
        """Show ocean."""

        pygame.display.set_caption('Ocean')
        self.screen.fill(self.background_color)

        predator_color = (255, 0, 0)
        victim_color = (0, 102, 0)
        obstacle_color = (0, 0, 0)

        for x in xrange(ocean.x_size):
            for y in xrange(ocean.y_size):
                if type(ocean.area[x][y]) is Predator:
                    color = predator_color
                elif type(ocean.area[x][y]) is Victim:
                    color = victim_color
                elif type(ocean.area[x][y]) is Obstacle:
                    color = obstacle_color
                else:
                    color = self.background_color
                pixel_size = self.pixel_size
                cell_parameters = (x*pixel_size, y*pixel_size, pixel_size, pixel_size)
                pygame.draw.rect(self.screen, color, cell_parameters)
        pygame.display.flip()
