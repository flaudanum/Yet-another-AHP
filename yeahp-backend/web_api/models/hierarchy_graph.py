from pydantic import BaseModel


class HierarchyGraph(BaseModel):
    nodes: list[str]
    edges: list[list[str]]
