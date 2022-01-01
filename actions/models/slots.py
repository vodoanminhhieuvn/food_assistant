from actions.models.nutrient_model import NutrientModel
from actions.models.recipe_parts_model import RecipePartsModel
from actions.models.recipe_search_keyword import RecipeSearchKeyword


class Slot:
    target_calory: int = 2000
    nutrient_slots = NutrientModel()
    recipe_parts_slots = RecipePartsModel()
    recipe_search_keyword_slots = RecipeSearchKeyword()

    def set_nutrient_attr(self, name: str, value: int):
        self.nutrient_slots.__setattr__(name, value)


slot = Slot()
