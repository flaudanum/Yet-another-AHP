import networkx as nx

from web_api.graph_drawing import optimization
from web_api.models.hierarchy_graph import HierarchyGraph
from web_api.models.layout import Layout


def compute_layout(hierarchy: HierarchyGraph) -> Layout:
    root = hierarchy.root
    graph = nx.DiGraph()
    graph.add_edges_from(hierarchy.dependencies)

    problem = optimization.Problem(graph, root)

    y_coordinates = problem.solve()

    return Layout(
        y_coordinates=list(zip(graph.nodes, y_coordinates)),
        class_by_depth=problem.depth_classification
    )
