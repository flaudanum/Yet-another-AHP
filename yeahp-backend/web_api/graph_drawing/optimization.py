import networkx as nx
import numpy as np


class OptimizationSetupError(Exception):
    ...


def nodes_by_dist(graph: nx.DiGraph, hierarchy_root: str) -> dict[int, list]:
    shortest_paths = nx.shortest_path(graph, hierarchy_root)
    classification: dict[int, list] = {}
    for node, path in shortest_paths.items():
        path_length = len(path)
        if classification.get(path_length) is None:
            classification[path_length] = []
        classification[path_length].append(node)

    return classification


def relabel_nodes(graph: nx.DiGraph, hierarchy_root: str) -> dict[str, tuple[int]]:
    classification = nodes_by_dist(graph, hierarchy_root)
    node_map = {}

    for depth, nodes in classification.items():
        node_map.update({
            node: (depth - 1, index)
            for index, node in enumerate(nodes)

        })

    return node_map


class Problem:

    def node_label(self, node: str) -> tuple[int]:
        return self._graph.nodes[node]["label"]

    @property
    def coord_map(self):
        return self._coord_map

    def __init__(self, graph: nx.DiGraph, root: str):
        try:
            if list(graph.predecessors(root)):
                raise OptimizationSetupError(f"Constructor: node '{root}' is not a tree root")
        except nx.exception.NetworkXError as err:
            raise OptimizationSetupError(f"Constructor: node '{root}' is not a tree root ({err})")

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

    def _compute_coord_map(self):
        nodes_label_map = self._graph.nodes(data=True)

        # Sort nodes by label
        self._coord_map = {
            node_data[0]: index
            for index, node_data in
            enumerate(sorted(nodes_label_map, key=lambda node_data: node_data[1]["label"]))
        }

    def equality_matrix(self) -> np.ndarray:
        nodes = [self._root]

        while nodes:
            parent = nodes.pop(0)
            # Gets child nodes
            successors = self._graph.successors(parent)
            # Adds successors to the graph traversal
            nodes += successors
