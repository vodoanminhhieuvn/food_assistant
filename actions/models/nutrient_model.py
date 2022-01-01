from typing import List, Optional
from pydantic import BaseModel, root_validator, validator


class NutrientModel(BaseModel):
    minCalories: Optional[int] = 50
    maxCalories: Optional[int] = 800
    minFat: Optional[int] = 10
    maxFat: Optional[int] = 200

    class Config:
        validate_assignment = True

    @root_validator()
    @classmethod
    def calculate_total_score(cls, values):

        minCalories = values["minCalories"] = values["minCalories"] or 50
        maxCalories = values["maxCalories"] = values["maxCalories"] or 800
        minFat = values["minFat"] = values["minFat"] or 10
        maxFat = values["maxFat"] = values["maxFat"] or 200

        if minCalories > maxCalories:
            values["minCalories"], values["maxCalories"] = (maxCalories, minCalories)

        if minFat > maxFat:
            values["minFat"], values["maxFat"] = maxFat, minFat

        return values
