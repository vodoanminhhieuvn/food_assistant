from typing import List
from actions.models.food_model import FoodResponse, RecipeModel
from actions.models.meal_plan_model import MealPlan


class FoodData:
    search_recipe_model: RecipeModel
    list_food_model: List[RecipeModel]
    list_current_food: List[RecipeModel]
    meal_plan: MealPlan

    def init(self, list_food_response: List[FoodResponse]):
        list_recipe_model: List[RecipeModel] = []

        if len(list_food_response) > 1:
            for food_response in list_food_response:
                list_recipe_model.extend(
                    recipe_model.recipe for recipe_model in food_response.hits[:3]
                )

            self.list_current_food = list_recipe_model

        else:
            self.list_current_food = [
                recipe_model.recipe for recipe_model in list_food_response[0].hits[:5]
            ]

    def init_search_model(self, search_food_response: List[FoodResponse]):
        self.search_recipe_model = search_food_response[0].hits[0].recipe

    def initMealPlan(self, meal_response: MealPlan):
        self.meal_plan = meal_response

    # def init_spoon_recipe_model(self, spoon_recipe_response: SpoonRecipeResponse):
    #     self.spoon_recipe_model = spoon_recipe_response


food_data = FoodData()
