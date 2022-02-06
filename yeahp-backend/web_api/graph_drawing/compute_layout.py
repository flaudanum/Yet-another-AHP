import networkx as nx

from web_api.models.hierarchy_graph import HierarchyGraph
from web_api.models.location import Point
from web_api.models.presentation_dimensions import PresentationDimensions


def compute_layout(graph: HierarchyGraph, dimensions: PresentationDimensions) -> list[Point]:
    di_graph = nx.DiGraph()
    di_graph.add_edges_from(graph.edges)

    return [
        Point(x=0, y=0, label="element0"),
        Point(x=0, y=0, label="element1"),
    ]
