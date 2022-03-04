import networkx as nx

from web_api.graph_drawing.optimization import nodes_by_depth
from web_api.models.hierarchy_graph import HierarchyGraph
from web_api.models.location import Point
from web_api.models.presentation_dimensions import PresentationDimensions


def compute_layout(graph: HierarchyGraph, dimensions: PresentationDimensions) -> list[Point]:
    hierarchy_root = graph.nodes[0]
    di_graph = nx.DiGraph()
    di_graph.add_edges_from(graph.edges)

    nodes_bdist = nodes_by_depth(di_graph, hierarchy_root)

    location_y: dict[str, float] = {node: 0. for node in graph.nodes}

    parent = hierarchy_root

    return [
        Point(x=0, y=0, label="element0"),
        Point(x=0, y=0, label="element1"),
    ]
