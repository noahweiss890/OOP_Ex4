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
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)

def play(ga: GraphAlgos):

    global min_x, max_x, min_y, max_y

    # get data proportions
    min_x = min(list(ga.getGraph().getNodes().values()), key=lambda n: n.getPos().getX()).getPos().getX()
    min_y = min(list(ga.getGraph().getNodes().values()), key=lambda n: n.getPos().getY()).getPos().getY()
    max_x = max(list(ga.getGraph().getNodes().values()), key=lambda n: n.getPos().getX()).getPos().getX()
    max_y = max(list(ga.getGraph().getNodes().values()), key=lambda n: n.getPos().getY()).getPos().getY()

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in ga.getGraph().getNodes().values():
        x = my_scale(n.getPos().getX(), x=True)
        y = my_scale(n.getPos().getY(), y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in ga.getGraph().getEdges().values():
        # find the edge nodes
        src = next(n for n in ga.getGraph().getNodes() if n.getId() == e.getSrc())
        dest = next(n for n in ga.getGraph().getNodes() if n.getId() == e.getDest())

        # scaled positions
        src_x = my_scale(src.getPos().getX(), x=True)
        src_y = my_scale(src.getPos().getY(), y=True)
        dest_x = my_scale(dest.getPos().getX(), x=True)
        dest_y = my_scale(dest.getPos().getY(), y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in ga.getAgents().value():
        pygame.draw.circle(screen, Color(122, 61, 23), (int(agent.getPos().getX()), int(agent.getPos().getY())), 10)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in ga.getPokemon():
        if p.type == 1:
            color = Color(0, 255, 0)
        else:
            color = Color(255, 0, 0)
        pygame.draw.circle(screen, color, (int(p.getPos().getX()), int(p.getPos().getY())), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)
