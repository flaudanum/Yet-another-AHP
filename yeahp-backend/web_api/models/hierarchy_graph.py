from pydantic import BaseModel, Extra


class HierarchyGraph(BaseModel, extra=Extra.forbid):
    nodes: list[str]
    edges: list[list[str]]
