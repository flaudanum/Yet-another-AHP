import networkx as nx
from numpy import testing as npt

from web_api.graph_drawing.compute_layout import compute_layout
from web_api.graph_drawing.optimization import nodes_by_depth, relabel_nodes
from web_api.models.hierarchy_graph import HierarchyGraph


def test_nodes_by_depth():
    graph = nx.DiGraph()
    graph.add_edges_from([
        ["1", "2"],
        ["1", "3"],
        ["1", "4"],
        ["2", "5"],
        ["2", "6"],
        ["3", "9"],
        ["3", "8"],
        ["3", "7"]
    ])
    root = "1"

    classification = nodes_by_depth(graph, root)

    assert classification == {
        1: ['1'],
        2: ['2', '3', '4'],
        3: ['5', '6', '9', '8', '7']
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


def test_compute_layout():
    graph = HierarchyGraph(
        root="Goal",
        dependencies=[
            ["Goal", "Criterion A"],
            ["Goal", "Criterion B"],
            ["Criterion A", "Criterion C"],
            ["Criterion A", "Criterion D"],
            ["Criterion B", "Criterion E"],
            ["Criterion B", "Criterion F"],
        ]
    )

    reference = {
        "y_coord": [
            ["Goal", 0],
            ["Criterion A", -1],
            ["Criterion B", 1],
            ["Criterion C", -1.5],
            ["Criterion D", -0.5],
            ["Criterion E", 0.5],
            ["Criterion F", 1.5],
        ],
        "class_by_depth": [
            ["Goal"],
            ["Criterion A", "Criterion B"],
            ["Criterion C", "Criterion D", "Criterion E", "Criterion F"]
        ]
    }

    layout = compute_layout(hierarchy=graph)

    for y_coord, ref_coord in zip(layout.y_coordinates, reference["y_coord"]):
        # Labels must match
        assert y_coord[0] == ref_coord[0]
        # y-coordinates are close to reference w/ a relative tolerance of 1e-8
        npt.assert_allclose(
            y_coord[1],
            ref_coord[1],
            rtol=1e-8,
        )

    assert layout.class_by_depth == reference["class_by_depth"]
