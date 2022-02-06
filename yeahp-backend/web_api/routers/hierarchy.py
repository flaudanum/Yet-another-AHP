from fastapi import APIRouter

from web_api.models.hierarchy_graph import HierarchyGraph

router = APIRouter(
    prefix="/hierarchy",
    tags=["hierarchy"]
)


@router.post("/layout/")
async def compute_layout(graph: HierarchyGraph):
    return {
        "nodes": len(graph.nodes),
        "edges": len(graph.edges),
    }
