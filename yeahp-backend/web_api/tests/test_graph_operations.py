import networkx as nx
import pytest

from web_api.graph_drawing.compute_layout import compute_layout
from web_api.graph_drawing.optimization import nodes_by_dist, relabel_nodes
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
        1: ['1'],
        2: ['2', '3', '4'],
        3: ['5', '6', '7', '8', '9']
    }


def test_relabel_nodes():
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

    ref_node_map = {
        "1": (0, 0),
        "2": (1, 0),
        "3": (1, 1),
        "4": (1, 2),
        "5": (2, 0),
        "6": (2, 1),
        "7": (2, 2),
        "8": (2, 3),
        "9": (2, 4),
    }

    assert relabel_nodes(graph, hierarchy_root="1") == ref_node_map


# TODO: to be completed
@pytest.mark.skip(reason="Not fully implemented")
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
