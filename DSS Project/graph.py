
import networkx as nx
import matplotlib.pyplot as plt

def create_graph():
    graph = nx.DiGraph()
    graph.add_edges_from([(11, 14), (11, 15), (14, 16), (11, 16), (13, 17), (11, 17), (14, 19), (11, 19), (11, 20), (15, 21), (14, 21), (11, 21), (14, 22), (11, 22), (16, 27), (11, 27), (14, 27), (11, 24), (14, 24), (14, 26), (11, 26), (15, 37), (11, 37), (11, 38), (14, 40), (11, 40), (11, 32), (14, 41), (11, 41), (15, 41), (16, 41), (20, 41), (15, 33), (11, 33), (11, 34), (11, 35), (16, 35), (14, 35), (11, 35), (14, 36), (11, 36), (16, 36), (44, 36), (14, 49), (11, 49), (15, 49), (14, 50), (11, 50), (16, 50), (14, 50), (11, 50), (11, 48), (39, 52), (14, 51), (11, 51), (13, 51), (16, 51), (14, 42), (11, 42), (15, 42), (20, 43), (11, 43), (11, 44), (14, 44), (16, 44), (11, 45), (14, 45), (14, 46), (11, 46), (16, 46), (44, 46), (28, 29), (29, 30), (28, 30), (11, 25), (14, 25), (15, 25), (11, 39), (14, 39), (15, 39), (16, 39), (24, 39), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (0, 25), (0, 26), (0, 27), (0, 28), (0, 29), (0, 30), (0, 31), (0, 32), (0, 33), (0, 34), (0, 35), (0, 36), (0, 37), (0, 38), (0, 39), (0, 40), (0, 41), (0, 42), (0, 43), (0, 44), (0, 45), (0, 46), (0, 47), (0, 48), (0, 49), (0, 50), (0, 51), (0, 52), (44, 47)], arrow=True)

    # nx.draw(graph, with_labels=True, arrows=True, node_size=500, node_color='skyblue', edge_color='black', linewidths=1, font_size=8)
    #
    # plt.savefig('graph.png')
    return graph

def get_ancestor_list(graph, id):
    res = nx.ancestors(graph, id)
    return list(res)
