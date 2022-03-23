import networkx as nx

from web_api.graph_drawing import optimization
from web_api.models.hierarchy_graph import HierarchyGraph
from web_api.models.layout import Layout

PRECISION_DIGIT = 5
prec_scale = 10 ** PRECISION_DIGIT


def compute_layout(hierarchy: HierarchyGraph) -> Layout:
    root = hierarchy.root
    graph = nx.DiGraph()
    graph.add_edges_from(hierarchy.dependencies)

    problem = optimization.Problem(graph, root)

    y_coordinates = [
        round(coord * prec_scale) / prec_scale
        for coord in
        problem.solve()
    ]

    return Layout(
        y_coordinates=list(zip(graph.nodes, y_coordinates)),
        class_by_depth=problem.depth_classification
    )
