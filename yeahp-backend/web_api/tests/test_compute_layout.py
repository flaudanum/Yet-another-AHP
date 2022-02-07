import networkx as nx

from web_api.graph_drawing.compute_layout import compute_layout, nodes_by_dist
from web_api.models.hierarchy_graph import HierarchyGraph
from web_api.models.presentation_dimensions import PresentationDimensions


def test_nodes_by_dist():
    graph = nx.DiGraph()
    graph.add_edges_from([
        ["1", "2"],
        ["1", "3"],
        ["1", "4"],
        ["2", "5"],
        ["2", "6"],
        ["3", "7"],
        ["3", "8"],
        ["3", "9"]
    ])
    root = "1"

    classification = nodes_by_dist(graph, root)

    assert classification == {
        1: {'1'},
        2: {'2', '4', '3'},
        3: {'5', '6', '9', '8', '7'}
    }


# TODO: to be completed
def test_compute_layout():
    graph = HierarchyGraph(
        nodes=["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        edges=[
            ["1", "2"],
            ["1", "3"],
            ["1", "4"],
            ["2", "5"],
            ["2", "6"],
            ["3", "7"],
            ["3", "8"],
            ["3", "9"]
        ]
    )

    dims = PresentationDimensions.parse_obj({
        "elementBox": {
            "height": 40,
            "width": 150
        },
        "horStep": 100,
        "vertStepMin": 40
    }, )

    layout = compute_layout(graph=graph, dimensions=dims)
