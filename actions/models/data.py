from typing import List
from actions.models.food_model import FoodResponse
from actions.models.food_model import RecipeModel


class FoodData:
    list_food_model: List[RecipeModel]
    list_current_food: List[RecipeModel]

    def init(self, food_response: FoodResponse):
        self.list_food_model = [
            recipe_model.recipe for recipe_model in food_response.hits
        ]
        
        self.list_current_food = self.list_food_model[:5]


food_data = FoodData()
