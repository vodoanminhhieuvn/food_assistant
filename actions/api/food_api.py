from actions import config
import requests


class FoodAPi:
    @staticmethod
    def get_food_recipe():
        params = {
            "q": "chicken",
            "app_id": "d736f71a",
            "app_key": "5a61563f39257241ba253b7e87328f5a",
        }

        res = requests.get(url="https://api.edamam.com/api/recipes/v2", params=params)
        res.raise_for_status()
        jsonData = res.json()

        print(jsonData["hits"][0]["recipe"]["label"])
