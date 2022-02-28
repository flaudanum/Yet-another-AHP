import networkx as nx
import numpy as np
from numpy.testing import assert_array_almost_equal_nulp

from web_api.graph_drawing.optimization import build_equal_matrix


def test_equality_matrix():
    graph = nx.DiGraph()
    graph.add_edges_from([
        ["1", "2"],
        ["1", "3"],
        ["2", "4"],
        ["2", "5"],
        ["3", "6"],
        ["3", "7"],
    ])

    node_map = {
        "1": (0, 0),
        "2": (1, 0),
        "3": (1, 1),
        "4": (2, 0),
        "5": (2, 1),
        "6": (2, 2),
        "7": (2, 3),
    }

    mat_a_eq_ref = np.array([
        [1, 1, 0, 0, 0, 0],
        [2, 0, -1, -1, 0, 0],
        [0, 2, 0, 0, -1, -1]
    ])

    assert_array_almost_equal_nulp(
        build_equal_matrix(graph, node_map),
        mat_a_eq_ref
    )
