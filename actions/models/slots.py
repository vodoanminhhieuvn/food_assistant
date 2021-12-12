from actions.models.nutrient_model import NutrientModel
from actions.models.recipe_parts_model import RecipePartsModel
from actions.models.recipe_search_keyword import RecipeSearchKeyword


class Slot:
    nutrient_slots = NutrientModel()

    def set_nutrient_attr(self, name: str, value: int):
        self.nutrient_slots.__setattr__(name, value)

    recipe_parts_slots = RecipePartsModel()

    recipe_search_keyword_slots = RecipeSearchKeyword()


slot = Slot()
