"""
here we will build a GUI
"""

import pygame
from pygame import *

from src import GraphAlgos
from src.Graph import Graph

# init pygame
WIDTH, HEIGHT = 1080, 720
radius = 15
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
pygame.display.set_caption("Ex4 - Gotta Catch E'm All!")
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)

def play(ga: GraphAlgos):

    global min_x, max_x, min_y, max_y

    # get data proportions
    min_x = min(list(ga.getGraph.nodes), key=lambda n: n.pos.x).pos.x
    min_y = min(list(ga.getGraph.nodes), key=lambda n: n.pos.y).pos.y
    max_x = max(list(ga.getGraph.nodes), key=lambda n: n.pos.x).pos.x
    max_y = max(list(ga.getGraph.nodes), key=lambda n: n.pos.y).pos.y

