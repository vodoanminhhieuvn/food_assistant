from typing import List, Optional
from pydantic import BaseModel, root_validator, validator


class NutrientModel(BaseModel):
    minCalories: Optional[int] = 50
    maxCalories: Optional[int] = 800
    minFat: Optional[int] = 1
    maxFat: Optional[int] = 100

    class Config:
        validate_assignment = True

    # @validator("minCalories", "maxCalories")
    def check_calories_none(cls, values):
        return {
            "minCalories": values["minCalories"] or 50,
            "maxCalories": values["maxCalories"] or 800,
        }

    # @validator("minFat", "maxFat")
    def check_calories_none(cls, values):
        return {
            "minCalories": values["minFat"] or 1,
            "maxCalories": values["maxFat"] or 100,
        }

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
