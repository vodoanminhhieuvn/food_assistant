from actions.api.config import EDAMAM_API_KEY, EDAMAM_APP_ID, SPOON_API_KEY
from actions.models.slots import Slot

import requests

get_spoon_config = {
    "apiKey": SPOON_API_KEY,
}

get_edamam_config = {"app_id": EDAMAM_APP_ID, "app_key": EDAMAM_API_KEY}


class SpoonAPI:
    def getRecipes():
        request_params = {**get_spoon_config}

        request_params.update(Slot.nutrient_slots)

        print(request_params)


class EdamAPI:
    def howToCook():
        request_params = {"q": "Chicken"}

        print(request_params)
