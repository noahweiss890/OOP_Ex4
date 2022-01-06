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
small_font = pygame.font.SysFont('Arial', 12, bold=True)

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
BLUE = Color(57, 126, 213)
DARK_BLUE = Color(61, 72, 126)
BROWN = Color(122, 61, 23)
GREEN = Color(0, 255, 0)
RED = Color(255, 0, 0)
DARK_GRAY = (43, 45, 47)



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
        return scale(data, 75, screen.get_height() - 50, min_y, max_y)

def play(ga: GraphAlgos, info_obj: dict, time_left: float) -> bool:

    global min_x, max_x, min_y, max_y, points_button, moves_button, time_to_end_button

    # get data proportions
    min_x = min(list(ga.getGraph().get_all_v().values()), key=lambda n: n.getPos()[0]).getPos()[0]
    min_y = min(list(ga.getGraph().get_all_v().values()), key=lambda n: n.getPos()[1]).getPos()[1]
    max_x = max(list(ga.getGraph().get_all_v().values()), key=lambda n: n.getPos()[0]).getPos()[0]
    max_y = max(list(ga.getGraph().get_all_v().values()), key=lambda n: n.getPos()[1]).getPos()[1]

    stop_button = pygame.Rect(0 * screen.get_width() // 4, 0, screen.get_width() // 4, screen.get_height() // 15)
    points_button = pygame.Rect(1 * screen.get_width() // 4, 0, screen.get_width() // 4, screen.get_height() // 15)
    moves_button = pygame.Rect(2 * screen.get_width() // 4, 0, screen.get_width() // 4, screen.get_height() // 15)
    time_to_end_button = pygame.Rect(3 * screen.get_width() // 4, 0, screen.get_width() // 4, screen.get_height() // 15)

    # refresh surface
    screen.fill(BLACK)

    points = info_obj["GameServer"]["grade"]
    moves = info_obj["GameServer"]["moves"]

    pygame.draw.rect(screen, RED, stop_button)
    pygame.draw.rect(screen, DARK_GRAY, stop_button, 3)
    screen.blit(FONT.render("STOP", True, DARK_GRAY), (0 * screen.get_width() // 4 + screen.get_width() // 4 / 2 - 35, screen.get_height() // 15 // 4))
    pygame.draw.rect(screen, BLUE, points_button)
    pygame.draw.rect(screen, DARK_GRAY, points_button, 3)
    screen.blit(FONT.render(f"Overall Points: {points}", True, DARK_GRAY), (1 * screen.get_width() // 4 + screen.get_width() // 4 / 3 - 35, screen.get_height() // 15 // 4))
    pygame.draw.rect(screen, BLUE, moves_button)
    pygame.draw.rect(screen, DARK_GRAY, moves_button, 3)
    screen.blit(FONT.render(f"Moves: {moves}", True, DARK_GRAY), (2 * screen.get_width() // 4 + screen.get_width() // 4 / 3 - 10, screen.get_height() // 15 // 4))
    pygame.draw.rect(screen, BLUE, time_to_end_button)
    pygame.draw.rect(screen, DARK_GRAY, time_to_end_button, 3)
    screen.blit(FONT.render(f"Time To End: {int(time_left // 1000)}", True, DARK_GRAY), (3 * screen.get_width() // 4 + screen.get_width() // 4 / 4 - 10, screen.get_height() // 15 // 4))

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
        pygame.draw.line(screen, DARK_BLUE, (src_x, src_y), (dest_x, dest_y))

    # draw nodes
    for n in ga.getGraph().get_all_v().values():
        x = my_scale(n.getPos()[0], x=True)
        y = my_scale(n.getPos()[1], y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y), radius, BLUE)
        gfxdraw.aacircle(screen, int(x), int(y), radius, WHITE)

        # draw the node id
        id_srf = FONT.render(str(n.getID()), True, WHITE)
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw agents
    for agent in ga.getAgents().values():
        pygame.draw.circle(screen, BROWN, (my_scale(agent.getPos()[0], x=True), my_scale(agent.getPos()[1], y=True)), 10)
        id_srf = small_font.render(str(agent.getID()), True, WHITE)
        rect = id_srf.get_rect(center=(my_scale(agent.getPos()[0], x=True), my_scale(agent.getPos()[1], y=True)))
        screen.blit(id_srf, rect)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for x, y, type, value in ga.get_current_pokemons():
        if type == 1:
            color = GREEN
        else:
            color = RED
        pygame.draw.circle(screen, color, (my_scale(x, x=True), my_scale(y, y=True)), 10)
        value_srf = small_font.render(str(int(value)), True, BLUE)
        rect = value_srf.get_rect(center=(my_scale(x, x=True), my_scale(y, y=True)))
        screen.blit(value_srf, rect)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if stop_button.collidepoint(event.pos):
                pygame.quit()
                return True

    return False
