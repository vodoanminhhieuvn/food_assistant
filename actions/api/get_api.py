import json
from rasa_sdk.events import SlotSet
from actions.api.config import (
    EDAMAM_API_KEY,
    EDAMAM_APP_ID,
    SPOON_API_KEY,
    SPOON_TARGET_URL,
)
from actions.models.food_model import FoodResponse
from actions.models.slots import Slot
from actions.models.data import food_data

import requests
from actions.models.slots import slot
from actions.api.config import EDAMAM_TARGET_URL

get_spoon_config = {
    "apiKey": SPOON_API_KEY,
    "number": 5,
    "offset": 10,
    "addRecipeNutrition": True,
    "query": "chicken",
}

get_edamam_config = {
    "app_id": EDAMAM_APP_ID,
    "app_key": EDAMAM_API_KEY,
    "type": "public",
    "q": "chicken",
    "calories": f"{slot.nutrient_slots.minCalories}-{slot.nutrient_slots.maxCalories}",
}


class SpoonAPI:
    def getRecipes():
        request_params = {**get_edamam_config}

        print(request_params)

        response = requests.get(EDAMAM_TARGET_URL, params=request_params)

        food_response = FoodResponse(**response.json())

        food_data.init(food_response)


class EdamAPI:
    def howToCook():
        request_params = {"q": "Chicken"}

        print(request_params)
