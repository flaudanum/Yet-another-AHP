import networkx as nx
import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal_nulp

from web_api.graph_drawing import optimization
from web_api.graph_drawing.optimization import OptimizationSetupError


@pytest.fixture(scope="function", name="graph")
def graph_fixture():
    graph = nx.DiGraph()
    graph.add_edges_from([
        ["1", "2"],
        ["1", "3"],
        ["2", "4"],
        ["2", "5"],
        ["3", "6"],
        ["3", "7"],
    ])
    return graph


@pytest.fixture(scope="function", name="graph2")
def graph2_fixture():
    graph = nx.DiGraph()
    graph.add_edges_from([
        ["A", "B"],
        ["A", "C"],
        ["C", "E"],
        ["C", "D"],
    ])
    return graph


def test_create_optimization_problem(graph):
    optimization.Problem(graph, root="1")

    for bad_node in ["2", "kaboom!"]:
        with pytest.raises(OptimizationSetupError) as excinfo:
            optimization.Problem(graph, root=bad_node)

        excinfo.match(f"Constructor: node '{bad_node}' is not a tree root")


def test_graph_labels(graph):
    problem = optimization.Problem(graph, root="1")
    ref = (
        ("1", (0, 0)),
        ("2", (1, 0)),
        ("3", (1, 1)),
        ("4", (2, 0)),
        ("5", (2, 1)),
        ("6", (2, 2)),
        ("7", (2, 3)),
    )
    for node, label in ref:
        assert problem.node_label(node) == label


def test_coordinate_map(graph2):
    problem = optimization.Problem(graph2, root="A")
    assert problem.coord_map == {
        "A": 0,
        "B": 1,
        "C": 2,
        "E": 3,
        "D": 4
    }


def test_equality_matrix(graph):
    problem = optimization.Problem(graph, root="1")

    mat_a_eq_ref = np.array([
        [1, 1, 0, 0, 0, 0],
        [2, 0, -1, -1, 0, 0],
        [0, 2, 0, 0, -1, -1]
    ])

    assert_array_almost_equal_nulp(
        problem.equality_matrix(),
        mat_a_eq_ref
    )
