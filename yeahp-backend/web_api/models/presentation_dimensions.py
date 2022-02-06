from pydantic import BaseModel, Extra


class BoxDimensions(BaseModel, extra=Extra.forbid):
    height: int
    width: int


class PresentationDimensions(BaseModel, extra=Extra.forbid):
    elementBox: BoxDimensions
    horStep: int
    vertStepMin: int
