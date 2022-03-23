import json
from copy import deepcopy
from dataclasses import dataclass

import cvxpy as cp
import networkx as nx
import numpy as np


class OptimizationSetupError(Exception):
    ...


def nodes_by_depth(graph: nx.DiGraph, hierarchy_root: str) -> dict[int, list]:
    shortest_paths = nx.shortest_path(graph, hierarchy_root)
    classification: dict[int, list] = {}
    for node, path in shortest_paths.items():
        path_length = len(path)
        if classification.get(path_length) is None:
            classification[path_length] = []
        classification[path_length].append(node)

    return classification


def relabel_nodes(graph: nx.DiGraph, hierarchy_root: str) -> dict[str, tuple[int]]:
    classification = nodes_by_depth(graph, hierarchy_root)
    node_map = {}

    for depth, nodes in classification.items():
        node_map.update({
            node: (depth - 1, index)
            for index, node in enumerate(nodes)

        })

    return node_map


@dataclass
class InequalityOperator:
    matrix: np.ndarray
    vector: np.ndarray


class Problem:

    def node_label(self, node: str) -> tuple[int]:
        return self._graph.nodes[node]["label"]

    @property
    def coord_map(self):
        return self._coord_map

    @property
    def depth_classification(self):
        return deepcopy(self._depth_classification)

    @property
    def size(self):
        return self._size

    @property
    def tree_depth(self):
        return self._tree_depth

    def __init__(self, graph: nx.DiGraph, root: str):
        try:
            if list(graph.predecessors(root)):
                raise OptimizationSetupError(json.dumps({
                    "message": f"Constructor: node '{root}' is not the root of the hierarchy"
                }))
        except nx.exception.NetworkXError as err:
            raise OptimizationSetupError(json.dumps({
                "message": f"Constructor: node '{root}' does not exist",
                "error_class": repr(type(err)),
                "error": str(err),
                "nodes": sorted(graph.nodes)
            }))

        # The graph is expected to be a tree, this node is the declared root
        self._root = root

        # Graph
        self._graph: nx.DiGraph = graph.copy()

        # Labels nodes by depth and occurrence order
        for node, tuple_label in relabel_nodes(self._graph, root).items():
            self._graph.nodes[node]["label"] = tuple_label

        # Map of nodes to the coordinate system of the optimization problem
        self._coord_map = {}
        self._compute_coord_map()

        # Problem's dimension
        self._size = len(self._coord_map)

        # Classification of nodes by depth
        self._depth_classification = self._classify_by_depth()

        # Tree's depth
        self._tree_depth: int = max([node_data[1]["label"][0] for node_data in self._graph.nodes(data=True)]) + 1

    def _compute_coord_map(self):
        """
        Maps of nodes to coordinate indices
        """
        nodes_label_map = self._graph.nodes(data=True)

        # Sort nodes by label
        self._coord_map = {
            node_data[0]: index - 1
            for index, node_data in
            enumerate(sorted(nodes_label_map, key=lambda node_data: node_data[1]["label"]))
            if node_data[1]["label"] != (0, 0)
        }

    def _classify_by_depth(self):
        nodes_by_depth_items: list[[int, list[int]]] = sorted(
            nodes_by_depth(self._graph, self._root).items(),
            key=lambda item: item[0]
        )

        return [
            pair[1]
            for pair in
            nodes_by_depth_items
        ]

    def equality_matrix(self) -> np.ndarray:
        """
        This matrix stands for the barycentric relation between the position of a node and children
        """
        matrix = np.zeros(shape=(self._tree_depth, self._size))

        nodes = [self._root]
        row = 0

        # Breadth first traversal of the tree
        while nodes:
            parent = nodes.pop(0)
            # Gets child nodes
            successors = list(self._graph.successors(parent))

            # If there are no child nodes then there is no barycentric relation
            if not successors:
                continue

            # Adds successors to the graph traversal
            nodes += successors

            # Coordinates of the parent node
            parent_coord: int | None = self._coord_map.get(parent)

            # TODO: fix this equation which is hardcoded for 2 child dependencies
            if parent_coord is not None:
                matrix[row, parent_coord] = len(successors)

            for node in successors:
                coord = self._coord_map[node]
                matrix[row, coord] = -1

            row += 1

        return matrix

    def inequality_operator(self) -> InequalityOperator:
        matrix = []
        vector = []

        for nodes in self.depth_classification:
            nodes: list[int]
            while nodes:
                node0 = nodes.pop(0)
                if not nodes:
                    continue
                node1 = nodes[0]
                row = np.zeros(shape=(self._size,))
                coord0 = self._coord_map[node0]
                coord1 = self._coord_map[node1]
                row[coord0] = -1.
                row[coord1] = 1.

                matrix.append(row)
                vector.append(1.)

        return InequalityOperator(
            matrix=np.array(matrix),
            vector=np.array(vector)
        )

    def cost_func_linform(self):
        linform_vector = np.zeros(shape=(self._size,))

        for nodes in self.depth_classification[1:]:
            node0 = nodes[0]
            node1 = nodes[-1]

            coord0 = self._coord_map[node0]
            coord1 = self._coord_map[node1]
            linform_vector[coord0] = -1
            linform_vector[coord1] = 1

        return linform_vector

    def solve(self):
        mat_eq = self.equality_matrix()
        ineq_op = self.inequality_operator()
        lform_cost = self.cost_func_linform()
        x = cp.Variable(shape=(self._size,), name="X")
        constraints = [cp.matmul(mat_eq, x) == 0, ineq_op.matrix @ x >= ineq_op.vector]
        objective = cp.Minimize(cp.matmul(lform_cost, x))
        problem = cp.Problem(objective, constraints)
        problem.solve()

        return np.array([0, *x.value])
