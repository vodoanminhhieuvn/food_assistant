from typing import List, Optional
from pydantic import BaseModel, root_validator


class NutrientModel(BaseModel):
    minCalories: Optional[int]
    maxCalories: Optional[int]
    minFat: Optional[int]
    maxFat: Optional[int]

    class Config:
        validate_assignment = True

    @root_validator()
    @classmethod
    def calculate_total_score(cls, values):
        minCalories = values["minCalories"]
        maxCalories = values["maxCalories"]
        minFat = values["minFat"]
        maxFat = values["maxFat"]

        if (minCalories is not None and maxCalories is not None) and (
            minCalories > maxCalories
        ):
            values["minCalories"], values["maxCalories"] = maxCalories, minCalories

        if (minFat is not None and maxFat is not None) and (minFat > maxFat):
            values["minFat"], values["maxFat"] = maxFat, minFat

        return values
