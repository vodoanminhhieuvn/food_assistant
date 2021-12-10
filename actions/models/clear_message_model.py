from pydantic import BaseModel, Field, root_validator
from typing import List, Literal, Optional


class ClearMessageModel(BaseModel):
    reset_min: Optional[str]
    reset_max: Optional[str]
    final: Optional[str]

    class Config:
        validate_assignment = True

    @root_validator()
    def calculate_total_score(cls, values):
        reset_min = values["reset_min"]
        reset_max = values["reset_max"]

        if min != None and max != None:
            values["final"] = "reset_all"

        elif min is None and max != None:
            values["final"] = max

        elif min != None:
            values["final"] = min

        return values
