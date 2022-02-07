import networkx as nx

from web_api.models.hierarchy_graph import HierarchyGraph
from web_api.models.location import Point
from web_api.models.presentation_dimensions import PresentationDimensions


def nodes_by_dist(graph: nx.DiGraph, hierarchy_root: str):
    shortest_paths = nx.shortest_path(graph, hierarchy_root)
    classification: dict[int, set] = {}
    for node, path in shortest_paths.items():
        path_length = len(path)
        if classification.get(path_length) is None:
            classification[path_length] = set()
        classification[path_length].add(node)

    return classification


def compute_layout(graph: HierarchyGraph, dimensions: PresentationDimensions) -> list[Point]:
    hierarchy_root = graph.nodes[0]
    di_graph = nx.DiGraph()
    di_graph.add_edges_from(graph.edges)

    return [
        Point(x=0, y=0, label="element0"),
        Point(x=0, y=0, label="element1"),
    ]
