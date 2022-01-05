import math as mh
import sys
from threading import Thread
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.Agent import Agent
from client_python.GUI import Gui
from client_python.Info import Info
from client_python.pokemon import Pokemon
from graph.GraphAlgo import GraphAlgo
from Button import Button


def run_agent(agent: Agent, g_algo: GraphAlgo):
    while len(agent.path) != 0:
        p = agent.path[0]
        if stop:  # global bool variable indicate when one pokemon found
            return
        client.choose_next_edge(
            '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(agent.path[1 % len(agent.path)]) + '}')
        agent.pos = g_algo.get_graph().nodes[agent.path[1 % len(agent.path)]].pos
        agent.path.remove(agent.path[0])
        if isinstance(g_algo.get_graph().get_all_v()[p], Pokemon):
            client.move()
            return


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
            dist, sp_path = graph.shortest_path(agent.src,
                                                pokemon.edge.src)  # find the shortest path from agent src to pokemon
            dist_1, sp_path_1 = graph.shortest_path(pokemon.edge.src, pokemon.edge.dest)
            dist += dist_1
            sp_path += sp_path_1
            # in case we found an agent with shorter path, switch
            if dist < min_weight:
                min_weight = dist
                path = sp_path
                agent_res = agent

        agent_res.path = path  # update the agent path
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


if __name__ == '__main__':
    """
    main method.
    this method run the game while connecting to the server.
    PORT: 6666
    HOST: 127.0.0.1 -> local host
    """

    # default port
    PORT = 6666
    # server host (default localhost 127.0.0.1)
    HOST = '127.0.0.1'

    client = Client()
    client.start_connection(HOST, PORT)
    graph_json = client.get_graph()

    # load the json string into SimpleNamespace Object
    graph = GraphAlgo()
    graph.load_from_json(json.loads(graph_json))

    # create am info object and add as needed agents
    game_info = Info.from_dict(json.loads(client.get_info()))
    for i in range(game_info.agents):
        client.add_agent("{\"id\":" + str(i) + "}")

    gui = Gui(graph)

    # this command starts the server - the game is running now
    client.start()

    # game started:
    try:
        while client.is_running() == 'true':

            game_info = Info.from_dict(json.loads(client.get_info()))  # each round, get the info from the server

            graph_copy = GraphAlgo()  # copy graph
            graph_copy.load_from_json(json.loads(graph_json))

            # initialize pokemon list
            pokemons = json.loads(client.get_pokemons())
            pokemon_list = []
            pokemons = pokemons.get("Pokemons")

            # create pokemons from the json file
            for pokemon in pokemons:
                key = max(graph_copy.get_graph().nodes.keys()) + 1
                poki = Pokemon.from_dict_pok(pokemon.get("Pokemon"), key)
                graph_copy.graph.add_pokemon(poki)

                edge, weight1, weight2 = graph.graph.find_edge(poki)        # find the edge the pokemon is on
                src = edge.src
                dest = edge.dest
                weight = edge.weight
                poki.edge = edge
                # modify graph_copy base on the pokemon values
                graph_copy.graph.add_edge(src, poki.key, weight1)
                graph_copy.graph.add_edge(poki.key, dest, weight2)
                graph_copy.graph.remove_edge(edge.src, edge.dest)
                # add pokemon to pokemon list for more usages
                pokemon_list.append(poki)

            # creating agent object from the json file
            agent_json = json.loads(client.get_agents())
            agents = []
            agent_json = agent_json.get("Agents")
            for agent in agent_json:
                agt = Agent.from_dict(agent.get("Agent"))
                agents.append(agt)

            # run the gui
            flag = gui.run_gui(agents, pokemon_list, str(float(client.time_to_end()) / 1000), game_info)
            if not flag:
                client.stop_connection()
                pygame.quit()
                exit(0)

            """
            Algorithm part -> when there is only one agent use thread
            else, use for loop.
            """
            pokemon_list = sorted(pokemon_list, key=sorting_func,reverse=True)  # sort the pokemons base on their values
            # assign agent for each pokemon
            for pokemon in pokemon_list:
                # finds an agent for the pokemon
                agent_id: int = find_nearest_avaliable_agent(agents, pokemon, graph_copy)
                pokemon.agent_id = agent_id

            stop = False  # global variable, used in threads

            # check the number of agents
            if len(agents) > 1:
                # loop between the agents in case of multiple agents
                for agent in agents:
                    run_agent(agent, graph_copy)  # run the agent on its path
            else:
                # use a thread for better results in case of one agent
                busy_agents = agents
                threads = []
                # create thread for the agent
                for agent in busy_agents:
                    thread = Thread(target=run_agent, args=(agent, graph_copy))
                    threads.append(thread)
                    thread.start()

                i = 0
                # loop until the thread stopped
                while threads[i % len(threads)].is_alive():
                    i += 1

                stop = True  # if the thread stopped
                for thread in threads:
                    thread.join()

    except ConnectionResetError as e:
        print("the server is down!", e)
        sys.exit(1)

# game over
