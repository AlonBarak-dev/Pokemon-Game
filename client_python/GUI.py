
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.Agent import Agent
from client_python.Info import Info
from client_python.pokemon import Pokemon
from graph.GraphAlgo import GraphAlgo
from Button import Button


class Gui:

    def __init__(self, graph: GraphAlgo):
        # create a pygame
        pygame.init()
        pygame.font.init()

        # screen
        self.screen = display.set_mode((1080, 720), depth=32, flags=RESIZABLE)
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont('Arial', 20, bold=True)

        # get data proportions
        self.min_x = min(list(graph.get_graph().nodes.values()), key=lambda n: n.pos.x).pos.x
        self.min_y = min(list(graph.get_graph().nodes.values()), key=lambda n: n.pos.y).pos.y
        self.max_x = max(list(graph.get_graph().nodes.values()), key=lambda n: n.pos.x).pos.x
        self.max_y = max(list(graph.get_graph().nodes.values()), key=lambda n: n.pos.y).pos.y

        self.radius = 15
        # algorithm variables
        self.graph = graph
        self.agents = []
        self.pokemon_list = []

        # buttons and text
        self.stop_button = None
        self.time_to_play = None
        self.overall_points = None
        self.moves_counter = None
        self.game_level = None

    def run_gui(self, agents: list, pokemon_list: list, ttl: str, game_info: Info):

        self.agents = agents
        self.pokemon_list = pokemon_list

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        # refresh surface
        self.screen.fill(Color(0, 0, 0))

        # draw elements in the screen base on given state and data
        self.draw_edges()
        self.draw_nodes()
        self.draw_agents()
        self.draw_pokemons()
        self.create_buttons(ttl, game_info)

        if self.stop_button.pressed:  # check if the client has stopped the game
            return False

        # update screen changes
        display.update()
        # refresh rate
        self.clock.tick(10)
        return True

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values
    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    def draw_nodes(self):
        # draw nodes
        for n in self.graph.get_graph().nodes.values():
            x = self.my_scale(n.pos.x, x=True)
            y = self.my_scale(n.pos.y, y=True)
            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(self.screen, int(x), int(y),
                                  self.radius, Color(240, 230, 140))
            gfxdraw.aacircle(self.screen, int(x), int(y),
                             self.radius, Color(255, 255, 255))

            # draw the node id
            id_srf = self.FONT.render(str(n.key), True, Color(0, 0, 0))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)

    def draw_edges(self):
        # draw edges
        for e in self.graph.get_graph().edges:
            # find the edge nodes
            src = next(n for n in self.graph.get_graph().nodes.values() if n.key == e.src)
            dest = next(n for n in self.graph.get_graph().nodes.values() if n.key == e.dest)

            # scaled positions
            src_x = self.my_scale(src.pos.x, x=True)
            src_y = self.my_scale(src.pos.y, y=True)
            dest_x = self.my_scale(dest.pos.x, x=True)
            dest_y = self.my_scale(dest.pos.y, y=True)

            # draw the line
            pygame.draw.line(self.screen, Color(51, 161, 201),
                             (src_x, src_y), (dest_x, dest_y))

    def draw_agents(self):
        # draw agents
        for agent in self.agents:
            x = self.my_scale(float(agent.pos.x), x=True)
            y = self.my_scale(float(agent.pos.y), y=True)
            pygame.draw.circle(self.screen, Color(107, 142, 35), (x, y), 10)

    def draw_pokemons(self):
        for p in self.pokemon_list:
            x = self.my_scale(float(p.pos.x), x=True)
            y = self.my_scale(float(p.pos.y), y=True)
            if p.type == -1:
                pygame.draw.circle(self.screen, Color(255, 128, 0), (x, y), 10)     # orange pokemons go down
            else:
                pygame.draw.circle(self.screen, Color(3, 18, 50), (x, y), 10)       # blue pokemons go up

    def create_buttons(self, ttl: str, game_info: Info):
        # draw stop button and more attributes for the user comfort
        self.stop_button = Button(self.screen, "STOP", self.FONT, 50, 30, (10, 10), 5)
        self.stop_button.check_click()
        self.stop_button.draw()
        self.time_to_play = self.FONT.render(f"Time: {ttl}", True, Color(255, 64, 64))
        self.screen.blit(self.time_to_play, (70, 10))
        self.overall_points = self.FONT.render(f"Points: {str(game_info.grade)}", True, Color(255, 64, 64))
        self.screen.blit(self.overall_points, (250, 10))
        self.moves_counter = self.FONT.render(f"Moves: {str(game_info.moves)}", True, Color(255, 64, 64))
        self.screen.blit(self.moves_counter, (400, 10))
        self.game_level = self.FONT.render(f"Game Level: {str(game_info.game_level)}", True, Color(255, 64, 64))
        self.screen.blit(self.game_level, (550, 10))

