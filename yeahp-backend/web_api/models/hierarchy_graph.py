from pydantic import BaseModel, Extra


class HierarchyGraph(BaseModel, extra=Extra.forbid):
    root: str
    dependencies: list[list[str]]
