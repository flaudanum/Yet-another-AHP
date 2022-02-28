import networkx as nx

from web_api.models.hierarchy_graph import HierarchyGraph
from web_api.models.location import Point
from web_api.models.presentation_dimensions import PresentationDimensions


def nodes_by_dist(graph: nx.DiGraph, hierarchy_root: str) -> dict[int, list]:
    shortest_paths = nx.shortest_path(graph, hierarchy_root)
    classification: dict[int, list] = {}
    for node, path in shortest_paths.items():
        path_length = len(path)
        if classification.get(path_length) is None:
            classification[path_length] = []
        classification[path_length].append(node)

    return classification


def relabel_nodes(graph: nx.DiGraph, hierarchy_root: str):
    classification = nodes_by_dist(graph, hierarchy_root)
    node_map = {}

    for depth, nodes in classification.items():
        node_map.update({
            node: (depth - 1, index)
            for index, node in enumerate(nodes)

        })

    return node_map


def compute_layout(graph: HierarchyGraph, dimensions: PresentationDimensions) -> list[Point]:
    hierarchy_root = graph.nodes[0]
    di_graph = nx.DiGraph()
    di_graph.add_edges_from(graph.edges)

    nodes_bdist = nodes_by_dist(di_graph, hierarchy_root)

    location_y: dict[str, float] = {node: 0. for node in graph.nodes}

    parent = hierarchy_root

    return [
        Point(x=0, y=0, label="element0"),
        Point(x=0, y=0, label="element1"),
    ]
