import json
import requests

from rasa_sdk.events import SlotSet
from actions.api.config import (
    EDAMAM_API_KEY,
    EDAMAM_APP_ID,
    SPOON_API_KEY,
    SPOON_TARGET_URL,
    EDAMAM_TARGET_URL,
    GENERATE_MEAL_URL,
)
from actions.models.food_model import FoodResponse
from actions.models.meal_plan_model import MealPlan
from actions.models.data import food_data

from actions.models.slots import slot


get_spoon_config = {
    "apiKey": SPOON_API_KEY,
    "number": 5,
    "offset": 10,
    "addRecipeNutrition": True,
    "query": "chicken",
}


generate_meal_plan_config = {
    "apiKey": SPOON_API_KEY,
    "targetCalories": slot.target_calory,
    "diet": "",
    "timeFrame": "day",
}


class SpoonAPI:
    def getRecipes():
        get_edamam_config = {
            "app_id": EDAMAM_APP_ID,
            "app_key": EDAMAM_API_KEY,
            "type": "public",
            "calories": f"{slot.nutrient_slots.minCalories}-{slot.nutrient_slots.maxCalories}",
            "fat": f"{slot.nutrient_slots.minFat}-{slot.nutrient_slots.maxFat}",
        }

        list_food_response = []

        request_params = {**get_edamam_config}

        for recipe in slot.recipe_search_keyword_slots.keywords:
            request_params["q"] = recipe

            response = requests.get(EDAMAM_TARGET_URL, params=request_params)

            list_food_response.append(FoodResponse(**response.json()))

        food_data.init(list_food_response)

    def getMealPlan():
        request_params = {**generate_meal_plan_config}

        response = requests.get(GENERATE_MEAL_URL, params=request_params)

        meal_response = MealPlan(**response.json())

        food_data.initMealPlan(meal_response)

    def getSearchRecipe(recipe_name: str):
        get_edamam_config = {
            "app_id": EDAMAM_APP_ID,
            "app_key": EDAMAM_API_KEY,
            "type": "public",
        }

        list_food_response = []

        request_params = {**get_edamam_config, "q": recipe_name}

        response = requests.get(EDAMAM_TARGET_URL, params=request_params)

        list_food_response.append(FoodResponse(**response.json()))

        food_data.init_search_model(list_food_response)


class EdamAPI:
    def howToCook():
        request_params = {"q": "Chicken"}

        print(request_params)
