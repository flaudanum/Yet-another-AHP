import networkx as nx
import numpy as np


class OptimizationSetupError(Exception):
    ...


def build_equal_matrix(graph: nx.DiGraph, node_map: dict[str, tuple]) -> np.ndarray:
    root = None
    for node, label in node_map.items():
        if label == (0, 0):
            root = node

    if root is None:
        raise OptimizationSetupError("Could not find a root in the node map")

    parent = root
    nodes = list(graph.successors(root))
    while nodes:
        # Build barycentric equation
        parent = nodes.pop(0)
        nodes += graph.successors(parent)





