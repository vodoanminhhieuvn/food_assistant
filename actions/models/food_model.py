from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Nutrient(BaseModel):
    label: str
    quantity: float
    unit: str


class Sub(BaseModel):
    label: str
    tag: str
    total: float
    has_rdi: bool = Field(..., alias="hasRDI")
    daily: float
    unit: str
    schema_org_tag: Optional[str] = Field(None, alias="schemaOrgTag")


class Digest_Sub(BaseModel):
    label: str
    tag: str
    total: float
    has_rdi: bool = Field(..., alias="hasRDI")
    daily: float
    unit: str
    schema_org_tag: Optional[str] = Field(None, alias="schemaOrgTag")
    sub: Optional[List[Sub]] = []


class Next_Self(BaseModel):
    href: str
    title: str


class _link(BaseModel):
    next_: Next_Self = Field(..., alias="next")


class _link_3X(BaseModel):
    self: Next_Self


class Large_Regular_Small_Thumbnail(BaseModel):
    url: str
    width: int
    height: int


class Image(BaseModel):
    thumbnail: Optional[Large_Regular_Small_Thumbnail] = Field(..., alias="THUMBNAIL")
    small: Optional[Large_Regular_Small_Thumbnail] = Field(..., alias="SMALL")
    regular: Optional[Large_Regular_Small_Thumbnail] = Field(None, alias="REGULAR")
    large: Optional[Large_Regular_Small_Thumbnail] = Field(None, alias="LARGE")


class Ingredient(BaseModel):
    text: str
    quantity: float
    food: str
    weight: float
    food_id: str = Field(..., alias="foodId")
    measure: Optional[str] = None
    food_category: Optional[str] = Field(None, alias="foodCategory")
    image: Optional[str] = None


class TotalDaily_TotalNutrient(BaseModel):
    enerc_kcal: Nutrient = Field(..., alias="ENERC_KCAL")
    fat: Nutrient = Field(..., alias="FAT")
    fasat: Nutrient = Field(..., alias="FASAT")
    chocdf: Nutrient = Field(..., alias="CHOCDF")
    fibtg: Nutrient = Field(..., alias="FIBTG")
    procnt: Nutrient = Field(..., alias="PROCNT")
    chole: Nutrient = Field(..., alias="CHOLE")
    na: Nutrient = Field(..., alias="NA")
    ca: Nutrient = Field(..., alias="CA")
    mg: Nutrient = Field(..., alias="MG")
    k: Nutrient = Field(..., alias="K")
    fe: Nutrient = Field(..., alias="FE")
    zn: Nutrient = Field(..., alias="ZN")
    p: Nutrient = Field(..., alias="P")
    vita_rae: Nutrient = Field(..., alias="VITA_RAE")
    vitc: Nutrient = Field(..., alias="VITC")
    thia: Nutrient = Field(..., alias="THIA")
    ribf: Nutrient = Field(..., alias="RIBF")
    nia: Nutrient = Field(..., alias="NIA")
    vitb6_a: Nutrient = Field(..., alias="VITB6A")
    foldfe: Nutrient = Field(..., alias="FOLDFE")
    vitb12: Nutrient = Field(..., alias="VITB12")
    vitd: Nutrient = Field(..., alias="VITD")
    tocpha: Nutrient = Field(..., alias="TOCPHA")
    vitk1: Nutrient = Field(..., alias="VITK1")
    fatrn: Optional[Nutrient] = Field(None, alias="FATRN")
    fams: Optional[Nutrient] = Field(None, alias="FAMS")
    fapu: Optional[Nutrient] = Field(None, alias="FAPU")
    chocd_fnet: Optional[Nutrient] = Field(None, alias="CHOCDF.net")
    sugar: Optional[Nutrient] = Field(None, alias="SUGAR")
    suga_radded: Optional[Nutrient] = Field(None, alias="SUGAR.added")
    folfd: Optional[Nutrient] = Field(None, alias="FOLFD")
    folac: Optional[Nutrient] = Field(None, alias="FOLAC")
    sugaralcohol: Optional[Nutrient] = Field(None, alias="Sugar.alcohol")
    water: Optional[Nutrient] = Field(None, alias="WATER")


class RecipeModel(BaseModel):
    uri: str
    label: str
    image: Optional[str]
    images: Image
    source: str
    url: str
    share_as: str = Field(..., alias="shareAs")
    yield_: int = Field(..., alias="yield")
    diet_labels: List[str] = Field(..., alias="dietLabels")
    health_labels: List[str] = Field(..., alias="healthLabels")
    cautions: List[str]
    ingredient_lines: List[str] = Field(..., alias="ingredientLines")
    ingredients: List[Ingredient]
    calories: float
    total_weight: float = Field(..., alias="totalWeight")
    total_time: int = Field(..., alias="totalTime")
    cuisine_type: List[str] = Field(..., alias="cuisineType")
    meal_type: List[str] = Field(..., alias="mealType")
    dish_type: List[str] = Field(..., alias="dishType")
    total_nutrients: TotalDaily_TotalNutrient = Field(..., alias="totalNutrients")
    total_daily: TotalDaily_TotalNutrient = Field(..., alias="totalDaily")
    digest: List[Digest_Sub]


class Hit(BaseModel):
    recipe: RecipeModel
    _links: _link_3X


class FoodResponse(BaseModel):
    from_: int = Field(..., alias="from")
    to: int
    count: int
    _links: _link
    hits: List[Hit]
