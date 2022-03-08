from fastapi import APIRouter

from web_api.models.hierarchy_graph import HierarchyGraph
from web_api.graph_drawing.compute_layout import compute_layout

router = APIRouter(
    prefix="/hierarchy",
    tags=["hierarchy"]
)


@router.post("/layout/", response_model=list)
def get_layout(graph: HierarchyGraph):
    return compute_layout(graph)
