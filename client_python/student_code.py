"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import math as mh
from threading import Thread
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.Agent import Agent
from client_python.Info import Info
from client_python.pokemon import Pokemon
from graph.DiGraph import DiGraph
from graph.GraphAlgo import GraphAlgo

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = GraphAlgo()
graph.load_from_json(json.loads(graph_json))

# get data proportions
min_x = min(list(graph.get_graph().nodes.values()), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.get_graph().nodes.values()), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.get_graph().nodes.values()), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.get_graph().nodes.values()), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

game_info = Info.from_dict(json.loads(client.get_info()))
for i in range(game_info.agents):
    client.add_agent("{\"id\":" + str(i) + "}")



# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""


def run_agent(agent: Agent, g_algo: GraphAlgo):
    while agent.path:
        p = agent.path[0]
        if stop:
            break
        client.choose_next_edge(
            '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(agent.path[1 % len(agent.path)]) + '}')
        agent.pos = g_algo.get_graph().nodes[agent.path[1 % len(agent.path)]].pos
        agent.path.remove(agent.path[0])
        if isinstance(g_algo.get_graph().get_all_v()[p], Pokemon):
            break


def sorting_func(pokemon):
    return pokemon.value


def find_nearest_avaliable_agent(agent_list: list, curr_pokemon: Pokemon, graph: GraphAlgo) -> int:
    free_agents = []
    min_weight = mh.inf
    path = []
    agent_res = None
    pokemon = curr_pokemon
    # find free agents
    for agent in agent_list:
        if len(agent.path) == 0:
            free_agents.append(agent)  # add to the list of free agents

    if len(free_agents) != 0:  # in case we found free agents
        for agent in free_agents:  # loop over the free agents
            dist, sp_path = graph.shortest_path(agent.src, pokemon.edge.src)  # find the shortest path from agent src to pokemon
            dist_1, sp_path_1 = graph.shortest_path(pokemon.edge.src, pokemon.edge.dest)
            dist += dist_1
            sp_path += sp_path_1
            # in case we found an agent with shorter path, switch
            if dist < min_weight:
                min_weight = dist
                path = sp_path
                agent_res = agent

        agent_res.path = path  # update the agent path
        print(path)
        return agent_res.id  # return the agent id

    else:  # in case there are no free agents, loop over the agents

        for agent in agent_list:
            # in case one of the agents already going to the pokemon node, allocate the same agent
            if pokemon.edge.src in agent.path and pokemon.edge.dest in agent.path:
                return agent.id
            # find the shortest path from the agent last destination to the pokemon
            dist, sp_path = graph.shortest_path(agent.path[-1], pokemon.edge.src)
            dist_1, sp_path_1 = graph.shortest_path(pokemon.edge.src, pokemon.edge.dest)
            dist += dist_1
            sp_path += sp_path_1
            # in case we found an agent with shorter path, switch
            if dist < min_weight:
                min_weight = dist
                path = sp_path
                agent_res = agent

        agent_res.path += path  # update the agent path
        return agent_res.id


while client.is_running() == 'true':

    graph_copy = GraphAlgo()  # copy graph
    graph_copy.load_from_json(json.loads(graph_json))

    # initialize pokemon list
    pokemons = json.loads(client.get_pokemons())
    pokemon_list = []
    pokemons = pokemons.get("Pokemons")

    for pokemon in pokemons:
        
        key = max(graph_copy.get_graph().nodes.keys()) + 1
        poki = Pokemon.from_dict_pok(pokemon.get("Pokemon"), key)
        graph_copy.graph.add_pokemon(poki)

        edge, weight1, weight2 = graph.graph.find_edge(poki)
        src = edge.src
        dest = edge.dest
        weight = edge.weight
        poki.edge = edge
        graph_copy.graph.add_edge(src, poki.key, weight1)
        graph_copy.graph.add_edge(poki.key, dest, weight2)
        graph_copy.graph.remove_edge(edge.src, edge.dest)

        pokemon_list.append(poki)
        print(poki.type)

    print(graph_copy.graph)
    # creating agent object from the json file
    agent_json = json.loads(client.get_agents())
    agents = []
    agent_json = agent_json.get("Agents")
    for agent in agent_json:
        agt = Agent.from_dict(agent.get("Agent"))
        # client.add_agent(client.add_agent("{\"id\":0}"))
        agents.append(agt)

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.get_graph().nodes.values():
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)
        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.key), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.get_graph().edges:
        # find the edge nodes
        src = next(n for n in graph.get_graph().nodes.values() if n.key == e.src)
        dest = next(n for n in graph.get_graph().nodes.values() if n.key == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        x = my_scale(float(agent.pos.x), x=True)
        y = my_scale(float(agent.pos.y), y=True)
        pygame.draw.circle(screen, Color(122, 61, 23), (x, y), 10)

    # draw Pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked
    # in the same way).

    for p in pokemon_list:
        x = my_scale(float(p.pos.x), x=True)
        y = my_scale(float(p.pos.y), y=True)
        pygame.draw.circle(screen, Color(0, 255, 255), (x, y), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(10)
    pokemon_list = sorted(pokemon_list, key=sorting_func, reverse=True)  # sort the pockemons base on their values

    # assign agent for each pokemon
    for pokemon in pokemon_list:
        agent_id: int = find_nearest_avaliable_agent(agents, pokemon, graph_copy)
        pokemon.agent_id = agent_id

    busy_agents = []
    for agent in agents:
        if agent.path is not None:
            busy_agents.append(agent)
    stop = False
    threads = []
    for agent in busy_agents:
        thread = Thread(target=run_agent, args=(agent, graph_copy))
        threads.append(thread)
        thread.start()

    i = 0
    while threads[i % len(threads)].is_alive():
        i += 1

    stop = True
    client.move()
    print("moved")
    for thread in threads:
        thread.join()

# game over:
