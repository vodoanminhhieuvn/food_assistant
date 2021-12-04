from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class CaloricBreakdown(BaseModel):
    percent_protein: float = Field(..., alias="percentProtein")
    percent_fat: float = Field(..., alias="percentFat")
    percent_carbs: float = Field(..., alias="percentCarbs")


class WeightPerServing(BaseModel):
    amount: int
    unit: Literal["g"]


class Length_Temperature(BaseModel):
    number: int
    unit: Literal["Fahrenheit", "minutes"]


class Equipment_Ingredient(BaseModel):
    id_: int = Field(..., alias="id")
    name: str
    localized_name: str = Field(..., alias="localizedName")
    image: str
    temperature: Optional[Length_Temperature] = None


class Step(BaseModel):
    number: int
    step: str
    ingredients: List[Equipment_Ingredient]
    equipment: List[Equipment_Ingredient]
    length: Optional[Length_Temperature] = None


class Flavonoid_Nutrient_Property(BaseModel):
    title: str
    name: str
    amount: float
    unit: Literal["", "IU", "g", "kcal", "mg", "µg"]
    percent_of_daily_needs: Optional[float] = Field(None, alias="percentOfDailyNeeds")


class Ingredient(BaseModel):
    id_: int = Field(..., alias="id")
    name: str
    amount: float
    unit: str
    nutrients: List[Flavonoid_Nutrient_Property]


class AnalyzedInstruction(BaseModel):
    name: str
    steps: List[Step]


class Nutrition(BaseModel):
    nutrients: List[Flavonoid_Nutrient_Property]
    properties: List[Flavonoid_Nutrient_Property]
    flavonoids: List[Flavonoid_Nutrient_Property]
    ingredients: List[Ingredient]
    caloric_breakdown: CaloricBreakdown = Field(..., alias="caloricBreakdown")
    weight_per_serving: WeightPerServing = Field(..., alias="weightPerServing")


class FoodModel(BaseModel):
    vegetarian: bool
    vegan: bool
    gluten_free: bool = Field(..., alias="glutenFree")
    dairy_free: bool = Field(..., alias="dairyFree")
    very_healthy: bool = Field(..., alias="veryHealthy")
    cheap: bool
    very_popular: bool = Field(..., alias="veryPopular")
    sustainable: bool
    weight_watcher_smart_points: int = Field(..., alias="weightWatcherSmartPoints")
    gaps: str
    low_fodmap: bool = Field(..., alias="lowFodmap")
    aggregate_likes: int = Field(..., alias="aggregateLikes")
    spoonacular_score: int = Field(..., alias="spoonacularScore")
    health_score: int = Field(..., alias="healthScore")
    credits_text: str = Field(..., alias="creditsText")
    license_: str = Field(..., alias="license")
    source_name: str = Field(..., alias="sourceName")
    price_per_serving: float = Field(..., alias="pricePerServing")
    id_: int = Field(..., alias="id")
    title: str
    ready_in_minutes: int = Field(..., alias="readyInMinutes")
    servings: int
    source_url: str = Field(..., alias="sourceUrl")
    image: str
    image_type: str = Field(..., alias="imageType")
    nutrition: Nutrition
    summary: str
    cuisines: List[str]
    dish_types: List[str] = Field(..., alias="dishTypes")
    diets: List[str]
    occasions: List[str]
    analyzed_instructions: List[AnalyzedInstruction] = Field(
        ..., alias="analyzedInstructions"
    )
    spoonacular_source_url: str = Field(..., alias="spoonacularSourceUrl")


class FoodResponse(BaseModel):
    results: List[FoodModel]
    offset: int
    number: int
    total_results: int = Field(..., alias="totalResults")
