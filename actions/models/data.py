from typing import List
from actions.models.food_model import FoodResponse
from actions.models.food_model import FoodModel


class FoodData:
    list_food_model: List[FoodModel]

    def init(self, food_response: FoodResponse):
        self.list_food_model = food_response.results


food_data = FoodData()
