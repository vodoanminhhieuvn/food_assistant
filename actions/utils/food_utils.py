NUTRIENT_LIST = ["calory", "fat"]


class Nutrients:
    @staticmethod
    def containNutrient(nutrient: str) -> bool:
        return nutrient in NUTRIENT_LIST
