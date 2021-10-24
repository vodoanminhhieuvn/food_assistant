from actions import config

import requests
import json
import os

from actions.extension_function import ExtensionFunction


class FoodAPI:
    @staticmethod
    def get_food_recipe(ingredients: str) -> str:
        try:
            jsonData = ExtensionFunction.getJsonFILE(
                f"src/actions/api/data/{ingredients}.json"
            )
            return jsonData["hits"][0]["recipe"]["label"]

        except Exception as e:
            params = {
                "q": f"{ingredients}",
                "app_id": f"{config.edamam_app_id}",
                "app_key": f"{config.edamam_app_key}",
                "type": "public",
                "random": "true",
            }

            res = requests.get(
                url="https://api.edamam.com/api/recipes/v2", params=params
            )
            res.raise_for_status()
            jsonData = res.json()

            with open(f"{ingredients}.json", "w") as writeFile:
                json.dump(jsonData, writeFile)

            return jsonData["hits"][0]["recipe"]["label"]
