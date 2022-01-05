"""
here we will build a GUI
"""

import pygame
from pygame import *
from pygame import gfxdraw

import GraphAlgos


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
        return scale(data, 100, screen.get_height() - 50, min_y, max_y)

def play(ga: GraphAlgos) -> bool:

    global min_x, max_x, min_y, max_y

    # get data proportions
    min_x = min(list(ga.getGraph().get_all_v().values()), key=lambda n: n.getPos()[0]).getPos()[0]
    min_y = min(list(ga.getGraph().get_all_v().values()), key=lambda n: n.getPos()[1]).getPos()[1]
    max_x = max(list(ga.getGraph().get_all_v().values()), key=lambda n: n.getPos()[0]).getPos()[0]
    max_y = max(list(ga.getGraph().get_all_v().values()), key=lambda n: n.getPos()[1]).getPos()[1]

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True

    draw(ga)
    return False


def draw(ga: GraphAlgos):

    # refresh rate
    clock.tick(60)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in ga.getGraph().get_all_v().values():
        x = my_scale(n.getPos()[0], x=True)
        y = my_scale(n.getPos()[1], y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.getID()), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in ga.getGraph().get_all_e().values():
        # find the edge nodes
        src = next(n for n in ga.getGraph().get_all_v().values() if n.getID() == e.getSrc())
        dest = next(n for n in ga.getGraph().get_all_v().values() if n.getID() == e.getDest())

        # scaled positions
        src_x = my_scale(src.getPos()[0], x=True)
        src_y = my_scale(src.getPos()[1], y=True)
        dest_x = my_scale(dest.getPos()[0], x=True)
        dest_y = my_scale(dest.getPos()[1], y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in ga.getAgents().values():
        pygame.draw.circle(screen, Color(122, 61, 23), (my_scale(agent.getPos()[0], x=True), my_scale(agent.getPos()[1], y=True)), 10)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    # for agent in ga.getAgents().values():
    for x, y, type in ga.get_current_pokemons():
        if type == 1:
            color = Color(0, 255, 0)
        else:
            color = Color(255, 0, 0)
        pygame.draw.circle(screen, color, (my_scale(x, x=True), my_scale(y, y=True)), 10)

    # update screen changes
    display.update()
