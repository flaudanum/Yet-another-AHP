from pydantic import BaseModel, Extra


class Point(BaseModel, extra=Extra.forbid):
    label: str
    x: float
    y: float
