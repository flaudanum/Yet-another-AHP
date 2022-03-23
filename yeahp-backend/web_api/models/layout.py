from typing import Tuple

from pydantic import BaseModel, Extra, Field


class Layout(BaseModel, extra=Extra.forbid):
    y_coordinates: list[Tuple[str, float]] = Field(..., description="Coordinates along y-axis")
    class_by_depth: list[list[str]] = Field(..., description="list of nodes classified by depth from 'root'")
