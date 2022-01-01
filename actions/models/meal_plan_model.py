from pydantic import BaseModel, Field
from typing import List, Literal


class Meal(BaseModel):
    id_: int = Field(..., alias="id")
    image_type: str = Field(..., alias="imageType")
    title: str
    ready_in_minutes: int = Field(..., alias="readyInMinutes")
    servings: int
    source_url: str = Field(..., alias="sourceUrl")


class NutrientInfo(BaseModel):
    calories: float
    protein: float
    fat: float
    carbohydrates: float


class MealPlan(BaseModel):
    meals: List[Meal]
    nutrients: NutrientInfo
