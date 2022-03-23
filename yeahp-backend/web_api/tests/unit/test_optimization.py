import networkx as nx
import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal_nulp, assert_allclose

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


def test_tree_depth(graph):
    problem = optimization.Problem(graph, root="1")
    assert problem.tree_depth == 3


def test_problem_dimension(graph):
    problem = optimization.Problem(graph, root="1")
    assert problem.size == 6


def test_coordinate_map(graph2):
    problem = optimization.Problem(graph2, root="A")
    assert problem.coord_map == {
        "B": 0,
        "C": 1,
        "E": 2,
        "D": 3
    }


def test_equality_matrix(graph):
    problem = optimization.Problem(graph, root="1")

    mat_a_eq_ref = np.array([
        [-1, -1, 0, 0, 0, 0],
        [2, 0, -1, -1, 0, 0],
        [0, 2, 0, 0, -1, -1]
    ])

    assert_array_almost_equal_nulp(
        problem.equality_matrix(),
        mat_a_eq_ref
    )


def test_inequality_operator(graph):
    problem = optimization.Problem(graph, root="1")

    operator = problem.inequality_operator()

    reference = {
        "matrix": np.array([
            [-1, 1, 0, 0, 0, 0],
            [0, 0, -1, 1, 0, 0],
            [0, 0, 0, -1, 1, 0],
            [0, 0, 0, 0, -1, 1],
        ]),
        "vector": np.array([1, 1, 1, 1])
    }

    assert_array_almost_equal_nulp(
        operator.matrix,
        reference["matrix"]
    )

    assert_array_almost_equal_nulp(
        operator.vector,
        reference["vector"]
    )


def test_cost_function_linear_form(graph):
    problem = optimization.Problem(graph, root="1")

    reference = np.array([-1, 1, -1, 0, 0, 1])

    assert_array_almost_equal_nulp(
        problem.cost_func_linform(),
        reference
    )


def test_solver(graph):
    problem = optimization.Problem(graph, root="1")

    #  [-30.  30. -45. -15.  15.  45.]
    reference = np.array([0, -1, 1, -1.5, -0.5, 0.5, 1.5])

    assert_allclose(
        problem.solve(),
        reference,
        rtol=1e-8
    )
